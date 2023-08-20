from flask import Flask, render_template, request, redirect, url_for, session, flash, g, Response
from pythonFiles.forms import Medical, Price
from pycaret.classification import *
from pycaret.regression import *
import numpy as np
import pandas as pd
import hydra
from hydra import utils
from omegaconf import DictConfig
import os

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html')

@hydra.main(config_path="poetry/config", config_name="main")
def run(config):
    global rf_model
    global rf_cols
    global hdb_model
    global hdb_cols
    current_path = utils.get_original_cwd() + "/"
    rf_model = load_model(current_path+config.model.medical)
    rf_cols = config.prediction.medical_column
    hdb_model = load_model(current_path+config.model.hdb)
    hdb_cols = config.prediction.hdb_column


run()

@app.route('/cvprediction', methods=['GET', 'POST'])
def cv():
    cv_form = Medical(request.form)
    if request.method == 'POST' and cv_form.validate():
        list_features = [x for x in request.form.values()]
        final = np.array(list_features)
        print(final)
        
        data_unseen = pd.DataFrame([final], columns=rf_cols)
        prediction = predict_model(rf_model, data=data_unseen, round=0)
        output_text = ""
        if int(prediction.prediction_label) == 0:
            output_text = f"You are predicted to not have cardiovascular disease with a confidence of {int(prediction.prediction_score*100)}%"
        else:
            output_text = f"You are predicted to have cardiovascular disease with a confidence of {int(prediction.prediction_score*100)}%"
        return render_template("medical/medical_form.html", pred=output_text, form=cv_form)

    return render_template('medical/medical_form.html', form=cv_form)


@app.route('/hdbprediction', methods=['GET', 'POST'])
def price():
    price_form = Price(request.form)
    if request.method == 'POST' and price_form.validate():
        list_features = [x for x in request.form.values()]
        final = np.array(list_features)
        print(final)
        
        data_unseen = pd.DataFrame([final], columns=hdb_cols)
        prediction = predict_model(hdb_model, data=data_unseen, round=0)
        output_text = ""
        output_text = f"The predicted price of your flat is ${int(prediction.prediction_label)}"
        return render_template("hdb/hdb.html", pred=output_text, form=price_form)

    return render_template('hdb/hdb.html', form=price_form)


if __name__ == '__main__':
    app.run(debug=True)
