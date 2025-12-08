"""
ㅂ irregular (ㅂ불규칙) conjugation rule.

Rule: ㅂ changes to 오/우 before vowel endings
- 1-syllable stems: 오 or 우 based on vowel harmony
- 2+ syllable stems: always 우

Example:
- 돕다 + 어 → 도와 (1 syllable, vowel harmony)
- 아름답다 + 어 → 아름다워 (2+ syllables, always 우)

Contractions also apply: 오+아→와, 우+어→워
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str, get_final_consonant, is_hangul, decompose, compose
from rules.vowel_harmony import get_harmonized_vowel
from rules.contraction import apply_b_irregular_contraction


def count_syllables(text):
    """Count the number of Hangul syllables in text."""
    return sum(1 for char in text if is_hangul(char))


def check_b_irregular(stem, ending, tag):
    """
    Check if ㅂ irregular rule should apply.

    Args:
        stem: Verb stem
        ending: Ending
        tag: Morphological tag

    Returns:
        bool: True if ㅂ irregular applies
    """
    # Check if stem ends with ㅂ
    if get_final_consonant(stem) != 'ㅂ':
        return False

    # Check if ending starts with a vowel
    if not ending or ending[0] not in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ', '아', '어', '오', '우', '으', '이', '애', '에', '외', '위', '의']:
        return False

    # Check tag for irregular marker
    if tag and 'ㅂ' in tag and '불규칙' in tag:
        return True

    return False


def apply_b_irregular(stem, ending):
    """
    Apply ㅂ irregular conjugation.

    Args:
        stem: Verb stem ending in ㅂ
        ending: Vowel-initial ending

    Returns:
        str: Conjugated form with ㅂ → 오/우
    """
    # Determine if 오 or 우
    syllable_count = count_syllables(stem)

    if syllable_count <= 1:
        # 1-syllable: use vowel harmony (오 or 우)
        harmonized_vowel = get_harmonized_vowel(stem)
        inserted_vowel = '오' if harmonized_vowel == '아' else '우'
    else:
        # 2+ syllables: always 우
        inserted_vowel = '우'

    # Remove ㅂ from stem
    last_char = stem[-1]
    cho, jung, jong = decompose(last_char)
    new_last_char = compose(cho, jung, '')
    new_stem = stem[:-1] + new_last_char

    # Decompose for contraction
    jamo_stem = decompose_str(new_stem)
    jamo_vowel = decompose_str(inserted_vowel)
    jamo_ending = decompose_str(ending)

    # Combine
    jamo_combined = jamo_stem + jamo_vowel + jamo_ending

    # Apply contraction: 오+아→와, 우+어→워
    jamo_contracted = apply_b_irregular_contraction(jamo_combined)

    result = compose_str(jamo_contracted)

    return result
