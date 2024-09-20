import logging
from typing import Any, Dict, List
from src.utils import valid_messages
from fastapi import FastAPI, HTTPException
from src.gemini import GeminiAPI
from src.custom_search import CustomSearchAPI
from src.web_extractor import WebExtractor
from src.utils import logger

app = FastAPI()

custom_search_api = CustomSearchAPI()
web_extractor = WebExtractor()

def message_of_search(md: str):
    return f""""
    (MESSAGE FROM SYSTEM : search response -> {md} <- search response);
    ACTION: Please update your answer only if seach's answer helps.
    Otherwise, just disregard it.
    remember conversation in the same language as the user
    """

@app.get("/test")
async def test():
    return {"message": "API is running!"}

@app.post("/chat")
async def chat(messages: List[Dict[str, Any]]):
    logger.debug("Incoming messages: %s", messages)
    try:
        if not valid_messages(messages):
            logger.error("Invalid messages: %s", messages)
            raise ValueError("Invalid or malformatted messages input.")

        logger.debug("Calling Gemini API with messages")
        gemini_api = GeminiAPI()
        gemini_response = gemini_api.generate_content(messages)
        logger.debug("Gemini response received: %s", gemini_response)
        
        response_text = gemini_response['response']
        search_tags: List[str] = gemini_response['search']
        
        if search_tags:
            logger.debug("Tags encontradas: %s", search_tags)
            query = '+'.join(search_tags)
            logger.debug("Query formada: %s", query)
            search_results = custom_search_api.search(query)
            if not search_results:
                logger.error("No search results for query: %s", query)
                return {"response": "No search results found."}
            
            links = [item['link'] for item in search_results]
            markdown_content = web_extractor.extract(links)
            markdown_content = markdown_content[2:]
            logger.debug("md c: %s", markdown_content)
            gemini_response = gemini_api.generate_content(
                [{"role": "user", "parts": [{"text": message_of_search(markdown_content)}]}]
            )
            response_text = gemini_response['response']

        return {"response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))