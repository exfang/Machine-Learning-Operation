# Machine Learning Operation Project

## Project Deliverables
- Website for users to interact with the models (HDB Pricing and Cardiovascular Prediction)
- Deployed Website

## Setting up the Environment

### Create virtual environment
Navigate to your project folder
```console
C:/MLOPS Website> python -m venv mlops
```
### Activate the virtual environment
Activate venv in administrator mode in command prompt 
```console
C:/MLOPS Website>mlops/Scripts/activate
(mlops)C:/MLOPS Website>
```
### Change directory to the root dir
Poetry is the root dir
```console
(mlops)C:/MLOPS Website>cd poetry
```
### Download the necessary dependencies
```console
(mlops)C:/MLOPS Website/poetry>poetry install
```
### Run the website locally
Right-click the main.py and run the file in terminal

## Our attempt at Render deployment

We were able to deploy the website. However, users were unable to interact with the model. Below are the steps we took to deploy it.

1. go to https://render.com
2. select new webservice
3. connect to the repo
4. enter your desired name
5. set root directory to poetry
6. start command: gunicorn main:app
7. add environment variable:
```
key: PYTHON_VERSION
value: 3.11.3
```
8. now wait for the website to deploy and done.

   
Note:
- If there is any error with the model, please rerun the pythonFiles > hdb/medical_model.py
