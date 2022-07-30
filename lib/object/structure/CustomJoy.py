class CustomJoy:
    def __init__(self, data):
        self.gyro_x = 0
        self.gyro_z = 0
        self.convert_data(data)

    def convert_data(self, data):
        try:
            self.gyro_x = 256*data[20]+data[21]-(65536 if data[20] > 127 else 0)
            self.gyro_z = 256*data[24]+data[25]-(65536 if data[24] > 127 else 0)

            self.gyro_x = self.gyro_x/2048
            self.gyro_z = self.gyro_z/2048
        except:
            pass


    def get_axis(self, number):
        
        if number == 0:
            return -self.gyro_x

        else:
            return -self.gyro_z