import pydicom
import json
import matplotlib.pyplot as plt

def overlay_masks(path_dicom, path_json, path_save):
    # Load the DICOM file
    ds = pydicom.dcmread(path_dicom)
    with open(path_json) as f:
        data = json.load(f)

    masks = [d["cgPoints"] for d in data]

    # Get pixel data from the DICOM image
    img = ds.pixel_array

    # Create a figure and axis for the image
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img, cmap="gray")
    ax.axis("off")  # Hide axes and ticks

    # Draw mask coordinates
    def draw_polygon(points):
        x = [p["x"] for p in points]
        y = [p["y"] for p in points]
        # Add the first point again to close the polygon
        x.append(points[0]["x"])
        y.append(points[0]["y"])
        ax.plot(x, y, color="yellow")

    for mask in masks:
        draw_polygon(mask)

    # Save the image without extra borders
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(path_save, bbox_inches='tight', pad_inches=0)
    plt.close(fig)


if __name__ == "__main__":
    path_dicom = "D1-0001_MLO_R_DicomFile.dcm"
    path_json = "D1-0001_MLO_R_AnnotationFile.json"
    path_save = "D1-0001_MLO_R_overlaied.png"
    overlay_masks(path_dicom, path_json, path_save)

    path_dicom = "D1-0002_MLO_L_DicomFile.dcm"
    path_json = "D1-0002_MLO_L_AnnotationFile.json"
    path_save = "D1-0002_MLO_L_overlaied.png"
    overlay_masks(path_dicom, path_json, path_save)