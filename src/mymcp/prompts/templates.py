"""
Prompt templates.
"""


def register_prompts(mcp):
    """Register prompt templates with the MCP server."""
    
    @mcp.prompt
    def summarize_text(text: str) -> str:
        """Generate a prompt asking the LLM to summarize text.
        
        Args:
            text: The text to summarize
        """
        return f"""Please provide a concise summary of the following text:

{text}

Summary:"""

    @mcp.prompt
    def code_review(code: str, language: str = "python") -> str:
        """Generate a prompt for code review.
        
        Args:
            code: The code to review
            language: Programming language of the code
        """
        return f"""Please review the following {language} code and provide feedback on:
1. Code quality and best practices
2. Potential bugs or issues
3. Suggestions for improvement

Code:
```{language}
{code}
```

Review:"""
