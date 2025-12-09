"""
FST implementation of ㅎ irregular (ㅎ불규칙) conjugation.

Rule: ㅎ drops before vowel endings, then contractions apply
- Adjectives with suffix -앟/-엏 (e.g., 파랗다)
- ㅎ drops: 파랗 + 아 → 파라 + 아
- Then contracts: 파라 + 아 → 파래

Special contraction patterns:
- ㅏㅇㅏ → ㅐ
- ㅓㅇㅓ → ㅔ

Note: Only adjectives (형용사) show this pattern.
좋다 is the only ㅎ-final adjective with regular conjugation.

Uses pynini FST to implement this transformation.
"""

import pynini
from rules.fst_utils import apply_fst, jamo_fst
from rules.fst_contraction import create_h_irregular_contraction_fst


def create_h_irregular_fst():
    """
    Create FST for ㅎ irregular conjugation.

    Transforms stems ending in ㅎ when followed by vowel-initial endings:
    - Pattern: ...ㅎㅇ + vowel → ...ㅇ + vowel → contraction
    - Example: ㅍㅏㄹㅏㅎㅇㅏ → ㅍㅏㄹㅏㅇㅏ → ㅍㅏㄹㅐ (파랗 + 아 → 파라아 → 파래)

    The FST removes ㅎ and applies special contractions.

    Returns:
        pynini.Fst: H-irregular FST
    """
    sigma_star = pynini.closure(jamo_fst)

    # Vowels that can follow
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'

    # Create transformation for each vowel
    # Pattern: ㅎㅇ + vowel → ㅇ + vowel (remove ㅎ)
    transformations = []
    for vowel in vowels:
        trans = pynini.cdrewrite(
            pynini.cross(f"ㅎㅇ{vowel}", f"ㅇ{vowel}"),
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

        # Apply ㅎ irregular contractions: ㅏㅇㅏ→ㅐ, ㅓㅇㅓ→ㅔ
        contraction_fst = create_h_irregular_contraction_fst()
        result = pynini.compose(result, contraction_fst)

        return result.optimize()
    else:
        return pynini.accep("")


def apply_h_irregular_fst(stem_jamo, ending_jamo):
    """
    Apply ㅎ irregular FST transformation.

    Args:
        stem_jamo: Stem in jamo form (e.g., 'ㅍㅏㄹㅏㅎ' for 파랗)
        ending_jamo: Ending in jamo form (e.g., 'ㅇㅏ')

    Returns:
        str: Transformed result in jamo form, or None if rule doesn't apply
    """
    # Check if stem ends with ㅎ
    if not stem_jamo.endswith('ㅎ'):
        return None

    # Check if ending starts with ㅇ + vowel (vowel-initial)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return None

    # Concatenate stem and ending
    combined = stem_jamo + ending_jamo

    # Apply FST
    fst = create_h_irregular_fst()
    result = apply_fst(fst, combined)

    # If FST applied successfully, return result
    if result != combined:
        return result

    return None


def check_h_irregular_fst(stem_jamo, ending_jamo, tag=None, stem=None):
    """
    Check if ㅎ irregular rule should apply (FST version).

    Args:
        stem_jamo: Stem in jamo form
        ending_jamo: Ending in jamo form
        tag: Morphological tag (optional)
        stem: Original stem in composed form (to check for 좋)

    Returns:
        bool: True if rule applies
    """
    # Check if stem ends with ㅎ
    if not stem_jamo.endswith('ㅎ'):
        return False

    # 좋다 is regular, not irregular
    if stem and stem == '좋':
        return False

    # Check if ending is vowel-initial (ㅇ + vowel)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return False

    # Check tag if provided
    if tag and 'ㅎ' in tag and '불규칙' in tag:
        return True

    # Default to irregular for ㅎ-final adjectives (except 좋다)
    return True
