"""
ㅅ irregular (ㅅ불규칙) conjugation rule.

Rule: ㅅ drops before vowel endings
Example: 짓다 + 어 → 지어 (not 짓어)

This applies to stems ending in ㅅ before vowel-initial endings.
Vowel harmony is also applied.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str, get_final_consonant
from rules.vowel_harmony import apply_vowel_harmony


def check_s_irregular(stem, ending, tag):
    """
    Check if ㅅ irregular rule should apply.

    Args:
        stem: Verb stem
        ending: Ending
        tag: Morphological tag (should contain irregular marker)

    Returns:
        bool: True if ㅅ irregular applies
    """
    # Check if stem ends with ㅅ
    if get_final_consonant(stem) != 'ㅅ':
        return False

    # Check if ending starts with a vowel
    if not ending or ending[0] not in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ', '아', '어', '오', '우', '으', '이', '애', '에', '외', '위', '의']:
        return False

    # Check tag for irregular marker (if provided)
    # Tag format might include '+ㅅ불규칙' or similar
    if tag and 'ㅅ' in tag and '불규칙' in tag:
        return True

    # Default: assume irregular if conditions met
    return True


def apply_s_irregular(stem, ending):
    """
    Apply ㅅ irregular conjugation.

    Args:
        stem: Verb stem ending in ㅅ
        ending: Vowel-initial ending

    Returns:
        str: Conjugated form with ㅅ dropped
    """
    # Apply vowel harmony to ending
    harmonized_ending = apply_vowel_harmony(stem, ending)

    # Decompose stem
    jamo_stem = decompose_str(stem)

    # Remove final ㅅ
    if jamo_stem.endswith('ㅅ'):
        jamo_stem = jamo_stem[:-1]

    # Decompose ending
    jamo_ending = decompose_str(harmonized_ending)

    # Combine
    result = compose_str(jamo_stem + jamo_ending)

    return result
