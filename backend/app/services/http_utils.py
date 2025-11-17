from typing import Dict
import requests
from flask import current_app

def send_json(url: str, data: Dict) -> Dict:
    """POSTリクエストを送り、JSONレスポンスを返す"""
    r = requests.post(url, data=data, timeout=current_app.config["REQUEST_TIMEOUT"])
    r.raise_for_status()
    return r.json()

def fetch_json(url: str, headers: Dict) -> Dict:
    """GETリクエストを送り、JSONレスポンスを返す"""
    r = requests.get(url, headers=headers, timeout=current_app.config["REQUEST_TIMEOUT"])
    r.raise_for_status()
    return r.json()