import cv2
import PIL.Image

class VisionEngine:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index

    def capture_frame(self):
        """Captures a single frame from the webcam and converts it to PIL Image."""
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            print("[Vision Error] Could not open webcam.")
            return None

        # Warm up camera sensor
        for _ in range(5):
            cap.read()

        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            print("[Vision Error] Failed to capture image frame.")
            return None

        # Convert BGR (OpenCV) to RGB (PIL)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return PIL.Image.fromarray(rgb_frame)
