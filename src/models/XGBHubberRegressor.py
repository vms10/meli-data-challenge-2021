import xgboost as xgb
import numpy as np
from sklearn.metrics import mean_squared_error as MSE


class XGBHubberRegressor():
    def __init__(self):
        self.model = None

    def train(self, X_train, T_train, Y_train, X_test, T_test, Y_test, output_file):

        X_train = np.concatenate(
            (X_train.reshape(X_train.shape[0], -1), T_train), axis=1)
        Y_train = np.argmax(Y_train, 1).reshape(-1, 1)

        X_test = np.concatenate(
            (X_test.reshape(X_test.shape[0], -1), T_test), axis=1)
        Y_test = np.argmax(Y_test, 1).reshape(-1, 1)

        train = xgb.DMatrix(X_train, Y_train)
        test = xgb.DMatrix(X_test, Y_test)

        params = {
            "learning_rate": 0.02,
            "max_depth": 7,
            "subsample": 0.5,
            "colsample_bytree": 0.8,
            "tree_method": 'gpu_hist',
            "min_child_weight": 0,
            "gamma": 0,
            "gpu_id": 0,
            "eval_metric": "mae",
            'objective': 'reg:pseudohubererror',
            "seed": 2021
        }

        # training, we set the early stopping rounds parameter
        model = xgb.train(params,
                          train, evals=[(train, "train"),
                                        (test, "validation")],
                          num_boost_round=20000, early_stopping_rounds=200)
        # # Predict the model
        # pred = model.predict(test)

        # # MAE Computation
        # mae = np.mean(np.abs(Y_test - pred))
        # print("Training finished, MAE test: % f" % (mae))

        model.save_model(output_file)

        self.model = xgb.XGBRegressor()
        self.model.load_model(output_file)

    def load(self, path):
        self.model = xgb.XGBRegressor()
        self.model.load_model(path)

    def predict(self, X, T):
        return self.model.predict(np.concatenate((X.reshape(X.shape[0], -1), T), axis=1)).reshape(-1, 1)

    def evaluate(self, X, T, Y):
        Y_pred = self.model.predict(np.concatenate(
            (X.reshape(X.shape[0], -1), T), axis=1))
        return np.mean(np.abs(Y_pred - Y))