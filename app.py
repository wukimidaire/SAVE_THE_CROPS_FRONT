import streamlit as st
import pandas as pd
from io import BytesIO
# Added for image handling
from PIL import Image

'''
# Save The Crops Front

This front queries the Save The Crops [save_the_crops API](https://taxifare.lewagon.ai/predict?pickup_datetime=2012-10-06%2012:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2)
'''


# Add a placeholder image to display initially

placeholder = Image.open("/Users/victordecoster/code/MahautHDL/save_the_crops_front/media/leaf_area.webp")
st.image(placeholder, use_column_width=True)

with st.form(key='params_for_api'):

    # Upload image file
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    ## test which image types are working and exclude those from the type

    if st.form_submit_button("Upload"):
        if uploaded_file is not None:
            # Try opening the image using PIL
            try:
                img = Image.open(uploaded_file)
                st.image(img, use_column_width=True)  # Display uploaded image
            except:
                st.error("Invalid image format. Please select a valid image file.")
        else:
            st.warning("Please upload an image file.")


#wagon_cab_api_url = 'https://taxifare.lewagon.ai/predict'
#response = requests.get(wagon_cab_api_url, params=params)

#prediction = response.json()

#pred = prediction['fare']

#st.header(f'Fare amount: ${round(pred, 2)}')
