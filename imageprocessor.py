import streamlit as st
from PIL import Image, ImageFilter

#Streamlit's file uploader for image input
image = Image.open(st.file_uploader('Upload Image:', type=['jpg', 'png']))

# Use PIL to apply a filter to the image
image = image.filter(ImageFilter.BLUR)

# Use Streamlit's image function to display the filtered image
st.image(image, caption='Blurred Image', width=500)