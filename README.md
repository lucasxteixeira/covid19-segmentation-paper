# Impact of lung segmentation on the diagnosis and explanation of COVID-19 in chest X-ray images

Code for the paper: "Impact of lung segmentation on the diagnosis and explanation of COVID-19 in chest X-ray images"

# Data

We did not include the original images used to compose the database evaluated in this work due to its large size. Instead, we provide all references and links directly in the paper.

This repository contains all the scripts developed for the experiments in this paper. The structure is as follows:

* 1_data contains all preprocessing scripts used to standardize the multiple image sources.
* 2_segmentation contains the notebook (code) as well as a cached version of the U-Net Keras model.
* 3_classification contains the notebooks used in the classification experiments in Keras and all the estimated statistical models and plots in R.
* 4_images contains the final segmented images and their respective masks used in our experiments.

# Results

## Lung segmentation

|        Database        | Jaccard distance | Dice coefficient |
|------------------------|------------------|------------------|
| Cohen v7labs           | 0.041 +- 0.027   | 0.979 +- 0.014   |
| Montgomery             | 0.019 +- 0.007   | 0.991 +- 0.003   |
| Shenzhen               | 0.017 +- 0.008   | 0.991 +- 0.004   |
| JSRT                   | 0.018 +- 0.011   | 0.991 +- 0.006   |
| Manually created masks | 0.071 +- 0.021   | 0.964 +- 0.011   |
| Test set               | 0.035 +- 0.027   | 0.982 +- 0.014   |

## COVID-19 identification

|            Class            | COVID-19 | Lung opacity | Normal | Macro-avg |
|-----------------------------|----------|--------------|--------|-----------|
| Segmented - VGG16           |     0.83 |         0.88 |    0.9 |      0.87 |
| Segmented - ResNet50V2      |     0.78 |         0.87 |   0.91 |      0.85 |
| Segmented - InceptionV3     |     0.83 |         0.89 |   0.92 |      0.88 |
| Non-segmented - VGG16       |     0.94 |         0.91 |   0.91 |      0.92 |
| Non-segmented - ResNet50V2  |     0.91 |          0.9 |   0.92 |      0.91 |
| Non-segmented - InceptionV3 |     0.86 |          0.9 |   0.91 |       0.9 |

## XAI

![](XAI.jpg?raw=true)

# Citation

```
@article{teixeira2020covidimpact,
  title = {Impact of Lung Segmentation on the Diagnosis and Explanation of COVID-19 in Chest X-ray Images},
  volume = {21},
  ISSN = {1424-8220},
  url = {http://dx.doi.org/10.3390/s21217116},
  DOI = {10.3390/s21217116},
  number = {21},
  journal = {Sensors},
  publisher = {MDPI AG},
  author = {Teixeira,  Lucas O. and Pereira,  Rodolfo M. and Bertolini,  Diego and Oliveira,  Luiz S. and Nanni,  Loris and Cavalcanti,  George D. C. and Costa,  Yandre M. G.},
  year = {2021},
  month = oct,
  pages = {7116}
}
```
