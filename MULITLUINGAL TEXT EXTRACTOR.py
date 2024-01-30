from dotenv import load_dotenv

load_dotenv()
import pathlib
import textwrap
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai 

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


#input means what to do by this app which is the input prompt and is general
#prompt means what it wants at that point of time
#image means what image we want to apply 
#this function gives the response from the model
def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text


#load the image and convert the image in bytes
def input_image_setup(uploaded_file):
      if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, 
                "data": bytes_data
            }
        ]
        return image_parts
      else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Mulitlanguage Invoice Extractor")

st.header("Mulitlanguage Invoice Extractor")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the image")


input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """



if submit:
    image_data=input_image_setup(uploaded_file)  #get the image data
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is")
    st.write(response)