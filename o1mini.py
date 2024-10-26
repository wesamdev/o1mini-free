import streamlit as st
from gradio_client import Client as GradioClient
from g4f.client import Client as G4FClient

# Define the Hugging Face Space's Gradio API URLs
API_URLS = {
    "o1": "https://yuntian-deng-o1.hf.space/",
    "o1mini": "https://yuntian-deng-o1mini.hf.space/"
}

g4f_name = {
    "gpt4o": "gpt-4o",
    "gpt3.5 turbo": "gpt-3.5-turbo",
    "gpt-4": "gpt-4"
}

g4f_client = G4FClient()

# Function to query the Hugging Face Space API
def query_huggingface_api(model_choice, input_text):
    client = GradioClient(API_URLS[model_choice])
    result = client.predict(input_text, api_name="/predict")
    return result[0][0][1]  # Assuming the generated text is in this position

def query_g4f(model_choice, input_text):
    response = g4f_client.chat.completions.create(
        model=g4f_name[model_choice],
        messages=[{"role": "user", "content": str(input_text)}],
    )
    result = response.choices[0].message.content
    return result

def display_chat_message(message, is_user):
    if is_user:
        st.markdown(message)
    else:
        st.markdown(message)

def main():
    st.title("Chat with ChatGpt-o1mini/o1 🤖")
    
    # Sidebar for conversation selection
    st.sidebar.title("Previous Conversations")
    
    # List to hold conversation histories
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # Allow users to select from previous conversations
    previous_conversations = st.sidebar.selectbox("Select a conversation:", 
                                                    options=[""] + [f"Conversation {i+1}" for i in range(len(st.session_state.conversation_history))])

    # Load the selected conversation if not empty
    if previous_conversations:
        index = int(previous_conversations.split(" ")[-1]) - 1
        user_input, response = st.session_state.conversation_history[index]
        display_chat_message(user_input, is_user=True)
        display_chat_message(response, is_user=False)
    else:
        user_input = ""

    # User input box for new conversation
    user_input = st.text_area("You:", user_input, height=150, placeholder="Type your message here...")

    # Dropdown menu for selecting the model
    model_choice = st.selectbox("Choose the model:", options=["o1", "o1mini", "gpt4o", "gpt3.5 turbo", "gpt-4"], index=1)

    if st.button("Think!") and user_input:
        # Query the Hugging Face Space API based on the selected model
        if model_choice in ["o1", "o1mini"]:
            response = query_huggingface_api(model_choice, user_input)
        else:
            response = query_g4f(model_choice, user_input)

        # Add the user's input and the model's response to the conversation history
        st.session_state.conversation_history.append((user_input, response))

        # Display the user's message and the model's response
        display_chat_message(user_input, is_user=True)
        display_chat_message(response, is_user=False)

if __name__ == "__main__":
    main()
