import numpy as np
import click
import imutils
import cv2
from pyzbar.pyzbar import decode, ZBarSymbol


@click.command()
@click.option("--image-file", type=str, help="Full path to image", required=True)
def main(image_file):
    img = cv2.imread(image_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    blurred = cv2.blur(gradient, (18, 18))
    cv2.imshow("blurred", blurred)
    cv2.waitKey(0)
    _, thresh = cv2.threshold(blurred, 115, 255, cv2.THRESH_BINARY)

    cv2.imshow("thresh", thresh)
    cv2.waitKey(0)

    main_area = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    new_area = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, main_area)
    cv2.imshow("area", new_area)
    cv2.waitKey(0)

    new_area = cv2.erode(new_area, None, iterations=6)
    new_area = cv2.dilate(new_area, None, iterations=5)
    cv2.imshow("area2", new_area)
    cv2.waitKey(0)

    contours = cv2.findContours(new_area.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    contours_min = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    (X, Y, W, H) = cv2.boundingRect(contours_min)
    rect = cv2.minAreaRect(contours_min)
    box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
    box = np.int0(box)

    cv2.drawContours(img, [box], -1, (0, 255, 0), 3)
    cropped_image = img[Y : Y + H, X : X + W].copy()
    cv2.imshow("final cropped", cropped_image)
    cv2.waitKey(0)

    detectedBarcodes = decode(cropped_image, symbols=[ZBarSymbol.EAN13])
    barcode = detectedBarcodes[0]
    # final result what we found
    print(barcode)
    print(f"Scanned code: {barcode.data}")


if __name__ == "__main__":
    main()
