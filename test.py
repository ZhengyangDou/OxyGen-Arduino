import pandas as pd
import matplotlib.pyplot as plt

# Read file and parse data
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
hourly_avg = df.resample("H").mean()

# Plot hourly averages
plt.figure(figsize=(10, 6))
for column in hourly_avg.columns:
    plt.plot(hourly_avg.index, hourly_avg[column], label=column)

    # Add small circles at each point
    plt.scatter(hourly_avg.index, hourly_avg[column], color='black', s=10)

    # Add data labels at each point
    for i in range(len(hourly_avg)):
        plt.text(hourly_avg.index[i], hourly_avg[column][i], f"{hourly_avg[column][i]:.2f}", fontsize=8, ha='center', va='bottom')

plt.xlabel('Time (Beijing Time)')
plt.ylabel('Average Value')
plt.title('Hourly Average Sensor Readings')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
