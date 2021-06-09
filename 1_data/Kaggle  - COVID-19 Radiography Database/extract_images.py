
import pandas as pd
import shutil
import os
import math
import re

# This repo has a lot of repeated images from Cohen repo, so we will just grab those that are not in Cohen repo

cohen_metadata = "../Cohen - covid-chestxray-dataset/metadata.csv"
metadata = "COVID-19.metadata.xlsx"
imagedir = "COVID-19"
outputdir = "../../2_Raw/KaggleCRD"

# Remove output dir if present
if os.path.isdir(outputdir):
  shutil.rmtree(outputdir)

mask_dir = os.path.join(outputdir, "Masks")
if not os.path.isdir(mask_dir):
  os.makedirs(mask_dir)

cohen_metadata_csv = pd.read_csv(cohen_metadata)
metadata_csv = pd.read_excel(metadata)

# images with bad resolution or otherwise bad
discard = [100, 101, 102, 103, 104, 105,
           110, 111, 112, 113, 122, 123,
           124, 125, 126, 217]

for (i, row) in metadata_csv.iterrows():

  if row["URL"] in cohen_metadata_csv["url"].values:
    continue

  if i + 1 in discard:
    continue

  filename = row["FILE NAME"]
  if not os.path.isfile(os.path.join(imagedir, filename + ".png")):
    filename = row["FILE NAME"].replace("(", " (")

  image_path = os.path.join(imagedir, filename + ".png")

  # Check if destination folder exists, if not create it
  dest_dir = os.path.join(outputdir, "COVID-19")
  if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

  # Copy image
  shutil.copy2(image_path, dest_dir)

  _, pid, _ = re.split("[()]", filename)
  offset = 0

  ext = os.path.splitext(filename)[1]
  new_filename = "P" + str(pid) + "_" + str(offset)
  new_filename_ext = "P" + str(pid) + "_" + str(offset) + ext
  old_file = os.path.join(dest_dir, filename + ".png")
  new_file = os.path.join(dest_dir, new_filename_ext + ".png")
  os.rename(old_file, new_file)

  # Check if there are any mask provided for this image
  mask_filename = filename + ".png"
  mask_filepath = os.path.join("Masks", mask_filename)
  if os.path.exists(mask_filepath):
    shutil.copy2(mask_filepath, mask_dir)
    old_file = os.path.join(mask_dir, mask_filename)
    new_file = os.path.join(mask_dir, new_filename + ".png")
    os.rename(old_file, new_file)