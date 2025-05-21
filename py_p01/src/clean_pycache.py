#!/usr/bin/env python3
"""
clean_pycache.py

This script recursively deletes all __pycache__ and .pytest_cache directories in the current project.
"""

import os
import shutil

def remove_pycache_dirs(path):
    """
    Recursively searches for and deletes __pycache__ directories starting from the given path.
    
    Parameters:
        path (str): The root directory to start the search.
    """
    for root, dirs, files in os.walk(path):
        if "__pycache__" in dirs:
            dir_to_remove = os.path.join(root, "__pycache__")
            print(f"Removing: {dir_to_remove}")
            shutil.rmtree(dir_to_remove)
            # Remove the folder from dirs list to prevent os.walk from searching it again.
            dirs.remove("__pycache__")

            
    for root, dirs, files in os.walk(path):
        if ".pytest_cache" in dirs:
            dir_to_remove = os.path.join(root, ".pytest_cache")
            print(f"Removing: {dir_to_remove}")
            shutil.rmtree(dir_to_remove)
            dirs.remove(".pytest_cache")

if __name__ == "__main__":
    remove_pycache_dirs(".")
