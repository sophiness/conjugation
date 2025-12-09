"""
FST implementation of 으 drop (으탈락) rule.

Rule: ㅡ sound drops before vowel endings
- 쓰 + 어 → 써 (not 쓰어)
- 크 + 었다 → 컸다 (not 크었다)

Uses pynini FST to implement this transformation.
"""

import pynini
from rules.fst_utils import apply_fst, jamo_fst, compose_fsts


def create_eu_drop_fst():
    """
    Create FST for 으 drop rule.

    Transforms stems ending in ㅡ when followed by vowel-initial endings:
    - Pattern: ...ㅡㅇ + vowel → ...consonant + vowel
    - Example: ㅆㅡㅇㅓ → ㅆㅓ (쓰 + 어 → 써)

    The FST removes ㅡ and the ㅇ marker before vowels.

    Returns:
        pynini.Fst: Eu-drop FST
    """
    sigma_star = pynini.closure(jamo_fst)

    # Vowels that can follow
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'

    # Create transformation for each vowel
    # Pattern: ㅡㅇ + vowel → vowel
    transformations = []
    for vowel in vowels:
        trans = pynini.cdrewrite(
            pynini.cross(f"ㅡㅇ{vowel}", vowel),
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


def apply_eu_drop_fst(stem_jamo, ending_jamo):
    """
    Apply 으 drop FST transformation.

    Args:
        stem_jamo: Stem in jamo form (e.g., 'ㅆㅡ' for 쓰)
        ending_jamo: Ending in jamo form (e.g., 'ㅇㅓ')

    Returns:
        str: Transformed result in jamo form, or None if rule doesn't apply
    """
    # Check if stem ends with ㅡ (no final consonant after ㅡ)
    if not stem_jamo.endswith('ㅡ'):
        return None

    # Check if ending starts with ㅇ + vowel (vowel-initial)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return None

    # Concatenate stem and ending
    combined = stem_jamo + ending_jamo

    # Apply FST
    fst = create_eu_drop_fst()
    result = apply_fst(fst, combined)

    # If FST applied successfully, return result
    if result != combined:
        return result

    return None


def check_eu_drop_fst(stem_jamo, ending_jamo):
    """
    Check if 으 drop rule should apply (FST version).

    Args:
        stem_jamo: Stem in jamo form
        ending_jamo: Ending in jamo form

    Returns:
        bool: True if rule applies
    """
    # Check if stem ends with ㅡ
    if not stem_jamo.endswith('ㅡ'):
        return False

    # Check if ending is vowel-initial (ㅇ + vowel)
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not (len(ending_jamo) >= 2 and ending_jamo[0] == 'ㅇ' and ending_jamo[1] in vowels):
        return False

    return True
