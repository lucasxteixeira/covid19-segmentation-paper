
import os
import shutil
import cv2
import pandas as pd
import pydicom
import random
import numpy as np

df = pd.read_csv("stage_2_train_labels.csv")
df_detailed = pd.read_csv("stage_2_detailed_class_info.csv")

x_ray_view = ["PA", "AP"]
outputdir = "output"

random.seed(1234)

# Remove output dir if present
if os.path.isdir(outputdir):
  shutil.rmtree(outputdir)

mask_dir = os.path.join(outputdir, "Masks")
if not os.path.isdir(mask_dir):
  os.makedirs(mask_dir)

global_pid = 0

for target in ["Normal", "No Lung Opacity / Not Normal", "Lung Opacity"]:
  positive_target = df_detailed["class"] == target
  local_df = df_detailed[positive_target]
  local_df.reset_index(inplace = True)
  nrows = local_df.shape[0]

  # Check if destination folder exists, if not create it
  if target == "No Lung Opacity / Not Normal":
    dest_dir = os.path.join(outputdir, "Not normal")
  else:
    dest_dir = os.path.join(outputdir, target)

  if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

  pid_list = []
  pid = 0
  while pid < 1000:
    random_pid = random.randint(0, nrows - 1)
    full_pid = local_df["patientId"][random_pid]

    if full_pid in pid_list:
      continue

    dcm_file = "stage_2_train_images/%s.dcm" % full_pid
    dcm_data = pydicom.read_file(dcm_file)
    if dcm_data.ViewPosition not in x_ray_view:
      continue

    global_pid += 1
    pid += 1
    pid_list.append(full_pid)

    shape = dcm_data.pixel_array.shape
    image = dcm_data.pixel_array

    print("PID: %s - Original PID: %s" % (global_pid, full_pid))

    file_path = os.path.join(dest_dir, "P" + str(global_pid) + "_0.png")
    cv2.imwrite(file_path, image)

    # Mask
    mask_filename = full_pid + ".png"
    mask_filepath = os.path.join("Masks", mask_filename)
    if os.path.exists(mask_filepath):
      shutil.copy2(mask_filepath, mask_dir)
      old_file = os.path.join(mask_dir, mask_filename)
      new_file = os.path.join(mask_dir, "P" + str(global_pid) + "_0.png")
      os.rename(old_file, new_file)
      continue
