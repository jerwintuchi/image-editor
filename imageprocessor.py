import streamlit as st
from PIL import Image, ImageFilter
import numpy as np
import cv2



st.markdown(""" <style style="text-align: center;"> .font {
    font-size:35px ; font-family: 'Times New Roman'; color: #00000;} 
    </style> """, unsafe_allow_html=True)
st.markdown('<p class="font">Upload your Image </p>', unsafe_allow_html=True)

#Streamlit's file uploader for image input
image = st.file_uploader("", type=['jpg','png','jpeg'])




#Add 'before' and 'after' columns
if image is not None:
    image = Image.open(image)
    
    col1, col2 = st.columns( [0.5, 0.5])# before and after columns

    #image processing logic
    with col1:
        st.markdown('<p style="text-align: center;">Original Image</p>',unsafe_allow_html=True)
        st.image(image,width=300)  

    with col2:
        st.markdown('<p style="text-align: center;">Result</p>',unsafe_allow_html=True)
        filter = st.sidebar.radio('Convert to', ['Original','Gray Image','Black and White', 'Pencil Sketch', 'Blur Effect','Remove Background','Gaussian Adaptive Thresholding'])
        if filter == 'Gray Image':
                converted_img = np.array(image.convert('RGB'))
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                st.image(gray_scale, width=300)
        elif filter == 'Black and White':
                converted_img = np.array(image.convert('RGB'))
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
                (thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
                st.image(blackAndWhiteImage, width=300)
        elif filter == 'Pencil Sketch':
                converted_img = np.array(image.convert('RGB')) 
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                inv_gray = 255 - gray_scale
                slider = st.sidebar.slider('Adjust the Intensity', 25, 255, 125, step=2)
                blur_image = cv2.GaussianBlur(inv_gray, (slider,slider), 0, 0)
                sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
                st.image(sketch, width=300) 
        elif filter == 'Blur Effect':
                converted_img = np.array(image.convert('RGB'))
                slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=2)
                converted_img = cv2.cvtColor(converted_img, cv2.COLOR_RGB2BGR)
                blur_image = cv2.GaussianBlur(converted_img, (slider,slider), 0, 0)
                st.image(blur_image, channels='BGR', width=300) 
        elif filter == 'Remove Background':
                converted_img = np.array(image.convert('RGB'))
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                ret,baseline = cv2.threshold(gray_scale,127,255,cv2.THRESH_TRUNC)
                ret,background = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY)
                ret,foreground = cv2.threshold(baseline,126,255,cv2.THRESH_BINARY_INV)
                foreground = cv2.bitwise_and(converted_img,converted_img, mask=foreground)  # Update foreground with bitwise_and to extract real foreground
                background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)# Convert black and white back into 3 channel greyscale
                finalimage = background+foreground #Combine the background and foreground to obtain our final image
                st.image(finalimage,width=300)
        elif filter == 'Gaussian Adaptive Thresholding':
                converted_img = np.array(image.convert('RGB'))
                converted_img = cv2.cvtColor(converted_img, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(converted_img, (7, 7), 0)
                adpt_thrsh= cv2.adaptiveThreshold(blurred, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4)
                st.image(adpt_thrsh,width=300)
        else: 
                st.image(image, width=300)

