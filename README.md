# TOMPEI-CMMD

This repository provides sample Python code to **view, overlay, and inspect** selected TOMPEI-CMMD dataset files from **The Cancer Imaging Archive (TCIA)**. Although actual DICOM images and JSON annotations are **not** included here, you can use these scripts to handle the corresponding files if you download them separately.

---

## Files

```
./
├── overlay_json.py       # Overlays annotation polygons (from JSON) onto a DICOM image
├── get_info_from_dicom.py  # Reads DICOM metadata, including potential private-tag annotations
├── overlay_json.ipynb    # Jupyter notebook version of overlay_json.py
├── overlay_images_save.py # Overlays annotation polygons on DICOM images and saves them (batch processing)
├── requirements.txt      # Dependencies
└── README.md             # This file
```

### overlay_json.py

- Reads a DICOM file and JSON polygons (`cgPoints`), then draws these overlays on the mammogram and saves as a PNG.

### get_info_from_dicom.py

- Checks certain private DICOM tags (e.g., `(0x0013, 0x1010)`) for mask/label data, then prints them.

### overlay_json.ipynb

- Jupyter notebook version for interactive demonstration.

---

## Usage

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run**:
   - Overlay example:
     ```bash
     python overlay_json.py
     ```
   - Inspect private tags:
     ```bash
     python get_info_from_dicom.py
     ```
3. **Notebook**:
   ```bash
   jupyter notebook overlay_json.ipynb
   ```

_(Adjust file paths as needed.)_

---

## Notes

- These scripts do **not** include DICOM or JSON data from TOMPEI-CMMD.
- For actual data, download the TOMPEI-CMMD dataset from TCIA.
- This code is a simple reference for research/education only.

Thank you for your interest in the TOMPEI-CMMD dataset!
