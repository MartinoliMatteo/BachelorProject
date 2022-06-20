import sys 
from wand.image import Image 
import cv2 as cv
import numpy as np  
import os 
import time

def find_s_v_means(a):
    """
    Takes an Image and converts it in HSV to find the saturation and brightness mean ignoring the zeros.

    :param a: Image whose saturation and brightness mean need to be find.
    :return: The mean of s and v.
    """
    hsv = cv.cvtColor(a, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)  

    zero_to_nan_s = np.where(s == 0, np.nan, s)
    ns = np.nanmean(zero_to_nan_s) 

    zero_to_nan_v = np.where(v == 0, np.nan, v)
    nv = np.nanmean(zero_to_nan_v)  
    return ns, nv


def decrease_brightness(img:np.array, ns:int, nv:int):
    """
    Takes an image and decrease the overall brightness by the given value.

    :param img: Image to which brightness has to be decreased;
    :param ns: Value by which saturation has to be increased;
    :param nv: Value by which brightness has to be decreased;
    :return: Image with decreased brightness.
    """
    if nv > 80:
        nv = 80

    if nv > 20:
        nv = nv - 20

    if ns > 20:
        ns = ns - 20

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)   

    lim = 0

    v[v <= lim] = 0
    v[v > lim] = v[v > lim] - nv

    s[s <= lim] = 0
    s[s > lim] = s[s > lim] + ns

    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return img


def blend_images(background, overlay_img, overlay_mask):
    """
    

    :param background:
    :param overlay_img:
    :param overlay_mask:
    :return: 
    """ 
    # The overlay mask is shrunk and blurred a little to make the transitions smoother
    overlay_mask = cv.erode(overlay_mask, cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3)))
    overlay_mask = cv.GaussianBlur(overlay_mask,(3,3),0)

    # The inverse mask, that covers all the black pixels
    background_mask = np.bitwise_not(overlay_mask)  

    # Create a masked-out background and overlay images
    # We convert the images to floating point in range 0.0 - 1.0
    background_part = (background * (1 / 255.0)) * (background_mask * (1 / 255.0)) 
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))   

    # Add them together, and re-scale it back to an 8bit integer image
    return np.uint8(cv.addWeighted(background_part, 255.0, overlay_part, 255.0, 0.0)) 


def main(file_path, filename, parent): 
    base = cv.imread(file_path)  

    with Image(filename=file_path) as img:  
        img.format = 'png'  
        img.transform_colorspace('gray')
        white_point = 0.85
        black_point = 0.85
        img.range_threshold(high_white = white_point, 
                            high_black = black_point) 

        img_array = np.array(img) 

    overlay_mask = np.bitwise_not(img_array)  

    is_all_zero = np.all((overlay_mask == 0))

    if not is_all_zero: 
        masked_overlay = np.bitwise_and(base, overlay_mask) 
        masked_background = np.bitwise_and(base, img_array)  

        back_s, back_v = find_s_v_means(masked_background)

        light_s, light_v = find_s_v_means(masked_overlay)

        ns = abs(int(back_s-light_s))
        nv = abs(int(back_v-light_v))  
        
        edited_overlay = decrease_brightness(masked_overlay, ns, nv)    

        combined_img = blend_images(base, edited_overlay, overlay_mask)     
    else:
        combined_img = base 

    cv.imwrite('{}eq_images/{}'.format(parent, filename), combined_img)  
    cmd = 'convert {}eq_images/{} -normalize {}eq_images/{}'.format(parent, filename, parent, filename) 
    os.system(cmd)
    cmd = 'convert -brightness-contrast 10x10 {}eq_images/{} \( +clone -blur 100x100 \) -compose Divide_Src -composite -sharpen 0x1 {}eq_images/{}'.format(parent, filename, parent, filename)
    os.system(cmd) 

if __name__ == '__main__':
    directory = sys.argv[1]
    split_path = directory.split('/')
    parent = directory.split(split_path[len(split_path)-1])[0]

    if parent != '':
        parent += ''

    cmd = 'mkdir -p {}eq_images'.format(parent)
    os.system(cmd) 
    b = time.time()
    files = os.listdir(directory)
    l = len([f for f in files if f.endswith('.jpg')])

    f = 1
    for file in files: 
        if file.endswith(".jpg"): 
            main(os.path.join(directory,file), file, parent) 
            print('{} EQUALIZATION COMPLETED ({}/{})'.format(file, f, l))
            f += 1
    print('\n./{} FILES SUCCESSFULLY EQUALIZED IN ./eq_images ({:.2f} s)'.format(split_path[len(split_path)-1], time.time() - b))