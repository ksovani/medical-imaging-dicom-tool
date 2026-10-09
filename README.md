# DICOM Medical Image Processing Tool

This project is a Python-based medical imaging tool for loading, visualizing, and processing DICOM images.

## Features

- Load DICOM medical images using pydicom
- Allow user to choose between a built-in sample DICOM file and local DICOM files from the data/ folder
- Extract and display DICOM metadata
- Convert CT image pixels using rescale slope and intercept
- Apply CT window/level adjustment
- Generate original/windowed image comparison outputs
- Save output visualizations

## Tools Used

- Python
- pydicom
- NumPy
- Matplotlib
  
## Development Support
ChatGPT was used as a learning and development aid for brainstorming project features, explaining DICOM concepts, debugging setup issues, and improving documentation. All code was reviewed and tested by the project author.

## Current Status

Milestone 1 completed: basic DICOM loading, metadata extraction, local file selection, visualization, and window/level adjustment.

## Future Improvements

- Add CT window/level presets for soft tissue, lung, bone, and brain
- Add segmentation
- Calculate region area and mean intensity
- Add image quality metrics
- Add support for loading full DICOM series
- Add a simple GUI
