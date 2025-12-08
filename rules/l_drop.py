"""
ㄹ-drop (ㄹ탈락) rule for Korean conjugation.

Rules:
1. ㄹ drops before the pre-final ending '느' (선어말어미 '느')
   Example: 놀 + 는 → 노는
2. ㄹ drops before endings that require the epenthetic vowel '으'
   Example: 놀 + ㄴ → 논 (with epenthetic ㅡ)

Note: This rule applies in specific morphological environments.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str, get_final_consonant


def check_l_drop(stem, ending):
    """
    Check if ㄹ-drop rule should apply.

    Args:
        stem: Verb stem
        ending: Ending

    Returns:
        bool: True if ㄹ-drop should apply
    """
    # Check if stem ends with ㄹ
    if get_final_consonant(stem) != 'ㄹ':
        return False

    # Check ending conditions
    # 1. Endings starting with 느: 는, 느라, etc.
    if ending.startswith('느'):
        return True

    # 2. Endings that require epenthetic ㅡ (incomplete consonant endings)
    # These are represented as single consonants: ㄴ, ㅂ, etc.
    if len(ending) > 0 and ending[0] in ['ㄴ', 'ㅂ', 'ㅅ', 'ㅁ']:
        return True

    return False


def apply_l_drop(stem, ending):
    """
    Apply ㄹ-drop rule.

    Args:
        stem: Verb stem ending in ㄹ
        ending: Ending

    Returns:
        str: Conjugated form with ㄹ dropped
    """
    if not check_l_drop(stem, ending):
        return None

    # Decompose stem
    jamo_stem = decompose_str(stem)

    # Remove final ㄹ
    if jamo_stem.endswith('ㄹ'):
        jamo_stem = jamo_stem[:-1]

    # For incomplete consonant endings, add epenthetic ㅡ
    if len(ending) > 0 and ending[0] in ['ㄴ', 'ㅂ', 'ㅅ', 'ㅁ']:
        jamo_ending = 'ㅡ' + ending
    else:
        jamo_ending = decompose_str(ending)

    # Combine and compose
    result = compose_str(jamo_stem + jamo_ending)

    return result
