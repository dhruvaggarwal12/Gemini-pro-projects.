#to upload images option
#to show the image
#after hitting show the total calories it should interact with google gemini pro vision api to give response according to prompt and give response according to format specified


import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv


load_dotenv() #load all environment varialbles in .env file currently it is having only api key


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,image,prompt):  #specifying what to give as input and how the model will react according to prompt and the image and data after image input setup function coming out 
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()   

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file mime type is the format of the text and the image which is jpg
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

#the get gemini response will be used after this
    
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:  #if image is there it will show the image there only
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me the total calories")

input_prompt="""  
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               in below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----     

        

"""





if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)
































































