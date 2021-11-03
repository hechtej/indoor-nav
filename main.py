import cv2
import depthai as dai
import numpy as np

MEASURED_AVERAGE = 255/771.665 #(max_dist-min_dist)/2+min_dist then converted to 0->255 range
WARNING_THRESHOLD = 20
DANGER_THRESHOLD = 50

CAM_WIDTH = 640
CAM_HEIGHT = 400

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
	
	xOutDisp = pipeline.createXLinkOut()
	xOutDisp.setStreamName("disparity")
	
	stereo.disparity.link(xOutDisp.input)
	
	# Connect device
	with dai.Device(pipeline) as device:
		disparityQueue = device.getOutputQueue(name="disparity", maxSize=1, blocking=False)
		depthQueue     = device.getOutputQueue(name="depth", maxSize=1, blocking=False)
		
		# map disparity from 0 to 255
		disparityMultiplier = 255 / stereo.getMaxDisparity()
		
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

			# Loop over every pixel to get average
			distance_sum = 0
			for col in range(0, CAM_WIDTH):
				for row in range(0, CAM_HEIGHT):
					distance_sum = distance_sum + disparity[row][col]
			
			distance_avg = distance_sum / (CAM_HEIGHT*CAM_WIDTH)

			#abs() allows for inclines & declines
			ratio_avg = abs(distance_avg/MEASURED_AVERAGE)

			#Detect if current dist_avg is off from the pre-measured average
			if distance_avg > DANGER_THRESHOLD:
				#ALERT_DANGER
				print("DANGER")

			elif distance_avg > WARNING_THRESHOLD:
				#ALERT_WARNING
				print("WARNING")


			cv2.imshow("Disparity", disparity)

			# Check for keyboard input
			key = cv2.waitKey(1)
			if key == ord('q'):
				# Quit when q is pressed
				break
