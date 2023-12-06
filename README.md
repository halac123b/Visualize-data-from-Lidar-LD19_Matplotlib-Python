# LIDAR_LD19_python_data_reader

This code can use Lidar's LD19 provided by LDROBOT from Python. and It displays the acquired point cloud in real time in matplotlib.

# How to use

1. Clone this repository and change `Serial(port='/dev/tty.usbserial-0001'...)` in main.py to your own port.
2. Run `pip install -r requirements.txt` in venv environment.
3. Run `python main.py`.
4. Press the E key to exit.

# About LD19

- Datasheet https://www.waveshare.com/wiki/DTOF_LIDAR_LD19
<!-- Thanks to repo from: https://github.com/henjin0/LIDAR_LD06_python_loder/tree/main -->
