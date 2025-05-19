import streamlit as st
from datetime import datetime
from models.content import ContentItem
from api.openai_client import OpenAIClient

def render_content_generator(api_key, content_type, model, temperature):
    """Render the content generation UI"""
    st.title("ProsPilot AI - Elevate Your Content Creation Journey 🚀")

    # Input section
    prompt_col1, prompt_col2 = st.columns([3, 1])

    with prompt_col1:
        user_prompt = st.text_area("What content would you like to generate?", height=100)

    with prompt_col2:
        st.write("Content Parameters")
        tone = st.selectbox("Tone", ["Professional", "Casual", "Enthusiastic", "Informative", "Technical"])
        max_length = st.number_input("Max Words", min_value=50, max_value=2000, value=500, step=50)

    # Generate button
    generate_pressed = st.button("Generate Content")

    # Generate content when the button is pressed
    if generate_pressed and user_prompt:
        with st.spinner("Generating content..."):
            openai_client = OpenAIClient(api_key)
            generated_text = openai_client.generate_content(
                user_prompt, content_type, tone, max_length, model, temperature
            )

            st.session_state.generated_content = generated_text

            # Add to conversation history
            content_item = ContentItem.create_from_generation(
                user_prompt, content_type, tone, generated_text
            )
            st.session_state.conversation_history.append(content_item.__dict__)

    # Display generated content
    if st.session_state.generated_content:
        st.subheader("Generated Content")
        st.markdown(st.session_state.generated_content)

        # Actions row
        col1, col2, col3 = st.columns(3)

        with col1:
            # Copy button
            st.button("Copy to Clipboard", help="Copy the generated content to clipboard")

        with col2:
            # Export as TXT
            st.download_button(
                label="Download as TXT",
                data=st.session_state.generated_content,
                file_name=f"{content_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

        with col3:
            # Export as MD
            st.download_button(
                label="Download as MD",
                data=st.session_state.generated_content,
                file_name=f"{content_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )

    # Return the current state for use in other components
    return {
        "user_prompt": user_prompt if 'user_prompt' in locals() else "",
        "tone": tone if 'tone' in locals() else "Professional",
        "max_length": max_length if 'max_length' in locals() else 500
    }

def render_conversation_history():
    """Render the conversation history"""
    if st.session_state.conversation_history:
        with st.expander("Conversation History", expanded=False):
            for i, exchange in enumerate(reversed(st.session_state.conversation_history)):
                st.write(f"**[{exchange['timestamp']}] {exchange['content_type']} ({exchange['tone']})**")
                st.write(f"Prompt: {exchange['prompt']}")
                st.write("Response:")
                st.markdown(exchange['response'])
                st.divider()