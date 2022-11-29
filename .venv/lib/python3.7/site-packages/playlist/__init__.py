"""Playlist Module (FL Studio built-in)

Allows you to control and interact with the FL Studio Playlist.

NOTES:
 * Playlist tracks are 1-indexed.

KNOWN ISSUES:
 * When a track index is required, track zero can be accessed, but does not give
   results (as track indexes start at 1)
 * Trying to access track `500` raises an Index out of range `TypeError`

HELP WANTED:
 * Explanations for display zone functions
 * Explanations for live performance related functions
"""

from .playlist import *
