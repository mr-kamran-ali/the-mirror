import argparse
import time
import numpy as np
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from pynput.keyboard import Listener, Key
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import keyboard
import getch
from sys import platform


key_press = []
key_in_e = []
key_in_i = []


def main():
    if len(key_press) < 1:
        with Listener(on_press=on_press) as listener:  # Setup the listener
            listener.join()  # Join the thread to the main thread
    else:
        exit()


def data_aq():
    print("Starting Data acquisition")
    BoardShim.enable_dev_board_logger()

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument(
        "--timeout",
        type=int,
        help="timeout for device discovery or connection",
        required=False,
        default=0,
    )
    parser.add_argument(
        "--ip-port", type=int, help="ip port", required=False, default=0
    )
    parser.add_argument(
        "--ip-protocol",
        type=int,
        help="ip protocol, check IpProtocolType enum",
        required=False,
        default=0,
    )
    parser.add_argument(
        "--ip-address", type=str, help="ip address", required=False, default=""
    )
    parser.add_argument(
        "--serial-port", type=str, help="serial port", required=False, default=""
    )
    parser.add_argument(
        "--mac-address", type=str, help="mac address", required=False, default=""
    )
    parser.add_argument(
        "--other-info", type=str, help="other info", required=False, default=""
    )
    parser.add_argument(
        "--streamer-params",
        type=str,
        help="streamer params",
        required=False,
        default="",
    )
    parser.add_argument(
        "--serial-number", type=str, help="serial number", required=False, default=""
    )
    parser.add_argument(
        "--board-id",
        type=int,
        help="board id, check docs to get a list of supported boards",
        required=True,
    )
    parser.add_argument("--file", type=str, help="file", required=False, default="")
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    board = BoardShim(args.board_id, params)
    inpt = args.streamer_params
    board.prepare_session()
    board.start_stream(10, inpt)

    if platform in ["linux", "linux2", "darwin"]:
        while True:
            confirmation = input(f"Press i or e for selection and q to quit:  ")
            if confirmation == "e":
                print("e")
                board.insert_marker(1)
            elif confirmation == "i":
                print("i")
                board.insert_marker(2)
            elif confirmation == "q":
                print("q")
                break
            else:
                print("Wrong Key, Press 'q' to exit.")

    elif platform in ["win32", "cygwin"]:
        while True:
            print("Getting Keys")
            key = getch.getche()
            print(key)
            if key == "b'e'":
                print("e")
                board.insert_marker(1)
            elif key == "b'i'":
                print("i")
                board.insert_marker(0)
            elif key == "b'q'":
                print("Aborted")
                break
            else:
                print("wrong key")
                board.insert_marker(2)
                break

    print("Processing Data...")
    time.sleep(1)
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()
    print(data)


def on_press(key):
    if key == Key.space:
        key_press.append(1)
        if len(key_press) > 1:
            data_aq()


if __name__ == "__main__":
    main()