import cv2
import depthai as dai
import numpy as np

MEASURED_AVERAGE = 255/771.665 #(max_dist-min_dist)/2+min_dist then converted to 0->255 range
WARNING_THRESHOLD = 5
DANGER_THRESHOLD = 10

def getFrame(queue):
	# Get frame from queue
	frame = queue.get()
	# Convert frame to OpenCV format
	return frame.getCvFrame()

def getMonoCamera(pipeline, isLeft):
	mono = pipeline.createMonoCamera()
	
	mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)

	if isLeft:
		mono.setBoardSocket(dai.CameraBoardSocket.LEFT)
	else:
		mono.setBoardSocket(dai.CameraBoardSocket.RIGHT)
	return mono

def getStereoPair(pipeline, monoLeft, monoRight):
	stereo = pipeline.createStereoDepth()
	
	# Turn on occlusion check (small performance hit, but output is less noisy)
	stereo.setLeftRightCheck(True)
	# Link mono cameras to the stereo pair
	monoLeft.out.link(stereo.left)
	monoRight.out.link(stereo.right)

	return stereo

if __name__ == '__main__':
	pipeline = dai.Pipeline()
	
	# Get side cameras
	monoLeft = getMonoCamera(pipeline, isLeft = True)
	monoRight = getMonoCamera(pipeline, isLeft = False)
	
	stereo = getStereoPair(pipeline, monoLeft, monoRight)
	
	# Define output depth map
	xOutDepth = pipeline.createXLinkOut()
	xOutDepth.setStreamName("depth")
	
	xOutDisp = pipeline.createXLinkOut()
	xOutDisp.setStreamName("disparity")

	xOutRectifiedLeft = pipeline.createXLinkOut()
	xOutRectifiedLeft.setStreamName("rectifiedLeft")

	xOutRectifiedRight = pipeline.createXLinkOut()
	xOutRectifiedRight.setStreamName("rectifiedRight")
	
	stereo.disparity.link(xOutDisp.input)
	
	stereo.rectifiedLeft.link(xOutRectifiedLeft.input)
	stereo.rectifiedRight.link(xOutRectifiedRight.input)
	
	# Connect device
	with dai.Device(pipeline) as device:
		disparityQueue = device.getOutputQueue(name="disparity", maxSize=1, blocking=False)
		rectifiedLeftQueue = device.getOutputQueue(name="rectifiedLeft", maxSize=1, blocking=False)
		rectifiedRightQueue = device.getOutputQueue(name="rectifiedRight", maxSize=1, blocking=False)
		
		# map disparity from 0 to 255
		disparityMultiplier = 255 / stereo.getMaxDisparity()

		cv2.namedWindow("Stereo Pair")
		
		'''
			Disparity: Double array of uint8
				each is in range from 0 -> 255, 0(furthest) 255(closest)
				[0][0] is top left (?)
				[0][X] is top right
				[X][0] is bottom left
				[X][X] is bottom right

		'''
		while True:
			disparity = getFrame(disparityQueue)
			
			disparity = (disparity * disparityMultiplier).astype(np.uint8)
			
			# Loop from [0][0]->[1280][800], get the average and print
			for col in range(edge_l,edge_r):
				for row in range(edge_t,edge_b):
					distance_sum = disparity[row][col]
			
			distance_avg = distance_sum / ((edge_b-edge_t)*(edge_r-edge_l))

			#abs() allows for inclines & declines
			ratio_avg = abs(distance_avg/MEASURED_AVERAGE)

			#Detect if current dist_avg is off from the pre-measured average
			if ratio_avg > DANGER_THRESHOLD:
				#ALERT_DANGER
				print("DANGER")

			elif ratio_avg > WARNING_THRESHOLD:
				#ALERT_WARNING
				print("WARNING")


			leftFrame = getFrame(rectifiedLeftQueue)
			rightFrame = getFrame(rectifiedRightQueue)
			
			# Show stereo view by averaging left and right cameras
			imOut = np.uint8(leftFrame/2 + rightFrame/2)


			cv2.imshow("Stereo Pair", imOut)
			cv2.imshow("Disparity", disparity)

			# Check for keyboard input
			key = cv2.waitKey(1)
			if key == ord('q'):
				# Quit when q is pressed
				break
