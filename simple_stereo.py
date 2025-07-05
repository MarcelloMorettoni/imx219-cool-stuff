import cv2
import argparse


def open_capture(src):
    """Open a camera source. Supports numeric indices and GStreamer pipelines."""
    if isinstance(src, int) or (isinstance(src, str) and src.isdigit()):
        return cv2.VideoCapture(int(src))
    return cv2.VideoCapture(src, cv2.CAP_GSTREAMER)


def main(left_source, right_source):
    left_cap = open_capture(left_source)
    right_cap = open_capture(right_source)

    if not left_cap.isOpened() or not right_cap.isOpened():
        print("Failed to open one or both cameras")
        return

    while True:
        ret_left, frame_left = left_cap.read()
        ret_right, frame_right = right_cap.read()
        if not (ret_left and ret_right):
            print("Frame grab failed")
            break

        combined = cv2.hconcat([frame_left, frame_right])
        cv2.imshow("Stereo View", combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    left_cap.release()
    right_cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple stereo viewer")
    parser.add_argument('left', nargs='?', default='0',
                        help='Left camera index or GStreamer pipeline')
    parser.add_argument('right', nargs='?', default='1',
                        help='Right camera index or GStreamer pipeline')
    args = parser.parse_args()
    main(args.left, args.right)
