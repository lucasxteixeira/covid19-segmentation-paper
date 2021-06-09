import os
import shutil
import re
import random
import cv2

# Split data in training/testing using a 80/20 distribution
# The distribution is centered around the patient since each person can have multiple images in different days
# So the idea is to keep all images from the same patient all in the same set (either train or test)


# The dataset is composed by CXR images of pneumonia (any other, except COVID-19), COVID-19 and Normal.
source_folders = ["A1", "A2", "Cohen", "Eurorad", "Radiopedia", "RSNA", "Actualmed", "Figure1", "Kaggle_CRD"]
pneumonia_folders = ["Bacteria", "Fungi", "Virus", "Pneumonia", "Lung Opacity"]
pathogen_folders = ["Bacteria", "Fungi", "Virus", "Pneumonia", "Lung Opacity", "COVID-19", "Normal"]
origin_folder = "2_Raw"
dest_folder = "3_Images"

img_size = 400

clahe = cv2.createCLAHE(clipLimit = 2.0, tileGridSize = (8, 8))

# Remove destination dir, if present, just for start clean
if os.path.isdir(dest_folder):
  shutil.rmtree(dest_folder)

# Create intermediate folders, if they are not present
if not os.path.isdir(dest_folder):
  os.makedirs(dest_folder)

if not os.path.isdir(os.path.join(dest_folder, "masks")):
  os.makedirs(os.path.join(dest_folder, "masks"))

for target in ["train", "test"]:
  for pathogen in ["Opacity", "COVID-19", "Normal"]:
    pathogen_folder = os.path.join(dest_folder, target, pathogen)
    if not os.path.isdir(pathogen_folder):
      os.makedirs(pathogen_folder)

# Iterate over all source folders and pathogens to copy the relevant images
for folder in source_folders:
  for pathogen in pathogen_folders:
    pathogen_folder = os.path.join(origin_folder, folder, pathogen)
    pathogen_coded = "Opacity" if pathogen in pneumonia_folders else pathogen
    if (os.path.isdir(pathogen_folder)):
      for (root, dirs, files) in os.walk(pathogen_folder, topdown = True):
        pid_list = {}
        for file in files:
          _, pid, offset = re.split("[P_]", os.path.splitext(file)[0])

          # If pid was not assigned to a group
          # Then random selected train/test following the desirable distribution
          if pid not in pid_list:
            prob = 0.8
            target_folder = "test" if random.uniform(0, 1) > prob else "train"
            pid_list[pid] = target_folder
          else:
            target_folder = pid_list[pid]

          # Copy image and rename file
          shutil.copy2(os.path.join(root, file), os.path.join(dest_folder, target_folder, pathogen_coded))
          new_filename = "%s_%s_%s_%s" % (folder, pathogen_coded, pid, offset)
          new_filename_ext = "%s%s" % (new_filename, os.path.splitext(file)[-1])
          os.rename(
            os.path.join(dest_folder, target_folder, pathogen_coded, file),
            os.path.join(dest_folder, target_folder, pathogen_coded, new_filename_ext),
          )

          # Well, let's already apply CLAHE to improve the CXR contrast and brightness
          img = cv2.imread(os.path.join(dest_folder, target_folder, pathogen_coded, new_filename_ext), 0)
          os.remove(os.path.join(dest_folder, target_folder, pathogen_coded, new_filename_ext))
          #img = clahe.apply(img)

          # Let's also resize the images so that all of them are standardize
          # Skip the image if it is too small
          w, h = img.shape
          if w < 300:
            continue

          img = cv2.resize(img, (img_size, img_size), interpolation = cv2.INTER_CUBIC)

          new_filename_ext = "%s%s" % (new_filename, ".png")
          cv2.imwrite(os.path.join(dest_folder, target_folder, pathogen_coded, new_filename_ext), img)

          # Check if there any mask for the specific
          # If yes, copy and resize it
          mask_file = "%s.png" % os.path.splitext(file)[0]
          mask_path = os.path.join(origin_folder, folder, "Masks", mask_file)
          if (os.path.isfile(mask_path)):
            mask_img = cv2.imread(mask_path, 0)
            mask_img = cv2.resize(mask_img, (img_size, img_size), interpolation = cv2.INTER_CUBIC)
            new_mask_filename = "%s_%s_%s_%s_%s.png" % (target_folder, folder, pathogen_coded, pid, offset)
            cv2.imwrite(os.path.join(dest_folder, "masks", new_mask_filename), mask_img)