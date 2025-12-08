"""
Regular conjugation rules with contractions.

This handles regular verb conjugation when no irregular patterns apply.
Applies vowel harmony and vowel contractions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str, get_final_consonant, decompose, is_hangul
from rules.vowel_harmony import apply_vowel_harmony
from rules.contraction import apply_regular_contraction, should_contract


def is_vowel_initial_ending(ending):
    """Check if ending starts with a vowel."""
    if not ending:
        return False
    first_char = ending[0]

    # Check if it's a vowel jamo
    if first_char in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ', 'ㅑ', 'ㅕ', 'ㅛ', 'ㅠ', 'ㅒ', 'ㅖ']:
        return True

    # Check if it's a Hangul syllable starting with ㅇ (vowel-initial)
    if is_hangul(first_char):
        cho, _, _ = decompose(first_char)
        return cho == 'ㅇ'

    return False


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
        # Incomplete consonant ending
        jamo_stem = decompose_str(stem)
        if get_final_consonant(stem):
            # Has jongsung: need epenthetic ㅡ
            # Example: 먹 + ㄴ → 먹은 (ㅁㅓㄱ + ㅇㅡㄴ)
            result = compose_str(jamo_stem + 'ㅇㅡ' + ending)
        else:
            # No jongsung: consonant becomes jongsung
            # Example: 가 + ㄴ → 간 (ㄱㅏ + ㄴ)
            result = compose_str(jamo_stem + ending)
        return result

    # Check if ending is vowel-initial or consonant-initial
    if is_vowel_initial_ending(ending):
        # Vowel ending: apply vowel harmony and contractions
        harmonized_ending = apply_vowel_harmony(stem, ending)
    else:
        # Consonant ending: most consonant endings don't need epenthetic vowel
        # They are complete syllables that can be directly concatenated
        # Only special morphological cases would need epenthetic vowel
        return stem + ending

    # Apply vowel harmony and contractions for vowel endings
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
