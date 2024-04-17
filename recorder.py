import metavision_hal
from metavision_hal import I_LL_Biases
from metavision_core.event_io.raw_reader import initiate_device
from metavision_core.event_io import EventsIterator
from metavision_sdk_core import PeriodicFrameGenerationAlgorithm
from metavision_sdk_ui import EventLoop, BaseWindow, Window, UIAction, UIKeyEvent
from matplotlib import pyplot as plt
import cv2
import numpy as np
import time


def parse_args():
    import argparse
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Metavision SDK Get Started sample.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--input-event-file', dest='event_file_path', default="",
        help="Path to input event file (RAW or HDF5). If not specified, the camera live stream is used. "
        "If it's a camera serial number, it will try to open that camera instead.")
    args = parser.parse_args()
    return args

def main():
    """ Main """
    args = parse_args()
    delta_t = 500

    device = initiate_device(path=args.event_file_path)
    if device.get_i_erc_module():  # we test if the facility is available on this device before using it
        device.get_i_erc_module().enable(False)

    # mv_iterator = EventsIterator(device=device, input_path=args.event_file_path, delta_t=delta_t)
    mv_iterator = EventsIterator.from_device(device=device, delta_t=delta_t)

    height, width = mv_iterator.get_size()  # Camera Geometry
    left_bound = 427
    right_bound = 853
    left_rate = 0
    right_rate = 0
    mid_rate = 0

    # Instantiate the I_LL_Biases object (assuming you have initialized your device)
    biases = device.get_i_ll_biases()
    # Set bias values
    success1 = biases.set('bias_diff_off', 50)
    success2 = biases.set('bias_diff_on', 50)
    success3 = biases.set('bias_hpf', 69)
    # print(success1, success2, success3)

    for ind, evs in enumerate(mv_iterator):
        if ind % 100 == 0:
            frame = (128*np.ones((height, width))).astype('uint8')
            mean_shift_input = []
            # print("----- New event buffer! -----")
            if evs.size == 0:
                print("fart")
            else:
                left_rate = sum((evs['x']<left_bound))
                mid_rate = sum((evs['x']>left_bound) & (evs['x']<right_bound))
                right_rate = sum((evs['x']>right_bound))

                if left_rate > mid_rate and left_rate > right_rate:
                    print("move left!")
                elif right_rate > left_rate and right_rate > mid_rate:
                    print("move right!")
                else:
                    print("CENTER")
                
                for event in evs:
                    # print(f"x: {event['x']}, y: {event['y']}, p: {event['p']}, t: {event['t']}")
                    x = int(event['x'])
                    y = int(event['y'])
                    # print(f"x: {x}")
                    # print(f"y: {y}")
                    frame[y][x] = 255
                    mean_shift_input.append((x, y))
                cv2.imshow('yeet', frame.astype('uint8'))
                # print(mean_shift_input)
                cv2.waitKey(1)


if __name__ == "__main__":
    # bias_file_path = "~/Documents/metavision/biases/biases.bias"
    # apply_bias_configuration(bias_file_path)
    main()

