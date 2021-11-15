import csv

if __name__ == '__main__':
    # Loop through 1 second of data
    for index in range(0,60): 
        dummy_frame_csv = open("dummy_data_wall_"+index+".csv") 
        dummy_frame = []
        for row in dummy_frame_csv:
            dummy_frame.append(row)