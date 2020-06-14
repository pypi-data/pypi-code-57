# import warnings
# import pandas as pd
# import numpy as np
# from funhouse import TA
# import talib
# from sklearn import preprocessing
# from sklearn.model_selection import train_test_split
# # from emission.storages.pa_regressor.client import MemoryRegressorClient

# """ TA Preprocessing """
# # regress_client = MemoryRegressorClient(address="localhost", port=5581)
# def fib_feature(row):
    
#     # Using instead

#     main_value = row["price"]

#     # low7 = row["low7"]
#     low6 = row["low6"]
#     low5 = row["low5"]
#     low4 = row["low4"]
#     low3 = row["low3"]
#     low2 = row["low2"]
#     low1 = row["low1"]

#     up1 = row["up1"]
#     up2 = row["up2"]
#     up3 = row["up3"]
#     up4 = row["up4"]
#     up5 = row["up5"]
#     up6 = row["up6"]

#     current_value = 0

#     if low2 < main_value < low1:
#         current_value = -1
#     if low3 < main_value < low2:
#         current_value = -2
#     if low4 < main_value < low3:
#         current_value = -3
#     if low5 < main_value < low4:
#         current_value = -4
#     if low6 < main_value < low5:
#         current_value = -5
#     if main_value < low6:
#         current_value = -6

#     if up1 < main_value < up2:
#         current_value = 1
#     if up2 < main_value < up3:
#         current_value = 2
#     if up3 < main_value < up4:
#         current_value = 3
#     if up4 < main_value < up5:
#         current_value = 4
#     if up5 < main_value < up6:
#         current_value = 5
#     if main_value > up6:
#         current_value = 6

#     return current_value


# def rsi_feature(row, buy=35, sell=70):
#     buy_point = buy
#     sell_point = sell

#     if row < buy_point:
#         return 1
#     elif row > sell_point:
#         return -1
#     return 0




# """
#     Coin Price Preprocessing
# """



# def reduce_coin_tables(coin_data):
#     coin_data = coin_data.drop(["session_id", "type"], axis=1)
#     return coin_data


# def get_ta_features(coin_data):
#     ta = TA(coin_data).SMA(window=10).SMA(window=20).SMA(window=30).VolTrans(
#         window=20).RSI().ATR().FIBBB(stdev=1.7, window=20).EMA(window=10).EMA(window=20)
#     return ta


# def feature_engineer_fib(df, key_value="price"):
#     """ Find if the price or other value is in-between other values"""
#     df['fib_bet'] = df.apply(fib_feature, axis=1)
#     df = df.drop(labels=["up1", "up2", "up3", "up4", "up5", "up6",
#                          "basis", "low1", "low2", "low3", "low4", "low5", "low6"], axis=1)
#     return df


# def feature_engineer_main(df: pd.DataFrame):
#     # Get the rsi value
#     # Get the volatility RSI
#     df['rsi_buy_sell'] = df.RSI_14.apply(rsi_feature)
#     df['vol_buy_sell'] = df.voltrans_rsi.apply(rsi_feature, buy=40, sell=60)
#     return df


# def preprocess_moving_information(main_df: pd.DataFrame, fib_df: pd.DataFrame):
#     shifted_main = main_df.shift(-3)
#     shifted_price = shifted_main.price
#     fib_position = fib_df.fib_bet

#     main_df['fib_pos'] = fib_position
#     main_df['fib_trend'] = talib.ROCP(fib_position, timeperiod=2)
#     main_df['fib_trend_2'] = talib.ROCP(fib_position, timeperiod=4)
#     main_df['fib_trend_3'] = talib.ROCP(fib_position, timeperiod=6)

#     latest_3 = main_df.tail(3)

#     main_df['y'] = shifted_price
#     prediction_main = main_df.dropna()

#     prediction_main = prediction_main.drop(
#         columns=["price", "y"]).dropna()
#     weights = np.exp(np.linspace(-1., 0., len(prediction_main)))
#     weights_pred = np.exp(np.linspace(-1., 0., len(latest_3)))
#     latest_3["weights"] = weights_pred
#     prediction_main['weights'] = weights
#     prediction_main['y'] = shifted_price

#     return prediction_main, latest_3


# def scale_split(data_future):
#     prediction_main, latest_3 = data_future[0], data_future[1]
#     X = prediction_main.iloc[:, :-1].values
#     y = prediction_main.iloc[:, -1].values
#     X_pred = latest_3.iloc[:, :-1].values

#     X_scale = preprocessing.scale(X)
#     X_scale_pred = preprocessing.scale(X_pred)
#     return X_scale, X_scale_pred, y


# # def train_score_train_predict(scsplit_data, regress_select):
# #     X_scale, X_scale_pred, y = scsplit_data[0], scsplit_data[1], scsplit_data[2]
# #     score = 0
# #     prediction = []

# #     X_train, X_test, y_train, y_test = train_test_split(X_scale, y, test_size=0.2)
# #     regress_client.train(regress_select, X_train, y_train)
# #     score = regress_client.score(regress_select, X_test, y_test)
# #     regress_client.train(regress_select, X_test, y_test)
# #     prediction = regress_client.predict(regress_select, X_scale_pred)
# #     return score, prediction


# # with warnings.catch_warnings():
# #     warnings.simplefilter("ignore")
