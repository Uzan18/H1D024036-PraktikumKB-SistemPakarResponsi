import sys
import os

# Menambahkan root directory ke sistem path agar bisa mengimport app.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
