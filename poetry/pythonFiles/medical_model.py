# import hydra
# from omegaconf import DictConfig
# from hydra import initialize, compose, utils
# from omegaconf import OmegaConf
# import pandas as pd
# import os
# from pycaret.classification import *

# current_directory = os.getcwd()
# global config

# @hydra.main(config_path="../config", config_name="main", version_base=None)
# def process_data(config: DictConfig):
#     print(f"Process data using {config.data.raw.medical}")
#     df = pd.read_csv(config.data.raw.medical)
#     print(df.head())
#     data_cleaning(df, config)

# def data_cleaning(df, config):
#     exp = setup(data=df,
#             target='cv_issue',
#             session_id=42,
#             ignore_features= config.medical.cleaning.columns_to_drop,
#             bin_numeric_features = config.medical.cleaning.bin_column,
#             categorical_features= config.medical.cleaning.categorical_features,
#             numeric_features=config.medical.cleaning.numeric_features,
#             normalize=True,
#             normalize_method='minmax',
#             transformation=True,
#             remove_outliers=True,
#             n_jobs=5,
#             experiment_name="medicalcleaning",
#             use_gpu=True)
    
#     transformed_data = exp.get_config("dataset_transformed")
#     print("Storing transformed data for model training...")
#     transformed_data.to_csv(config.medical.clean_data_location, index=False)

#     print("Training the model now...")
#     # train random forest with some hyper parameter tunings
#     rf = create_model('rf', min_samples_split=10, min_samples_leaf=15, criterion="log_loss", random_state=42)
#     print("Training done. Finalizing...")
#     # finalize the model
#     final_best = finalize_model(rf)

#     # save model to disk
#     save_model(final_best, config.medical.trained_model)
#     print("Model saved.")

# if __name__ == "__main__":
#     process_data()