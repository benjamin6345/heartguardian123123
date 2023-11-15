import streamlit as st
import pickle
import numpy as np
from collections import defaultdict

st.title("HeartGuardian")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Basic Information基本資料")
    age = st.slider("Age年齡", 5, 100, 1)
    weight = st.slider("Weight體重(Kg)", 35, 200, 35)
    height = st.slider("Height高度(m)", 0.80, 2.4, 0.80)
    smoker = st.radio('Smoker吸煙者', ["Yes是", "No否"])
    

    
    
    
with col2:
    st.subheader("Health History健康歷史")
    stroke = st.radio("Have/Had Stroke(曾)中風", ["Yes是", "No否"])
    diabetic = st.radio("Had/Has Diabetes(曾)有糖尿病", ["Yes是", "Yes(During Pregnancy)是（當懷孕)","No否"])
    diffwalk = st.radio("Difficulty Walking走路困難", ["Yes是", "No否"])
    highbp = st.radio('High Blood Pressure 高血壓', ["Yes是", "No否"])
    


with open("model3.pkl", 'rb') as file:
    model = pickle.load(file)

def submit_actions():
    age_final = age/65
    BMI = weight / (height * height)
    BMI = BMI / 40
    smoker_final = 1 if smoker == 'Yes是' else 0

    stroke_final = 1 if stroke == 'Yes是' else 0
    diabetic_final = 1 if diabetic == 'Yes是' else 2 if diabetic == "Yes(During Pregnancy)是（當懷孕)" else 0
    diffwalk_final = 1 if diffwalk == 'Yes是' else 0
    highbp_final = 1 if highbp == 'Yes是' else 0
    
    
    result = [age_final, diffwalk_final, highbp_final, stroke_final, diabetic_final, smoker_final, BMI]

    arr = np.array(result).reshape(1, -1)
    y_pred = np.round(model.predict(arr))[0]
   

    
    if y_pred == 1:
        st.subheader('Your body condition can be vulnerable to heart disease.')
        st.subheader('你較容易患有心臟病。')
        
        st.markdown('Professional Body Checks in Hospitals are Recommended. \n建議到醫院進行專業的身體檢查\n')
        if diabetic_final == 1:
            st.markdown('Please manage your body sugar level. 請控制身體血糖量。 \n')
        if BMI > 23:
            st.markdown('Please control your weight/BMI. 請控制你的體重/BMI。\n')
        if smoker_final == 1:
            st.write('Please stop smoking. 請不要吸煙。')
            
        if highbp_final == 1:
            st.write('Please maintain a good lifestyle to maintain a lower blood pressure. 請保持健康的身活習慣以減低血壓。')
            
    else:
        st.subheader('Your body condition are not vulnerable to heart disease.')
        st.subheader('你較不容易患上心臟病。')
        st.markdown('Professional Body Checks in Hospitals are not Necessary. \n不必到醫院進行專業的身體檢查\n')
    
    
button = st.button("Submit提交", on_click=submit_actions)
