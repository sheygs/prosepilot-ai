from typing import Any
import streamlit as st
from datetime import datetime
from models.content import ContentItem
from api.openai_client import EnhancedOpenAIClient


def render_content_generator(api_key, content_type, model, temperature) -> dict[str, Any]:
    """Render the content generation UI with RAG enhancement"""

    st.markdown(
        """
         <h1 style='font-size: 28px; font-family: "Playfair Display", serif; font-weight: 400; letter-spacing: 0.5px; color: #fff;'>
             From Concept to Published Content in mins 🚀
         </h1>
        """,
        unsafe_allow_html=True
    )

    # Input section
    prompt_column1, prompt_column2 = st.columns([3, 1])

    with prompt_column1:
        user_prompt = st.text_area(
            "What content would you like to generate?", height=100)

    with prompt_column2:
        st.write("Content Parameters")
        tone = st.selectbox(
            "Tone", ["Professional", "Casual", "Enthusiastic", "Informative", "Technical"])
        max_length = st.number_input(
            "Max Words", min_value=50, max_value=2000, value=500, step=50)

        # RAG enhancement indicator
        st.info("🧠 RAG Enhancement: ON\nUsing writing best practices and guidelines")

    generate_pressed = st.button("Generate Content")

    # Generate content when the button is pressed
    if generate_pressed and user_prompt:
        with st.spinner("Generating content with RAG enhancement.."):
            openai_client = EnhancedOpenAIClient(api_key)
            generated_text = openai_client.generate_content(
                user_prompt, content_type, tone, max_length, model, temperature
            )

            # Analyze content
            content_analysis = openai_client.get_content_analysis(
                generated_text, content_type)

            st.session_state.generated_content = generated_text
            st.session_state.content_analysis = content_analysis

            # Add to conversation history
            content_item = ContentItem.create_from_generation(
                user_prompt, content_type, tone, generated_text
            )
            st.session_state.conversation_history.append(content_item.__dict__)

    # Display generated content
    if st.session_state.generated_content:
        st.subheader("Generated Content")
        st.markdown(st.session_state.generated_content)

        # Show content analysis
        if hasattr(st.session_state, 'content_analysis'):
            with st.expander("Content Analysis", expanded=False):
                analysis = st.session_state.content_analysis

                # Overall quality score
                st.subheader(
                    f"Overall Quality Score: {analysis['overall_quality']}/100")

                # Detailed metrics
                column1, column2, column3, column4 = st.columns(4)
                with column1:
                    st.metric("Word Count", analysis["word_count"])
                with column2:
                    st.metric("Structure Score",
                              f"{analysis['structure_score']}/100")
                with column3:
                    st.metric("SEO Score", f"{analysis['seo_score']}/100")
                with column4:
                    st.metric("Readability",
                              f"{analysis['readability_score']}/100")

                # Detailed breakdown
                if st.checkbox("Show detailed breakdown"):
                    st.json(analysis["structure_details"])
                    st.json(analysis["seo_details"])
                    st.json(analysis["readability_details"])

        # Actions row
        column1, column2, column3 = st.columns(3)

        with column1:
            st.button("Copy to Clipboard",
                      help="Copy the generated content to clipboard")

        with column2:
            st.download_button(
                label="Download as TXT",
                data=st.session_state.generated_content,
                file_name=f"{content_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

        with column3:
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


def render_conversation_history() -> None:
    """Render the conversation history"""
    if st.session_state.conversation_history:
        with st.expander("Conversation History", expanded=False):
            for i, exchange in enumerate(reversed(st.session_state.conversation_history)):
                st.write(
                    f"**[{exchange['timestamp']}] {exchange['content_type']} ({exchange['tone']})**")
                st.write(f"Prompt: {exchange['prompt']}")
                st.write("Response:")
                st.markdown(exchange['response'])
                st.divider()
