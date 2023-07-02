import streamlit as st
import json                    
import requests
import base64

api = 'http://localhost:5000/test'

st.header("ASL Alphabet Translator")
st.subheader("This app translates the ASL alphabet into English letters.")
st.write("To use this app, please take an image of a hand sign for a letter in the ASL alphabet. The app will then translate the image into the corresponding English letter.")

picture = st.camera_input("Take a picture")

if st.button("Translate"):
    bytes_data = picture.getvalue()
    im_b64 = base64.b64encode(bytes_data).decode("utf8")
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    payload = json.dumps({"image": im_b64})
    response = requests.post(api, data=payload, headers=headers)
    data = response.json()
    st.write("The letter is: ", data["output"])