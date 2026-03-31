"""
Self-Evolution - Self-Improving AI Agent Engine

A comprehensive self-evolution system for AI agents with:
- Automatic error capture and learning
- Pattern detection and consolidation
- AI-powered attribution analysis
- Skill utility tracking
- Evolution dashboard

Version: 1.0.0
"""

__version__ = "2.4.0"
__author__ = "Mr Lee"
__email__ = "your-email@example.com"
__license__ = "MIT"

from .auto_error_catcher import AutoErrorCatcher, auto_catch, catch_and_learn
from .auto_pattern_detector import AutoPatternDetector
from .ai_attributor import AIAttributor
from .auto_consolidator import AutoConsolidator
from .evolution_tracker import EvolutionTracker
from .evolution_memory import EvolutionMemory
from .evolution_dashboard import EvolutionDashboard
from .weekly_review import WeeklyReview
from .learn_from_feedback import LearnFromFeedback

__all__ = [
    # Core components
    "EvolutionTracker",
    "EvolutionMemory",
    
    # Auto error capture
    "AutoErrorCatcher",
    "auto_catch",
    "catch_and_learn",
    
    # Pattern detection
    "AutoPatternDetector",
    
    # Attribution analysis
    "AIAttributor",
    
    # Consolidation
    "AutoConsolidator",
    
    # Dashboard
    "EvolutionDashboard",
    
    # Review
    "WeeklyReview",
    
    # Feedback
    "LearnFromFeedback",
]
