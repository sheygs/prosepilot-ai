"""Content writing knowledge base for RAG system"""

WRITING_GUIDELINES = {
    "Blog Post": {
        "structure": """
            1. Compelling headline with target keyword
            2. Engaging introduction (hook + preview)
            3. Main content with subheadings (H2, H3)
            4. Practical examples and actionable tips
            5. Strong conclusion with key takeaways
            6. Clear call-to-action
         """,

        "best_practices": [
            "Use conversational tone to connect with readers",
            "Include personal anecdotes and experiences",
            "Break up text with bullet points and lists",
            "Add relevant images and visual elements",
            "Keep paragraphs short (2-3 sentences max)",
            "Use active voice over passive voice",
            "Include statistics and data to support claims",
            "Write scannable content with clear headings"
        ],
        "seo_tips": [
            "Include target keyword in title and first paragraph",
            "Use keyword variations throughout content naturally",
            "Write meta description under 160 characters",
            "Add internal and external links",
            "Use long-tail keywords in subheadings",
            "Optimize for featured snippets with question formats",
            "Include related keywords and semantic variations"
        ],
        "hashnode_specific": [
            "Use markdown formatting effectively",
            "Add relevant tags (maximum 5)",
            "Include code blocks with syntax highlighting",
            "Use cover images for better engagement",
            "Write compelling subtitles",
            "Engage with the community through comments"
        ]
    },

    "Technical Article": {
        "structure": """
            1. Clear problem statement or technical challenge
            2. Background and context explanation
            3. Detailed solution with step-by-step approach
            4. Code examples and implementation details
            5. Testing and validation methods
            6. Troubleshooting common issues
            7. Conclusion with lessons learned
         """,
        "best_practices": [
            "Start with problem definition and scope",
            "Include working code examples",
            "Explain complex concepts with analogies",
            "Add diagrams and flowcharts where helpful",
            "Provide multiple solution approaches when possible",
            "Include performance considerations",
            "Add links to documentation and resources",
            "Test all code examples before publishing"
        ],
        "seo_tips": [
            "Use technical keywords naturally",
            "Include programming language in title",
            "Add code snippets with proper syntax highlighting",
            "Reference popular frameworks and tools",
            "Include version numbers for specificity",
            "Link to official documentation",
            "Use schema markup for technical content"
        ],
        "hashnode_specific": [
            "Use code blocks with language specification",
            "Include GitHub repository links",
            "Add technical tags relevant to the stack",
            "Use collapsible sections for long code",
            "Include demo links or live examples",
            "Engage with developer community"
        ]
    },

    "Tutorial": {
        "structure": """
            1. Tutorial overview and learning objectives
            2. Prerequisites and required tools
            3. Step-by-step instructions with screenshots
            4. Code examples with explanations
            5. Common errors and troubleshooting
            6. Next steps and advanced topics
            7. Resources for further learning
         """,
        "best_practices": [
            "Define clear learning objectives upfront",
            "List all prerequisites and assumptions",
            "Use numbered steps for easy following",
            "Include screenshots for visual guidance",
            "Provide downloadable resources",
            "Test tutorial with fresh environment",
            "Add difficulty level indication",
            "Include estimated time to complete"
        ],
        "seo_tips": [
            "Use 'how to' and 'tutorial' keywords",
            "Include skill level in title",
            "Add step numbers in subheadings",
            "Use action-oriented language",
            "Include tool and technology names",
            "Add FAQ section for common questions"
        ]
    },

    "Opinion Piece": {
        "structure": """
           1. Strong opening with clear stance
           2. Context and background information
           3. Supporting arguments with evidence
           4. Addressing counterarguments
           5. Personal insights and experiences
           6. Call for discussion or action
         """,
        "best_practices": [
            "Take a clear, defensible position",
            "Support opinions with facts and data",
            "Acknowledge opposing viewpoints",
            "Use persuasive but respectful language",
            "Include personal experiences as evidence",
            "Encourage reader engagement and discussion",
            "Stay focused on main argument"
        ],
        "seo_tips": [
            "Use opinion and perspective keywords",
            "Include trending topic keywords",
            "Add debate and discussion terms",
            "Use emotional and engaging language",
            "Include current events and timely references"
        ]
    }
}

TONE_GUIDELINES = {
    "Professional": {
        "characteristics": [
            "Formal language and proper grammar",
            "Objective and fact-based approach",
            "Industry-standard terminology",
            "Structured and logical flow",
            "Authoritative but not condescending"
        ],
        "avoid": [
            "Casual slang or colloquialisms",
            "Overly emotional language",
            "Personal anecdotes unless relevant",
            "Humor unless appropriate",
            "Controversial statements without basis"
        ]
    },

    "Casual": {
        "characteristics": [
            "Conversational and friendly tone",
            "Simple, everyday language",
            "Personal touches and experiences",
            "Light humor when appropriate",
            "Direct and approachable style"
        ],
        "avoid": [
            "Overly formal or stiff language",
            "Complex technical jargon",
            "Lengthy, complex sentences",
            "Pretentious vocabulary",
            "Cold, impersonal approach"
        ]
    },

    "Enthusiastic": {
        "characteristics": [
            "Energetic and positive language",
            "Exclamation points for emphasis",
            "Action-oriented vocabulary",
            "Encouraging and motivational",
            "Passionate about the subject"
        ],
        "avoid": [
            "Monotonous or flat delivery",
            "Negative or discouraging language",
            "Overly technical explanations",
            "Passive voice constructions",
            "Boring or dry presentations"
        ]
    },

    "Informative": {
        "characteristics": [
            "Clear and concise explanations",
            "Fact-based and educational",
            "Well-structured information",
            "Neutral and objective tone",
            "Focus on teaching and explaining"
        ],
        "avoid": [
            "Biased or subjective statements",
            "Emotional manipulation",
            "Unclear or confusing explanations",
            "Missing important details",
            "Assumptions about reader knowledge"
        ]
    },

    "Technical": {
        "characteristics": [
            "Precise technical terminology",
            "Detailed specifications and data",
            "Step-by-step methodical approach",
            "Reference to standards and documentation",
            "Focus on accuracy and completeness"
        ],
        "avoid": [
            "Vague or imprecise language",
            "Oversimplification of complex topics",
            "Missing technical details",
            "Informal explanations",
            "Unverified technical claims"
        ]
    }
}

CONTENT_EXAMPLES = {
    "Blog Post": [
        {
            "title": "5 Python Tips That Will Make You a Better Developer",
            "opening": "Python's simplicity often masks its powerful features. After 5 years of professional Python development, I've discovered techniques that transformed how I write code...",
            "structure_example": "Hook → Personal credibility → Promise of value → Specific tips with examples → Conclusion with action items"
        }
    ],
    "Technical Article": [
        {
            "title": "Building a RESTful API with FastAPI: A Complete Guide",
            "opening": "Modern web applications demand fast, reliable APIs. FastAPI has emerged as Python's premier framework for building high-performance APIs with automatic documentation...",
            "structure_example": "Problem statement → Solution introduction → Implementation walkthrough → Performance benefits → Real-world example"
        }
    ]
}


SEO_KEYWORDS = {
    "general": [
        "how to", "guide", "tutorial", "tips", "best practices",
        "complete guide", "step by step", "beginner", "advanced",
        "examples", "practical", "effective", "proven", "ultimate",
        "comprehensive", "detailed", "easy", "quick", "simple"
    ],
    "technical": [
        "implementation", "architecture", "framework", "library",
        "development", "programming", "coding", "software",
        "API", "database", "deployment", "testing", "debugging",
        "performance", "optimization", "security", "scalability"
    ],
    "content_creation": [
        "writing", "content", "blogging", "publishing", "SEO",
        "engagement", "audience", "traffic", "conversion",
        "content strategy", "content marketing", "copywriting",
        "storytelling", "content creation", "blog post"
    ],
    "business": [
        "strategy", "growth", "productivity", "efficiency",
        "management", "leadership", "innovation", "success",
        "entrepreneurship", "startup", "business development"
    ],
    "learning": [
        "learn", "master", "understand", "explain", "teach",
        "education", "training", "course", "lesson", "skill",
        "knowledge", "expertise", "fundamentals", "basics"
    ]
}
