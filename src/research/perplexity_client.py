"""Perplexity API client for deep research."""

import requests
from typing import Dict, List, Optional
from loguru import logger
from utils.helpers import retry_with_backoff


class PerplexityClient:
    """Client for interacting with Perplexity API."""
    
    def __init__(self, api_key: str, model: str = "llama-3.1-sonar-large-128k-online"):
        """
        Initialize Perplexity client.
        
        Args:
            api_key: Perplexity API key
            model: Model to use for research
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    @retry_with_backoff(max_retries=3, initial_delay=5)
    def search(
        self,
        query: str,
        max_tokens: int = 4000,
        temperature: float = 0.2,
        return_citations: bool = True
    ) -> Dict:
        """
        Perform a search using Perplexity API.
        
        Args:
            query: Search query
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            return_citations: Whether to return citations
        
        Returns:
            API response dictionary
        """
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a thorough research assistant. Provide comprehensive, well-cited information."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "return_citations": return_citations,
            "return_images": False
        }
        
        logger.info(f"Searching Perplexity API with query: {query[:100]}...")
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Perplexity search successful, received {len(result.get('choices', []))} results")
            
            return result
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Perplexity API request failed: {str(e)}")
            raise
    
    def extract_content(self, response: Dict) -> str:
        """
        Extract content from Perplexity API response.
        
        Args:
            response: API response dictionary
        
        Returns:
            Extracted content text
        """
        try:
            if "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"]
            return ""
        except (KeyError, IndexError) as e:
            logger.warning(f"Failed to extract content from response: {str(e)}")
            return ""
    
    def extract_citations(self, response: Dict) -> List[str]:
        """
        Extract citations from Perplexity API response.
        
        Args:
            response: API response dictionary
        
        Returns:
            List of citation URLs
        """
        try:
            citations = response.get("citations", [])
            return citations if isinstance(citations, list) else []
        except Exception as e:
            logger.warning(f"Failed to extract citations: {str(e)}")
            return []
