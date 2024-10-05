import streamlit as st
from gradio_client import Client

# Define the Hugging Face Space's Gradio API URLs
API_URLS = {
    "o1": "https://yuntian-deng-o1.hf.space/",
    "o1mini": "https://yuntian-deng-o1mini.hf.space/"
}

# Function to query the Hugging Face Space API
def query_huggingface_api(model_choice, input_text):
    # Initialize the Gradio client based on the user's choice
    client = Client(API_URLS[model_choice])

    # Send the input to the model via the Gradio client
    result = client.predict(input_text, api_name="/predict")

    # Extract and return the relevant response (the generated text)
    return result[0][0][1]  # Assuming the generated text is in this position

def display_message(message):
    # Split the message by newline characters to handle new lines


    # Use st.markdown to render the formatted message
    st.markdown(message)

def main():
    st.title("Chat with ChatGpt-o1mini/o1")

    # Dropdown menu for selecting the model
    model_choice = st.selectbox("Choose the model:", options=["o1", "o1mini"])

    # User input box, allowing multi-line input
    user_input = st.text_area("You:", "", height=150)

    if st.button("Think!") and user_input:
        # Query the Hugging Face Space API based on the selected model
        response = query_huggingface_api(model_choice, user_input)

        # Display the model's response
        display_message(response)

if __name__ == "__main__":
    main()
