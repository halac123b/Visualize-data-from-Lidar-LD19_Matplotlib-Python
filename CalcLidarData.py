import math

class LidarData:
    #def __init__(self, FSA, LSA, CS, Speed, TimeStamp, Confidence_i, Angle_i, Distance_i):
    def __init__(self, FSA, LSA, CS, Speed, TimeStamp, Degree_angle, Angle_i, Distance_i):
        self.FSA = FSA
        self.LSA = LSA
        self.CS = CS
        self.Speed = Speed
        self.TimeStamp = TimeStamp
        self.Degree_angle = Degree_angle

        #self.Confidence_i = Confidence_i
        self.Angle_i = Angle_i
        self.Distance_i = Distance_i



def CalcLidarData(str):
    # Loại bỏ dấu cách
    str = str.replace(' ','')
    # Speed 2 byte, vì khi đọc string bị đảo ngược nên phải cộng ngược lại
        # Tốc độ quay Lidar, đơn vị (degree/s)
    Speed = int(str[2:4] + str[0:2], 16) / 100

    # Start angle: góc đầu tiên của data packet
        # Đơn vị (0.01 degree)
    FSA = float(int(str[6:8] + str[4:6], 16)) / 100

    # End angle: góc cuối của data packet
    LSA = float(int(str[-8:-6] + str[-10:-8], 16)) / 100

    # Thời gian capture của packet, đơn vị (ms)
    TimeStamp = int(str[-4:-2] + str[-6:-4], 16)

    # CRC check
    CS = int(str[-2:], 16)

    Confidence_i = list()
    Angle_i = list()
    Distance_i = list()
    Degree_angle = list()

    # Tính giá trị góc của packet
        # Chia 12 tức khoảng đo của 12 điểm trong 1 packet
    if(LSA - FSA > 0):
        angleStep = float(LSA - FSA) / 12
    else:
        angleStep = float((LSA + 360) - FSA) / 12

    counter = 0
    circle = lambda deg : deg - 360 if deg >= 360 else deg
    # Phân tích 12 điểm trong 1 packet
    for i in range(0, 6 * 12, 6):
        # Khoảng cách, đơn vị (mm)
        Distance_i.append(int(str[8+i+2 : 8+i+4] + str[8+i : 8+i+2], 16) / 1000)
        # Intensity, cường độ ánh sáng, càng lớn tức độ tin cậy càng chính xác
        #Confidence_i.append(int(str[8+i+4 : 8+i+6], 16))
        # Góc chiếu của điểm trong packet
        Degree_angle.append(circle(angleStep * counter + FSA))
        Angle_i.append(circle(angleStep * counter + FSA) * math.pi / 180.0)
        counter += 1

    lidarData = LidarData(FSA, LSA, CS, Speed, TimeStamp, Degree_angle, Angle_i, Distance_i)
    # Return data của Lidar
    return lidarData

