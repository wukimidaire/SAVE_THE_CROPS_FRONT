import streamlit as st
import pandas as pd
from io import BytesIO
import requests
import time # needed for adding a delay (optional)
# Added for image handling
from PIL import Image
import base64

'''
# Save The Crops Front

This front queries the Save The Crops [save_the_crops API](https://taxifare.lewagon.ai/predict?pickup_datetime=2012-10-06%2012:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2)
'''


def set_bg_image(img_path):
    """
    Sets the background image for the Streamlit app.

    Args:
        img_path (str): Path to the background image.
    """

    st.markdown(f'''
    <style>
      body {{
        background-image: url("{img_path}");
        background-size: cover;
        background-position: center;
      }}
    </style>
    ''', unsafe_allow_html=True)

# Set the background image path
img_path= "/Users/victordecoster/code/MahautHDL/save_the_crops_front/media/Brown_wheat.jpg"

## Call the custom component
set_bg_image(img_path)

# adds a placeholder image to display initially
placeholder = Image.open("/Users/victordecoster/code/MahautHDL/save_the_crops_front/media/leaf_area.webp")

# displays initial placeholder image
st.image(placeholder, use_column_width=True)

with st.form(key='params_for_api'):

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

                        # displays uploaded image, its overwrites the placeholder
                        st.image(uploaded_file, use_column_width=True, key="uploaded_image")

                    except (KeyError, ValueError) as e:
                        st.error(f"Error parsing API response: {e}")
                else:
                    st.error(f"API error: {response.status_code}")
        else:
            st.warning("Please upload an image file.")
