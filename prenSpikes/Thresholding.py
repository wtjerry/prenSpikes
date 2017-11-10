import cv2
import os
import numpy as np

base = 'base'
stainsInWhite = 'stainsInWhite'
stainsInBlackAndWhite = 'stainsInBlackAndWhite'
stainsInBlack = 'stainsInBlack'


def show_image(windowname, img):
    cv2.imshow(windowname, img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def save_img(path, img):
    cv2.imwrite(path, img)


def threshold_and_show_image(path):
    i = cv2.imread(path)
    windowname = os.path.basename(path)
    ret, thresh = cv2.threshold(i, 200, 255, cv2.THRESH_BINARY)
    # ret, thresh = cv2.threshold(thresh, 250, 255, cv2.THRESH_BINARY_INV)
    # ret, thresh = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY)
    show_image(windowname, thresh)


def invert_image(image):
    return cv2.bitwise_not(image)


def invert_mask(mask):
    return cv2.invert(mask)


def mask_image(image, mask):
    tmp_img = image
    masked_image = cv2.bitwise_and(image, tmp_img, mask=mask)
    return masked_image


def run():
    images = {
        base: '../resources/blackWhiteTarget.png',
        stainsInWhite: '../resources/targetWithColorStainsInWhiteAreas.png',
        stainsInBlackAndWhite: '../resources/targetWithColorStainsInBlackAndWhiteAreas.png',
        stainsInBlack: '../resources/targetWithColorStainsInBlackAreas.png'
    }

    path = images[stainsInBlackAndWhite]    # choose which base image to use
    img = cv2.imread(path)
    img = invert_image(img)     # comment this line if you want to have the not inverted image, mask etc.
    show_image('base', img)
    create_and_print_mask_etc(img)


def create_and_print_mask_etc(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    zero_matrix = np.array([0, 0, 0])
    upper_black = np.array([30, 30, 30])

    mask = cv2.inRange(hsv, zero_matrix, upper_black)
    show_image('mask', mask)

    inverted_image = invert_image(img)
    show_image('inverted image', inverted_image)

    masked_image = mask_image(inverted_image, mask)
    show_image('masked image', masked_image)

    inverted_masked_image = invert_image(masked_image)
    show_image('inverted masked image', inverted_masked_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    cap = cv2.VideoCapture('../resources/slow.h264')
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        img = cv2.resize(img, (500, 500))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 127, 255, 0)
        img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) > 5000:  # remove small areas like noise etc
                hull = cv2.convexHull(cnt)  # find the convex hull of contour
                hull = cv2.approxPolyDP(hull, 0.1 * cv2.arcLength(hull, True), True)
                if len(hull) == 4:
                    cv2.drawContours(img, [hull], 0, (0, 255, 0), 2)

        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # run()
