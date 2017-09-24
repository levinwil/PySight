import imutils
import cv2
import time

def motion_estimation(video):
	camera = cv2.VideoCapture(video)
	initial_frame = None
	while(1):
		(grabbed, frame) = camera.read()
		try:
			frame = imutils.resize(frame, width=900)
		except:
			break
		gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (21, 21), 0)
		if initial_frame is None:
			initial_frame = gray
		frameDelta = cv2.absdiff(initial_frame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=1)
		_, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		for contour in contours:
			if cv2.contourArea(contour) < 10000:
				continue
			(x_0, y_0, delta_x, delta_y) = cv2.boundingRect(contour)
			cv2.imwrite("./data/test/test/" + str(int(time.time())) + ".jpg", frame[y_0:y_0 + delta_y, x_0:x_0 + delta_x])
			cv2.rectangle(frame, (x_0, y_0), (x_0 + delta_x, y_0 + delta_y), (0, 255, 0), 2)
		cv2.imshow("Car Detection", frame)
		key = cv2.waitKey(1) & 0xFF
