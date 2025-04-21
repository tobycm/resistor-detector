import cv2
import cvzone
import numpy as np
from cvzone.FPS import FPS
from sklearn.cluster import KMeans

# Reference HSV color values (Hue: 0–179 for OpenCV)
HSV_BAND_COLORS = {
    'black': (0, 0, 0),
    'brown': (10, 150, 80),
    'red': (0, 255, 255),
    'orange': (10, 255, 255),
    'yellow': (30, 255, 255),
    'green': (60, 255, 255),
    'blue': (120, 255, 255),
    'violet': (140, 100, 255),
    'gray': (0, 0, 120),
    'white': (0, 0, 255)
}

fpsReader = FPS(avgCount=30)

cam_id = int(input("Enter camera ID (default 0): ") or 0)

cap = cv2.VideoCapture(cam_id)
cap.set(cv2.CAP_PROP_FPS, 30)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    cropped = cv2.resize(frame, None, fx=0.5, fy=0.5)  #[0:1080, 150:1300]
    blurred = cv2.bilateralFilter(cropped, 9, 75, 75)

    # adjusted = cv2.convertScaleAbs(blurred, alpha=alpha)

    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    thres = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)
    inverted = cv2.bitwise_not(thres)

    kernel = np.ones((5, 5), np.uint8)

    closing = cv2.morphologyEx(inverted, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    filled = cv2.drawContours(closing,
                              contours,
                              -1,
                              color=(255, 255, 255),
                              thickness=cv2.FILLED)

    closing2 = cv2.morphologyEx(filled, cv2.MORPH_CLOSE, kernel)

    kernel = np.ones((10, 10), np.uint8)

    opening2 = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    cv2.imshow("Resistor Color 1", opening2)

    contours, _ = cv2.findContours(opening2, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) < 500:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(cropped, "Resistor", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)

    fps, img = fpsReader.update(cropped,
                                pos=(20, 50),
                                bgColor=(255, 0, 255),
                                textColor=(255, 255, 255),
                                scale=3,
                                thickness=3)

    cv2.imshow("Resistor Color 2", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
