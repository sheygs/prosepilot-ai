# ProsePilot AI

A full-stack AI content generation tool built with Python and Streamlit that allows you to create and publish blog posts directly to Hashnode.

## Overview

ProsePilot AI Agent helps you rapidly generate high-quality content using OpenAI's powerful language models and publish it directly to your Hashnode blog with just a few clicks. Perfect for technical writers, developers, and content creators looking to streamline their content workflow.

## Features

- **AI-Powered Content Generation**: Create blog posts, tutorials, and technical articles with OpenAI
- **Hashnode Direct Publishing**: Publish content as drafts directly to your Hashnode blog
- **Content Type Customization**: Generate different types of content with various tones and lengths
- **Multiple Export Options**: Download content as Markdown or text files
- **Conversation History**: Track your content generation sessions
- **User-Friendly Interface**: Clean, intuitive Streamlit interface

## Requirements

- Python 3.7+
- OpenAI API key
- Hashnode account with API key & Publication ID

## Setup Instructions

### 1. Installation

```bash
# Clone the repository or download the code
git clone https://github.com/sheygs/prosepilot-ai.git
cd prosepilot-ai

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install dependencies
pip3 install -r requirements.txt
```

### 2. API Keys Setup

Rename `.env.sample` file to `.env` file in the project directory and populate the required placeholders:

```
OPENAI_API_KEY=your_openai_api_key_here
HASHNODE_API_KEY=your_hashnode_api_key_here
HASHNODE_PUBLICATION_ID=your_hashnode_publication_id_here
```

### 3. Getting Your API Keys

#### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to the API section
4. Create a new API key

#### Hashnode API Key

1. Log in to [Hashnode](https://hashnode.com/)
2. Go to your profile picture → Developer Settings
3. Click "Generate New Token" in the Personal Access Tokens section
4. Copy the token (you won't be able to see it again)

#### Hashnode Publication ID (Required)

1. Log in to [Hashnode](https://hashnode.com/)
2. Go to your dashboard
3. Click on "Publications" in the left sidebar
4. Select your publication
5. Look at the URL: `https://hashnode.com/dashboard/publications/[YOUR_PUBLICATION_ID]/...`
6. Copy the ID portion from the URL

### 4. Running the Application

```bash
streamlit run main.py
```

Your web browser should open automatically to `http://localhost:8501`.

## Usage Guide

### Generating Content

1. Enter your OpenAI API key in the sidebar
2. Select content type, model, and temperature
3. Enter a prompt describing what content you want to generate
4. Select tone and maximum word count
5. Click "Generate Content"

### Publishing to Hashnode

1. Connect your Hashnode account by entering your API key and publication ID
2. After generating content, provide a title and optional subtitle
3. Search for and select relevant tags if desired
4. Click "Publish to Hashnode"
5. Your content will be created as a draft in your Hashnode publication
6. Go to your Hashnode dashboard to review and publish the draft

## Important Notes

- **Publication ID is Required**: You must provide a valid Hashnode publication ID to publish content
- **Drafts Only**: The app creates drafts in Hashnode which you must manually publish from your Hashnode dashboard
- **API Key Security**: Your API keys are masked in the interface for security
- **Content Length**: Be mindful of token limits in the OpenAI models when generating long content

## Deployment Options

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy your app
4. Add your API keys as secrets

### Docker

```bash
# Build the Docker image
docker build -t prosepilot-ai .

# Run the container
docker run -p 8501:8501 prosepilot-ai
```

## Troubleshooting

- **Authentication Errors**: Ensure your API keys have the correct permissions
- **Publication ID Issues**: Verify you're using the correct publication ID format
- **Content Generation Errors**: Check OpenAI API quota and token limits
- **Hashnode API Changes**: The Hashnode API may change over time; check for updates

## License

This project is available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

Created with ❤️ using Python, Streamlit, OpenAI, and Hashnode API.
