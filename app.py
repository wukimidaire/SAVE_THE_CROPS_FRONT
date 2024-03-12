import streamlit as st
import os # needed for the file paths
import pandas as pd
import requests
import time # needed for adding a delay (optional)
import base64
from requests_toolbelt.multipart.encoder import MultipartEncoder




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

# test_url = https://vliegendepater.app.n8n.cloud/webhook-test/7e052c57-cbea-48f7-8d20-4db249e032c6
def send_message(message):
    """Sends a message to the chatbot backend."""
    response = requests.post(WEBHOOK_URL, json={"message": message})
    return response.json()

def send_image_to_api(image_data, api_url="https://quirkynightingale-ivqufm4oza-ew.a.run.app/upload"):
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


# create a container for the text, buttons and black background
container = st.container()
with container:

    '''
    # Save The Crops Front

    This front queries the Save The Crops [save_the_crops API])
    '''
    # Wrap the user input and submit button within a form
    #with st.form(key="chatbot_form"):  # Give the form a unique key
    #    user_input = st.text_input("Ask a question to the chatbot:", "")
    #    submit_button = st.form_submit_button(label="Send to Chatbot")

    #if user_input:
    #    if submit_button:  # Check if the submit button was pressed
     #       response = send_message(user_input)
     #       st.write("Chatbot:", response["message"])


    # Streamlit App
    st.title("Image Upload App")
    uploaded_image = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        try:
            response = send_image_to_api(uploaded_image)  # Pass the full uploaded_image object
            if response:
                st.write(f"Plant : {response['plant']}")
                st.write(f"Disease : {response['disease']}")
                st.image(uploaded_image, width=400)  # Display the uploaded image
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
