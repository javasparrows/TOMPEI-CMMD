import os
import pandas as pd
import pydicom
import json
import matplotlib.pyplot as plt
from glob import glob
from tqdm import tqdm

def overlay_masks(path_dicom, path_json, path_save, show=True):
    """
    Load a DICOM file and JSON annotation, then overlay the mask polygon on the mammogram image.

    Arguments:
    ----------
    path_dicom : str
        Path to the DICOM file.
    path_json : str
        Path to the JSON annotation file.
    path_save : str
        Path to save the overlaid image.
    show : bool
        If True, display the plot after creating it.
    """
    # Read the DICOM file
    ds = pydicom.dcmread(path_dicom)
    # Load annotation JSON
    with open(path_json, "r") as f:
        data = json.load(f)

    # Extract mask polygons
    masks = [d["cgPoints"] for d in data]

    # Get the pixel array from DICOM
    img = ds.pixel_array

    # Plot the image
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img, cmap="gray")
    ax.axis("off")  # Hide axes, ticks

    # Define a helper to draw polygon
    def draw_polygon(points):
        x = [p["x"] for p in points]
        y = [p["y"] for p in points]
        # Close the polygon
        x.append(points[0]["x"])
        y.append(points[0]["y"])
        ax.plot(x, y, color="yellow")

    # Draw each mask
    for mask in masks:
        draw_polygon(mask)

    # Save figure without extra borders
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(path_save, bbox_inches="tight", pad_inches=0)
    if show:
        plt.show()
    plt.close(fig)


def get_mammo_laterality_and_view(path_dicom: str):
    """
    Retrieve the laterality (L or R) and view (MLO or CC) from the DICOM metadata.

    Arguments:
    ----------
    path_dicom : str
        Path to the DICOM file.

    Returns:
    --------
    laterality : str
        'L' or 'R' or 'Unknown'
    view_position : str
        'MLO', 'CC', or 'Unknown'
    """
    ds = pydicom.dcmread(path_dicom)
    laterality = ds.get((0x0020, 0x0062), "Unknown").value
    if ds.get((0x0054, 0x0220))[0].get((0x0008, 0x0104), "Unknown").value == "cranio-caudal":
        view_position = "CC"
    else:
        view_position = "MLO"
    return laterality, view_position


def main():
    """
    Main function that reads the CSV, sorts data, and processes each row to match DICOM files with JSON annotations.
    """
    # Read and sort CSV
    df = pd.read_csv("TOMPEI-CMMD.csv")
    df = df.sort_values(by="Subject ID").reset_index(drop=True)

    # Retrieve Series UID and Subject ID
    uid_list = df["Series UID"].values.tolist()
    id_list = df["Subject ID"].values.tolist()

    # Collect all JSON paths
    paths_json = sorted(glob("TOMPEI-CMMD_v01_20250121/*.json"))

    # Create output directory
    os.makedirs("overlay_images", exist_ok=True)

    # Iterate through each entry
    for i in tqdm(range(len(uid_list))):
        uid = uid_list[i]
        subj_id = id_list[i]

        # Find JSON path that matches the subject id
        path_json = [p for p in paths_json if subj_id in p][0]
        # Example: "D1-0001_MLO_R_AnnotationFile.json" -> parse
        _, view_json, laterality_json, _ = path_json.split("/")[-1].split("_")

        # Gather DICOM files for that UID
        paths_dicom = sorted(glob(f"tciaDownload/{uid}/*.dcm"))

        # Match the DICOM that has the same laterality + view
        for path_dicom in paths_dicom:
            lat, view = get_mammo_laterality_and_view(path_dicom)

            if lat == laterality_json and view == view_json:
                path_save = f"overlay_images/{subj_id}_MLO_{lat}_overlaied.png"
                overlay_masks(path_dicom, path_json, path_save, show=False)


if __name__ == "__main__":
    main()
