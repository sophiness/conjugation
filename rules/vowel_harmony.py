"""
Vowel harmony (모음조화) rules for Korean conjugation.

In Korean, certain endings change based on the vowel of the stem:
- Bright vowels (양성모음: ㅏ, ㅗ) → -아 endings
- Dark vowels (음성모음: ㅓ, ㅜ, ㅡ, etc.) → -어 endings
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import get_vowel, is_bright_vowel


def apply_vowel_harmony(stem, ending):
    """
    Apply vowel harmony to the ending based on the stem's last vowel.

    Args:
        stem: Verb stem
        ending: Ending to harmonize (usually starts with 어 or 아)

    Returns:
        str: Harmonized ending
    """
    if not ending:
        return ending

    # Get the last vowel from the stem
    last_vowel = get_vowel(stem)

    if not last_vowel:
        return ending

    # Apply vowel harmony
    harmonized = ending

    # Convert 어 ↔ 아 based on vowel harmony
    if is_bright_vowel(last_vowel):
        # Bright vowel: use 아-series
        harmonized = harmonized.replace('어', '아')
        harmonized = harmonized.replace('여', '야')
        harmonized = harmonized.replace('에', '애')
    else:
        # Dark vowel: use 어-series
        harmonized = harmonized.replace('아', '어')
        harmonized = harmonized.replace('야', '여')
        harmonized = harmonized.replace('애', '에')

    return harmonized


def get_harmonized_vowel(stem):
    """
    Get the harmonized vowel (아 or 어) for a given stem.

    Args:
        stem: Verb stem

    Returns:
        str: '아' for bright vowels, '어' for dark vowels
    """
    last_vowel = get_vowel(stem)

    if not last_vowel:
        return '어'

    return '아' if is_bright_vowel(last_vowel) else '어'
