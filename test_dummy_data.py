import csv
import main 
import analyze_frame

if __name__ == '__main__':
    test("basket")
    test("drop")
    test("empty")
    test("mug")
    test("table")
    test("wall")


def test(test_name):
    print("Testing for "+test_name+"---------------")
    if test_name == "empty":
        print("--THERE SHOULD BE NO WARNINGS OR DANGER HERE--")
    # Test test_name
    for index in range(0,60): 
        dummy_frame_csv = cv2.imread("testing/test_"+test_name+"/image"+str(index)+".png", cv2.IMREAD_UNCHANGED) 
        dummy_frame = []
        for row in dummy_frame_csv:
            dummy_frame.append(row)
        danger = int(min(abs(distance_avg - ESTIMATED_SAFE_VALUE), DANGER_THRESHOLD))
        if danger > 10:
            print("DANGER")
        else if danger > 5:
            print("WARNING")
    print("Finished testing for "+test_name+"---------------")