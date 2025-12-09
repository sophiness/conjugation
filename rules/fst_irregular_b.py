"""
FST implementation of ㅂ irregular (ㅂ불규칙) conjugation.

Rule: ㅂ changes to 오/우 before vowel endings
- 1-syllable stems: 오 or 우 based on vowel harmony
- 2+ syllable stems: always 우

Examples:
- 돕다 + 어 → 도와 (1 syllable, vowel harmony)
- 아름답다 + 어 → 아름다워 (2+ syllables, always 우)

Contractions also apply: 오+아→와, 우+어→워

Uses pynini FST to implement this transformation.
"""

import pynini
from rules.fst_utils import apply_fst, jamo_fst
from rules.fst_contraction import create_b_irregular_contraction_fst


def create_b_irregular_fst(use_o=True):
    """
    Create FST for ㅂ irregular conjugation.

    Transforms stems ending in ㅂ when followed by vowel-initial endings:
    - Pattern: ...ㅂㅇ + vowel → ...ㅇ + 오/우 + ㅇ + vowel
    - Example: ㄷㅗㅂㅇㅓ → ㄷㅗㅇㅗㅇㅓ → ㄷㅗㅇㅘ (돕 + 어 → 도오어 → 도와)

    Args:
        use_o: True to use 오 (for 1-syllable bright stems), False for 우

    Returns:
        pynini.Fst: B-irregular FST
    """
    sigma_star = pynini.closure(jamo_fst)

    # Inserted vowel based on syllable count and harmony
    inserted_vowel = 'ㅇㅗ' if use_o else 'ㅇㅜ'

    # Vowels that can follow
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'

    # Create transformation for each vowel
    # Pattern: ㅂㅇ + vowel → inserted_vowel + ㅇ + vowel → contracted form
    transformations = []
    for vowel in vowels:
        # First transform: ㅂㅇvowel → inserted + ㅇvowel
        trans = pynini.cdrewrite(
            pynini.cross(f"ㅂㅇ{vowel}", f"{inserted_vowel}ㅇ{vowel}"),
            "",
            "",
            sigma_star
        )
        transformations.append(trans)

    # Compose all transformations
    if transformations:
        result = transformations[0]
        for trans in transformations[1:]:
            result = pynini.compose(result, trans)

        # Apply contractions: ㅗㅇㅏ→ㅘ, ㅜㅇㅓ→ㅝ
        contraction_fst = create_b_irregular_contraction_fst()
        result = pynini.compose(result, contraction_fst)

        return result.optimize()
    else:
        return pynini.accep("")


def apply_b_irregular_fst(stem_jamo, ending_jamo, use_o=True):
    """
    Apply ㅂ irregular FST transformation.

    Args:
        stem_jamo: Stem in jamo form (e.g., 'ㄷㅗㅂ' for 돕)
        ending_jamo: Ending in jamo form (e.g., 'ㅇㅓ')
        use_o: True for 오 (1-syllable bright), False for 우

    Returns:
        str: Transformed result in jamo form, or None if rule doesn't apply
    """
    # Check if stem ends with ㅂ
    if not stem_jamo.endswith('ㅂ'):
        return None

    # Check if ending starts with ㅇ + vowel (vowel-initial)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return None

    # Concatenate stem and ending
    combined = stem_jamo + ending_jamo

    # Apply FST
    fst = create_b_irregular_fst(use_o)
    result = apply_fst(fst, combined)

    # If FST applied successfully, return result
    if result != combined:
        return result

    return None


def check_b_irregular_fst(stem_jamo, ending_jamo, tag=None):
    """
    Check if ㅂ irregular rule should apply (FST version).

    Args:
        stem_jamo: Stem in jamo form
        ending_jamo: Ending in jamo form
        tag: Morphological tag (optional)

    Returns:
        bool: True if rule applies
    """
    # Check if stem ends with ㅂ
    if not stem_jamo.endswith('ㅂ'):
        return False

    # Check if ending is vowel-initial (ㅇ + vowel)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return False

    # Check tag if provided
    if tag and 'ㅂ' in tag and '불규칙' in tag:
        return True

    return False
