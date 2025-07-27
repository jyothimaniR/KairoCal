"""
KairoCal NLP Package
Natural Language Processing for intelligent event creation
"""

from .entities import ExtractedEvent, NLPResponse, IntentType
from .text_processor import TextProcessor
from .pattern_matcher import PatternMatcher

__all__ = [
    "ExtractedEvent",
    "NLPResponse", 
    "IntentType",
    "TextProcessor",
    "PatternMatcher"
]

__version__ = "1.0.0"