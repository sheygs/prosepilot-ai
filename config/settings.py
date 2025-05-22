import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HASHNODE_API_KEY = os.getenv("HASHNODE_API_KEY", "")
HASHNODE_PUBLICATION_ID = os.getenv("HASHNODE_PUBLICATION_ID", "")

# API Endpoints
HASHNODE_GRAPHQL_URL = "https://gql.hashnode.com/"

# Content Generation Settings
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000
DEFAULT_TONE = "Professional"
DEFAULT_CONTENT_TYPE = "Blog Post"

# RAG Settings
RAG_ENABLED = True
RAG_MAX_CONTEXT_LENGTH = 2000
RAG_SIMILARITY_THRESHOLD = 0.7

# UI Settings
PAGE_TITLE = "ProsePilot AI"
PAGE_ICON = "📝"
LAYOUT = "wide"
