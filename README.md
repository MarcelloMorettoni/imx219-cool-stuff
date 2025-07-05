# imx219-cool-stuff

A collection of simple demos using the IMX219‑83 stereo camera on the Jetson Orin Nano.

## Requirements

* JetPack R36 (includes CUDA, V4L2 and GStreamer)
* Python 3 with the following packages:
  * `opencv-python`
  * `Pillow`
  * `tkinter` (usually included with Python)

Install the Python dependencies with:

```bash
pip install opencv-python Pillow
```

## Running the demo

Execute the `stereo_demo.py` script. By default it tries to open `/dev/video0` and `/dev/video1`.

```bash
python3 stereo_demo.py
```

You will see a window with two tabs:

* **3D Snapshot** – press **Take Snapshot** to capture frames from both sensors and save them side by side.
* **Stereo View** – displays a live feed from both cameras next to each other.

Snapshots are saved in the current directory with a timestamped filename.
