import cv2
import main 
import os

WINDOW = "Indoor Nav"

def test(test_name):
    print("Testing for "+test_name+"---------------")
    if test_name == "empty":
        print("--THERE SHOULD BE NO WARNINGS OR DANGER HERE--")
    path, dirs, files = next(os.walk("testing/test_"+test_name))
    file_count = len(files)

    reference = main.get_reference()

    # Test test_name
    for index in range(0,file_count): 
        dummy_frame = cv2.imread("testing/test_"+test_name+"/image"+str(index)+".png", cv2.IMREAD_UNCHANGED) 

        danger, result = main.analyze_frame(dummy_frame, reference)

        if danger >= 6:
            print("DANGER")
        elif danger >= 3:
            print("WARNING")

    print("Finished testing for "+test_name+"---------------")

if __name__ == '__main__':
    test("basket")
    test("drop")
    test("empty")
    test("mug")
    test("table")
    test("wall")

