import cv2
from main import analyze_frame

if __name__ == '__main__':
    # Loop through all data in our test folder
    for index in range(0,101): 
        dummy_frame = cv2.imread("testing/test_wall/image"+str(index)+".png", cv2.IMREAD_UNCHANGED) 
        danger = analyze_frame(dummy_frame)
