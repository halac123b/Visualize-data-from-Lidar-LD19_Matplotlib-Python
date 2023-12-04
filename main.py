import serial
from CalcLidarData import CalcLidarData
import matplotlib.pyplot as plt
import math

# Tạo 1 figure với pyplot của matplotlib
# Figure có thể hiểu là 1 canvas, trên đó ta có thể vẽ nhiều biểu đồ
fig = plt.figure(figsize=(8,8))

# Tạo 1 biểu đồ trên Figure
  # Tại tọa độ 111, tức (1, 1) và mang index = 1 trên figure
  # Hệ tọa độ polar, hình tròn, thường dùng trong các bản đồ radar
ax = fig.add_subplot(111, projection='polar')
# Title cho biểu đồ
ax.set_title('Lidar LD19 (exit: Key E)',fontsize=18)

# Com port kết nối serial
com_port = "COM5"

# Tạo 1 event cho pyplot
  # 'key_press_event': event nhấn 1 key
  # 1 hàm đc trigger cùng event
  # Press E to exit
plt.connect('key_press_event', lambda event: exit(1) if event.key == 'e' else None)

# Tạo kết nối Serial
ser = serial.Serial(port=com_port,
                    baudrate=230400,
                    timeout=5.0,
                    bytesize=8,
                    parity='N',
                    stopbits=1)

tmpString = ""
lines = list()
angles = list()
distances = list()

i = 0
while True:
    loopFlag = True
    flag2c = False

    if (i % 40 == 39):
        if ('line' in locals()):
            line.remove()

        # Vẽ biểu đồ scatter (biểu đồ dạng điểm)
            # Thường biểu diễn tương quan giữa 2 giá trị, ở đây là góc + khoảng cách
            # c: color, s: size of points
        print(len(angles))
        line = ax.scatter(angles, distances, c="blue", s=5)
        # Set offset cho vị trí của góc 0 độ trong hệ tọa độ polar
            # Với hệ tọa độ của Lidar, góc 0 độ ứng với trục 0y nên cần set offset pi / 2
        ax.set_theta_offset(math.pi / 2)
        # Update Figure, hoặc delay 1 khoảng thời gian
        plt.pause(0.01)
        # Clear tập giá trị
        angles.clear()
        distances.clear()

        i = 0


    while loopFlag:
        # Đọc data từ Serial
        b = ser.read()
        # Convert int từ byte đọc được
            # big: byte order của chuỗi bit, các bit quan trọng nhất nằm ở đầu
        tmpInt = int.from_bytes(b, 'big')

        # 0x54, indicating the beginning of the data packet (LD19 document)
        if (tmpInt == 0x54):
            tmpString += b.hex() + " "
            flag2c = True
            continue

        # 0x2c: fixed value of VerLen (LD19 document)
        elif (tmpInt == 0x2c and flag2c):
            tmpString += b.hex()


            if (not len(tmpString[0:-5].replace(' ','')) == 90):
                tmpString = ""
                loopFlag = False
                flag2c = False
                continue

            # Sau khi đọc full 1 gói data Lidar sẽ có kích thước = 90, lấy string và đưa vào hàm CalcLidarData()
            lidarData = CalcLidarData(tmpString[0:-5])
            # Get giá trị của góc và distance
            angles.extend(lidarData.Angle_i)
            distances.extend(lidarData.Distance_i)

            #print(distances)

            tmpString = ""
            loopFlag = False
        else:
            tmpString += b.hex()+ " "

        flag2c = False

    i += 1

ser.close()