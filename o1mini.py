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
    lines = message.split('\n')

    # Process the message and separate text and code
    formatted_message = ""
    code_buffer = []  # To collect lines for the current code block
    code_block = False  # Flag to indicate if we are in a code block

    for line in lines:
        if line.startswith("```"):  # Detect start or end of code block
            if code_block:
                # We are ending a code block
                formatted_message += f"```python\n{''.join(code_buffer)}\n```\n"  # Add the buffered code block to the formatted message
                code_buffer = []  # Reset buffer for the next code block
                code_block = False
            else:
                # We are starting a code block
                code_block = True
        elif code_block:
            code_buffer.append(line.strip())  # Collect lines for the code block, stripping extra spaces
        else:
            if line.strip():  # Only show non-empty lines
                formatted_message += line + "\n"  # Add normal text to the formatted message

    # If there was a code block open at the end, display it
    if code_block and code_buffer:
        formatted_message += f"```python\n{''.join(code_buffer)}\n```\n"  # Display the final code block without extra new lines

    # Use st.markdown to render the formatted message
    st.markdown(formatted_message)

def main():
    st.title("Chat with Chatgpt o1/o1mini")

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
