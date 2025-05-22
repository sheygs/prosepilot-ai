"""RAG (Retrieval-Augmented Generation) system for ProsePilot AI"""

from typing import List, Dict, Any
from .content_knowledge import WRITING_GUIDELINES, TONE_GUIDELINES, CONTENT_EXAMPLES, SEO_KEYWORDS


class SimpleRAGSystem:
    """
    Simple RAG implementation using keyword matching and content relevance.
    Can be enhanced later with vector embeddings for more sophisticated retrieval.
    """

    def __init__(self):
        self.knowledge_base = self._build_knowledge_base()

    def _build_knowledge_base(self) -> Dict[str, Any]:
        """Build searchable knowledge base from content guidelines"""
        return {
            "writing_guidelines": WRITING_GUIDELINES,
            "tone_guidelines": TONE_GUIDELINES,
            "content_examples": CONTENT_EXAMPLES,
            "seo_keywords": SEO_KEYWORDS
        }

    def retrieve_content_guidelines(self, content_type: str, tone: str) -> Dict[str, Any]:
        """Retrieve specific guidelines for content type and tone"""
        guidelines = {}

        # Get content type specific guidelines
        if content_type in self.knowledge_base["writing_guidelines"]:
            guidelines["content_guidelines"] = self.knowledge_base["writing_guidelines"][content_type]

        # Get tone specific guidelines
        if tone in self.knowledge_base["tone_guidelines"]:
            guidelines["tone_guidelines"] = self.knowledge_base["tone_guidelines"][tone]

        # Get relevant examples
        if content_type in self.knowledge_base["content_examples"]:
            guidelines["examples"] = self.knowledge_base["content_examples"][content_type]

        return guidelines

    # deprecated
    def retrieve_seo_keywords_(self, content_type: str, topic: str) -> List[str]:
        """Retrieve relevant SEO keywords based on content type and topic"""
        keywords = []

        # Add general keywords
        keywords.extend(self.knowledge_base["seo_keywords"]["general"])

        # Add technical keywords if applicable
        if content_type.lower() in ["technical article", "tutorial"]:
            keywords.extend(self.knowledge_base["seo_keywords"]["technical"])

        # Add content creation keywords for blog posts
        if content_type.lower() == "blog post":
            keywords.extend(
                self.knowledge_base["seo_keywords"]["content_creation"])

        return keywords[:10]  # Return top 10 relevant keywords

    # updated method
    def retrieve_seo_keywords(self, content_type: str, topic: str) -> List[str]:
        """Retrieve relevant SEO keywords based on content type and topic"""
        keywords = []

        # Add general keywords
        keywords.extend(self.knowledge_base["seo_keywords"]["general"])

        # Add technical keywords if applicable
        if content_type.lower() in ["technical article", "tutorial"]:
            keywords.extend(self.knowledge_base["seo_keywords"]["technical"])

        # Add content creation keywords for blog posts
        if content_type.lower() == "blog post":
            keywords.extend(
                self.knowledge_base["seo_keywords"]["content_creation"])

        # Topic-specific keyword enhancement
        topic_keywords = self._extract_topic_keywords(topic.lower())
        keywords.extend(topic_keywords)

        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for keyword in keywords:
            if keyword not in seen:
                seen.add(keyword)
                unique_keywords.append(keyword)

        return unique_keywords[:15]  # Return top 15 relevant keywords

    def _extract_topic_keywords(self, topic: str) -> List[str]:
        """Extract and suggest keywords based on the topic content"""
        topic_keywords = []

        # Technology-related keywords
        tech_terms = {
            'python': ['python programming', 'python development', 'python tutorial', 'python guide'],
            'javascript': ['javascript', 'js', 'web development', 'frontend'],
            'react': ['react js', 'react development', 'react tutorial', 'react guide'],
            'ai': ['artificial intelligence', 'machine learning', 'AI development', 'ML'],
            'web': ['web development', 'website', 'web design', 'frontend', 'backend'],
            'api': ['API development', 'REST API', 'GraphQL', 'web services'],
            'database': ['database design', 'SQL', 'NoSQL', 'data management'],
            'cloud': ['cloud computing', 'AWS', 'Azure', 'cloud deployment'],
            'mobile': ['mobile development', 'app development', 'iOS', 'Android'],
            'data': ['data science', 'data analysis', 'big data', 'analytics']
        }

        # Business and productivity keywords
        business_terms = {
            'productivity': ['productivity tips', 'efficiency', 'workflow', 'time management'],
            'marketing': ['digital marketing', 'content marketing', 'SEO', 'social media'],
            'business': ['business strategy', 'entrepreneurship', 'startup', 'growth'],
            'design': ['UI design', 'UX design', 'graphic design', 'design principles'],
            'project': ['project management', 'agile', 'scrum', 'team collaboration'],
            'career': ['career development', 'professional growth', 'job search', 'skills']
        }

        # Content and writing keywords
        content_terms = {
            'writing': ['content writing', 'copywriting', 'blog writing', 'technical writing'],
            'seo': ['SEO optimization', 'search engine optimization', 'keyword research'],
            'content': ['content creation', 'content strategy', 'content marketing'],
            'blog': ['blogging', 'blog post', 'blogger', 'blog strategy'],
            'social': ['social media', 'social media marketing', 'engagement', 'audience']
        }

        # Combine all term dictionaries
        all_terms = {**tech_terms, **business_terms, **content_terms}

        # Check topic against known terms
        for key, keywords in all_terms.items():
            if key in topic:
                topic_keywords.extend(keywords)

        # Extract important words from the topic itself
        topic_words = topic.split()
        for word in topic_words:
            if len(word) > 3:  # Only include meaningful words
                topic_keywords.append(word)
                topic_keywords.append(f"{word} guide")
                topic_keywords.append(f"{word} tutorial")
                topic_keywords.append(f"how to {word}")

        return topic_keywords[:10]  # Limit topic-specific keywords

    def retrieve_hashnode_optimization(self, content_type: str) -> List[str]:
        """Retrieve Hashnode-specific optimization tips"""
        guidelines = self.knowledge_base["writing_guidelines"].get(
            content_type, {})
        return guidelines.get("hashnode_specific", [])

    # deprecated
    def build_context_prompt_(self, content_type: str, tone: str, topic: str) -> str:
        """Build enhanced context for content generation"""
        guidelines = self.retrieve_content_guidelines(content_type, tone)
        seo_keywords = self.retrieve_seo_keywords(content_type, topic)
        hashnode_tips = self.retrieve_hashnode_optimization(content_type)

        context_parts = []

        # Add content structure
        if "content_guidelines" in guidelines and "structure" in guidelines["content_guidelines"]:
            context_parts.append(
                f"STRUCTURE:\n{guidelines['content_guidelines']['structure']}")

        # Add best practices
        if "content_guidelines" in guidelines and "best_practices" in guidelines["content_guidelines"]:
            practices = "\n".join(
                [f"- {practice}" for practice in guidelines["content_guidelines"]["best_practices"]])
            context_parts.append(f"BEST PRACTICES:\n{practices}")

        # Add tone guidelines
        if "tone_guidelines" in guidelines:
            tone_chars = "\n".join(
                [f"- {char}" for char in guidelines["tone_guidelines"]["characteristics"]])
            context_parts.append(f"TONE CHARACTERISTICS:\n{tone_chars}")

            tone_avoid = "\n".join(
                [f"- {avoid}" for avoid in guidelines["tone_guidelines"]["avoid"]])
            context_parts.append(f"AVOID:\n{tone_avoid}")

        # Add SEO guidelines
        if "content_guidelines" in guidelines and "seo_tips" in guidelines["content_guidelines"]:
            seo_tips = "\n".join(
                [f"- {tip}" for tip in guidelines["content_guidelines"]["seo_tips"]])
            context_parts.append(f"SEO OPTIMIZATION:\n{seo_tips}")

        # Add Hashnode-specific tips
        if hashnode_tips:
            hashnode_formatted = "\n".join(
                [f"- {tip}" for tip in hashnode_tips])
            context_parts.append(
                f"HASHNODE OPTIMIZATION:\n{hashnode_formatted}")

        # Add relevant keywords
        if seo_keywords:
            keyword_list = ", ".join(seo_keywords)
            context_parts.append(f"RELEVANT KEYWORDS: {keyword_list}")

        return "\n\n".join(context_parts)

    # updated build_context_prompt method
    def build_context_prompt(self, content_type: str, tone: str, topic: str) -> str:
        """Build enhanced context for content generation"""
        guidelines = self.retrieve_content_guidelines(content_type, tone)
        seo_keywords = self.retrieve_seo_keywords(
            content_type, topic)  # Now properly uses topic
        hashnode_tips = self.retrieve_hashnode_optimization(content_type)

        context_parts = []

        # Add content structure
        if "content_guidelines" in guidelines and "structure" in guidelines["content_guidelines"]:
            context_parts.append(
                f"STRUCTURE:\n{guidelines['content_guidelines']['structure']}")

        # Add best practices
        if "content_guidelines" in guidelines and "best_practices" in guidelines["content_guidelines"]:
            practices = "\n".join(
                [f"- {practice}" for practice in guidelines["content_guidelines"]["best_practices"]])
            context_parts.append(f"BEST PRACTICES:\n{practices}")

        # Add tone guidelines
        if "tone_guidelines" in guidelines:
            tone_chars = "\n".join(
                [f"- {char}" for char in guidelines["tone_guidelines"]["characteristics"]])
            context_parts.append(f"TONE CHARACTERISTICS:\n{tone_chars}")

            tone_avoid = "\n".join(
                [f"- {avoid}" for avoid in guidelines["tone_guidelines"]["avoid"]])
            context_parts.append(f"AVOID:\n{tone_avoid}")

        # Add SEO guidelines
        if "content_guidelines" in guidelines and "seo_tips" in guidelines["content_guidelines"]:
            seo_tips = "\n".join(
                [f"- {tip}" for tip in guidelines["content_guidelines"]["seo_tips"]])
            context_parts.append(f"SEO OPTIMIZATION:\n{seo_tips}")

        # Add Hashnode-specific tips
        if hashnode_tips:
            hashnode_formatted = "\n".join(
                [f"- {tip}" for tip in hashnode_tips])
            context_parts.append(
                f"HASHNODE OPTIMIZATION:\n{hashnode_formatted}")

        # Add relevant keywords (now topic-aware)
        if seo_keywords:
            keyword_list = ", ".join(seo_keywords)
            context_parts.append(
                f"RELEVANT KEYWORDS (incorporate naturally): {keyword_list}")

        # Add topic-specific guidance
        topic_guidance = self._get_topic_specific_guidance(topic, content_type)
        if topic_guidance:
            context_parts.append(f"TOPIC-SPECIFIC GUIDANCE:\n{topic_guidance}")

        return "\n\n".join(context_parts)

    def _get_topic_specific_guidance(self, topic: str, content_type: str) -> str:
        """Provide topic-specific writing guidance"""
        guidance_parts = []

        # Technology topics
        if any(tech in topic.lower() for tech in ['python', 'javascript', 'react', 'api', 'programming', 'code']):
            guidance_parts.append(
                "- Include practical code examples and explanations")
            guidance_parts.append(
                "- Reference official documentation and best practices")
            guidance_parts.append(
                "- Consider different skill levels of readers")
            guidance_parts.append(
                "- Mention version compatibility and requirements")

        # Business/productivity topics
        if any(biz in topic.lower() for biz in ['productivity', 'business', 'marketing', 'strategy']):
            guidance_parts.append(
                "- Include actionable strategies and frameworks")
            guidance_parts.append(
                "- Use data and statistics to support points")
            guidance_parts.append(
                "- Provide real-world examples and case studies")
            guidance_parts.append("- Focus on measurable outcomes and ROI")

        # Tutorial/educational topics
        if content_type.lower() in ['tutorial', 'guide'] or 'how to' in topic.lower():
            guidance_parts.append(
                "- Break down complex processes into simple steps")
            guidance_parts.append("- Include prerequisites and required tools")
            guidance_parts.append(
                "- Add troubleshooting tips for common issues")
            guidance_parts.append("- Provide next steps for further learning")

        return "\n".join(guidance_parts) if guidance_parts else ""
