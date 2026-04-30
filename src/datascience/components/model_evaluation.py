import numpy as np
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from urllib.parse import urlparse
from pathlib import Path
from src.datascience.constant import *
from src.datascience.utils.common import read_yaml, create_directories, save_json
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from src.datascience.entity.config_entity import ModelEvaluationConfig

import os
os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/korede-folarin/DATASCIENCEPROJECT2.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "korede-folarin"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "2b28ec87c94248199a63df09406346c520efa243"


class ModelEvaluation:
    def __init__(self, config):
        self.config = config

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def log_into_mlflow(self):                                          # ✅ indented inside class
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis=1)   # ✅ consistent lowercase test_x
        test_y = test_data[[self.config.target_column]]

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme  # ✅ only defined once

        with mlflow.start_run():
            predicted_qualities = model.predict(test_x)
            (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)

            # Save metrics locally
            scores = {"rmse": rmse, "mae": mae, "r2": r2}
            save_json(path=Path(self.config.metric_file_name), data=scores)  # ✅ only once

            mlflow.log_params(self.config.all_params)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)

            # Model registry does not work with file store
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(model, "model", registered_model_name="ElasticnetModel")
            else:
                mlflow.sklearn.log_model(model, "model")