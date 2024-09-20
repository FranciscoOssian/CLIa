from utils import diagnose_error, send_to_clia
from utils import diagnose_error
import os
import platform
import subprocess
import re
import requests

def help_command():
    pass

def execute_command(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    if result.stderr == '':
        print('Errrr 🤓 working done, mean? this execution have no stderr content')
        return
    
    url = "http://localhost:8000/chat"
    payload = [
        {
            "role": "user",
            "parts": [{"text": result.stderr}]
        }
    ]
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.json()['response'])

def chat_command():
    print("Iniciando chat com Clia...")
    pass
