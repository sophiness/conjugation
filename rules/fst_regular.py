"""
FST implementation of regular conjugation.

Handles regular verb conjugation when no irregular patterns apply.
Combines vowel harmony and vowel contractions.

Uses pynini FST to implement this transformation.
"""

import pynini
from rules.fst_utils import apply_fst
from rules.fst_vowel_harmony import create_vowel_harmony_fst
from rules.fst_contraction import create_regular_contraction_fst


def create_regular_conjugation_fst(is_bright=False):
    """
    Create FST for regular conjugation.

    Combines:
    1. Vowel harmony (if bright vowel stem)
    2. Vowel contractions

    Args:
        is_bright: True if stem has bright vowel (ㅏ, ㅗ)

    Returns:
        pynini.Fst: Regular conjugation FST
    """
    # Create vowel harmony FST (only if bright)
    if is_bright:
        harmony_fst = create_vowel_harmony_fst()
    else:
        # Identity FST for dark vowels
        harmony_fst = pynini.closure(
            pynini.union(*[pynini.accep(c) for c in 'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉㅏㅓㅗㅜㅡㅣㅐㅔㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞㅚㅟㅢ'])
        )

    # Create contraction FST
    contraction_fst = create_regular_contraction_fst()

    # Compose harmony and contraction
    # First apply harmony, then contractions
    regular_fst = pynini.compose(harmony_fst, contraction_fst).optimize()

    return regular_fst


def apply_regular_conjugation_fst(stem_jamo, ending_jamo, is_bright=False, allow_contraction=True):
    """
    Apply regular conjugation FST.

    Args:
        stem_jamo: Stem in jamo form
        ending_jamo: Ending in jamo form
        is_bright: True if stem has bright vowel
        allow_contraction: True to apply contractions (default: True)

    Returns:
        str: Conjugated form in jamo, or None if rule doesn't apply
    """
    # Concatenate stem and ending
    combined = stem_jamo + ending_jamo

    # Create and apply FST
    fst = create_regular_conjugation_fst(is_bright)
    result = apply_fst(fst, combined)

    return result


def is_bright_vowel_stem(stem_jamo):
    """
    Check if stem has bright vowel (ㅏ, ㅗ).

    Args:
        stem_jamo: Stem in jamo form

    Returns:
        bool: True if stem has bright vowel
    """
    bright_vowels = ['ㅏ', 'ㅗ', 'ㅑ', 'ㅛ', 'ㅘ']

    # Find the last vowel in the stem
    for char in reversed(stem_jamo):
        if char in bright_vowels:
            return True
        elif char in ['ㅓ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅕ', 'ㅠ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']:
            return False

    # Default to dark (음성모음)
    return False
