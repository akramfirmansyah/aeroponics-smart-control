import pandas as pd
import numpy as np
import os
from pathlib import Path
from constant.directory import predict_dir, logs_dir
from datetime import datetime


def verify_input(
    airTemperature: int | float, humidity: int | float, waterTemperature: int | float
) -> tuple[int | float, int | float, int | float]:

    if airTemperature < 0:
        airTemperature = 0
    elif airTemperature > 45:
        airTemperature = 45

    if humidity < 0:
        humidity = 0
    elif humidity > 100:
        humidity = 100

    if waterTemperature < 0:
        waterTemperature = 0
    elif waterTemperature > 45:
        waterTemperature = 45

    # Detect anomaly
    airTemperature, humidity, waterTemperature = detect_anomaly(
        airTemperature, humidity, waterTemperature
    )

    return airTemperature, humidity, waterTemperature


def detect_anomaly(
    airTemperature: int | float, humidity: int | float, waterTemperature: int | float
) -> tuple[int | float, int | float, int | float]:
    # List all csv files in the predict_dir
    csv_files = list(Path(predict_dir).glob("*.csv"))

    # Get the latest Predict file
    predict_file = max(csv_files, key=os.path.getctime)
    df_predict = pd.read_csv(predict_file)

    # Get the latest metrix file
    df_metrix_air = pd.read_csv(f"{logs_dir}metrix_airTemperature.csv").iloc[-1]
    df_metrix_hum = pd.read_csv(f"{logs_dir}metrix_humidity.csv").iloc[-1]
    df_metrix_water = pd.read_csv(f"{logs_dir}metrix_waterTemperature.csv").iloc[-1]

    # Get current datetime in the format "YYYY-MM-DD HH:MM:00"
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:00")

    # Calculate absolute error
    error_air = np.abs(
        airTemperature
        - df_predict.loc[
            df_predict["datetime"] == datetime_now, "airTemperature"
        ].values[0]
    )
    error_hum = np.abs(
        humidity
        - df_predict.loc[df_predict["datetime"] == datetime_now, "humidity"].values[0]
    )
    error_water = np.abs(
        waterTemperature
        - df_predict.loc[
            df_predict["datetime"] == datetime_now, "waterTemperature"
        ].values[0]
    )

    # If error greater than mae, replace with predicted value
    if error_air > df_metrix_air["mae"]:
        airTemperature = df_predict.loc[
            df_predict["datetime"] == datetime_now, "airTemperature"
        ].values[0]

    if error_hum > df_metrix_hum["mae"]:
        humidity = df_predict.loc[
            df_predict["datetime"] == datetime_now, "humidity"
        ].values[0]

    if error_water > df_metrix_water["mae"]:
        waterTemperature = df_predict.loc[
            df_predict["datetime"] == datetime_now, "waterTemperature"
        ].values[0]

    return airTemperature, humidity, waterTemperature
