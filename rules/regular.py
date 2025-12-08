"""
Regular conjugation rules with contractions.

This handles regular verb conjugation when no irregular patterns apply.
Applies vowel harmony and vowel contractions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str, get_final_consonant
from rules.vowel_harmony import apply_vowel_harmony
from rules.contraction import apply_regular_contraction, should_contract


def apply_regular_conjugation(stem, ending):
    """
    Apply regular conjugation with vowel harmony and contractions.

    Args:
        stem: Verb stem
        ending: Ending

    Returns:
        str: Conjugated form
    """
    # Determine ending type
    if not ending:
        return stem

    # Check if ending starts with incomplete consonant (자소)
    # Incomplete consonant endings: ㄴ, ㅂ, ㅅ, etc.
    if len(ending) == 1 and ending in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']:
        # Incomplete consonant ending: just compose together (모아쓰기)
        jamo_stem = decompose_str(stem)
        result = compose_str(jamo_stem + ending)
        return result

    # Check if ending starts with consonant (full syllable)
    first_char = ending[0]
    if first_char not in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ'] and ord(first_char) >= ord('가'):
        # Consonant ending: check if stem needs epenthetic vowel
        if get_final_consonant(stem):
            # Has final consonant: add epenthetic ㅡ
            jamo_stem = decompose_str(stem)
            jamo_ending = decompose_str(ending)
            result = compose_str(jamo_stem + 'ㅡ' + jamo_ending)
            return result
        else:
            # No final consonant: direct concatenation
            return stem + ending

    # Vowel ending: apply vowel harmony and contractions
    harmonized_ending = apply_vowel_harmony(stem, ending)

    # Decompose
    jamo_stem = decompose_str(stem)
    jamo_ending = decompose_str(harmonized_ending)

    # Combine
    jamo_combined = jamo_stem + jamo_ending

    # Apply contractions if allowed
    if should_contract(stem, ending):
        jamo_contracted = apply_regular_contraction(jamo_combined)
    else:
        jamo_contracted = jamo_combined

    result = compose_str(jamo_contracted)

    return result
