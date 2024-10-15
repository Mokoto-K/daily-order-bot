from tensorflow import keras, config
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import numpy as np

# Set a global random state so that the nn gives the same results each time
keras.utils.set_random_seed(69)

# If using TensorFlow, this will make GPU ops as deterministic as possible,
# but it will affect the overall performance, so be mindful of that.
config.experimental.enable_op_determinism()

# File path for our data
csv_path: str = "./BTC-1D-PRICE-HISTORY.csv"

# Load the price data as a pandas dataframe
price_data = pd.read_csv(csv_path)

# Assign variables to all main points of data from our dataframe
price_open = price_data.open
price_close = price_data.close
price_high = price_data.high
price_low = price_data.low
price_vol = price_data.volume

#-------------Create our target labels for our algorithm---------------
target = []

for row in range(len(price_open)):

    if price_close[row] - price_open[row] > 0:
        target.append("long")
    else:
        target.append("short")

price_data["target"] = target

#-------------Create day and month columns------------
dates = price_data.date
day_list = []
month_list = []

for row in dates:
    day = row.split("-")[0]
    month = row.split("-")[2]

    day_list.append(day)
    month_list.append(month)

price_data["day"] = day_list
price_data["month"] = month_list

price_data = price_data.drop(["date", "time"], axis=1)

#--------------Create daily open change column----------
daily_change = [0]

for row in range(len(price_open)):

    if row == 0:
        continue

    change = (price_open[row] - price_open[row-1]) / price_open[row - 1] * 100
    daily_change.append(round(change,8))

price_data["daily_change"] = daily_change

#-----------Create volitility column-----------
volitility = [0, 0]

for row in range(len(price_high)):

    if row == 0 or row == 1:
        continue

    vol = (price_high[row-2] - price_low[row-2]) /100
    volitility.append(vol)

price_data["volitility"] = volitility

#----------------Create highs, lows, highs distance and lows distance-------------
highs = [0, 0]
lows = [0, 0]
highs_from_open = [0, 0]
lows_from_open = [0, 0]

for row in range(len(price_high)):

    if row == 0 or row == 1:
        continue

    highs.append(price_high[row-2]/1000)
    lows.append(price_low[row-2]/1000)

    highs_from_open.append((price_high[row-2]-price_open[row-2])/10000)
    lows_from_open.append((price_low[row-2]-price_open[row-2])/10000)
# lows from open and highs from open
price_data["high"] = highs
price_data["low"] = lows

price_data["highs_from_open"] = highs_from_open
price_data["lows_from_open"] = lows_from_open

#---------------Create volumn column---------
volume = [0, 0]

for row in range(len(price_vol)):

    if row == 0 or row == 1:
        continue

    volume.append(price_vol[row - 2] / 1000000000)

price_data["volume"] = volume
price_data.tail(5)

# Ecode all text features to numbers for the nn to use
day_encoder = LabelEncoder()
month_encoder = LabelEncoder()
target_encoder = LabelEncoder()

day = day_encoder.fit_transform(price_data.day)
price_data["day"] = day

month = month_encoder.fit_transform(price_data.month)
price_data["month"] = month

target = target_encoder.fit_transform(price_data.target)
price_data["target"] = target

# Select the features to be used in training the nn
X = price_data.filter(["day", "month", "daily_change",  "volitility","volume", "highs_from_open", "lows_from_open", "target",]) # "volume", "low", "high", , "volitility", "highs_from_open", "lows_from_open"

# Split the training and test sets
X_train_full, X_test, y_train_full, y_test = train_test_split(X.drop("target", axis=1), X.target, random_state = 42)

# Split the alidation and training sets
X_val, X_train = X_train_full[:100], X_train_full[100:]
y_val, y_train = y_train_full[:100], y_train_full[100:]

# Get the number of features in the dataset by isolating the second number in "shape", this is needed to feed into the
# NN inputlayer
input_shape = X_train_full.shape[1]

# Build the nn model
model = keras.models.Sequential([
    keras.layers.InputLayer(shape=(input_shape,)),
    keras.layers.Dense(357, activation="relu"),
    keras.layers.Dense(325, activation="relu"),
    keras.layers.Dense(95, activation="relu"),
    keras.layers.Dense(25, activation="relu"),
    keras.layers.Dense(2, activation="softmax")
          ])

model.compile(loss="sparse_categorical_crossentropy",
             optimizer=keras.optimizers.SGD(learning_rate=0.001),
             metrics=["accuracy"])

history = model.fit(X_train, y_train, epochs=175, validation_data=(X_val, y_val))

# Evaluate the results on the test set
model.evaluate(X_test, y_test)

# Select the current column to predict a value on
c = price_data[-1:]

# price = [val for val in c.open]
# entry_price = price[0]

c = c.filter(["day", "month", "daily_change",  "volitility","volume", "highs_from_open", "lows_from_open"]) #, "volitility", "highs_from_open", "lows_from_open"

# Make a prediction
h = np.argmax(model.predict(c), axis=-1)

# Return the diection determined by the prediction
if h == 0:
    direction = "buy"
else:
    direction = "sell"





