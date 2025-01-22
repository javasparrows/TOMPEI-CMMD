import pydicom
import json

def check_masks_and_labels_in_dicom(dicom_path):
    # Load the DICOM file
    ds = pydicom.dcmread(dicom_path)

    # Display basic patient information
    print("Patient's Name:", ds.get("PatientName", "Unknown"))
    print("Patient ID:", ds.get("PatientID", "Unknown"))
    print("Patient's Sex:", ds.get("PatientSex", "Unknown"))
    print("Study Date:", ds.get("StudyDate", "Unknown"))
    print("Modality:", ds.get("Modality", "Unknown"))

    # Display the image laterality and view type
    image_laterality = ds.get((0x0020, 0x0062), "Unknown")
    print("Image Laterality:", image_laterality)
    view_sequence = ds.get((0x0054, 0x0220), [])
    if view_sequence:
        view_code = view_sequence[0].get((0x0008, 0x0104), "Unknown View")
        print("View Type:", view_code)
    else:
        print("View Type: Unknown")

    # Define the private tags where masks and labels are stored
    private_mask_tag = (0x0013, 0x1010)  # Mask data
    private_label_tag = (0x0013, 0x1011)  # Label data
    
    # Check if data is stored in the private tags
    if private_mask_tag in ds and private_label_tag in ds:
        # Retrieve mask data
        mask_json = ds[private_mask_tag].value
        mask_list = json.loads(mask_json)
        print(f"len(mask_list): {len(mask_list)}")
        print(mask_list[-1])

        # Retrieve label data
        label_json = ds[private_label_tag].value
        label_list = json.loads(label_json)
        print(f"len(label_list): {len(label_list)}")
        print(label_list)
    else:
        print("No masks or labels found in this DICOM file.")

# Specify the path to the DICOM file
dicom_path = "D2-0116/MLO_R/DicomFile.dcm"
check_masks_and_labels_in_dicom(dicom_path)
