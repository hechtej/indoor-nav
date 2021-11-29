import csv
import cv2
import main 

MEASURED_AVERAGE = 255/771.665 #(max_dist-min_dist)/2+min_dist then converted to 0->255 range

ESTIMATED_SAFE_VALUE = 140 # Camera pointed about 30 degrees down 14 inches from the ground reads this pretty consistently
WARNING_THRESHOLD = 5
DANGER_THRESHOLD =  10

CAM_WIDTH = 640
CAM_HEIGHT = 400

WINDOW = "Indoor Nav"

def test(test_name):
    print("Testing for "+test_name+"---------------")
    if test_name == "empty":
        print("--THERE SHOULD BE NO WARNINGS OR DANGER HERE--")
    # Test test_name
    for index in range(0,60): 
        dummy_frame = cv2.imread("testing/test_"+test_name+"/image"+str(index)+".png", cv2.IMREAD_UNCHANGED) 
        distance_avg = dummy_frame[dummy_frame != 0].mean()
        danger = int(min(abs(distance_avg - ESTIMATED_SAFE_VALUE), DANGER_THRESHOLD))
        if danger > 10:
            print("DANGER")
        elif danger > 5:
            print("WARNING")
    print("Finished testing for "+test_name+"---------------")

if __name__ == '__main__':
    test("basket")
    test("drop")
    test("empty")
    test("mug")
    test("table")
    test("wall")

