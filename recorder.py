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

    # mv_iterator = EventsIterator(input_path=args.event_file_path, delta_t=1000)

    # counter = 0  # This will track how many events we processed
    # event_rate = 0
    mv_iterator = EventsIterator(input_path=args.event_file_path, delta_t=delta_t)
    height, width = mv_iterator.get_size()  # Camera Geometry
    left_bound = 427
    right_bound = 853
    for ind, evs in enumerate(mv_iterator):
        if ind % 100 == 0:
            frame = (128*np.ones((height, width))).astype('uint8')
            mean_shift_input = []
            # print("----- New event buffer! -----")
            if evs.size == 0:
                print("fart")
            else:
                print(sum((evs['x']>left_bound) & (evs['x']<right_bound)))
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
    


    # # Process events
    # for evs in mv_iterator:
    #     print("----- New event buffer! -----")
    #     if evs.size == 0:
    #         print("The current event buffer is empty.")
    #     else:
    #         min_t = evs['t'][0]   # Get the timestamp of the first event of this callback
    #         max_t = evs['t'][-1]  # Get the timestamp of the last event of this callback
    #         global_max_t = max_t  # Events are ordered by timestamp, so the current last event has the highest timestamp

    #         counter = evs.size  # Local counter
    #         global_counter += counter  # Increase global counter

    #         print(f"There were {counter} events in this event buffer.")
    #         print(f"There were {global_counter} total events up to now.")
    #         print(f"The current event buffer included events from {min_t} to {max_t} microseconds.")
    #         print("----- End of the event buffer! -----")

    # # Print the global statistics
    # duration_seconds = global_max_t / 1.0e6
    # print(f"There were {global_counter} events in total.")
    # print(f"The total duration was {duration_seconds:.2f} seconds.")
    # if duration_seconds >= 1:  # No need to print this statistics if the total duration was too short
    #     print(f"There were {global_counter / duration_seconds :.2f} events per second on average.")


if __name__ == "__main__":
    main()

