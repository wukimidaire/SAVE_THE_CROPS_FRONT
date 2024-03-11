import streamlit as st
import os # needed for the file paths
import pandas as pd
from io import BytesIO
import requests
import time # needed for adding a delay (optional)
# Added for image handling
from PIL import Image
import base64



# construct the relative path of the backgroun image
base_dir = os.path.dirname(os.path.realpath(__file__))
img_path = os.path.join(base_dir, "media", "field.jpg")


def set_bg_image(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.

    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"

    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}

         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_image(img_path)



# Replace with your chatbot's webhook URL
WEBHOOK_URL = "https://vliegendepater.app.n8n.cloud/webhook/bc011292-0fb8-4913-92c0-fe4fc02aae8d/chat"



# create a container for the text, buttons and black background
container = st.container()
with container:

    '''
    # Save The Crops Front

    This front queries the Save The Crops [save_the_crops API](https://taxifare.lewagon.ai/predict?pickup_datetime=2012-10-06%2012:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2)
    '''
    with st.form(key='params_for_api'):


        # test_url = https://vliegendepater.app.n8n.cloud/webhook-test/7e052c57-cbea-48f7-8d20-4db249e032c6
        def send_message(message):
            """Sends a message to the chatbot backend."""
            response = requests.post(WEBHOOK_URL, json={"message": message})
            return response.json()



        # Chatbot section
        user_input = st.text_input("Ask a question to the chatbot:", "")
        submit_button = st.form_submit_button(label="Send to Chatbot")

        if user_input:
            response = send_message(user_input)
            st.write("Chatbot:", response["message"])

        # Upload image file
        uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

        if st.form_submit_button("Upload"):
            if uploaded_file is not None:
                # Convert uploaded image to bytes
                img_bytes = uploaded_file.read()

                # Send image data to the backend API
                files = {'image': (uploaded_file.name, img_bytes, uploaded_file.type)}
                save_the_crops_url = 'https://taxifare.lewagon.ai/predict'

                # Display loading spinner while waiting for API response
                with st.spinner("Predicting crop species..."):
                    # Introduce a 10-second delay
                    time.sleep(5) # optional, only want to use this for testing with the backend api

                    # sends the request and process the response
                    response = requests.post(save_the_crops_url, files=files)

                    # handles API response and display prediction
                    if response.status_code == 200:
                        try:
                            prediction = response.json()
                            pred = prediction['crop species']  # Assuming the key is 'crop species'
                            st.header(f'Predicted crop species: {round(pred, 2)}')

                            # displays uploaded image, its overwrites the placeholder image
                            st.image(uploaded_file, use_column_width=True, key="uploaded_image")

                        except (KeyError, ValueError) as e:
                            st.error(f"Error parsing API response: {e}")
                        else:
                            st.error(f"API error: {response.status_code}")
                    else:
                        st.warning("Please upload an image file.")
