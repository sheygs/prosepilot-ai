from typing import Any, Dict
import openai
import streamlit as st
from config.settings import OPENAI_API_KEY
from knowledge.rag_system import SimpleRAGSystem


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


class EnhancedOpenAIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or OPENAI_API_KEY
        self.rag_system = SimpleRAGSystem()

    def generate_content(self, prompt, content_type, tone, max_length, model, temperature):
        """generate content using RAG-enhanced prompting"""
        if not self.api_key:
            return "please enter your OpenAI API key in the sidebar."

        try:
            openai.api_key = self.api_key

            # get RAG context
            rag_context = self.rag_system.build_context_prompt(
                content_type, tone, prompt)

            # build enhanced system message with RAG context
            enhanced_system_message = f"""
                You are an expert content creator with access to professional writing guidelines.

                WRITING GUIDELINES AND CONTEXT:
                {rag_context}

                TASK: Create a {content_type} with a {tone.lower()} tone about: {prompt}

                REQUIREMENTS:
                - Keep the content under {max_length} words
                - Format the content in Markdown
                - Follow the structure and best practices provided above
                - Incorporate SEO optimization naturally
                - Ensure the tone matches the specified characteristics
                - Make it engaging and valuable for readers
                - Optimize for Hashnode platform

                Focus on creating high-quality, professional content that follows industry best practices.

                Remember: This is a TEXT-ONLY content generation. No images, no image sources, no visual references.
            """

            full_prompt = f"Create a {content_type} about: {prompt}"

            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": enhanced_system_message},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=temperature,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating content: {str(e)}"

    # deprecated
    def get_content_analysis_(self, content: str, content_type: str) -> Dict[str, Any]:
        """analyze generated content against RAG guidelines"""
        guidelines = self.rag_system.retrieve_content_guidelines(
            content_type, "Professional")

        analysis = {
            "word_count": len(content.split()),
            "has_structure": self._check_structure(content, content_type),
            "seo_optimized": self._check_seo_elements(content),
            "tone_appropriate": True,  # simplified check
            "hashnode_ready": self._check_hashnode_formatting(content)
        }

        return analysis

    #  (Updated get_content_analysis method)
    def get_content_analysis(self, content: str, content_type: str) -> Dict[str, Any]:
        """Analyze generated content against RAG guidelines"""
        guidelines = self.rag_system.retrieve_content_guidelines(
            content_type, "Professional")

        # Perform comprehensive analysis
        structure_analysis = self._analyze_structure(content, content_type)
        seo_analysis = self._analyze_seo_elements(content)
        readability_analysis = self._analyze_readability(content)

        analysis = {
            "word_count": len(content.split()),
            "character_count": len(content),
            "structure_score": structure_analysis["score"],
            "structure_details": structure_analysis["details"],
            "seo_score": seo_analysis["score"],
            "seo_details": seo_analysis["details"],
            "readability_score": readability_analysis["score"],
            "readability_details": readability_analysis["details"],
            "hashnode_ready": self._check_hashnode_formatting(content),
            "overall_quality": self._calculate_overall_quality(structure_analysis, seo_analysis, readability_analysis)
        }

        return analysis

    def _analyze_structure(self, content: str, content_type: str) -> Dict[str, Any]:
        """Detailed structure analysis"""
        headers = content.count('#')
        lines = content.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]

        structure_checks = {
            'Blog Post': self._check_blog_post_structure(content, headers, non_empty_lines),
            'Technical Article': self._check_technical_article_structure(content, headers, non_empty_lines),
            'Tutorial': self._check_tutorial_structure(content, headers, non_empty_lines),
            'Opinion Piece': self._check_opinion_piece_structure(content, headers, non_empty_lines)
        }

        # Get the check result for this content type
        structure_pass = structure_checks.get(
            content_type, self._check_default_structure(content, headers, non_empty_lines))

        return {
            "score": 85 if structure_pass else 60,
            "details": {
                "has_proper_headers": headers >= 2,
                "appropriate_length": len(non_empty_lines) >= 8,
                "content_type_structure": structure_pass,
                "header_count": headers,
                "paragraph_count": len(non_empty_lines)
            }
        }

    def _analyze_seo_elements(self, content: str) -> Dict[str, Any]:
        """Analyze SEO optimization elements"""
        seo_checks = {
            "has_headers": '#' in content,
            "has_links": '[' in content and ']' in content,
            "has_bold_text": '**' in content,
            "has_lists": any(marker in content for marker in ['-', '*', '1.', '2.']),
            "good_length": 300 <= len(content.split()) <= 2000,
            "has_code_blocks": '```' in content
        }

        score = (sum(seo_checks.values()) / len(seo_checks)) * 100

        return {
            "score": int(score),
            "details": seo_checks
        }

    def _analyze_readability(self, content: str) -> Dict[str, Any]:
        """Analyze content readability"""
        words = content.split()
        sentences = content.count(
            '.') + content.count('!') + content.count('?')

        if sentences == 0:
            sentences = 1  # Avoid division by zero

        avg_words_per_sentence = len(words) / sentences

        readability_checks = {
            "appropriate_sentence_length": 10 <= avg_words_per_sentence <= 20,
            "has_short_paragraphs": True,  # Simplified check
            "uses_active_voice": True,  # Simplified check
            "good_word_choice": True  # Simplified check
        }

        score = (sum(readability_checks.values()) /
                 len(readability_checks)) * 100

        return {
            "score": int(score),
            "details": {
                **readability_checks,
                "avg_words_per_sentence": round(avg_words_per_sentence, 1),
                "total_sentences": sentences
            }
        }

    def _calculate_overall_quality(self, structure_analysis: Dict, seo_analysis: Dict, readability_analysis: Dict) -> int:
        """Calculate overall content quality score"""
        weights = {
            "structure": 0.4,
            "seo": 0.3,
            "readability": 0.3
        }

        overall_score = (
            structure_analysis["score"] * weights["structure"] +
            seo_analysis["score"] * weights["seo"] +
            readability_analysis["score"] * weights["readability"]
        )

        return int(overall_score)

    # deprecated
    def _check_structure_(self, content: str, content_type: str) -> bool:
        """check if content follows recommended structure"""
        # simplified structure check - count headers
        headers = content.count('#')
        return headers >= 3  # Basic structure check

    # api/openai_client.py (Updated _check_structure method)

    def _check_structure(self, content: str, content_type: str) -> bool:
        """Check if content follows recommended structure for the specific content type"""

        # Count headers and sections
        headers = content.count('#')
        lines = content.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]

        # Content type specific structure checks
        if content_type.lower() == "blog post":
            return self._check_blog_post_structure(content, headers, non_empty_lines)

        elif content_type.lower() == "technical article":
            return self._check_technical_article_structure(content, headers, non_empty_lines)

        elif content_type.lower() == "tutorial":
            return self._check_tutorial_structure(content, headers, non_empty_lines)

        elif content_type.lower() == "opinion piece":
            return self._check_opinion_piece_structure(content, headers, non_empty_lines)

        else:
            # Default structure check for custom content types
            return self._check_default_structure(content, headers, non_empty_lines)

    def _check_blog_post_structure(self, content: str, headers: int, lines: list) -> bool:
        """Check blog post specific structure"""
        checks = {
            'has_title': headers >= 1,  # At least one main title
            'has_sections': headers >= 3,  # Multiple sections
            'good_length': len(lines) >= 10,  # Reasonable content length
            'has_conclusion': any('conclusion' in line.lower() or 'summary' in line.lower()
                                  for line in lines[-5:]),  # Check last 5 lines for conclusion
            # Has some introductory content
            'has_introduction': len(lines) >= 3
        }

        # Blog post passes if it meets most criteria
        return sum(checks.values()) >= 3

    def _check_technical_article_structure(self, content: str, headers: int, lines: list) -> bool:
        """Check technical article specific structure"""
        checks = {
            'has_sections': headers >= 4,  # Technical articles need more sections
            'has_code_blocks': '```' in content,  # Should have code examples
            'has_problem_statement': any(keyword in content.lower()
                                         for keyword in ['problem', 'challenge', 'issue', 'solution']),
            'has_implementation': any(keyword in content.lower()
                                      for keyword in ['implementation', 'code', 'example', 'setup']),
            # Technical content is usually longer
            'good_technical_length': len(lines) >= 15,
            # Links or references
            'has_references': '[' in content and ']' in content
        }

        return sum(checks.values()) >= 4

    def _check_tutorial_structure(self, content: str, headers: int, lines: list) -> bool:
        """Check tutorial specific structure"""
        checks = {
            'has_steps': headers >= 3,  # Multiple steps/sections
            'has_numbered_items': any(line.strip().startswith(('1.', '2.', '3.'))
                                      for line in lines),  # Numbered steps
            'has_prerequisites': any(keyword in content.lower()
                                     for keyword in ['prerequisite', 'requirement', 'need', 'install']),
            'has_examples': '```' in content or 'example' in content.lower(),
            'step_by_step': any(keyword in content.lower()
                                for keyword in ['step', 'first', 'next', 'then', 'finally']),
            'has_outcome': any(keyword in content.lower()
                               for keyword in ['result', 'output', 'complete', 'finish'])
        }

        return sum(checks.values()) >= 4

    def _check_opinion_piece_structure(self, content: str, headers: int, lines: list) -> bool:
        """Check opinion piece specific structure"""
        checks = {
            'has_clear_position': any(keyword in content.lower()
                                      for keyword in ['believe', 'think', 'opinion', 'argue', 'position']),
            'has_supporting_evidence': any(keyword in content.lower()
                                           for keyword in ['because', 'evidence', 'research', 'study', 'data']),
            'addresses_counterarguments': any(keyword in content.lower()
                                              for keyword in ['however', 'although', 'critics', 'opposing', 'counter']),
            'has_personal_insight': any(keyword in content.lower()
                                        for keyword in ['experience', 'personally', 'i have', 'my']),
            'has_call_to_action': any(keyword in content.lower()
                                      for keyword in ['should', 'must', 'need to', 'call', 'action']),
            'reasonable_structure': headers >= 2
        }

        return sum(checks.values()) >= 4

    def _check_default_structure(self, content: str, headers: int, lines: list) -> bool:
        """Default structure check for custom content types"""
        checks = {
            'has_headers': headers >= 2,
            'reasonable_length': len(lines) >= 8,
            'has_paragraphs': len([line for line in lines if not line.startswith('#') and len(line) > 50]) >= 3,
            'good_formatting': any(marker in content for marker in ['**', '*', '-', '1.']),
        }

        return sum(checks.values()) >= 3

    def _check_seo_elements(self, content: str) -> bool:
        """check for basic SEO elements"""
        # Check for headers, links, etc.
        has_headers = '#' in content
        has_links = '[' in content and ']' in content
        return has_headers or has_links

    def _check_hashnode_formatting(self, content: str) -> bool:
        """check if content is properly formatted for Hashnode"""
        # Check for markdown formatting
        markdown_elements = ['#', '```', '**', '*', '-', '1.']
        return any(element in content for element in markdown_elements)


# For backward compatibility
OpenAIClient = EnhancedOpenAIClient
