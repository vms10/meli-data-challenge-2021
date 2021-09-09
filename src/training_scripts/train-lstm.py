import os
import sys
from datasetutils import load_lvl_0_dataset
from models.LSTMBasedNN import LSTMBasedNN
from models.InputScaler import InputScaler
sys.path.append(os.path.abspath('./'))
import config

X_train, T_train, Y_train, X_val, T_val, Y_val = load_lvl_0_dataset(config.DATA_REPETITIONS_NN)

scaler = InputScaler.load(config.SCALER_PATH)

X_train, T_train = scaler.transform(X_train, T_train)
X_val, T_val = scaler.transform(X_val, T_val)

model = LSTMBasedNN()
model.train(X_train, T_train, Y_train, X_val, T_val, Y_val, config.LSTM_PATH, config.DEFAULT_BATCH_SIZE)

