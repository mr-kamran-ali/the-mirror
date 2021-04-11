import argparse
import time
import numpy as np
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from pynput.keyboard import Listener, Key
import matplotlib
import atexit

matplotlib.use("Agg")
from datetime import datetime

key_press = []


def main():
    """Main method to start the app and responsible to receive and process args"""
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
        "--serial-port", type=str, help="serial port", required=True, default=""
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

    global board
    global input
    board = BoardShim(args.board_id, params)
    input = args.streamer_params

    start_test()


def start_test():
    """Starts the test session setting up the lister for key inputs"""
    with Listener(on_press=start_in) as listener:  # Setup the listener
        listener.join()  # Join the thread to the main thread
    print("\nStarting test.")
    start_stream()


def start_stream():
    """Prepares and starts the data stream from the OpenBCI Board"""
    print("\nStarting data acquisition.")
    board.prepare_session()
    board.start_stream(45000, input)
    key_marker()


def key_marker():
    """Send key press markers to the OpenBCI board which ultimately marks the data and saves it"""
    print("\nWaiting for key input.")
    with Listener(on_press=key_in) as listener:
        listener.join()
    end_test()


def end_test():
    """Ends the test and flushes the saved data in a file in same directory"""
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()
    now = datetime.now()

    file = now.strftime("%d.%m.%Y_%H.%M.%S") + "_eeg_data.csv"
    DataFilter.write_file(data, file, "w")
    print("\nTest ended.")


def start_in(key):
    """In the start of the experiments double space press is required, this handles the double space

    Args:
        key (pynput Key): Key Pressed

    Returns:
        [bool]: False if there are already two space presses.
    """
    if key == Key.space:
        key_press.append(1)
    if len(key_press) > 1:
        return False


def key_in(key):
    """Handles different key presses and sends board markers on the basis of different keys

    Args:
        key (pynput Key): Key Pressed

    Returns:
        [bool]: False if user presses "q"
    """
    if key == Key.space:
        board.insert_marker(3)
        print("#####   Block ended   #####")
    elif key.char == "e":
        board.insert_marker(1)
        print("e pressed")
    elif key.char == "i":
        board.insert_marker(2)
        print("i pressed")

    elif key.char == "q":
        return False


def exit_handler():
    print("Test Ended")
    end_test()


atexit.register(exit_handler)

if __name__ == "__main__":
    main()