import streamlit as st
import requests
from PIL import Image


# 404 ERROR => 'book that isn't even in the library's catalog'
# 400 ERROR => http://127.0.0.1:8080/upload 'server understands request but can't process it due to an issue on your end'
# 405 ERROR => http://127.0.0.1:8080  'check out a book by eating it'

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

def send_image_to_api(image_data, api_url="http://127.0.0.1:8080/upload"):
  try:
    multipart_data = MultipartEncoder(
      fields={"file": (image_data.name, image_data, "image/jpeg")}
    )
    headers = {"Content-Type": multipart_data.content_type}

    response = requests.post(api_url, headers=headers, data=multipart_data)
    response.raise_for_status()  # Raise an exception for non-2xx status codes
    return response.json()
  except requests.exceptions.RequestException as e:
    st.error(f"An error occurred while sending the image: {e}")
    return None

# Streamlit App
st.title("Image Upload App")
uploaded_image = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
  try:
    response = send_image_to_api(uploaded_image)  # Pass the full uploaded_image object
    if response:
      st.write(f"API Response: {response}")
    st.image(uploaded_image, width=400)  # Display the uploaded image
  except requests.exceptions.RequestException as e:
    st.error(f"An error occurred: {e}")
