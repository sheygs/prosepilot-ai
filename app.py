import streamlit as st
import openai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key from environment if available
openai_api_key = os.getenv("OPENAI_API_KEY", "")

# Set up page configuration
st.set_page_config(page_title="Content AI Agent", layout="wide")

# Initialize session state variables if they don't exist
if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Sidebar for API configuration
with st.sidebar:
    st.title("Content AI Agent")
    api_key = st.text_input("Enter OpenAI API Key", value=openai_api_key, type="password")

    # Content type selection
    content_type = st.selectbox(
        "Select Content Type",
        ["Blog Post", "Social Media Post", "Product Description", "Email", "Custom"]
    )

    if content_type == "Custom":
        custom_type = st.text_input("Enter custom content type")
        content_type = custom_type if custom_type else "General Content"

    # Model selection
    model = st.selectbox(
        "Select Model",
        ["gpt-3.5-turbo", "gpt-4.1"]
    )

    # Temperature slider
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

    # Clear conversation button
    if st.button("Clear Conversation"):
        st.session_state.conversation_history = []
        st.session_state.generated_content = ""

# Main app interface
st.title("Content Generator AI Agent")

# Input section
prompt_col1, prompt_col2 = st.columns([3, 1])

with prompt_col1:
    user_prompt = st.text_area("What content would you like to generate?", height=100)

with prompt_col2:
    st.write("Content Parameters")
    tone = st.selectbox("Tone", ["Professional", "Casual", "Enthusiastic", "Informative", "Persuasive"])
    max_length = st.number_input("Max Words", min_value=50, max_value=2000, value=500, step=50)

# Generate button
generate_pressed = st.button("Generate Content")

# Function to call OpenAI API
def generate_content(prompt, content_type, tone, max_length):
    if not api_key:
        return "Please enter your OpenAI API key in the sidebar."

    try:
        openai.api_key = api_key

        system_message = f"""You are an expert content creator specialized in creating {content_type}s.
        Create content with a {tone.lower()} tone.
        Keep the content under {max_length} words.
        Focus on quality, engagement, and relevance."""

        full_prompt = f"Create a {content_type} about: {prompt}"

        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": full_prompt}
            ],
            temperature=temperature,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating content: {str(e)}"

# Generate content when the button is pressed
if generate_pressed and user_prompt:
    with st.spinner("Generating content..."):
        generated_text = generate_content(user_prompt, content_type, tone, max_length)
        st.session_state.generated_content = generated_text

        # Add to conversation history
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.conversation_history.append({
            "timestamp": timestamp,
            "prompt": user_prompt,
            "content_type": content_type,
            "tone": tone,
            "response": generated_text
        })

# Display generated content
if st.session_state.generated_content:
    st.subheader("Generated Content")
    st.write(st.session_state.generated_content)

    # Copy button
    st.button("Copy to Clipboard", help="Copy the generated content to clipboard")

    # Export options
    export_col1, export_col2 = st.columns(2)
    with export_col1:
        st.download_button(
            label="Download as TXT",
            data=st.session_state.generated_content,
            file_name=f"{content_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

    with export_col2:
        # Format content as markdown
        st.download_button(
            label="Download as MD",
            data=st.session_state.generated_content,
            file_name=f"{content_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )

# Display conversation history
if st.session_state.conversation_history:
    with st.expander("Conversation History", expanded=False):
        for i, exchange in enumerate(reversed(st.session_state.conversation_history)):
            st.write(f"**[{exchange['timestamp']}] {exchange['content_type']} ({exchange['tone']})**")
            st.write(f"Prompt: {exchange['prompt']}")
            st.write("Response:")
            st.write(exchange['response'])
            st.divider()

# Footer
st.markdown("---")
st.caption("Content AI Agent - Created with Streamlit and OpenAI")