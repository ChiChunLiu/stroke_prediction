import pickle
import pandas as pd
import flasgger
from flasgger import Swagger
from flask import Flask
from flask import request



app = Flask(__name__)
Swagger(app)

predict_dict = {1: 'have stroke', 0: 'not have stroke'}


with open("classifier.pkl","rb") as clf_pkl:
    clf = pickle.load(clf_pkl)
    
    
@app.route('/')
def rootpage():
    return "Hello! You can evaluate a person's stroke risk here!"


@app.route('/stroke_prediction',methods=["POST"])
def predict_note_file():
    """Predict stroke from input query file
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
      
    responses:
        200:
            description: stroke prediction
    """
    
    prompt = """
    gender
    age
    hypertension
    heart_disease
    ever_married
    work_type
    Residence_type
    avg_glucose_level
    bmi
    smoking_status
    stroke"""
    
    print(prompt)
    
    df_test = pd.read_csv(request.files.get("file"))
    print(df_test.head())
    pred = clf.predict(df_test)
    
    return str(list(pred))


if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)