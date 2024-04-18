from flask import Flask, send_file
import serial
from threading import Thread
from flask_cors import CORS
import time
import pandas as pd
import matplotlib.pyplot as plt
import os

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
            new_data = f"{time.time()} CO2:{sprit_data[0]} TVOC:{sprit_data[1]} TEMP:{sprit_data[2]} Rh:{sprit_data[3]}\n"
            with open("data.txt", "a") as f:
                f.write(new_data)
            data = f"二氧化碳:{sprit_data[0]}%  总可挥发性有机物:{sprit_data[1]}%\n温度:{sprit_data[2]}度 湿度:{sprit_data[3]}%"
        except Exception as e:
            print(f"Error reading data: {e}")
            continue


@app.route('/')
def index():
    return "浴室氧气检测实时数据"


@app.route('/data')
def get_data():
    return data


@app.route("/data_img")
def get_data_img():
    file_path = "data.txt"
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        parts = line.strip().split(" ")
        timestamp = float(parts[0])
        co2 = float(parts[1].split(":")[1])
        tvoc = float(parts[2].split(":")[1])
        temp = float(parts[3].split(":")[1])
        rh = float(parts[4].split(":")[1])
        data.append([timestamp, co2, tvoc, temp, rh])

    # Create DataFrame
    df = pd.DataFrame(data, columns=["timestamp", "CO2", "TVOC", "TEMP", "Rh"])

    # Convert timestamp to datetime and adjust for Beijing Time
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s') + pd.Timedelta(hours=8)

    # Set timestamp as index
    df.set_index('timestamp', inplace=True)

    # Calculate hourly averages
    hourly_avg = df.resample('T').mean()

    # Plot hourly averages
    plt.figure(figsize=(10, 6))
    for column in hourly_avg.columns:
        plt.plot(hourly_avg.index, hourly_avg[column], label=column)

        # Add small circles at each point
        plt.scatter(hourly_avg.index, hourly_avg[column], color='black', s=10)

        # Add data labels at each point
        for i in range(len(hourly_avg)):
            plt.text(hourly_avg.index[i], hourly_avg[column][i], f"{hourly_avg[column][i]:.2f}", fontsize=8,
                     ha='center', va='bottom')

    plt.xlabel('Time (Beijing Time)')
    plt.ylabel('Average Value')
    plt.title('Hourly Average Sensor Readings')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the image file
    img_path = "data_plot.png"
    plt.savefig(img_path)

    # Close the plot and release resources
    plt.close()

    # Return the path to the image file
    return send_file(img_path, mimetype='image/png')


if __name__ == '__main__':
    socket_thread = Thread(target=app.run)
    socket_thread.start()
    read_data()
