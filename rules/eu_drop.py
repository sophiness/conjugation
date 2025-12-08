"""
으 drop (으탈락) rule for Korean conjugation.

Rule: Simple ㅡ sound drops before vowel endings
- 쓰 + 어 → 써 (not 쓰어)
- 크 + 었다 → 컸다 (not 크었다)

This applies to stems ending in ㅡ (with no final consonant).
Vowel harmony and contractions are also applied.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str, get_vowel, get_final_consonant
from rules.vowel_harmony import apply_vowel_harmony
from rules.contraction import apply_regular_contraction


def check_eu_drop(stem, ending):
    """
    Check if 으 drop rule should apply.

    Args:
        stem: Verb stem
        ending: Ending

    Returns:
        bool: True if 으 drop applies
    """
    # Check if stem ends with ㅡ vowel (no final consonant)
    if get_final_consonant(stem):
        return False

    if get_vowel(stem) != 'ㅡ':
        return False

    # Check if ending starts with a vowel
    if not ending or ending[0] not in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ', '아', '어', '오', '우', '으', '이', '애', '에', '외', '위', '의']:
        return False

    return True


def apply_eu_drop(stem, ending):
    """
    Apply 으 drop rule.

    Args:
        stem: Verb stem ending in ㅡ
        ending: Vowel-initial ending

    Returns:
        str: Conjugated form with ㅡ dropped
    """
    # Apply vowel harmony (based on the vowel before ㅡ if exists)
    harmonized_ending = apply_vowel_harmony(stem, ending)

    # Decompose stem and remove final ㅡ
    jamo_stem = decompose_str(stem)

    # Remove the ㅡ vowel
    if jamo_stem.endswith('ㅡ'):
        jamo_stem = jamo_stem[:-1]

    # Decompose ending
    jamo_ending = decompose_str(harmonized_ending)

    # Combine
    jamo_combined = jamo_stem + jamo_ending

    # Apply regular contractions
    jamo_contracted = apply_regular_contraction(jamo_combined)

    result = compose_str(jamo_contracted)

    return result
