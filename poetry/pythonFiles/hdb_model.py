from hydra import initialize, compose, utils
from omegaconf import OmegaConf
import pandas as pd
import os

current_directory = os.getcwd()

with initialize(version_base=None, config_path="../../config/"):
    cfg = compose(config_name='main.yaml')
    print(f"Process data using {cfg.data.raw.hdb}")
    csv_file_path = os.path.join(current_directory, "../../", cfg.data.raw.hdb)
    df = pd.read_csv(csv_file_path)
    print(df.head())

df = df.drop(['block', 'street_name', 'latitude', 'longitude'], axis=1)

df[["Year", "Month"]] = df['month'].str.split("-", expand=True)

df = df.drop(['month'], axis=1)

from pycaret.regression import *
s = setup(df, 
          target = 'resale_price', 
          transform_target = True,
          log_experiment = True, 
          experiment_name = 'hdb_1',
          train_size = 0.8,
          categorical_features = ['town','postal_code', 'Year', 'Month', 'flat_type', 'storey_range', 'flat_model', 'lease_commence_date'],
          numeric_features = ['floor_area_sqm', 'cbd_dist', 'min_dist_mrt'],
          remove_outliers = True,
          remove_multicollinearity = True,
          multicollinearity_threshold = 0.8,
          transform_target_method = 'quantile',
          preprocess = True,
          categorical_imputation = 'drop',
          use_gpu = True
         )

gb = create_model('gbr')

# finalize the model
final_best = finalize_model(gb)

# save model to disk
save_model(final_best, 'gb')