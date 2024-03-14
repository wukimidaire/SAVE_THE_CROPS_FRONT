import streamlit as st
import os # needed for the file paths
import pandas as pd
import requests
import base64
from requests_toolbelt.multipart.encoder import MultipartEncoder


st.set_page_config(page_title = "Save The Crops", page_icon="✨", layout = "centered", initial_sidebar_state = "expanded")


# construct the relative path of the backgroun image
base_dir = os.path.dirname(os.path.realpath(__file__))
img_path = os.path.join(base_dir, "media", "field.jpg")
# Secrets variables
api_url = os.environ["API_URL"]


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

def send_image_to_api(image_data, api_url=api_url):
    try:
        multipart_data = MultipartEncoder(
            fields={
                "file": (image_data.name, image_data, "image/jpeg"),
                "plant": options[0]
            }
        )
        headers = {"Content-Type": multipart_data.content_type}

        response = requests.post(api_url, headers=headers, data=multipart_data)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while sending the image: {e}")
        return None


# This is providing a shaded background so there is more contrast on the buttons and text fields
css_body_container = f'''
<style>
    section [data-testid="stAppViewBlockContainer"] {{background-color:rgba(0, 66, 37, 0.6)}}

</style>
'''
st.markdown(css_body_container,unsafe_allow_html=True)


# Create the container
container = st.container(height=1000)

with container:
    '''
    # Save The Crops
    '''

    options = st.multiselect(
    'What plant are you uploading?',
    ['tomato', 'maize', 'cassava', 'cashew', 'all'], max_selections=1)
    uploaded_image = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])



    if uploaded_image is not None:
        if not options:  # Check if a specie has been selected
            st.error("Select a specie before we can help you out")
        else:
            selected_specie = options[0]  # Get the selected specie

        if True:
        # try:
            response = send_image_to_api(uploaded_image, api_url)
            if response:
                st.subheader(f"{(response['disease'].capitalize())}")
                st.image(uploaded_image, width=400)
        # except requests.exceptions.RequestException as e:
        #     st.error(f"An error occurred: {e}")
