from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import matplotlib.pyplot as plt
import cv2
from tensorflow import keras
import numpy as np
from PIL import Image,ImageOps
import tensorflow as tf
import pandas as pd
import altair as alt

st.title('Colorectal cancer histology classifier')

class_names = ['tumor','stroma','complex','lympho','debris','mucosa','adipose','empty']

uploaded_image = st.file_uploader(label='Image upload',type=['png','jpg'])
if uploaded_image:
    file_bytes = np.asarray(bytearray(uploaded_image.read()),dtype=np.uint8)
    cv_image = cv2.imdecode(file_bytes,1)
    gray_img = cv2.cvtColor(cv_image,cv2.COLOR_BGR2RGB)
    gray_img = cv2.resize(gray_img,dsize=(224,224))
    gray_img = gray_img.astype('float32')
    gray_img /= 255
    gray_img = np.array([gray_img])
    for_display_image = cv2.cvtColor(cv_image,cv2.COLOR_BGR2RGB)
    for_display_image = cv2.resize(for_display_image,dsize=(120,120,))
    st.image(for_display_image)
with st.form("key1"):
        # ask for input
    button_check = st.form_submit_button("Predict")
if button_check:
    with tf.device('/device:CPU:0'):
        model = keras.models.load_model('saved_model/model.04-0.53.h5')
        result = model.predict(gray_img)



        st.title('Result')
        data = pd.DataFrame({
            'category' : class_names,
            'value' : result[0]})
        
        chart = alt.Chart(data).mark_bar().encode(
            x='category',
            y='value',
            color='category'
        ).properties(width=400)

        st.altair_chart(chart, use_container_width=True)
