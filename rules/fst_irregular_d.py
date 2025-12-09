"""
FST implementation of ㄷ irregular (ㄷ불규칙) conjugation.

Rule: ㄷ changes to ㄹ before vowel endings
Example: 듣다 + 어 → 들어 (not 듣어)

Uses pynini FST to implement this transformation.
"""

import pynini
from rules.fst_utils import apply_fst, jamo_fst


def create_d_irregular_fst():
    """
    Create FST for ㄷ irregular conjugation.

    Transforms stems ending in ㄷ when followed by vowel-initial endings:
    - Pattern: ...ㄷㅇ + vowel → ...ㄹㅇ + vowel
    - Example: ㄷㅡㄷㅇㅓ → ㄷㅡㄹㅇㅓ (듣 + 어 → 들어)

    The FST changes ㄷ to ㄹ before vowels.

    Returns:
        pynini.Fst: D-irregular FST
    """
    sigma_star = pynini.closure(jamo_fst)

    # Vowels that can follow
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'

    # Create transformation for each vowel
    # Pattern: ㄷㅇ + vowel → ㄹㅇ + vowel
    transformations = []
    for vowel in vowels:
        trans = pynini.cdrewrite(
            pynini.cross(f"ㄷㅇ{vowel}", f"ㄹㅇ{vowel}"),
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
        return result.optimize()
    else:
        return pynini.accep("")


def apply_d_irregular_fst(stem_jamo, ending_jamo):
    """
    Apply ㄷ irregular FST transformation.

    Args:
        stem_jamo: Stem in jamo form (e.g., 'ㄷㅡㄷ' for 듣)
        ending_jamo: Ending in jamo form (e.g., 'ㅇㅓ')

    Returns:
        str: Transformed result in jamo form, or None if rule doesn't apply
    """
    # Check if stem ends with ㄷ
    if not stem_jamo.endswith('ㄷ'):
        return None

    # Check if ending starts with ㅇ + vowel (vowel-initial)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return None

    # Concatenate stem and ending
    combined = stem_jamo + ending_jamo

    # Apply FST
    fst = create_d_irregular_fst()
    result = apply_fst(fst, combined)

    # If FST applied successfully, return result
    if result != combined:
        return result

    return None


def check_d_irregular_fst(stem_jamo, ending_jamo, tag=None):
    """
    Check if ㄷ irregular rule should apply (FST version).

    Args:
        stem_jamo: Stem in jamo form
        ending_jamo: Ending in jamo form
        tag: Morphological tag (optional)

    Returns:
        bool: True if rule applies
    """
    # Check if stem ends with ㄷ
    if not stem_jamo.endswith('ㄷ'):
        return False

    # Check if ending is vowel-initial (ㅇ + vowel)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return False

    # Check tag if provided (must have irregular marker)
    if tag and 'ㄷ' in tag and '불규칙' in tag:
        return True

    # For ㄷ irregular, we need explicit tag confirmation
    return False
