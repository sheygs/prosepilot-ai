# ProsePilot AI

## Overview

ProsePilot AI Agent is a full-stack AI content generation tool built with Python and Streamlit. This application allows you to quickly generate high-quality content such as blog posts, social media posts, product descriptions, and emails using OpenAI's powerful language models.

## Features

- **Multiple Content Types**: Generate blog posts, social media posts, product descriptions, emails, or custom content
- **Tone Selection**: Choose from various tones like Professional, Casual, Enthusiastic, etc.
- **Model Selection**: Choose between different OpenAI models
- **Adjustable Parameters**: Control temperature and maximum word count
- **Content Export**: Download generated content as TXT or MD files
- **Conversation History**: Keep track of all your generated content

## Setup Instructions

### 1. Prerequisites

- Python >=3.7
- [OpenAI API key](https://openai.com/api/)
- Git

### 2. Installation

1. Create a new directory for your project and navigate to it:

```bash
mkdir prosepilot-ai
cd prosepilot-ai
```

2. Create a virtual environment and activate it:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Create a file named `requirements.txt` with these dependencies:

```
streamlit>=1.22.0
openai>=0.27.0
python-dotenv>=1.0.0
```

4. Install the dependencies:

```bash
pip3 install -r requirements.txt
```

5. Create a file named `app.py` and paste the entire code from the provided application.

6. (Optional) Create a `.env` file to store your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

### 3. Running the Application Locally

1. Make sure your virtual environment is activated.

2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. Your web browser should automatically open with the app running at `http://localhost:8501`.

## Deployment Instructions

### Option 1: Deploy to Streamlit Cloud

1. Create a GitHub repository and push your code:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/prosepilot-ai.git
git push -u origin main
```

2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in.

3. Click "New app" and select your GitHub repository, branch, and the main file path (`app.py`).

4. Add your OpenAI API key as a secret in the Streamlit Cloud dashboard:

   - Go to "Advanced settings" > "Secrets"
   - Add your API key in this format:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. Deploy your app. Streamlit Cloud will automatically build and deploy it.

### Option 2: Deploy with Docker

1. Create a `Dockerfile` in your project directory:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Build the Docker image:

```bash
docker build -t prosepilot-ai .
```

3. Run the container:

```bash
docker run -p 8501:8501 -e OPENAI_API_KEY=your_api_key_here prosepilot-ai
```

4. Access your app at `http://localhost:8501`.

### Option 3: Deploy on AWS, Google Cloud, or Azure

For more scalable and production-ready deployments, you can use cloud platforms:

1. **AWS Elastic Beanstalk**:

   - Install the EB CLI and initialize your application
   - Create a `requirements.txt` file and include `streamlit` and other dependencies
   - Configure environment variables for the API key
   - Deploy with `eb deploy`

2. **Google Cloud Run**:

   - Use the Docker deployment approach
   - Push the Docker image to Google Container Registry
   - Deploy using Google Cloud Run with the appropriate environment variables

3. **Azure App Service**:
   - Create an App Service with Python support
   - Set up deployment from GitHub or use Azure DevOps
   - Configure environment variables for your API key

## Usage

1. Enter your OpenAI API key in the sidebar (or set it in the `.env` file).
2. Select the content type you want to generate.
3. Choose the AI model and adjust the temperature.
4. Enter your prompt describing what content you want.
5. Select the tone and maximum word count.
6. Click "Generate Content" to create your content.
7. Use the buttons to copy or download your generated content.
8. View your conversation history in the expandable section.

## Security Considerations

- Do not hardcode your OpenAI API key in your code
- Use environment variables for sensitive information
- Consider implementing user authentication for multi-user deployments
- Store conversation history securely if implementing persistence

## Troubleshooting

1. **API Key Issues**: If you encounter errors related to the API key, make sure:

   - Your API key is valid
   - You have sufficient credits in your OpenAI account
   - You have proper permissions for the models you're trying to use

2. **OpenAI Client Version**: If you receive errors about function calls or parameters, ensure you're using the right OpenAI client version.

3. **Model Availability**: Not all OpenAI models may be available to your account.

4. **Streamlit Deployment Issues**:
   - Check if your dependencies are correctly specified
   - Verify that your environmental variables are properly set
   - Examine deployment logs for specific error messages

## Next Steps and Improvements

1. Add user authentication for multiple users
2. Implement content templates
3. Add more advanced customization options
4. Integrate with storage solutions
5. Add content revision capabilities
6. Implement content scheduling
7. Add SEO optimization features

## License

This project is available under the MIT License.
