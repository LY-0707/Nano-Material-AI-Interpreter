import cv2

def load_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img


def preprocess(img):
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)
    return thresh