import hydra
from omegaconf import DictConfig
from hydra import initialize, compose, utils
from omegaconf import OmegaConf
import pandas as pd
import os
from pycaret.regression import *

current_directory = os.getcwd()
global config

@hydra.main(config_path="../config", config_name="main", version_base=None)
def process_data(config: DictConfig):
    print(f"Process data using {config.data.raw.hdb}")
    df = pd.read_csv(config.data.raw.hdb)
    print(df.head())
    data_cleaning(df, config)

def data_cleaning(df, config):
    df = df.drop(config.hdb.cleaning.columns_to_drop, axis=1)

    df[["Year", "Month"]] = df['month'].str.split("-", expand=True)

    df = df.drop(['month'], axis=1)

    s = setup(df, 
              target = 'resale_price', 
              transform_target = True,
              log_experiment = True, 
              experiment_name = 'hdb_1',
              train_size = 0.8,
              categorical_features = config.hdb.cleaning.categorical_features,
              numeric_features = config.hdb.cleaning.numeric_features,
              remove_outliers = True,
              remove_multicollinearity = True,
              multicollinearity_threshold = 0.8,
              transform_target_method = 'quantile',
              preprocess = True,
              categorical_imputation = 'drop',
              use_gpu = True
             )
    
    transformed_data = s.get_config("dataset_transformed")
    print("Storing transformed data for model training...")
    transformed_data.to_csv(config.hdb.clean_data_location, index=False)

    print("Training the model now...")
    gb = create_model('gbr')
    print("Training done. Finalizing...")
    # finalize the model
    final_best = finalize_model(gb)

    # save model to disk
    save_model(final_best, config.hdb.trained_model)
    print("Model saved.")

if __name__ == "__main__":
    process_data()