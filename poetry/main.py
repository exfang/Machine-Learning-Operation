from flask import Flask, render_template, request
from wtforms import Form, validators, IntegerField, DecimalField, SelectField
from pycaret.classification import *
from pycaret.regression import *
import numpy as np
import pandas as pd
import hydra
from hydra.core.global_hydra import GlobalHydra

app = Flask(__name__)


@hydra.main(config_path="config", config_name="main")
def run_config(config):
    print("file found!")
    print(config.model)
    print(config.prediction)
    
    global rf_model, rf_cols, hdb_model, hdb_cols
    # current_path = utils.get_original_cwd() + "/"
    rf_model = load_model(config.model.medical)
    print(rf_model)
    rf_cols = config.prediction.medical_column
    print(rf_cols)
    hdb_model = load_model(config.model.hdb)
    hdb_cols = config.prediction.hdb_column
    return(rf_model, rf_cols, hdb_model, hdb_cols)


class Medical(Form):
    age = IntegerField('Age', [validators.NumberRange(min=1, max=130), validators.DataRequired()])
    # gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[validators.DataRequired()])
    chest_pain = SelectField('Chest Pain', choices=[('TA', 'Typical Angina'), ('ATA', 'Atypical Angina'), ('NAP', 'Non-Anginal Pain'), ('ASY', 'Asymptomatic')], validators=[validators.DataRequired()])
    resting_BP = DecimalField('Resting Blood Pressure', [validators.NumberRange(min=30), validators.DataRequired()])
    cholesterol = DecimalField('Cholesterol', [validators.NumberRange(min=30), validators.DataRequired()])
    # fasting_BS = DecimalField('Fasting Blood Sugar', [validators.NumberRange(min=0), validators.DataRequired()])
    # resting_ECG = SelectField('Resting ECG', choices=[('Normal', 'Normal'), ('ST', 'ST-T wave abnormality'), ('LVH', 'Probable or definite LVH')], validators=[validators.DataRequired()])
    max_HR = IntegerField('Max Heart Rate', [validators.NumberRange(min=60, max=202), validators.DataRequired()])
    # exercise_angina = SelectField('Exercise-Induced Angina', choices=[('Y', 'Yes'), ('N', 'No')], validators=[validators.DataRequired()])
    old_peak = DecimalField('Old Peak', [validators.NumberRange(min=-10, max=10), validators.DataRequired()])
    ST_slope = SelectField('ST Slope', choices=[('Up', 'Upsloping'), ('Flat', 'Flat'), ('Down', 'Downsloping')], validators=[validators.DataRequired()])


class Price(Form):
    town =  SelectField('Flat Type', choices=[('ANG MO KIO', 'ANG MO KIO'),
                                              ('BEDOK', 'BEDOK'),
                                              ('BISHAN', 'BISHAN'),
                                              ('BUKIT BATOK', 'BUKIT BATOK'),
                                              ('BUKIT MERAH', 'BUKIT MERAH'),
                                              ('BUKIT PANJANG', 'BUKIT PANJANG'),
                                              ('BUKIT TIMAH', 'BUKIT TIMAH'),
                                              ('CENTRAL AREA', 'CENTRAL AREA'),
                                              ('CHOA CHU KANG', 'CHOA CHU KANG'),
                                              ('CLEMENTI', 'CLEMENTI'),
                                              ('GEYLANG', 'GEYLANG'),
                                              ('HOUGANG', 'HOUGANG'),
                                              ('JURONG EAST', 'JURONG EAST'),
                                              ('JURONG WEST', 'JURONG WEST'),
                                              ('KALLANG/WHAMPOA', 'KALLANG/WHAMPOA'),
                                              ('MARINE PARADE', 'MARINE PARADE'),
                                              ('PASIR RIS', 'PASIR RIS'),
                                              ('PUNGGOL', 'PUNGGOL'),
                                              ('QUEENSTOWN', 'QUEENSTOWN'),
                                              ('SEMBAWANG', 'SEMBAWANG'),
                                              ('SENGKANG', 'SENGKANG'),
                                              ('SERANGOON', 'SERANGOON'),
                                              ('TAMPINES', 'TAMPINES'),
                                              ('TOA PAYOH', 'TOA PAYOH'),
                                              ('WOODLANDS', 'WOODLANDS'),
                                              ('YISHUN', 'YISHUN')],  validators=[validators.DataRequired()])     
    postal_code =  IntegerField('Postal Code', [validators.NumberRange(min=0, max=999999), validators.DataRequired()])        
    month = IntegerField('Month of purchase',  [validators.NumberRange(min=1, max=12), validators.DataRequired()])       
    year = IntegerField('Year of purchase',  [validators.NumberRange(min=1900, max=2030), validators.DataRequired()])     
    flat_type = SelectField('Flat Type', choices=[('1 ROOM', '1 ROOM'), 
                                                  ('2 ROOM', '2 ROOM'), 
                                                  ('3 ROOM', '3 ROOM'), 
                                                  ('4 ROOM', '4 ROOM'), 
                                                  ('5 ROOM', '5 ROOM'), 
                                                  ('EXECUTIVE', 'EXECUTIVE'), 
                                                  ('MULTI-GENERATION', 'MULTI-GENERATION')], 
                                                  validators=[validators.DataRequired()]) 
    storey_range = SelectField('Storey Range', choices=[('01 TO 03', '01 TO 03'), 
                                                        ('04 TO 06', '04 TO 06'), 
                                                        ('07 TO 09', '07 TO 09'), 
                                                        ('10 TO 12', '10 TO 12'), 
                                                        ('13 TO 15', '13 TO 15'), 
                                                        ('16 TO 18', '16 TO 18'), 
                                                        ('19 TO 21', '19 TO 21'), 
                                                        ('22 TO 24', '22 TO 24'), 
                                                        ('25 TO 27', '25 TO 27'), 
                                                        ('28 TO 30', '28 TO 30'), 
                                                        ('31 TO 33', '31 TO 33'), 
                                                        ('34 TO 36', '34 TO 36'), 
                                                        ('37 TO 39', '37 TO 39'), 
                                                        ('40 TO 42', '40 TO 42'), 
                                                        ('43 TO 45', '43 TO 45'), 
                                                        ('46 TO 48', '46 TO 48'), 
                                                        ('49 TO 51', '49 TO 51')], 
                                                        validators=[validators.DataRequired()])         
    floor_area_sqm = DecimalField('Floor Area in Square Metres', [validators.NumberRange(min=0), validators.DataRequired()])       
    flat_model = SelectField('Flat Type', choices=[('Improved', 'Improved'),
                                                   ('New Generation', 'New Generation'),
                                                   ('Model A', 'Model A'),
                                                   ('Standard', 'Standard'),
                                                   ('Simplified', 'Simplified'),
                                                   ('Premium Apartment', 'Premium Apartment'),
                                                   ('Maisonette', 'Maisonette'),
                                                   ('Apartment', 'Apartment'),
                                                   ('Model A2', 'Model A2'),
                                                   ('Type S1', 'Type S1'),
                                                   ('Type S2', 'Type S2'),
                                                   ('Adjoined flat', 'Adjoined flat'),
                                                   ('Terrace', 'Terrace'),
                                                   ('DBSS', 'DBSS'),
                                                   ('Model A-Maisonette', 'Model A-Maisonette'),
                                                   ('Premium Maisonette', 'Premium Maisonette'),
                                                   ('Multi Generation', 'Multi Generation'),
                                                   ('Premium Apartment Loft', 'Premium Apartment Loft'),
                                                   ('Improved-Maisonette', 'Improved-Maisonette'),
                                                   ('2-room', '2-room'),
                                                   ('3Gen', '3Gen')], 
                                                   validators=[validators.DataRequired()])            
    lease_commence_date = IntegerField('Lease Year',  [validators.NumberRange(min=1900, max=2030), validators.DataRequired()])     
    cbd_dist = DecimalField('Distance to nearest business district', [validators.NumberRange(min=0), validators.DataRequired()])               
    min_dist_mrt = DecimalField('Distance to nearest MRT', [validators.NumberRange(min=0), validators.DataRequired()])


@app.route('/')
def home():
    print("Running home ver6")
    return render_template('home.html')


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
    # GlobalHydra.instance().clear()
    app.run(debug=True)
    run_config()
