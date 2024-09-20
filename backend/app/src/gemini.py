from typing import Any, Dict, List, TypedDict
from src.prompt import prompt
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import os
import json
from src.utils import logger

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 3000,
    "response_schema": content.Schema(
        type=content.Type.OBJECT,
        enum=[],
        required=["response"],
        properties={
            "response": content.Schema(
                type=content.Type.STRING,
            ),
            "search": content.Schema(
                type=content.Type.ARRAY,
                items=content.Schema(
                    type=content.Type.STRING,
                ),
            ),
        },
    ),
    "response_mime_type": "application/json",
}

class GeminiAPI:
    def __init__(self):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-exp-0827",
            generation_config=generation_config
        )
        self.history = [{
            'role': 'user',
            'parts': [{'text': prompt}]
        }]
    
    def add_to_history(self, messages):
        self.history.extend(messages)
    
    def generate_content(self, messages: List[Dict[str, Any]]):  
        self.history.extend(messages)
        try:
            chat_session = self.model.start_chat(history=self.history)
            response = chat_session.send_message(self.history[-1])
            logger.debug("Response: %s", json.loads(response.text))
            return json.loads(response.text)
        except Exception as e:
            logger.error("Error in generate_content: %s", str(e))
            raise RuntimeError(f"An error occurred during content generation: {str(e)}")
