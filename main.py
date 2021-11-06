import cv2
import depthai as dai
import numpy as np
import time

MEASURED_AVERAGE = 255/771.665 #(max_dist-min_dist)/2+min_dist then converted to 0->255 range

ESTIMATED_SAFE_VALUE = 140 # Camera pointed about 30 degrees down 14 inches from the ground reads this pretty consistently
WARNING_THRESHOLD = 5
DANGER_THRESHOLD =  10

CAM_WIDTH = 640
CAM_HEIGHT = 400

WINDOW = "Indoor Nav"

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

# UI helper functions to workaround lambda arguments
def makeSlider(name, window, a_min, a_max):
	cv2.createTrackbar(name, window, a_min, a_max, (lambda x: x))
	cv2.setTrackbarPos(name, window, int((a_min+a_max)/2))

def setSlider(name, window, val):
	cv2.setTrackbarPos(name,window,val)

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
		
		# map disparity from 0 to 255
		disparityMultiplier = 255 / stereo.initialConfig.getMaxDisparity()
		
		'''
			Disparity: Double array of uint8
				each is in range from 0 -> 255, 0(furthest) 255(closest)
				[0][0] is top left (?)
				[0][X] is top right
				[X][0] is bottom left
				[X][X] is bottom right

		'''

		cv2.namedWindow(WINDOW)

		makeSlider("Danger", WINDOW, 0, DANGER_THRESHOLD)

		skipFrame = False

		while True:
			# If we spend every iteration of the loop just processing the frames, we get to a point
			# where keyboard inputs are HUGELY delayed (presumably some opencv event loop gets 
			# overloaded?).  quick hacky fix is to spend every other iteration not doing anything 
			# other than user input
			skipFrame = not skipFrame
			if not skipFrame:
				disparity = getFrame(disparityQueue)
				disparity = (disparity * disparityMultiplier).astype(np.uint8)

				# Loop over every pixel to get average
				distance_sum = 0
				sample_count = 0
				for col in range(0, CAM_WIDTH):
					for row in range(0, CAM_HEIGHT):
						# disparity reading of 0 means the true value is unknown.
						# there's probably some clever way of patching the gaps by interpolating
						# nearby valid readings, but for now we'll just ignore it.
						# this can cause some issues when things are too close to the camera for
						# proper readings, but ideally we'll catch the danger before it's that close
						if disparity[row][col] != 0:
							sample_count = sample_count + 1
							distance_sum = distance_sum + disparity[row][col]
			
				distance_avg = distance_sum / sample_count

				# danger increases if above or below the calibrated value, detecting both
				# obstacles and drops.  we cap it at DANGER_THRESHOLD for display.
				# an emergency stop should be triggered if we exceed WARNING_THRESHOLD
				danger = int(min(abs(distance_avg - ESTIMATED_SAFE_VALUE), DANGER_THRESHOLD))

				setSlider("Danger", WINDOW, danger)

				cv2.imshow(WINDOW, disparity)

			# Check for keyboard input
			key = cv2.waitKey(1)
			if key == ord('q'):
				# Quit when q is pressed
				break


		cv2.destroyAllWindows()
