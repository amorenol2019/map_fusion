import cv2 
import numpy as np
import pywt

def arithmetic_mean(image_1, image_2):
    image = image_1 + image_2
    return np.array(image // 2, np.uint8)

def dwt(image):
    image =  np.float64(image)   
    image /= 255
    # compute coefficients 
    return pywt.wavedec2(image, 'haar', level = 2)

def details_mean(d1, d2):
    d = [0, 0, 0]
    d[0] = arithmetic_mean(d1[0], d2[0])
    d[1] = arithmetic_mean(d1[1], d2[1])
    d[2] = arithmetic_mean(d1[2], d2[2])

    return d

def mean_dwt(image_1, image_2):
    aproximation_1, details1_2, details1_1  = dwt(image_1)
    aproximation_2, details2_2, details2_1 = dwt(image_2)

    aproximation = arithmetic_mean(aproximation_1, aproximation_2)
    details_m1 = details_mean(details1_1, details2_1)
    details_m2 = details_mean(details1_2, details2_2)

    coeffs = (aproximation, details_m2, details_m1)

    # reconstruction => IDWT
    image_final = pywt.waverec2(coeffs, 'haar')
    image_final *= 255
    image_final =  np.uint8(image_final)
    
    return image_final

img1 = "../Images/testmap.png"
img2 = "../Images/rotated_map_2.png"

wn_amean = "Image Arithmetic"
wn_gmean = "Image Gaussian"
wn_dwt_amean = "Mean DWT"

img1 = cv2.imread(img1)
img2 = cv2.imread(img2)
img1_gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

img1_gray = np.array(img1_gray, np.uint)
img2_gray = np.array(img2_gray, np.uint)

cv2.imshow("Image 1", img1)
cv2.imshow("Image 2", img2)

img_arithmetic = arithmetic_mean(img1_gray, img2_gray)
cv2.imshow(wn_amean, img_arithmetic)

img_ar_dwt = mean_dwt(img1_gray, img2_gray)
cv2.imshow(wn_dwt_amean, img_ar_dwt)

cv2.waitKey(0)

cv2.destroyAllWindows()