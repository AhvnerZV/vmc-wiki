"""
build_wiki.py
Entry point. Run this to compile all player files into wiki_data.json.

Usage:
    python build_wiki.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from src.wiki.build import build

if __name__ == "__main__":
    build()
