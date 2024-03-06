import streamlit as st
import os # needed for the file paths
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


# set the base directory relative to the script's location
base_dir = os.path.dirname(os.path.realpath(__file__))

# construct the relative paths
img_path = os.path.join(base_dir, "media", "field.jpg")


placeholder_path = os.path.join(base_dir, "media", "leaf_area.webp")



# adds a placeholder image to display initially
placeholder = Image.open(placeholder_path)

# displays initial placeholder image
st.image(placeholder, use_column_width=True)


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

                        # displays uploaded image, its overwrites the placeholder image
                        st.image(uploaded_file, use_column_width=True, key="uploaded_image")

                    except (KeyError, ValueError) as e:
                        st.error(f"Error parsing API response: {e}")
                else:
                    st.error(f"API error: {response.status_code}")
        else:
            st.warning("Please upload an image file.")



def set_bg_black():
   '''
   A function to create a black element behind the text.

   Returns
   -------
   None
   '''
   black_element_width = "1000px"  # Adjust this based on your needs
   black_element_height = "900px"  # Adjust this based on your needs
   black_element_top = "-900px"  # Adjust this to position the element
   black_element_left = "0"  # Left position

   st.markdown(
       f"""
       <style>
       .black-element {{
           position: absolute;
           top: {black_element_top};
           left: 50%;
           transform: translateX(-50%);
           width: {black_element_width};
           height: {black_element_height};
           background-color: black;
           opacity: 0.7;  # Adjust opacity as needed
           z-index: 0;  # Set lower z-index
       }}

       .text-on-black {{
         color: white;  # Set text color to white
         padding: 10px;  # Add padding
       }}

       </style>
       """,
       unsafe_allow_html=True
   )

   # Add a class to the text element to position it in front of the black element
   st.markdown(
       "<div class='black-element'></div>",
       unsafe_allow_html=True
   )

# Call the function to create the black element
set_bg_black()
