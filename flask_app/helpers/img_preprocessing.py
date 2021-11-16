import cv2
import numpy as np
import matplotlib.pyplot as plt


# GRAYSCALE
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# NOISE REMOVAAL
def remove_noise(image):
    return cv2.medianBlur(image, 5)


" THRESHOLDING"
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# DILATION
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# EROSION
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# CANNY EDGES DETECTOPN
def canny(image):
    return cv2.Canny(image, 100, 200)


# SKEW CORRECTION
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# TEMPLATE MATCHING
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# SHOW IMAGES
def show_images(images, cols=1, titles=None):
    assert ((titles is None) or (len(images) == len(titles)))
    n_images = len(images)
    if titles is None: titles = ['Image (%d)' % i for i in range(1, n_images + 1)]
    fig = plt.figure()
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images / float(cols)), n + 1)
        if image.ndim == 2:
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
    plt.show()


image = plt.imread('website/ocr/image.jpg')
image = image[..., ::-1]
img_transforms = [gray, thresh, rnoise, dilate, erode, opening, canny]
show_images(images, 3, ["gray", "thresh", "rnoise", "dilate", "erode", "opening", "canny"])


# print(image)
# deskew = deskew(image)
gray = get_grayscale(image)
thresh = thresholding(gray)
rnoise = remove_noise(gray)
dilate = dilate(gray)
erode = erode(gray)
opening = opening(gray)
canny = canny(gray)

# Adding custom options
# custom_config = r'--oem 3 --psm 6'
# pytesseract.image_to_string(img, config=custom_config)

# PAGE SEGMENTTION METHOD

psm = {
    0: "Orientation and script detection (OSD) only.",
    1: "Automatic page segmentation with OSD.",
    2: "Automatic page segmentation, but no OSD, or OCR.",
    3: "Fully automatic page segmentation, but no OSD. (Default)",
    4: "Assume a single column of text of variable sizes.",
    5: "Assume a single uniform block of vertically aligned text.",
    6: "Assume a single uniform block of text.",
    7: "Treat the image as a single text line.",
    8: "Treat the image as a single word.",
    9: "Treat the image as a single word in a circle.",
    10: "Treat the image as a single character.",
    11: "Sparse text (Find as much text as possible in no particular order)",
    12: "Sparse text with OSD.",
    13: "Raw line(Treat the image as a single text line bypassing hacks that are Tesseract-specific)"
}

# OCR ENGINE MODE

engine_mode = {
    0: "Legacy engine only.",
    1: "Neural nets LSTM engine only.",
    2: "Legacy + LSTM engines.",
    3: "Default, based on what is available."
}