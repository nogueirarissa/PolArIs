import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as gen_ai

# Configure Streamlit page settings
st.set_page_config(
    page_title="POLARIS",
    page_icon="🧭",
    layout="centered",    
)

load_dotenv()
polArIs_logo = "assets\polArIs_logo.png"


# Set up Google Gemini model
gen_ai.configure(api_key=os.getenv("API_KEY"))
model = gen_ai.GenerativeModel(model_name='gemini-1.5-pro-latest', system_instruction="Your name is Polaris, you are a female teacher engaged to help people at any level of knowledge in the areas of technology. However, your users are mostly beginners. Therefore, keep the language accessible and always prioritize establishing step-by- step instructions for beginners manage to break down bigger problems and always maintain engagement. Dont'be verbose, be practical an direct, and still be welcoming. Its principle is that knowledge is a staircase where we learn step by step, and that today we know more than we did before.")
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[{'role':'model', 'parts': [model.generate_content("Você deve falar: Como posso te ajudar hoje?").text]}])



# Load text
text1 = "👋 Olá!👋"
text2 = "Sou a Polaris, sua guia no vasto mar da tecnologia!"
text3 = "Meu propósito é facilitar a sua jornada de aprendizado! Vamos subir essa escada do conhecimento juntos, um passo de cada vez!😊 Se surgir algum problema, não se preocupe! Estou aqui para te dar o caminho das pedras, explicando cada passo de forma clara e simples."
text4 = "✨ Afinal, cada desafio que enfrentamos nos faz crescer e aprender ainda mais!✨"


# Create container with the image and the text

with st.container():
    st.image(polArIs_logo, use_column_width="auto")
    st.markdown("""
    <div style="display: flex; justify-content: center;">
        <div style="text-align: center;">
            <p style="font-size: 1.2em;"><strong>{text1}<strong></p>
            <p style="font-size: 1.2em;"><strong>{text2}<strong></p>
            <p style="font-size: 1.2em;"><strong>{text3}<strong></p>
            <p style="font-size: 1.2em;"><strong>{text4}<strong></p>
        </div>
    </div>
""".format(text1=text1, text2=text2, text3=text3, text4=text4), unsafe_allow_html=True)

# Divide the presentation part from the interation part
st.divider()


# Display the chat history
for message in st.session_state.chat_session.history:
    avatar = r"assets\polArIs_img.png" if translate_role_for_streamlit(message.role) == "assistant" else r"assets\user_img.png"
    with st.chat_message(translate_role_for_streamlit(message.role), avatar=avatar):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("O que vamos aprender hoje? ")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user", avatar= r"assets\user_img.png").markdown(user_prompt)

    # Send user's message to Gemini and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini's response
    with st.chat_message("assistant", avatar= r"assets\polArIs_img.png"):
        st.markdown(gemini_response.text)