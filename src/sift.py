# import required libraries
import numpy as np
import cv2, math
import matplotlib.pyplot as plt

def matching_images(image1, image2):
    # Create SIFT object
    sift = cv2.SIFT_create()

    # Detect keypoints and compute descriptors for both images
    kp1, des1 = sift.detectAndCompute(image1, None)
    kp2, des2 = sift.detectAndCompute(image2, None)

    # Create matcher object
    bf = cv2.BFMatcher()

    # Match descriptors
    matches = bf.match(des1, des2)

    # Sort the matches by distance
    matches = sorted(matches, key = lambda x:x.distance)

    # Draw the top 10 matches
    img_matches = cv2.drawMatches(image1, kp1, image2, kp2, matches, None, flags=2)

    # Find the homography matrix
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)

    return M

def arithmetic_mean(image_1, image_2, l_x, r_x, b_y, t_y):
    """
    Arithmetic mean of images (one warped)
    Avoiding extra edges added while warping
    """
    image = image_2
    image[t_y:b_y, l_x:r_x] = image_1[t_y:b_y, l_x:r_x] + image_2[t_y:b_y, l_x:r_x]
    image[t_y:b_y, l_x:r_x] = image[t_y:b_y, l_x:r_x] // 2

    return np.array(image, np.uint8)

def getTransform(M, point):
    """
    Getting point transformed to know position in resulting image
    """
    x = point[0]
    y = point[1]
    d = M[2, 0] * x + M[2, 1] * y + M[2, 2]

    return (
        int((M[0, 0] * x + M[0, 1] * y + M[0, 2]) / d), # x
        int((M[1, 0] * x + M[1, 1] * y + M[1, 2]) / d), # y
    )

def get_corners(height, width):
    """
    Function to extract the corner points of an image from its width and height
    and arrange it in the form of a numpy array.
    """
    corners_array = np.array([[0, 0], [width - 1, 0],
                            [width - 1, height - 1], [0, height - 1]])
    return corners_array

def get_start_points(bl_y, br_y, tr_x, br_x, width, height):
    """
    Find start of x and y.
    """
    if (bl_y < height - 1) and (bl_y < br_y):
        y_top = bl_y
    elif (br_y < height - 1) and (br_y < bl_y):
        y_top = br_y
    else:
        y_top = height - 1

    if (tr_x < width - 1) and (tr_x < br_x):
        x_left = tr_x
    elif (br_x < width - 1) and (br_x < tr_x):
        x_left = br_x
    else:
        x_left = width - 1

    return y_top, x_left

def get_end_points(tl_y, tr_y, tl_x, bl_x):
    """
    Find end of x and y.
    """
    if (tl_y > 0) and (tl_y > tr_y):
        y_bottom = tl_y
    elif (tr_y > 0) and (tr_y > tl_y):
        y_bottom = tr_y
    else:
        y_bottom = 0

    if (tl_x > 0) and (tl_x > bl_x):
        x_right = tl_x
    elif (bl_x > 0) and (bl_x > tl_x):
        x_right = bl_x
    else:
        x_right = 0

    return y_bottom, x_right

def get_crop_points(M, img_1, img_2, stitch_direc):
    """
    Find pixel corners in stitched image to not compute mean to 
    false pixel values.
    """
    img_1_h, img_1_w, _ = img_1.shape
    img_2_h, img_2_w, _ = img_2.shape

    corners_b = get_corners(img_1_h, img_1_w)

    transform_corners_b = [[0,0], [0,0], [0,0], [0,0]]

    for i in range(corners_b.shape[0]) :
        transform_corners_b[i] = np.absolute(getTransform(M, corners_b[i]))

    top_x_left, top_y_left = transform_corners_b[0]
    top_x_right, top_y_right = transform_corners_b[1]
    bottom_x_right, bottom_y_right = transform_corners_b[2]
    bottom_x_left, bottom_y_left = transform_corners_b[3]

    y_bottom, x_right = get_end_points(top_y_left, top_y_right, top_x_left, bottom_x_left)
    y_top, x_left = get_start_points(bottom_y_left, bottom_y_right, top_x_right, bottom_x_right, img_1_w, img_1_h)
        
    return x_left, x_right, y_bottom, y_top

# Read two input images as grayscale
img1 = "../Images/map_max_rot.png"
img2 = "../Images/testmap.png"

img1 = cv2.imread(img1)
img2 = cv2.imread(img2)

M = matching_images(img1, img2)

# Warp the first image
img1_warp = cv2.warpPerspective(img1, M, (img2.shape[1], img2.shape[0]))
cv2.imshow("Image 1 after homography-warping", img1_warp)

img1_warp = np.array(img1_warp, np.uint)
img2 = np.array(img2, np.uint)

# Merge both
x_left, x_right, y_bottom, y_top = get_crop_points(M, img1, img1_warp, 1)
result = arithmetic_mean(img1_warp, img2, x_left, x_right, y_bottom, y_top)

# Transforming a point from Image 1 to Resulting image
p1 = (400,700)
p1_r = getTransform(M, p1)
img1 = cv2.circle(img1, p1, 3, (255,0,0),-1)
result = cv2.circle(result, p1_r, 3, (255,0,0),-1)

img1 = np.array(img1, np.uint8)
img2 = np.array(img2, np.uint8)
result = np.array(result, np.uint8)

cv2.imshow("Image 1", img1)
cv2.imshow("Image 2", img2)
cv2.imshow("Result of fusing two images", result)

cv2.waitKey(0)
cv2.destroyAllWindows()