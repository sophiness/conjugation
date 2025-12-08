"""
Contraction (축약) rules for Korean conjugation.

Handles various vowel contraction patterns:
1. Regular contractions: ㅣ+ㅓ→ㅕ, ㅜ+ㅓ→ㅝ, ㅗ+ㅏ→ㅘ
2. ㅂ irregular contractions: ㅗ+ㅏ→ㅘ, ㅜ+ㅓ→ㅝ
3. 러 irregular contractions: ㄹ+ㅇ+vowel → ㄹ+vowel
4. ㅎ irregular contractions: ㅏ+ㅇ+ㅏ→ㅐ, ㅓ+ㅇ+ㅓ→ㅔ
5. 이다 contractions: 이+ㅓ→ㅕ, 이+ㅔ→ㅖ, 이+ㅑ→ㅑ
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str


def apply_contraction(jamo_str, contraction_type='regular'):
    """
    Apply contraction rules to a jamo string.

    Args:
        jamo_str: Decomposed jamo string
        contraction_type: Type of contraction ('regular', 'b_irregular', 'reo_irregular',
                         'h_irregular', 'ida')

    Returns:
        str: Contracted jamo string
    """
    if contraction_type == 'regular':
        return apply_regular_contraction(jamo_str)
    elif contraction_type == 'b_irregular':
        return apply_b_irregular_contraction(jamo_str)
    elif contraction_type == 'reo_irregular':
        return apply_reo_irregular_contraction(jamo_str)
    elif contraction_type == 'h_irregular':
        return apply_h_irregular_contraction(jamo_str)
    elif contraction_type == 'ida':
        return apply_ida_contraction(jamo_str)
    else:
        return jamo_str


def apply_regular_contraction(jamo_str):
    """
    Apply regular contraction rules.

    Patterns:
    - ㅣ + ㅓ → ㅕ
    - ㅜ + ㅓ → ㅝ
    - ㅗ + ㅏ → ㅘ

    Exceptions: Stems ending in 기-, 미-, 비-, 띠- do not contract.
    """
    # Check for exceptions (stems that don't contract)
    exception_patterns = ['ㄱㅣ', 'ㅁㅣ', 'ㅂㅣ', 'ㄸㅣ']
    for pattern in exception_patterns:
        if pattern in jamo_str:
            # Find the position and check if it's before the contraction point
            pos = jamo_str.rfind(pattern)
            # If this pattern appears near the end (within last 4 chars before potential contraction)
            if pos >= len(jamo_str) - 6:
                return jamo_str

    # Apply contractions
    result = jamo_str

    # ㅣ + ㅓ → ㅕ
    result = result.replace('ㅣㅓ', 'ㅕ')

    # ㅜ + ㅓ → ㅝ
    result = result.replace('ㅜㅓ', 'ㅝ')

    # ㅗ + ㅏ → ㅘ
    result = result.replace('ㅗㅏ', 'ㅘ')

    return result


def apply_b_irregular_contraction(jamo_str):
    """
    Apply ㅂ irregular contraction rules.

    After ㅂ → 오/우 transformation:
    - ㅗ + ㅏ → ㅘ
    - ㅜ + ㅓ → ㅝ
    """
    result = jamo_str

    # ㅗ + ㅏ → ㅘ
    result = result.replace('ㅗㅏ', 'ㅘ')

    # ㅜ + ㅓ → ㅝ
    result = result.replace('ㅜㅓ', 'ㅝ')

    return result


def apply_reo_irregular_contraction(jamo_str):
    """
    Apply 러 irregular contraction rules.

    Pattern: ㄹ + ㅇ + vowel → ㄹ + vowel
    (Remove the ㅇ placeholder)
    """
    result = jamo_str

    # ㄹ + ㅇ + vowel patterns
    vowels = ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ']
    for vowel in vowels:
        result = result.replace(f'ㄹㅇ{vowel}', f'ㄹ{vowel}')

    return result


def apply_h_irregular_contraction(jamo_str):
    """
    Apply ㅎ irregular contraction rules.

    After ㅎ deletion:
    - ㅏ + ㅇ + ㅏ → ㅐ
    - ㅓ + ㅇ + ㅓ → ㅔ
    """
    result = jamo_str

    # ㅏ + ㅇ + ㅏ → ㅐ
    result = result.replace('ㅏㅇㅏ', 'ㅐ')

    # ㅓ + ㅇ + ㅓ → ㅔ
    result = result.replace('ㅓㅇㅓ', 'ㅔ')

    return result


def apply_ida_contraction(jamo_str):
    """
    Apply 이다 (copula) contraction rules.

    Only applies when there's no final consonant:
    - 이 + ㅓ → ㅕ
    - 이 + ㅔ → ㅖ
    - 이 + ㅑ → ㅑ
    """
    result = jamo_str

    # 이 + ㅓ → ㅕ
    result = result.replace('ㅇㅣㅓ', 'ㅇㅕ')

    # 이 + ㅔ → ㅖ
    result = result.replace('ㅇㅣㅔ', 'ㅇㅖ')

    # 이 + ㅑ → ㅑ
    result = result.replace('ㅇㅣㅑ', 'ㅇㅑ')

    return result


def should_contract(stem, ending):
    """
    Determine if contraction should be applied.

    Args:
        stem: Verb stem
        ending: Ending

    Returns:
        bool: True if contraction should apply
    """
    # Check for exception stems
    exception_stems = ['기', '미', '비', '띠']
    for exc in exception_stems:
        if stem.endswith(exc):
            return False

    return True
