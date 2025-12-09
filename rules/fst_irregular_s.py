"""
FST implementation of ㅅ irregular (ㅅ불규칙) conjugation.

Rule: ㅅ drops before vowel endings
Example: 짓다 + 어 → 지어 (not 짓어)

Uses pynini FST to implement this transformation.
"""

import pynini
from rules.fst_utils import apply_fst, jamo_fst


def create_s_irregular_fst():
    """
    Create FST for ㅅ irregular conjugation.

    Transforms stems ending in ㅅ when followed by vowel-initial endings:
    - Pattern: ...ㅅㅇ + vowel → ...ㅇ + vowel
    - Example: ㅈㅣㅅㅇㅓ → ㅈㅣㅇㅓ (짓 + 어 → 지어)

    The FST removes ㅅ before vowels.

    Returns:
        pynini.Fst: S-irregular FST
    """
    sigma_star = pynini.closure(jamo_fst)

    # Vowels that can follow
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'

    # Create transformation for each vowel
    # Pattern: ㅅㅇ + vowel → ㅇ + vowel (remove ㅅ)
    transformations = []
    for vowel in vowels:
        trans = pynini.cdrewrite(
            pynini.cross(f"ㅅㅇ{vowel}", f"ㅇ{vowel}"),
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


def apply_s_irregular_fst(stem_jamo, ending_jamo):
    """
    Apply ㅅ irregular FST transformation.

    Args:
        stem_jamo: Stem in jamo form (e.g., 'ㅈㅣㅅ' for 짓)
        ending_jamo: Ending in jamo form (e.g., 'ㅇㅓ')

    Returns:
        str: Transformed result in jamo form, or None if rule doesn't apply
    """
    # Check if stem ends with ㅅ
    if not stem_jamo.endswith('ㅅ'):
        return None

    # Check if ending starts with ㅇ + vowel (vowel-initial)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return None

    # Concatenate stem and ending
    combined = stem_jamo + ending_jamo

    # Apply FST
    fst = create_s_irregular_fst()
    result = apply_fst(fst, combined)

    # If FST applied successfully, return result
    if result != combined:
        return result

    return None


def check_s_irregular_fst(stem_jamo, ending_jamo, tag=None):
    """
    Check if ㅅ irregular rule should apply (FST version).

    Args:
        stem_jamo: Stem in jamo form
        ending_jamo: Ending in jamo form
        tag: Morphological tag (optional)

    Returns:
        bool: True if rule applies
    """
    # Check if stem ends with ㅅ
    if not stem_jamo.endswith('ㅅ'):
        return False

    # Check if ending is vowel-initial (ㅇ + vowel)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return False

    # Check tag if provided
    if tag and 'ㅅ' in tag and '불규칙' in tag:
        return True

    # Default to true if conditions met
    return True
