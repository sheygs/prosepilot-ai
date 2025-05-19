import openai
import streamlit as st
from config.settings import OPENAI_API_KEY

class OpenAIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or OPENAI_API_KEY

    def generate_content(self, prompt, content_type, tone, max_length, model, temperature):
        """Generate content using OpenAI API"""
        if not self.api_key:
            return "Please enter your OpenAI API key in the sidebar."

        try:
            openai.api_key = self.api_key

            system_message = f"""You are an expert content creator specialized in creating {content_type}s.
            Create content with a {tone.lower()} tone.
            Keep the content under {max_length} words.
            Format the content in Markdown.
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