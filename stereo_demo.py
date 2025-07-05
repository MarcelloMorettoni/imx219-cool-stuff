import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time

class StereoApp(tk.Tk):
    def __init__(self, left_index=0, right_index=1):
        super().__init__()
        self.title("IMX219 Stereo Demos")
        self.left_cam = cv2.VideoCapture(left_index)
        self.right_cam = cv2.VideoCapture(right_index)
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
    app = StereoApp()
    app.mainloop()
