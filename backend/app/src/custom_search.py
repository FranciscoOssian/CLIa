from googleapiclient.discovery import build
import os

class CustomSearchAPI:
    def __init__(self):
        self.service = build("customsearch", "v1", developerKey=os.environ["CUSTOM_SEARCH_API_KEY"])
        self.cx = os.environ["CUSTOM_SEARCH_CX"]

    def search(self, query):
        response = self.service.cse().list(q=query, cx=self.cx).execute()
        return response.get("items", [])