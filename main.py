import pydicom
from pydicom.data import get_testdata_file
import numpy as np
import matplotlib.pyplot as plt
import os #os module lets python script interact with operating system. Itis needed if the code needs to 1) Create folders, 2) check if a file/folder exists, 3) list files in a folder, 4) gets the current working directory, or 5) works with file paths


def apply_window_level(image, window, level):
    """
    Apply CT-style window/level adjustment.
    """
    lower = level - window / 2
    upper = level + window / 2

    image_windowed = np.clip(image, lower, upper)
    image_windowed = (image_windowed - lower) / (upper - lower)
    image_windowed = image_windowed * 255

    return image_windowed.astype(np.uint8)


def get_image_pixels(ds):
    """
    Convert DICOM pixel data to float image.
    If CT data has RescaleSlope and RescaleIntercept,
    apply them to convert to Hounsfield Units.
    """
    image = ds.pixel_array.astype(np.float32)

    slope = float(ds.get("RescaleSlope", 1))
    intercept = float(ds.get("RescaleIntercept", 0))

    image = image * slope + intercept

    return image


def print_metadata(ds):
    """
    Print useful DICOM metadata.
    """
    print("===== DICOM Metadata =====")
    print("Patient ID:", ds.get("PatientID", "N/A"))
    print("Modality:", ds.get("Modality", "N/A"))
    print("Study Description:", ds.get("StudyDescription", "N/A"))
    print("Series Description:", ds.get("SeriesDescription", "N/A"))
    print("Rows:", ds.get("Rows", "N/A"))
    print("Columns:", ds.get("Columns", "N/A"))
    print("Pixel Spacing:", ds.get("PixelSpacing", "N/A"))
    print("Slice Thickness:", ds.get("SliceThickness", "N/A"))
    print("==========================\n")

def is_dicom_image(file_path):
    """
    Checks whether a file looks like a readable DICOM image
    FIlters out non image files like .tcia, .zip, etc
    """
    try:
        ds = pydicom.dcmread(file_path, stop_before_pixels=True, force=True)

        modality = ds.get("Modality", None)
        rows = ds.get("Rows", None)
        columns = ds.get("Columns", None)

        # Only keep files that look like actual image slices
        if modality in ["CT", "MR", "PT", "CR", "DX"] and rows is not None and columns is not None:
            return True

        return False

    except Exception:
        return False
        

def find_dicom_images(root_folder="data"):
    """
    Search the data folder for DICOM image files.
    """
    dicom_files = []

    if not os.path.exists(root_folder):
        return dicom_files

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)

            if is_dicom_image(file_path):
                dicom_files.append(file_path)

    return dicom_files


def choose_dicom_path():
    """
    Let the user choose either the built-in pydicom sample
    or a local DICOM image from the data folder.
    """
    print("\nChoose DICOM source:")
    print("1. Use built-in pydicom sample")
    print("2. Choose local DICOM file from data/ folder")

    choice = input("Enter choice 1 or 2: ")

    if choice == "1":
        return get_testdata_file("CT_small.dcm")

    elif choice == "2":
        dicom_files = find_dicom_images("data")

        if len(dicom_files) == 0:
            print("\nNo local DICOM image files found in data/.")
            print("Using built-in pydicom sample instead.")
            return get_testdata_file("CT_small.dcm")

        print("\nFound DICOM image files:")

        for i, file_path in enumerate(dicom_files):
            print(f"{i + 1}. {file_path}")

        while True:
            try:
                selected = int(input("\nEnter file number to open: "))

                if 1 <= selected <= len(dicom_files):
                    return dicom_files[selected - 1]
                else:
                    print("Invalid number. Try again.")

            except ValueError:
                print("Please enter a valid number.")

    else:
        print("\nInvalid choice. Using built-in pydicom sample instead.")
        return get_testdata_file("CT_small.dcm")

def main():
    os.makedirs("outputs", exist_ok=True) #this is the line that required os, makedirs makes a directory

    # Use a built-in sample CT DICOM file from pydicom
    #dicom_path = get_testdata_file("CT_small.dcm")
    #dicom_path = "/home/kanaad/Projects/medical-imaging-dicom-tool/data/tcia_download_small/FDG-PET-CT-Lesions/PETCT_ff39795341/09-22-2005-PET-CT (Ganzkoerper  primaer mit KM)-98939/6.000000-GK p.v.3 s-65485/1-123.dcm"
    dicom_path = choose_dicom_path()    
    ds = pydicom.dcmread(dicom_path)

    print_metadata(ds)

    image = get_image_pixels(ds)

    # Common soft tissue CT window (units are in HU)
    window = 400
    level = 40

    windowed_image = apply_window_level(image, window, level)

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap="gray")
    plt.title("Original CT Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(windowed_image, cmap="gray")
    plt.title("Window/Level Adjusted")
    plt.axis("off")

    plt.tight_layout()
    plt.savefig("outputs/dicom_viewer_result.png", dpi=300)
    plt.show()

    print("Saved output image to outputs/dicom_viewer_result.png")


if __name__ == "__main__":
    main()
