import csv
import main import analyze_frame

if __name__ == '__main__':
    # Test wall
    for index in range(0,60): 
        dummy_frame_csv = open("/testing/test_wall/dummy_data_wall_"+index+".csv") 
        dummy_frame = []
        for row in dummy_frame_csv:
            dummy_frame.append(row)
        danger = int(min(abs(distance_avg - ESTIMATED_SAFE_VALUE), DANGER_THRESHOLD))
        if danger > 10:
            print("DANGER")
        else if danger > 5:
            print("WARNING")
            
    # Test empty
    for index in range(0,60): 
        dummy_frame_csv = open("/testing/test_wall/dummy_data_empty_"+index+".csv") 
        dummy_frame = []
        for row in dummy_frame_csv:
            dummy_frame.append(row)
        danger = int(min(abs(distance_avg - ESTIMATED_SAFE_VALUE), DANGER_THRESHOLD))
        if danger > 10:
            print("DANGER")
        else if danger > 5:
            print("WARNING")
