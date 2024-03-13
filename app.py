import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import os # needed for the file paths
import pandas as pd
import requests
import time # needed for adding a delay (optional)
import base64
from requests_toolbelt.multipart.encoder import MultipartEncoder


# construct the relative path of the backgroun image
base_dir = os.path.dirname(os.path.realpath(__file__))
img_path = os.path.join(base_dir, "media", "field.jpg")
# Secrets variables
api_url = os.environ["API_URL"]
webhook_url = st.secrets["WEBHOOK_URL"]


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

def send_message(message):
    """Sends a message to the chatbot backend."""
    response = requests.post(webhook_url, json={"message": message})
    return response.json()

def send_image_to_api(image_data, api_url=api_url):
    try:
        multipart_data = MultipartEncoder(
        fields={"file": (image_data.name, image_data, "image/jpeg")})
        headers = {"Content-Type": multipart_data.content_type}

        response = requests.post(api_url, headers=headers, data=multipart_data)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while sending the image: {e}")
        return None



css_body_container = f'''
<style>
    section [data-testid="stAppViewBlockContainer"] {{background-color:rgba(0, 66, 37, 0.6)}}

</style>
'''
st.markdown(css_body_container,unsafe_allow_html=True)


# Create the container
container = st.container(height=1000)

with container:
    # Streamlit App
    st.title("Image Upload App")
    options = st.multiselect(
    'What plant specie are you uploading?',
    ['Tomato', 'Maize', 'Cassava', 'Cashew'], max_selections=1)
    uploaded_image = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        if not options:  # Check if a specie has been selected
            st.error("Select a specie before we can help you out")
        else:
            selected_specie = options[0]  # Get the selected specie
            api_url_with_specie = f"{api_url}?specie={selected_specie}"

        try:
            response = send_image_to_api(uploaded_image, api_url_with_specie)
            if response:
                st.write(f"Disease : {response['disease']}")
                st.image(uploaded_image, width=400)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    #(style=f"""
    #background-color: {container_color};
    #padding: 10px;  /* Optional padding for content */
    #border-radius: 5px;  /* Optional rounded corners */
    #"""):


    #''' # Save The Crops Front This front queries the Save The Crops [save_the_crops API])'''
    # Wrap the user input and submit button within a form
    #with st.form(key="chatbot_form"):  # Give the form a unique key
    #    user_input = st.text_input("Ask a question to the chatbot:", "")
    #    submit_button = st.form_submit_button(label="Send to Chatbot")

    #if user_input:
    #    if submit_button:  # Check if the submit button was pressed
     #       response = send_message(user_input)
     #       st.write("Chatbot:", response["message"])
