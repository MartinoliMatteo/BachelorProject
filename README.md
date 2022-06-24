# Image Luminosity Equalization For Deep Learning Applications
In this project, we will use image processing to modify the lighting conditions and reduce the noise of the images in the dataset used to train the deep learning models for the SmartTrap project.

In order to reduce the differences between the images and make the insects more visible and distinct, two different processes were carried out:
- Over-exposed areas correction
- Light equalization and shadow removal

![89882280666023306248_2108130703_0714](https://user-images.githubusercontent.com/55786046/175517424-4c5bdda9-a5a4-4e3d-a86f-4034d34caefc.jpg)
![89882280666023306248_2108130703_0714](https://user-images.githubusercontent.com/55786046/175517487-1543cd64-5745-4f90-924d-13238fb22ed1.jpg)

## How to run the algorithm
python3 img_equalizer.py [IMAGES_PATH]

IMAGES_PATH = Path to a folder containing the image set that needs to be equalized

## Output
It creates a new folder called eq_images where all the post-processed images are stored \
<img width="519" alt="Schermata 2022-05-30 alle 14 31 36" src="https://user-images.githubusercontent.com/55786046/174866854-83f52fdd-53b7-4ae4-933c-5f859e06c921.png">

