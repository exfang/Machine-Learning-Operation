import hydra
from omegaconf import DictConfig
from pycaret.classification import *
import pandas as pd
import os

# print("Hello1")
# rf_model = load_model(r"poetry\config\model\rf_model")
# print("Hello")
# print(rf_model)
@hydra.main(config_path="../config", config_name="main", version_base=None)
def process_data(config: DictConfig):
    print(f"Process data using {config.data.medical}")
    data = pd.read_csv(config.data.raw.medical)
    print(data.head())


if __name__ == "__main__":
    process_data()