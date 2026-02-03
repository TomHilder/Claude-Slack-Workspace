"""
Claude-Slack-Workspace package.

This package is managed by Claude Code through Slack.
Features Conway's Game of Life - a cellular automaton simulation!
"""

__version__ = "0.1.0"

from .game_of_life import GameOfLife, PATTERNS

__all__ = ["GameOfLife", "PATTERNS"]
