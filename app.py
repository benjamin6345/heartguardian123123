import streamlit as st
import pickle
import numpy as np
from collections import defaultdict

st.title("HeartGuardian")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Basic Information基本資料")
    age = st.slider("Age年齡", 5, 100, 1)
    sex = st.radio('Sex性別', ['Male男', 'Female女'])
    weight = st.slider("Weight體重(Kg)", 35, 200, 35)
    height = st.slider("Height高度(m)", 0.80, 2.4, 0.80)
    smoker = st.radio('Smoker吸煙者', ["Yes是", "No否"])
    

    
    
    
with col2:
    st.subheader("Health History健康歷史")
    stroke = st.radio("Have/Had Stroke(曾)中風", ["Yes是", "No否"])
    diabetic = st.radio("Had/Has Diabetes(曾)有糖尿病", ["Yes是", "Yes(During Pregnancy)是（當懷孕)","No否"])
    diffwalk = st.radio("Difficulty Walking走路困難", ["Yes是", "No否"])
    highbp = st.radio('High Blood Pressure 高血壓', ["Yes是", "No否"])
    highchol = st.radio('High Cholesterol 高膽固醇', ["Yes是", "No否"])
    physcAct = st.radio('Sport in the last 30 days過去三十天有做運動', ["Yes是", "No否"])
    veggies = st.radio('Consume vegetables every day每天吃菜', ["Yes是", "No否"])
    fruits = st.radio('Consume Fruits every day每天吃水果', ["Yes是", "No否"])
    num_beer = st.slider('Cups of alcohol per week每週飲酒量(杯)', 1, 20, 1)
    bad_menthealth_days = st.slider('Number of days suffering for mental issues in the past 30 days過去三十天有多少天是心理狀況不佳的', 0, 30, 0)
    bad_physhealth_days = st.slider('Number of days suffering for physics issues in the past 30 days過去三十天有多少天是身體狀況不佳的', 0, 30, 0)
    
    
    


with open("heartmodel.pkl", 'rb') as file:
    model = pickle.load(file)

def submit_actions():
    age_final = age/65
    BMI = weight / (height * height)
    BMI = BMI / 40
    smoker_final = 1 if smoker == 'Yes是' else 0
    sex_final = 1 if sex == 'Male男' else 0
    

    stroke_final = 1 if stroke == 'Yes是' else 0
    diabetic_final = 1 if diabetic == 'Yes是' else 2 if diabetic == "Yes(During Pregnancy)是（當懷孕)" else 0
    diffwalk_final = 1 if diffwalk == 'Yes是' else 0
    highbp_final = 1 if highbp == 'Yes是' else 0
    highchol_final = 1 if highchol == 'Yes是' else 0
    physAct_final = 1 if physcAct == 'Yes是' else 0
    veggies_final = 1 if veggies == 'Yes是' else 0
    fruits_final = 1 if fruits == 'Yes是' else 0
    bad_menthealth_days_final = bad_menthealth_days/30
    bad_physhealth_days_final = bad_physhealth_days/30
    
    if sex == 1: #Male
        highalc_final = 1 if num_beer >= 14 else 0
    
    else:
        highalc_final = 1 if num_beer >= 7 else 0
        
    
    
    
    result = [highbp_final, highchol_final, BMI, smoker_final, stroke_final, diabetic_final, physAct_final, fruits_final, veggies_final, highalc_final, bad_menthealth_days_final, bad_physhealth_days_final, diffwalk_final, sex_final, age_final]

    arr = np.array(result).reshape(1, -1)
    y_pred = np.round(model.predict(arr))[0]
   

    
    if y_pred == 1:
        st.subheader('Your body condition can be vulnerable to heart disease.')
        st.subheader('你較容易患有心臟病。')
        
        if diabetic_final == 1:
            st.markdown('Please manage your body sugar level. 請控制身體血糖量。 \n')
        if BMI > 23:
            st.markdown('Please control your weight/BMI. 請控制你的體重/BMI。\n')
        if smoker_final == 1:
            st.write('Please stop smoking. 請不要吸煙。')
            
        if highbp_final == 1:
            st.write('Please maintain a good lifestyle to maintain a lower blood pressure. 請保持健康的生活習慣以減低血壓。')

        if highchol_final == 1:
            st.write('Please maintain a good lifestyle to maintain a lower cholesterol level. 請保持健康的生活習慣以減低身體膽固醇含量。')
        if fruits_final == 0:
            st.write('Please eat fruits everyday. 請每天吃水果')
        if veggies_final == 0:
            st.write('Please eat vegetables everyday. 請每天吃菜')
        if physAct_final == 0:
            st.write('Please do more sports. 請多做運動')

        if bad_menthealth_days > 10:
            st.write('Please maintain mental health 請注意心理健康')

        if bad_physhealth_days >= 10:
            st.write('Please maintain physical health 請注意身體健康')
            
    else:
        st.subheader('Your body condition are not vulnerable to heart disease.')
        st.subheader('你較不容易患上心臟病。')
    
    
button = st.button("Submit提交", on_click=submit_actions)
