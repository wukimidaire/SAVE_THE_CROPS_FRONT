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
img_path = os.path.join(base_dir, "media", "Brown_wheat.jpg")


placeholder_path = os.path.join(base_dir, "media", "leaf_area.webp")



# adds a placeholder image to display initially
placeholder = Image.open(placeholder_path)

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

                        # displays uploaded image, its overwrites the placeholder image
                        st.image(uploaded_file, use_column_width=True, key="uploaded_image")

                    except (KeyError, ValueError) as e:
                        st.error(f"Error parsing API response: {e}")
                else:
                    st.error(f"API error: {response.status_code}")
        else:
            st.warning("Please upload an image file.")


def set_bg_hack(main_bg):
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

set_bg_hack("/Users/victordecoster/code/MahautHDL/save_the_crops_front/media/field.jpg")

############# NOT WORKING ############
## Call the custom component
#def set_bg_image(img_path):
#    """
#    Sets the background image for the Streamlit app.
#
#    Args:
#        img_path (str): Path to the background image.
#    """
#
#    st.markdown(f'''
#    <style>
#      body {{
#        background-image: url("{img_path}");
#        background-size: cover;
#        background-position: center;
#      }}
#    </style>
#    ''', unsafe_allow_html=True)
#set_bg_image(img_path)

############# NOT WORKING II ############
#page_bg_img = '''
#<style>
#body {
#background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
#background-size: cover;
#  /* Add !important to override conflicting styles */
#  background-image: important !important;
#}
#</style>
#'''

#st.markdown(page_bg_img, unsafe_allow_html=True)
