"""
이다 (copula) conjugation rules.

The copula 이다 has special contraction rules:
- With final consonant: No contraction (학생 + 이다 → 학생이다)
- Without final consonant: Contractions apply
  - 이 + ㅓ → ㅕ (나무 + 이었다 → 나무였다)
  - 이 + ㅔ → ㅖ (나무 + 이에요 → 나무예요)
  - 이 + ㅑ → ㅑ (나무 + 이야 → 나무야)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str, has_final_consonant
from rules.contraction import apply_ida_contraction


def check_ida(stem):
    """
    Check if the stem is 이다.

    Args:
        stem: Verb stem

    Returns:
        bool: True if stem is 이 (from 이다)
    """
    return stem == '이'


def apply_ida_conjugation(prev_word, stem, ending):
    """
    Apply 이다 conjugation rules.

    Args:
        prev_word: Previous word (noun) before 이다
        stem: Stem (should be '이')
        ending: Ending

    Returns:
        str: Conjugated form
    """
    if not check_ida(stem):
        return None

    # Check if previous word has final consonant
    has_consonant = has_final_consonant(prev_word) if prev_word else True

    if has_consonant:
        # No contraction: simple concatenation
        jamo_stem = decompose_str(stem)
        jamo_ending = decompose_str(ending)
        result = compose_str(jamo_stem + jamo_ending)
    else:
        # Apply contraction
        jamo_stem = decompose_str(stem)
        jamo_ending = decompose_str(ending)
        jamo_combined = jamo_stem + jamo_ending

        # Apply 이다 contraction rules
        jamo_contracted = apply_ida_contraction(jamo_combined)
        result = compose_str(jamo_contracted)

    return result


def conjugate_ida(prev_word, ending):
    """
    Conjugate 이다 with the given ending.

    Args:
        prev_word: Previous word (noun) before 이다
        ending: Ending

    Returns:
        str: Conjugated form (without the previous word)
    """
    return apply_ida_conjugation(prev_word, '이', ending)
