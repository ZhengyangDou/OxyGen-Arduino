from flask import Flask, jsonify
import serial
from threading import Thread
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
data = ""
# 打开串口连接
ser = serial.Serial('COM3', 9600)

# 从串口读取数据
def read_data():
    while True:
        global data
        data = ser.readline().decode().strip()

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
