from flask import Flask, render_template, request, redirect, url_for, session, flash, g, Response
from pythonFiles.forms import Medical, Price
from pycaret.classification import *
from pycaret.regression import *
import numpy as np
import pandas as pd

app = Flask(__name__)

# rf_model = load_model('models/rf_model')
# rf_cols = [
#     "age", "gender", "chest_pain", "resting_BP", "cholesterol",
#     "fasting_BS", "resting_ECG", "max_HR", "exercise_angina",
#     "old_peak", "ST_slope"
# ]

# Add your model code here
# hdb = load_model('./model/test')
# hdb_cols = ['town', 'postal_code', 'month', 'flat_type',
#       'storey_range', 'floor_area_sqm', 'flat_model', 'lease_commence_date',
#       'cbd_dist', 'min_dist_mrt' ]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cvprediction', methods=['GET', 'POST'])
def cv():
    cv_form = Medical(request.form)
    # if request.method == 'POST' and cv_form.validate():
    #     list_features = [x for x in request.form.values()]
    #     final = np.array(list_features)
    #     data_unseen = pd.DataFrame([final], columns=rf_cols)
    #     # transform the data to the right format
    #
    #     prediction = predict_model(rf_model, data=data_unseen, round=0)
    #     prediction = int(prediction.Label[0])
    #     return render_template("medical/medical_form.html", pred="Expected bill will be {}".format(prediction))

    return render_template('medical/medical_form.html', form=cv_form)


@app.route('/hdbprediction', methods=['GET', 'POST'])
def price():
    price_form = Price(request.form)
    # if request.method == 'POST' and price_form.validate():
    #     list_features = [x for x in request.form.values()]
    #     final = np.array(list_features)
    #     data_unseen = pd.DataFrame([final], columns=hdb_cols)
    #     # transform the data to the right format
    
    #     prediction = predict_model(hdb, data=data_unseen, round=0)
    #     prediction = int(prediction.prediction_label[0])
    #     return render_template('hdb/hdb.html', pred="Expected price will be {}".format(prediction))
    return render_template('hdb/hdb.html', form=price_form)


if __name__ == '__main__':
    app.run(debug=True)
