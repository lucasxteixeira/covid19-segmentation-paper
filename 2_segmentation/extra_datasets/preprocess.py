import os
import shutil
import cv2
import numpy as np

# Preprocess the Montgomery and Shenzhen datasets in order to resize all images to our standard resolution
# and also apply CLAHE
# This will save time when running the notebooks in the future

img_size = 400

clahe = cv2.createCLAHE(clipLimit = 2.0, tileGridSize = (8, 8))



# Let's start with Montgomery dataset
montgomery_folder = "Montgomery"
dest_folder = os.path.join(montgomery_folder, "processed")

# Remove destination dir, if present, just for start clean
if os.path.isdir(dest_folder):
  shutil.rmtree(dest_folder)

# Create intermediate folders, if they are not present
if not os.path.isdir(dest_folder):
  os.makedirs(dest_folder)

CXR_folder = os.path.join(dest_folder, "CXR")
if not os.path.isdir(CXR_folder):
  os.makedirs(CXR_folder)

masks_folder = os.path.join(dest_folder, "Masks")
if not os.path.isdir(masks_folder):
  os.makedirs(masks_folder)

for img_path in os.listdir(os.path.join(montgomery_folder, "CXR")):
  img = cv2.imread(os.path.join(montgomery_folder, "CXR", img_path), 0)
  img = cv2.resize(img, (img_size, img_size), interpolation = cv2.INTER_CUBIC)
  #img = clahe.apply(img)

  mask_left_path = os.path.join(montgomery_folder, "Masks", "Left", img_path)
  mask_left = cv2.imread(mask_left_path, 0)
  mask_left = cv2.resize(mask_left, (img_size, img_size), interpolation = cv2.INTER_CUBIC)

  mask_right_path = os.path.join(montgomery_folder, "Masks", "Right", img_path)
  mask_right = cv2.imread(mask_right_path, 0)
  mask_right = cv2.resize(mask_right, (img_size, img_size), interpolation = cv2.INTER_CUBIC)

  mask = np.add(mask_left, mask_right)

  cv2.imwrite(os.path.join(CXR_folder, img_path), img)
  cv2.imwrite(os.path.join(masks_folder, img_path), mask)





# Let's start with Shenzhen dataset
shenzhen_folder = "Shenzhen"
dest_folder = os.path.join(shenzhen_folder, "processed")

# Remove destination dir, if present, just for start clean
if os.path.isdir(dest_folder):
  shutil.rmtree(dest_folder)

# Create intermediate folders, if they are not present
if not os.path.isdir(dest_folder):
  os.makedirs(dest_folder)

CXR_folder = os.path.join(dest_folder, "CXR")
if not os.path.isdir(CXR_folder):
  os.makedirs(CXR_folder)

masks_folder = os.path.join(dest_folder, "Masks")
if not os.path.isdir(masks_folder):
  os.makedirs(masks_folder)

for img_path in os.listdir(os.path.join(shenzhen_folder, "CXR")):
  img = cv2.imread(os.path.join(shenzhen_folder, "CXR", img_path), 0)
  img = cv2.resize(img, (img_size, img_size), interpolation = cv2.INTER_CUBIC)
  #img = clahe.apply(img)

  mask_filename = os.path.splitext(img_path)[0] + "_mask.png"

  # Not all images from Shenzhen have manually segmented masks
  # If the lung is not segmented, then just skip it
  # Also, some images contain the heart information while others don't
  # This probably won't much difference but it is important to mention it in the article
  if os.path.exists(os.path.join(shenzhen_folder, "Masks", mask_filename)):
    mask_path = os.path.join(shenzhen_folder, "Masks", mask_filename)
    mask = cv2.imread(mask_path, 0)
    mask = cv2.resize(mask, (img_size, img_size), interpolation = cv2.INTER_CUBIC)

    cv2.imwrite(os.path.join(CXR_folder, img_path), img)
    cv2.imwrite(os.path.join(masks_folder, img_path), mask)








# Let's start with JSRT dataset
jsrt_folder = "JSRT"
dest_folder = os.path.join(jsrt_folder, "processed")

# Remove destination dir, if present, just for start clean
if os.path.isdir(dest_folder):
  shutil.rmtree(dest_folder)

# Create intermediate folders, if they are not present
if not os.path.isdir(dest_folder):
  os.makedirs(dest_folder)

CXR_folder = os.path.join(dest_folder, "CXR")
if not os.path.isdir(CXR_folder):
  os.makedirs(CXR_folder)

masks_folder = os.path.join(dest_folder, "Masks")
if not os.path.isdir(masks_folder):
  os.makedirs(masks_folder)

for img_path in os.listdir(os.path.join(jsrt_folder, "CXR")):
  img = cv2.imread(os.path.join(jsrt_folder, "CXR", img_path), cv2.IMREAD_UNCHANGED).astype(np.uint8)
  img = cv2.resize(img, (img_size, img_size), interpolation = cv2.INTER_CUBIC)
  #img = clahe.apply(img)

  mask = cv2.imread(os.path.join(jsrt_folder, "Masks", img_path), cv2.IMREAD_UNCHANGED).astype(np.uint8)
  mask = cv2.resize(mask, (img_size, img_size), interpolation = cv2.INTER_CUBIC)

  img_path = os.path.splitext(img_path)[0]
  img_path = img_path + ".png"

  cv2.imwrite(os.path.join(CXR_folder, img_path), img)
  cv2.imwrite(os.path.join(masks_folder, img_path), mask)