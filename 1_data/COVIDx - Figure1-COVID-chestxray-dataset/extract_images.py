
import pandas as pd
import shutil
import os
import math
import re

# I'm assuming that this repo does not contain repeated images from Cohen

metadata = "metadata.csv"
imagedir = "images"
outputdir = "../../2_Raw/Figure1"

# Remove output dir if present
if os.path.isdir(outputdir):
  shutil.rmtree(outputdir)

mask_dir = os.path.join(outputdir, "Masks")
if not os.path.isdir(mask_dir):
  os.makedirs(mask_dir)

metadata_csv = pd.read_csv(metadata, encoding = 'ISO-8859-1')

for (i, row) in metadata_csv.iterrows():

  if row["finding"] != "COVID-19":
    continue

  filename = row["patientid"]

  if os.path.isfile(os.path.join(imagedir, filename + ".png")):
    ext = ".png"
  else:
    ext = ".jpg"

  image_path = os.path.join(imagedir, filename + ext)

  # Check if destination folder exists, if not create it
  dest_dir = os.path.join(outputdir, "COVID-19")
  if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

  # Copy image
  shutil.copy2(image_path, dest_dir)

  _, pid = re.split("-", row["patientid"])
  offset = row["offset"]

  try:
    offset = int(offset)
  except:
    offset = 0

  new_filename = "P" + str(pid) + "_" + str(offset)
  new_filename_ext = "P" + str(pid) + "_" + str(offset)
  old_file = os.path.join(dest_dir, filename + ext)
  new_file = os.path.join(dest_dir, new_filename_ext + ext)
  os.rename(old_file, new_file)

  # Check if there are any mask provided for this image
  mask_filename = filename + ".png"
  mask_filepath = os.path.join("Masks", mask_filename)
  if os.path.exists(mask_filepath):
    shutil.copy2(mask_filepath, mask_dir)
    old_file = os.path.join(mask_dir, mask_filename)
    new_file = os.path.join(mask_dir, new_filename + ".png")
    os.rename(old_file, new_file)
