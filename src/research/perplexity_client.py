"""Perplexity API client for research and generation."""

import json
import time
from typing import Any, Dict

import requests

from src.config.settings import Settings
from src.utils.logger import get_logger


class PerplexityClient:
    """Client for interacting with Perplexity API.
    
    Provides methods for search and chat completion with retry logic.
    """

    # Perplexity API endpoints
    SEARCH_API_URL = "https://api.perplexity.ai/search"
    CHAT_API_URL = "https://api.perplexity.ai/chat/completions"

    def __init__(self, settings: Settings):
        """Initialize the Perplexity client.
        
        Args:
            settings: Application settings containing API key and retry config
        """
        self.settings = settings
        self.api_key = settings.perplexity_api_key
        self.max_retries = settings.max_llm_retries
        self.backoff_base = settings.llm_backoff_base
        self.timeout = settings.http_timeout_seconds
        self.logger = get_logger()

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with API key."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def search(self, query: str, max_results: int = 7) -> Dict[str, Any]:
        """Perform a standalone search using Perplexity API.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary containing search results with sources
            
        Raises:
            requests.exceptions.RequestException: If all retries fail
        """
        payload = {
            "query": query,
            "max_results": max_results
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(
                    f"Perplexity search attempt {attempt}/{self.max_retries}: "
                    f"query='{query[:50]}...'"
                )

                response = requests.post(
                    self.SEARCH_API_URL,
                    headers=self._get_headers(),
                    json=payload,
                    timeout=self.timeout
                )

                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    self.logger.warning(
                        f"Rate limited. Waiting {retry_after}s before retry"
                    )
                    time.sleep(retry_after)
                    continue

                response.raise_for_status()
                result = response.json()
                
                self.logger.info(
                    f"Search successful: found {len(result.get('results', []))} results"
                )
                return result

            except requests.exceptions.Timeout:
                self.logger.warning(
                    f"Search timeout on attempt {attempt}/{self.max_retries}"
                )
                if attempt == self.max_retries:
                    raise
                time.sleep(self.backoff_base ** attempt)

            except requests.exceptions.RequestException as e:
                self.logger.error(
                    f"Search error on attempt {attempt}/{self.max_retries}: {e}"
                )
                if attempt == self.max_retries:
                    raise
                time.sleep(self.backoff_base ** attempt)

        raise RuntimeError(f"Search failed after {self.max_retries} attempts")

    def chat_json(
        self, prompt: str, model: str = "sonar", temperature: float = 0.2
    ) -> str:
        """Call Perplexity chat completion expecting JSON response.
        
        Args:
            prompt: The prompt to send
            model: Model to use (sonar, sonar-pro, etc.)
            temperature: Temperature for generation (0.0-1.0)
            
        Returns:
            JSON string from the model's response content
            
        Raises:
            requests.exceptions.RequestException: If all retries fail
            json.JSONDecodeError: If response is not valid JSON
        """
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that always responds with valid JSON only. Never include explanations outside the JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "max_tokens": 4096
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.info(
                    f"Perplexity chat attempt {attempt}/{self.max_retries}: "
                    f"model={model}, prompt_len={len(prompt)}"
                )

                response = requests.post(
                    self.CHAT_API_URL,
                    headers=self._get_headers(),
                    json=payload,
                    timeout=self.timeout
                )

                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    self.logger.warning(
                        f"Rate limited. Waiting {retry_after}s before retry"
                    )
                    time.sleep(retry_after)
                    continue

                response.raise_for_status()
                result = response.json()
                
                # Extract content from response
                content = result["choices"][0]["message"]["content"]
                
                # Validate it's proper JSON
                json.loads(content)  # This will raise JSONDecodeError if invalid
                
                self.logger.info("Chat completion successful, valid JSON returned")
                return content

            except requests.exceptions.Timeout:
                self.logger.warning(
                    f"Chat timeout on attempt {attempt}/{self.max_retries}"
                )
                if attempt == self.max_retries:
                    raise
                time.sleep(self.backoff_base ** attempt)

            except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
                self.logger.error(
                    f"Chat error on attempt {attempt}/{self.max_retries}: {e}"
                )
                if attempt == self.max_retries:
                    raise
                time.sleep(self.backoff_base ** attempt)

        raise RuntimeError(f"Chat completion failed after {self.max_retries} attempts")
