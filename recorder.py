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
import serial
import serial.tools.list_ports as ports

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

def calibrate_cam(ser=serial.Serial):
     #calibrate the camera position
    while(1):
        inputSer = input("Enter a character: ")[0]
        ser.write(inputSer.encode())
        if(inputSer == 'w'):
            break

def main():
    """ Main """
    args = parse_args()
    delta_t = 500

    com_ports = list(ports.comports())  # create a list of com ['COM1','COM2']
    for i in com_ports:
        print(i.device)  # returns 'COMx'

    #Initialize serial coms with arduino
    # ser = serial.Serial('COM3', 9600)
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    calibrate_cam(ser=ser)

    device = initiate_device(path=args.event_file_path)
    if device.get_i_erc_module():  # we test if the facility is available on this device before using it
        device.get_i_erc_module().enable(False)

    # mv_iterator = EventsIterator(device=device, input_path=args.event_file_path, delta_t=delta_t)
    mv_iterator = EventsIterator.from_device(device=device, delta_t=delta_t)

    height, width = mv_iterator.get_size()  # Camera Geometry
    percentage_center = 0.85 #percentage of frame considered center
    left_bound = int(1280*(1-percentage_center)/2)
    right_bound = int(1280-left_bound)
    left_rate = 0
    right_rate = 0
    mid_rate = 0
    tot_rate = 0
    position = 0 # 0=left, 1=center, 2=right, -1=lost

    # Success metric
    total_success_time = 0
    total_fail_time = 0
    percent_success = 0
    last_move = 0
    last_ref_time = 0
    prev_mean_timer = 0

    # Adaptive movement
    average_velocity = 0
    alpha = 0.75
    x_mean = 0
    current_x_mean = 0
    prev_x_mean = 0

    # Instantiate the I_LL_Biases object (assuming you have initialized your device)
    biases = device.get_i_ll_biases()
    # Set bias values
    success1 = biases.set('bias_diff_off', 50)
    success2 = biases.set('bias_diff_on', 50)
    success3 = biases.set('bias_hpf', 69)
    # print(success1, success2, success3)

    start_success = False
    last_move = time.time()
    last_ref_time = time.time()
    last_check = time.time()
    for ind, evs in enumerate(mv_iterator):
        #defaults .2 and time.time() - last_check > .01
        if time.time()-last_move > .2 and time.time() - last_check > .01:
            frame = (128*np.ones((height, width))).astype('uint8')
            # print("----- New event buffer! -----")
            if evs.size == 0:
                pass
            else:
                left_rate = sum((evs['x']<left_bound))
                mid_rate = sum((evs['x']>left_bound) & (evs['x']<right_bound))
                right_rate = sum((evs['x']>right_bound))
                tot_rate = sum([left_rate, right_rate, mid_rate])
                
                if tot_rate < 100:
                    average_velocity = 0
                    if start_success == True:
                        total_fail_time += time.time() - last_ref_time
                        last_ref_time = time.time()
                    else:
                        last_ref_time = time.time()
                    ser.write(("rxx").encode())
                    if position == 0:
                        print("LOST... last seen left")
                    elif position == 2:
                        print("LOST... last seen right")
                elif left_rate > mid_rate and left_rate > right_rate:
                    total_success_time += time.time() - last_ref_time
                    last_ref_time = time.time()
                    ser.write(("gxx").encode())
                    start_success = True
                    print("move left!")
                    if abs(average_velocity) < 30:
                        ser.write(("a81").encode())
                    else:
                        ser.write(("a82").encode())
                    last_move = time.time()
                    position = 0
                elif right_rate > left_rate and right_rate > mid_rate:
                    total_success_time += time.time() - last_ref_time
                    last_ref_time = time.time()
                    ser.write(("gxx").encode())
                    start_success = True
                    print("move right!")
                    if abs(average_velocity) < 30:
                        ser.write(("d81").encode())
                    else:
                        ser.write(("d82").encode())
                    last_move = time.time()
                    position = 2
                else:
                    # In the center
                    if prev_x_mean == 0:
                        prev_x_mean = sum(evs['x'])/len(evs['x'])
                        prev_mean_timer = time.time()
                    else:
                        x_mean = sum(evs['x'])/len(evs['x'])
                        average_velocity = (average_velocity*alpha) + (((x_mean - prev_x_mean))*(1-alpha))
                        prev_mean_timer = time.time()
                        #print(f"mean_position: {x_mean}")
                        # print(f"average_velocity: {average_velocity}")
                        prev_x_mean = x_mean
                    total_success_time += time.time() - last_ref_time
                    last_ref_time = time.time()
                    ser.write(("gxx").encode())
                    start_success = True
                    print("CENTER")
                    position = 1
                if start_success:
                    percent_success = total_success_time/(total_success_time+total_fail_time)
                    print(f"Success_rate: {percent_success}")
                for event in evs:
                    # print(f"x: {event['x']}, y: {event['y']}, p: {event['p']}, t: {event['t']}")
                    x = int(event['x'])
                    y = int(event['y'])
                    # print(f"x: {x}")
                    # print(f"y: {y}")
                    frame[y][x] = 255
                last_check = time.time()
                cv2.imshow('yeet', frame.astype('uint8'))
                cv2.waitKey(1)


if __name__ == "__main__":
    main()

