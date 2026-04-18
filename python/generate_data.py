import pandas as pd
import math
import random

data = []

for t in range(300):
    base = 3.0 + 0.3 * math.sin(t / 10)
    noise = random.uniform(-0.1, 0.1)
    current = base + noise
    data.append([t, round(current, 3)])

df = pd.DataFrame(data, columns=["time", "current"])
df["moving_avg"] = df["current"].rolling(window=5, min_periods=1).mean()
df.to_csv("normal_fan_data.csv", index=False)

print("Generated normal_fan_data.csv")