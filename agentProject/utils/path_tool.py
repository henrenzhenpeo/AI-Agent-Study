
"""
为整个工程提供统一的路径
"""
import os

def get_project_root() -> str:
    current_file = os.path.abspath(__file__)
