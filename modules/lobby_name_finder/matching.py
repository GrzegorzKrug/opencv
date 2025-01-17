import pytesseract
import numpy as np
import time
import glob
import cv2
import os

all_pic_paths = glob.glob("Screenshots/*png")

"Load template for looking for group"
template = cv2.imread("template_looking.png")
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
height, width = template.shape
extend = 220
threshold = 0.8

for pic_path in all_pic_paths:
    "Iterate over pictures to find names in it"

    "Print picture and directory"
    cur_dir = os.path.join(f"exports")
    print(pic_path.ljust(80))

    "Load picture"
    img_bgr = cv2.imread(pic_path)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    if len(loc[0]) < 1:
        continue

    "Create folder to put all pics into."
    os.makedirs(cur_dir, exist_ok=True)
    for num, pt in enumerate(zip(*loc)):
        "Save matched positions"
        image_path = os.path.join(cur_dir, f"pic_{num:>02}_{int(time.time() * 10000)}.png")
        h, w = pt
        if os.path.isfile(image_path):
            print(f"This file exists! {image_path}")
            continue
        pic_of_name = img_bgr[h:h + height, w - extend:w + width]
        cv2.imwrite(image_path, pic_of_name)

print("Iteration over")
cv2.destroyAllWindows()
