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

## Running the demos

### Tkinter demo

Execute the `stereo_demo.py` script. When numeric camera IDs are provided, the
script opens the Jetson CSI cameras using the `nvarguscamerasrc` pipeline only.
The scripts no longer fall back to V4L2 devices, so make sure the `nvargus-daemon`
service is running (restart with `sudo systemctl restart nvargus-daemon` if needed):

```bash
python3 stereo_demo.py 0 1
```

You can still pass full GStreamer pipelines if you need custom settings:

```bash
python3 stereo_demo.py \
  "nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=1280, height=720, framerate=30/1 ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! appsink" \
  "nvarguscamerasrc sensor-id=1 ! video/x-raw(memory:NVMM), width=1280, height=720, framerate=30/1 ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! appsink"
```

You will see a window with two tabs:

* **3D Snapshot** – press **Take Snapshot** to capture frames from both sensors and save them side by side.
* **Stereo View** – displays a live feed from both cameras next to each other.

Snapshots are saved in the current directory with a timestamped filename.

### Simple OpenCV viewer

For a minimal example without Tkinter, run `simple_stereo.py`. When numeric
camera IDs are provided, the script opens the Jetson CSI cameras using only the
`nvarguscamerasrc` pipeline. It shows both streams side by
side in an OpenCV window. Press **q** to quit.

```bash
python3 simple_stereo.py 0 1
```

You can still pass full GStreamer pipelines if needed.

### Jetcam-based viewer

If the optional `jetcam` library is installed, you can run `jetcam_stereo.py`
to capture frames using the `CSICamera` interface instead of OpenCV's
`VideoCapture`. This script shows both camera streams side by side in an
OpenCV window:

```bash
python3 jetcam_stereo.py 0 1 --width 640 --height 480
```

Press **q** to exit the viewer.
