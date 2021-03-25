import pickle
import pandas as pd
import streamlit as st

predict_dict = {1: 'have stroke', 0: 'not have stroke'}


with open("classifier.pkl","rb") as clf_pkl:
    clf = pickle.load(clf_pkl)
    
header = []
with open("header.txt") as h:
    for line in h:
        header.append(line.strip())

def rootpage():
    return "Hello! You can evaluate a person's stroke risk here!"


def predict_stroke(gender, 
                   age,
                   hypertension, 
                   heart_disease, 
                   ever_married, 
                   work_type, 
                   Residence_type, 
                   avg_glucose_level, 
                   bmi, 
                   smoking_status):
    
    status_map = {'Yes': 0, 'No': 1}
    hypertension = status_map[hypertension]
    heart_disease = status_map[heart_disease]
    
    
    target = pd.DataFrame([[gender,
                           age,
                           hypertension, 
                           heart_disease, 
                           ever_married, 
                           work_type, 
                           Residence_type, 
                           avg_glucose_level, 
                           bmi, 
                           smoking_status]], 
                           columns = header)
    pred = clf.predict(target)
    print(pred)
    return pred


def main():
    st.title("Stroke Prediction")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Stroke prediction app with an ensemble model</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    gender = st.selectbox('Select your gender', ('Male', 'Female'))
    age = st.slider("Age", min_value=10, max_value=120)
    hypertension = st.selectbox('Hypertension status', ('Yes', 'No'))
    heart_disease = st.selectbox('Heart disease status', ('Yes', 'No'))
    ever_married = st.selectbox('Ever married?', ('Yes', 'No'))
    work_type = st.selectbox('Type of work', 
                             ('Private', 'Self-employed', 'Govt_job', 'children', 'Never_worked'))
    Residence_type = st.selectbox('Residence Type', ('Urban', 'Rural'))
    avg_glucose_level = st.slider("average glucose level", min_value=50, max_value=300)
    bmi = st.slider("BMI", min_value=5, max_value=100)
    smoking_status = st.selectbox('Ever smoke?', 
                                  ('formerly smoked', 'never smoked', 'smokes', 'Unknown'))
    
    
    result=""
    if st.button("Evaluate stroke status"):
        result = predict_stroke(gender, 
                   age,
                   hypertension, 
                   heart_disease, 
                   ever_married, 
                   work_type, 
                   Residence_type, 
                   avg_glucose_level, 
                   bmi, 
                   smoking_status)

    predict_dict = {1: 'have stroke', 0: 'not have stroke'}

    st.success('Predicted to {}'.format(predict_dict[result[0]]))
    
    if st.button("About"):
        st.text("stroke prediction with an ensemble ML model")
        st.text("Built with Streamlit")

if __name__=='__main__':
    main()
    
    