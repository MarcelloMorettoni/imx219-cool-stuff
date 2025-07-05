import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import argparse


def gstreamer_pipeline(sensor_id=0,
                        capture_width=1280,
                        capture_height=720,
                        display_width=640,
                        display_height=480,
                        framerate=30,
                        flip_method=2):
    """Return a GStreamer pipeline for the Jetson CSI cameras."""
    return (
        f"nvarguscamerasrc sensor-id={sensor_id} ! "
        f"video/x-raw(memory:NVMM), width={capture_width}, height={capture_height}, framerate={framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width={display_width}, height={display_height}, format=BGRx ! "
        f"videoconvert ! appsink"
    )

def open_capture(source):
    """Open a camera source using the Jetson Argus pipeline only."""
    if isinstance(source, int) or (isinstance(source, str) and source.isdigit()):
        pipeline = gstreamer_pipeline(sensor_id=int(source))
        cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        if cap.isOpened():
            return cap
        return cap
    return cv2.VideoCapture(source, cv2.CAP_GSTREAMER)


class StereoApp(tk.Tk):
    def __init__(self, left_source=0, right_source=1):
        super().__init__()
        self.title("IMX219 Stereo Demos")
        self.left_cam = open_capture(left_source)
        self.right_cam = open_capture(right_source)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.snapshot_frame = ttk.Frame(self.notebook)
        self.view_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.snapshot_frame, text="3D Snapshot")
        self.notebook.add(self.view_frame, text="Stereo View")

        # Snapshot widgets
        self.snap_button = ttk.Button(
            self.snapshot_frame,
            text="Take Snapshot",
            command=self.take_snapshot
        )
        self.snap_button.pack(pady=10)
        self.snap_label = ttk.Label(self.snapshot_frame)
        self.snap_label.pack()

        # Stereo view widgets
        self.view_label = ttk.Label(self.view_frame)
        self.view_label.pack()
        self.update_view()

    def take_snapshot(self):
        ret_l, frame_l = self.left_cam.read()
        ret_r, frame_r = self.right_cam.read()
        if ret_l and ret_r:
            combined = cv2.hconcat([frame_l, frame_r])
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"snapshot_{timestamp}.png"
            cv2.imwrite(filename, combined)
            rgb = cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            img_tk = ImageTk.PhotoImage(img)
            self.snap_label.configure(image=img_tk)
            self.snap_label.image = img_tk

    def update_view(self):
        ret_l, frame_l = self.left_cam.read()
        ret_r, frame_r = self.right_cam.read()
        if ret_l and ret_r:
            combined = cv2.hconcat([frame_l, frame_r])
            rgb = cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            img_tk = ImageTk.PhotoImage(img)
            self.view_label.configure(image=img_tk)
            self.view_label.image = img_tk
        self.after(30, self.update_view)

    def on_close(self):
        self.left_cam.release()
        self.right_cam.release()
        self.destroy()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IMX219 stereo camera demo')
    parser.add_argument('left', nargs='?', default='0',
                        help='Left camera index or GStreamer pipeline')
    parser.add_argument('right', nargs='?', default='1',
                        help='Right camera index or GStreamer pipeline')
    args = parser.parse_args()

    app = StereoApp(args.left, args.right)
    app.mainloop()
