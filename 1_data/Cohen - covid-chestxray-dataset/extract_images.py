
import pandas as pd
import shutil
import os
import math
import json
import cv2
import numpy as np

# Cohen repo provides a very heterogeneous set of radiological images from a diagnostic point of view
#  I tried to be as accurate as possible while following our objective of identifying the cause of infection that lead to pneumonia
covid = ["Pneumonia/Viral/COVID-19"]

virus = ["Pneumonia/Viral/SARS", "Pneumonia/Viral/Influenza", "Pneumonia/Viral/Herpes", "Pneumonia/Viral/Herpes ", "Pneumonia/Viral/MERS-CoV",
  "Pneumonia/Viral/SARS", "Pneumonia/Viral/Varicella", "Pneumonia/Viral/Influenza/H1N1"]

bacteria = ["Pneumonia/Bacterial/Streptococcus", "Pneumonia/Bacterial/Klebsiella", "Pneumonia/Bacterial/Legionella",
	"Pneumonia/Bacterial/Nocardia", "Pneumonia/Bacterial/Staphylococcus/MRSA", "Pneumonia/Bacterial/E.Coli",
  "Pneumonia/Bacterial/Mycoplasma", "Pneumonia/Bacterial/Chlamydophila"]

fungi = ["Pneumonia/Fungal/Pneumocystis", "Pneumonia/Fungal/Aspergillosis", "Pneumonia/Bacterial/Streptococcus",
  "Pneumonia/Bacterial/E.Coli"]

normal = ["No Finding"]

pneumonia = ["Pneumonia", "Pneumonia/Lipoid", "Pneumonia/Aspiration"]

ignore = ["todo", "Tuberculosis", "Unknown"]

# We are going to use PA, AP and AP Supine view, right now we are not interested in lateral x-ray
x_ray_view = ["PA", "AP", "AP Supine", "AP semi erect", "AP erect"]

metadata = "metadata.csv"
imagedir = "images"
outputdir = "../../2_Raw/Cohen"

# Remove output dir if present
if os.path.isdir(outputdir):
  shutil.rmtree(outputdir)

mask_dir = os.path.join(outputdir, "Masks")
if not os.path.isdir(mask_dir):
  os.makedirs(mask_dir)


# Open the v7labs JSON that contains information about the segmentation masks
v7labs_mask_dict = {}
for json_filename in os.listdir("../Masks - covid-19-xray-dataset/annotations/all-images"):
  with open(os.path.join("../Masks - covid-19-xray-dataset/annotations/all-images", json_filename)) as json_file:
    data = json.load(json_file)
    v7labs_filename = os.path.splitext(json_filename)[0]
    cohen_filename = data["image"]["original_filename"]
    v7labs_mask_dict[cohen_filename] = v7labs_filename


metadata_csv = pd.read_csv(metadata)
for (i, row) in metadata_csv.iterrows():
  # Only use X-ray with PA (frontal) view
  if row["view"] not in x_ray_view:
    continue

  # Split the images by its finding
  fndg = row["finding"]
  if fndg in ignore:
  	continue
  elif fndg in virus:
    folder = "Virus"
  elif fndg in covid:
    folder = "."
  elif fndg in bacteria:
    folder = "Bacteria"
  elif fndg in fungi:
    folder = "Fungi"
  elif fndg in normal:
    folder = "."
    fndg = "Normal"
  elif fndg == "Pneumonia/Bacterial":
    folder = "."
    fndg = "Bacteria"
  elif fndg in pneumonia:
    folder = "."
    fndg = "Pneumonia"
  else:
    print("New class = ", fndg)
    continue

  fndg = fndg.replace("Pneumonia/Fungal/", "")
  fndg = fndg.replace("Pneumonia/Bacterial/", "")
  fndg = fndg.replace("Pneumonia/Viral/", "")

  filename = row["filename"].split(os.path.sep)[-1]
  image_path = os.path.sep.join([imagedir, filename])

  # Check if destination folder exists, if not create it
  dest_dir = os.path.join(outputdir, folder, fndg)
  if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

  # Copy image
  shutil.copy2(image_path, dest_dir)

  # Rename the file to a more representative name
  pid = row["patientid"]
  offset = row["offset"]

  try:
    offset = int(offset)
  except:
    offset = 0

  ext = os.path.splitext(filename)[1]
  new_filename = "P" + str(pid) + "_" + str(offset)
  new_filename_ext = "P" + str(pid) + "_" + str(offset) + ext
  old_file = os.path.join(dest_dir, filename)
  new_file = os.path.join(dest_dir, new_filename_ext)
  os.rename(old_file, new_file)


  # Check if there are any mask provided for this image
  # First, lets check the v7labs mask
  if filename in v7labs_mask_dict:
    mask_filename = v7labs_mask_dict[filename] + ".png"
    mask_filepath = os.path.join("../Masks - covid-19-xray-dataset/annotations/all-images-semantic-png/masks", mask_filename)
    shutil.copy2(mask_filepath, mask_dir)
    old_file = os.path.join(mask_dir, mask_filename)
    new_file = os.path.join(mask_dir, new_filename + ".png")
    os.rename(old_file, new_file)

    # Remove the mask with pixels containing 127
    img = cv2.imread(new_file, 0)
    img = np.uint8(img == 255) * 255
    cv2.imwrite(new_file, img)
    continue

  # Then, check the VAE provided masks
  mask_filename = os.path.splitext(filename)[0] + "_mask.png"
  mask_filepath = os.path.join("annotations/lungVAE-masks", mask_filename)
  if os.path.exists(mask_filepath):
    shutil.copy2(mask_filepath, mask_dir)
    old_file = os.path.join(mask_dir, mask_filename)
    new_file = os.path.join(mask_dir, new_filename + ".png")
    os.rename(old_file, new_file)
    continue

  # Finally, check for our manually created masks
  mask_filename = os.path.splitext(filename)[0] + "_mask.png"
  mask_filepath = os.path.join("annotations/manual_masks", mask_filename)
  if os.path.exists(mask_filepath):
    shutil.copy2(mask_filepath, mask_dir)
    old_file = os.path.join(mask_dir, mask_filename)
    new_file = os.path.join(mask_dir, new_filename + ".png")
    os.rename(old_file, new_file)
    continue
