import cv2
import numpy as np


class ReadFile:
    def __init__(self, file):
        self.file_name = str(file)
        self.img = cv2.imread(self.file_name, cv2.IMREAD_GRAYSCALE)
        self.im = cv2.resize(self.img, None, fx=0.45, fy=0.45,interpolation=cv2.INTER_CUBIC)
        # edge detection
        self.edges = cv2.Canny(self.im,100,230)
        # blob detection
        # smoothing to reduce noise
        self.blur= cv2.GaussianBlur(self.edges,(3,3),0)  # number needs to be positive and odd
        (ret, thresh) = cv2.threshold(self.blur, 30, 200, cv2.THRESH_BINARY)  # Try different thresholding
        kernel = np.ones((5,5), np.uint8)  # kernel for dilation and erosion
        img_erosion = cv2.erode(thresh, kernel, iterations=1)  # process boundary pixels, removes white noise and shrink object
        self.img_dilation = cv2.dilate(img_erosion, kernel, iterations=1) # dilate object back to right size

    def set_params(self):
        params = cv2.SimpleBlobDetector_Params()
        # change thresholds
        params.minThreshold = 80
        params.maxThreshold = 200

        # just filter by area
        params.filterByArea = True
        params.minArea = 20 # for geese
        params.maxArea = 100

        params.filterByColor = False
        params.blobColor = 0

        params.filterByCircularity = True
        params.minCircularity = 0.5

        params.filterByConvexity = False
        params.minConvexity = 0.2

        params.filterByInertia = False
        params.minInertiaRatio = 0.01

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(self.img_dilation)

        im_key3 = cv2.drawKeypoints(self.im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        im_key4 = cv2.drawKeypoints(self.img_dilation, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        im_key5 = cv2.drawKeypoints(self.edges, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        result = [im_key3, im_key4, im_key5]
        return result



def main():
    files = ['/home/madeline/Development/utat/geese.jpg']
    for item in files:
        file = ReadFile(item)
        results = file.set_params()
        for im in results:
            cv2.imshow('img', im)
            cv2.waitKey(0)

main()
