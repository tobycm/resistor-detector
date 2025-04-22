# Resistor detector using OpenCV

This is a primitive OpenCV project that detects resistors in an image or a video feed. It finds contours in the image, apply some color conversion, adaptive thresholding, morphological open and close, and finally drawing bounding boxes around the detected resistors.

## How to use

### Requirements
- Python 3.x

### Setup

Install the required packages using pip:

```sh
pip install -U -r requirements.txt
```

### Run the script

```sh
python3 main.py
```