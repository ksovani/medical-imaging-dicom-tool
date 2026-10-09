import os
import pydicom

root_folder = "data/tcia_download_small"

count = 0

for root, dirs, files in os.walk(root_folder):
    for file in files:
        path = os.path.join(root, file)

        try:
            ds = pydicom.dcmread(path, stop_before_pixels=True, force=True)

            if "Modality" in ds:
                print("DICOM file:", path)
                print("  Modality:", ds.get("Modality", "N/A"))
                print("  Study Description:", ds.get("StudyDescription", "N/A"))
                print("  Series Description:", ds.get("SeriesDescription", "N/A"))
                print()
                count += 1

                if count >= 10:
                    break

        except Exception:
            pass

    if count >= 10:
        break

print(f"Found {count} DICOM-like files.")
