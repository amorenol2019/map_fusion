# import required libraries
import numpy as np
import cv2
import matplotlib.pyplot as plt

# read two input images as grayscale
img1 = "testmap.png"
img2 = "rotated_map.png"
img1 = cv2.imread(img1)
img2 = cv2.imread(img2)
img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Initiate SIFT detector
sift = cv2.SIFT_create()

# detect and compute the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# create BFMatcher object
bf = cv2.BFMatcher()

# Match descriptors.
#matches = bf.match(des1,des2)
matches = bf.knnMatch(des1, des2, k=2)
# sort the matches based on distance
#matches = sorted(matches, key=lambda val: val.distance)

plt.imshow(cv2.drawKeypoints(img2_gray, kp2, img2.copy()))

good_matches = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good_matches.append([m])

print(len(good_matches))
print(len(matches))

ref_matched_kpts = np.float32([kp1[m[0].queryIdx].pt for m in good_matches])
sensed_matched_kpts = np.float32([kp2[m[0].trainIdx].pt for m in good_matches])

height = img2.shape[0]
width = img1.shape[1]
# move both images to the center a bit
corners = np.float32([[0, 0], [0, height], [width, 0], [width, height]])
corners_moved = np.float32([[5, 5], [5, height + 5], [5 + width, 5], [5 + width, 5 + height]])

# Compute homography
H = cv2.getPerspectiveTransform(corners, corners_moved) #, cv2.RANSAC,5.0)

# Warp image
warped_image = cv2.warpPerspective(img1, H, (img1.shape[1], img1.shape[0]), cv2.INTER_AREA)
            
cv2.imshow('warped.jpg', warped_image)
#dest = cv2.addWeighted(source1, 1, source2, 1, 0.0)

# Draw first 50 matches.
#out = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, flags=2)
#plt.imshow(out)
# plt.show()
cv2.waitKey(0)
  
# closing all open windows
cv2.destroyAllWindows()