# Helper functions that perform operations with screen

import os
import time
import numpy as np
import cv2


# --- Pre-generate scaled solid template crops at startup ---
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "notification_tree.png")
_raw_template = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_UNCHANGED)

# Optimal scale for your device resolution (2340x1080) is ~0.79
SCALES = [0.78, 0.80]

SCALED_TEMPLATES = []
if _raw_template is not None:
    # Solid 22x24 crop of the tree icon and interior (no transparent corners)
    _crop = _raw_template[3:25, 2:26, :3]
    _crop_h, _crop_w = _crop.shape[:2]

    for s in SCALES:
        tw = max(4, int(_crop_w * s))
        th = max(4, int(_crop_h * s))
        t_crop = cv2.resize(_crop, (tw, th), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
        # Offset to template center (14, 17) from crop origin (2, 3)
        offset_x = int(12 * s)
        offset_y = int(14 * s)
        SCALED_TEMPLATES.append((s, tw, th, t_crop, offset_x, offset_y))


def screenshot(d):
    """Take a screenshot."""
    img = d.screenshot()
    # To CV2 format
    cv_img = np.array(img.convert('RGB'))
    # Convert RGB to BGR
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    return cv_img


def pop_bubbles(d, cv_img, threshold=0.68):
    """
    Finds and clicks all notification bubbles.
    """
    if not SCALED_TEMPLATES:
        print("Template notification_tree.png not loaded.")
        return

    # Morphological kernel for fast peak finding (local maxima)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    detected_bubbles = []

    for s, tw, th, t_crop, off_x, off_y in SCALED_TEMPLATES:
        res = cv2.matchTemplate(cv_img, t_crop, cv2.TM_CCOEFF_NORMED)

        # Vectorized local peak detection in OpenCV
        dilated = cv2.dilate(res, kernel)
        peaks = (res == dilated) & (res >= threshold)
        ys, xs = np.where(peaks)

        for y, x in zip(ys, xs):
            score = float(res[y, x])
            cx = x + off_x
            cy = y + off_y
            detected_bubbles.append((cx, cy, score))

    if not detected_bubbles:
        return

    # Sort peaks by score descending
    detected_bubbles.sort(key=lambda b: b[2], reverse=True)

    # Deduplicate peaks across different scales
    unique_centers = []
    min_dist_sq = 15 ** 2

    for cx, cy, _ in detected_bubbles:
        if not any((cx - ux) ** 2 + (cy - uy) ** 2 < min_dist_sq for ux, uy in unique_centers):
            unique_centers.append((cx, cy))

    # Click detected bubbles
    for cx, cy in unique_centers:
        d.click(cx, cy)
        time.sleep(0.1)


def close_notification(d, cv_img):
    """Close a notification if it is accidentally opened."""
    c = cv_img[600:660, 860:930]
    clr_min = np.array([80, 90, 210])
    clr_max = np.array([90, 100, 220])
    clr_mean = c.mean(axis=(0, 1))
    if np.all((clr_mean >= clr_min) & (clr_mean <= clr_max)):
        d.click(900, 630)


def check(d):
    """Check and pop all the bubbles on screen."""
    img = screenshot(d)
    pop_bubbles(d, img)
    close_notification(d, img)


def check_heart(d):
    """Check and collect the heart."""
    # Check if heart available
    while not heart_available(d):
        time.sleep(1)
    d.click(970, 380)
    time.sleep(5)
    d.click(0.5, 0.52)
    img = screenshot(d)
    # Top heart
    img1 = img[850:1050, 730:950]
    if check_if_heart_here(img1):
        d.swipe(850, 950, 850, 950, 4)
    # Middle heart
    img2 = img[1100:1350, 730:950]
    if check_if_heart_here(img2):
        d.swipe(850, 1200, 850, 1200, 4)
    # Bottom heart
    img3 = img[1350:1600, 730:950]
    if check_if_heart_here(img3):
        d.swipe(850, 1450, 850, 1450, 4)
    time.sleep(2)
    d.swipe(930, 1800, 930, 1800, 0.1)
    time.sleep(1)
    d.click(900, 630)


def check_heart_instant(d):
    """Check and collect the heart with first wonder unlocked."""
    # Check if heart available
    while not heart_available(d):
        time.sleep(1)
    d.click(970, 380)
    time.sleep(5)
    d.click(0.5, 0.52)
    time.sleep(2)
    d.swipe(930, 1800, 930, 1800, 0.1)
    time.sleep(1)
    time.sleep(1)
    d.click(900, 630)


def heart_available(d):
    """Check if any heart is available for collecting."""
    img = screenshot(d)
    a = img[380, 970]
    time.sleep(0.11)
    img = screenshot(d)
    b = img[380, 970]
    if a[0] == b[0]:
        return False
    else:
        return True


def check_if_heart_here(img):
    """Check if heart is in the selected position."""
    img = cv2.GaussianBlur(img, (25, 25), 0)
    img = cv2.Canny(image=img, threshold1=5, threshold2=10)
    if img.sum() > 1000:
        return True
    else:
        return False
