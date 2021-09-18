"""
Various utility functions
"""

from pathlib import Path


def get_repo_root():
    """
    Resolve the filepath of the repo root
    """

    return Path(__file__).parent.parent
