"""
ㄷ irregular (ㄷ불규칙) conjugation rule.

Rule: ㄷ changes to ㄹ before vowel endings
Example: 묻다 + 어 → 물어 (not 묻어)

Note: This only applies to ㄷ irregular verbs, not all ㄷ-final stems.
Regular ㄷ verbs like 묻다 (to bury) conjugate regularly: 묻어
Vowel harmony is applied.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str, get_final_consonant, decompose, compose
from rules.vowel_harmony import apply_vowel_harmony


def check_d_irregular(stem, ending, tag):
    """
    Check if ㄷ irregular rule should apply.

    Args:
        stem: Verb stem
        ending: Ending
        tag: Morphological tag (should contain irregular marker)

    Returns:
        bool: True if ㄷ irregular applies
    """
    # Check if stem ends with ㄷ
    if get_final_consonant(stem) != 'ㄷ':
        return False

    # Check if ending starts with a vowel
    if not ending or ending[0] not in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ', '아', '어', '오', '우', '으', '이', '애', '에', '외', '위', '의']:
        return False

    # Check tag for irregular marker
    if tag and 'ㄷ' in tag and '불규칙' in tag:
        return True

    return False


def apply_d_irregular(stem, ending):
    """
    Apply ㄷ irregular conjugation.

    Args:
        stem: Verb stem ending in ㄷ
        ending: Vowel-initial ending

    Returns:
        str: Conjugated form with ㄷ → ㄹ
    """
    # Apply vowel harmony to ending
    harmonized_ending = apply_vowel_harmony(stem, ending)

    # Decompose stem
    last_char = stem[-1]
    cho, jung, jong = decompose(last_char)

    # Change ㄷ to ㄹ
    new_last_char = compose(cho, jung, 'ㄹ')
    new_stem = stem[:-1] + new_last_char

    # Simply concatenate
    result = new_stem + harmonized_ending

    return result
