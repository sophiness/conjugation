"""
FST implementation of 러 irregular (러불규칙) conjugation.

Rule: Some verbs ending in 르 + vowel ending → 러
Example: 이르다 + 어 → 이르러 (not 이를어)

This is different from 르 irregular, which applies to most 르-final stems.
Only specific verbs follow this pattern (e.g., 이르다, 푸르다).

Uses pynini FST to implement this transformation.
"""

import pynini
from rules.fst_utils import apply_fst, jamo_fst
from rules.fst_contraction import create_reo_irregular_contraction_fst


def create_reo_irregular_fst():
    """
    Create FST for 러 irregular conjugation.

    Transforms: 르 + vowel → ㄹ + 러 + rest
    - Pattern: ...ㅡㄹㅇ + vowel → ...ㄹㄹㅓ + rest
    - Example: ㅇㅣㅡㄹㅇㅓ → ㅇㅣㄹㄹㅓ (이르 + 어 → 이르러)

    Returns:
        pynini.Fst: Reo-irregular FST
    """
    sigma_star = pynini.closure(jamo_fst)

    # Vowels that can follow
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'

    # Create transformations for each vowel
    # Pattern: ㅡㄹㅇvowel → ㄹㄹㅓ (always 러 regardless of ending vowel)
    transformations = []
    for vowel in vowels:
        # Transform: ㅡㄹㅇvowel → ㄹㄹㅓ + rest
        # For 어-series, just ㄹㄹㅓ
        # For other series, we need to handle differently
        if vowel == 'ㅓ':
            # 이르 + 어 → 이르러
            trans = pynini.cdrewrite(
                pynini.cross("ㅡㄹㅇㅓ", "ㄹㄹㅓ"),
                "",
                "",
                sigma_star
            )
        else:
            # For other endings, still insert 러
            # 이르 + 았다 → 이르렀다 (not implemented here, simplified)
            trans = pynini.cdrewrite(
                pynini.cross(f"ㅡㄹㅇ{vowel}", f"ㄹㄹㅓ"),
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

        # Apply contractions to remove ㅇ placeholders
        contraction_fst = create_reo_irregular_contraction_fst()
        result = pynini.compose(result, contraction_fst)

        return result.optimize()
    else:
        return pynini.accep("")


def apply_reo_irregular_fst(stem_jamo, ending_jamo):
    """
    Apply 러 irregular FST transformation.

    Args:
        stem_jamo: Stem in jamo form (e.g., 'ㅇㅣㅡㄹ' for 이르)
        ending_jamo: Ending in jamo form (e.g., 'ㅇㅓ')

    Returns:
        str: Transformed result in jamo form, or None if rule doesn't apply
    """
    # Check if stem ends with ㅡㄹ (르)
    if not stem_jamo.endswith('ㅡㄹ'):
        return None

    # Check if ending starts with ㅇ + vowel (vowel-initial)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return None

    # Concatenate stem and ending
    combined = stem_jamo + ending_jamo

    # Apply FST
    fst = create_reo_irregular_fst()
    result = apply_fst(fst, combined)

    # If FST applied successfully, return result
    if result != combined:
        return result

    return None


def check_reo_irregular_fst(stem_jamo, ending_jamo, tag=None):
    """
    Check if 러 irregular rule should apply (FST version).

    Args:
        stem_jamo: Stem in jamo form
        ending_jamo: Ending in jamo form
        tag: Morphological tag (optional)

    Returns:
        bool: True if rule applies
    """
    # Check if stem ends with 르
    if not stem_jamo.endswith('ㅡㄹ'):
        return False

    # Check if ending is vowel-initial (ㅇ + vowel)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return False

    # Check tag if provided (must have irregular marker)
    if tag and '러' in tag and '불규칙' in tag:
        return True

    return False
