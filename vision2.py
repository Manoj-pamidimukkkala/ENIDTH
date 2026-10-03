import cv2
import mss
import PIL.Image

class VisionEngine:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index

    def capture_webcam(self):
        """Captures a single frame from the physical webcam."""
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            print("[Vision Error] Unable to access camera device.")
            return None

        for _ in range(5):  # Warmup sensor
            cap.read()

        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            print("[Vision Error] Frame capture failed.")
            return None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return PIL.Image.fromarray(rgb_frame)

    def capture_screen(self):
        """Captures high-resolution snapshot of the current primary display."""
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor
            sct_img = sct.grab(monitor)
            img = PIL.Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            return img
