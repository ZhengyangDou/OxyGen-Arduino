from flask import Flask
import serial
from threading import Thread
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)
data = ""
ser = serial.Serial('COM3', 9600)


def read_data():
    while True:
        global data
        try:
            data = ser.readline().decode().strip()
            sprit_data = data.split()
            print(sprit_data)
            new_data = f"{time.time()} CO2:{sprit_data[0]} TVOC:{sprit_data[1]} TEMP:{sprit_data[2]} Rh:{sprit_data[3]}\n"
            with open("data.txt", "a") as f:
                f.write(new_data)
        except:
            continue


def backend():
    app.run()


@app.route('/')
def index():
    return "浴室氧气检测实时数据"


@app.route('/data')
def get_data():
    return data


if __name__ == '__main__':
    socket_thread = Thread(target=backend)
    socket_thread.start()
    read_data()
