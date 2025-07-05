import argparse
import cv2
import numpy as np

try:
    from jetcam.csi_camera import CSICamera
except ImportError as e:
    raise ImportError("Jetcam library is required for this script: {}".format(e))


def main(left_index=0, right_index=1, width=640, height=480):
    left_cam = CSICamera(width=width, height=height, capture_device=left_index)
    right_cam = CSICamera(width=width, height=height, capture_device=right_index)

    left_cam.running = True
    right_cam.running = True

    try:
        while True:
            frame_left = left_cam.value
            frame_right = right_cam.value

            if frame_left is None or frame_right is None:
                continue

            combined = np.hstack((frame_left, frame_right))
            cv2.imshow("Jetcam Stereo View", combined)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        left_cam.running = False
        right_cam.running = False
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stereo viewer using Jetcam")
    parser.add_argument('left', nargs='?', default='0', help='Left camera index')
    parser.add_argument('right', nargs='?', default='1', help='Right camera index')
    parser.add_argument('--width', type=int, default=640, help='Capture width')
    parser.add_argument('--height', type=int, default=480, help='Capture height')
    args = parser.parse_args()

    main(int(args.left), int(args.right), args.width, args.height)
