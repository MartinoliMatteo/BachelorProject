# Image Luminosity Equalization For Deep Learning Applications
In this project, we will use image processing to modify the lighting conditions and reduce the noise of the images in the dataset used to train the deep learning models for the SmartTrap project.

In order to reduce the differences between the images and make the insects more visible and distinct, two different processes were carried out:
- Over-exposed areas correction
- Light equalization and shadow removal

<img width="400" alt="a" src=https://user-images.githubusercontent.com/55786046/174867759-f7ef2cc5-bed1-41ce-8e66-074de66b1494.jpg)>
<img width="400" alt="b" src=https://user-images.githubusercontent.com/55786046/174867871-6c4e98b2-9c51-4e63-8ccd-82de3f17990d.jpg)>

## How to run the algorithm
python3 img_equalizer.py [IMAGES_PATH]

IMAGES_PATH = Path to a folder containing the image set that needs to be equalized

## Output
It creates a new folder called eq_images where all the post-processed images are stored \
<img width="519" alt="Schermata 2022-05-30 alle 14 31 36" src="https://user-images.githubusercontent.com/55786046/174866854-83f52fdd-53b7-4ae4-933c-5f859e06c921.png">

