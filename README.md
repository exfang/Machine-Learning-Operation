# Setting up the Environment

## Create virtual environment
Navigate to your project folder
```console
C:/MLOPS Website> python -m venv mlops
```
## Activate the virtual environment
Activate venv in administrator mode in command prompt 
```console
C:/MLOPS Website>mlops/Scripts/activate
(mlops)C:/MLOPS Website>
```
## Change directory to the root dir
Poetry is the root dir
```console
(mlops)C:/MLOPS Website>cd poetry
```
## Download the necessary dependencies
```console
(mlops)C:/MLOPS Website/poetry>poetry install
```
## Run the website locally
Right-click the main.py and run the file in terminal

Note:
- If there is any error with the model, please rerun the pythonFiles > hdb/medical_model.py
