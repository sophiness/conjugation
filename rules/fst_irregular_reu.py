"""
FST implementation of 르 irregular (르불규칙) conjugation.

Rule: Stems ending in 르 + vowel ending → ㅡ drops, ㄹ is doubled
- 흐르 + 어 → 흘러 (ㅡ drops, ㄹ added before 어)
- Pattern: 르 → ㄹ + ㄹ + vowel

Uses pynini FST to implement this transformation.
Note: Dictionary-based checking is done in Python, FST handles transformation.
"""

import os
import pynini
from rules.fst_utils import apply_fst, jamo_fst


# Load 르 irregular stems from dictionary
def load_reu_irregular_stems():
    """Load 르 irregular stems from data file."""
    stems = set()
    data_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'data', 'reu_irregular_stems.txt'
    )

    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    stems.add(line)
    except FileNotFoundError:
        # Return default set if file not found
        stems = {'흐르', '따르', '부르', '오르', '치르', '고르', '누르', '자르', '모르', '이르', '다르'}

    return stems


REU_IRREGULAR_STEMS = load_reu_irregular_stems()


def create_reu_irregular_fst():
    """
    Create FST for 르 irregular conjugation.

    Transforms the pattern at stem-ending boundary:
    - Stem ending in ㅡㄹ (르) + vowel → ㄹㄹ + vowel
    - Examples: ㅎㅡㄹ + ㅇㅓ → ㅎㄹㄹㅓ (흐르 + 어 → 흘러)

    The FST removes ㅡ and doubles ㄹ before vowel.

    Returns:
        pynini.Fst: Reu-irregular FST
    """
    # Create FST that handles the transformation:
    # Pattern: ...ㅡㄹ + vowel → ...ㄹㄹ + vowel

    sigma_star = pynini.closure(jamo_fst)

    # Vowel symbols (jamo form)
    vowels = pynini.union(*[pynini.accep(v) for v in 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'])

    # Transform: ㅡㄹ followed by vowel → ㄹㄹ followed by same vowel
    # We need to capture the vowel and preserve it
    # Pattern: ㅡㄹㅏ → ㄹㄹㅏ, ㅡㄹㅓ → ㄹㄹㅓ, etc.

    transformations = []
    for vowel in 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ':
        # ㅡㄹ + vowel → ㄹㄹ + vowel
        trans = pynini.cdrewrite(
            pynini.cross(f"ㅡㄹ{vowel}", f"ㄹㄹ{vowel}"),
            "",
            "",
            sigma_star
        )
        transformations.append(trans)

    # Compose all vowel transformations
    if transformations:
        result = transformations[0]
        for trans in transformations[1:]:
            result = pynini.compose(result, trans)
        return result.optimize()
    else:
        return pynini.accep("")


def apply_reu_irregular_fst(stem_jamo, ending_jamo, stem=None):
    """
    Apply 르 irregular FST transformation.

    Args:
        stem_jamo: Stem in jamo form (e.g., 'ㅎㅡㄹ' for 흐르)
        ending_jamo: Ending in jamo form (e.g., 'ㅇㅓ')
        stem: Original stem in composed form (for dictionary check)

    Returns:
        str: Transformed result in jamo form, or None if rule doesn't apply
    """
    # Check if stem is in dictionary (need original stem)
    if stem and stem not in REU_IRREGULAR_STEMS:
        return None

    # Check if stem ends with ㅡㄹ (르)
    if not stem_jamo.endswith('ㅡㄹ'):
        return None

    # Check if ending starts with vowel
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not ending_jamo or ending_jamo[0] not in vowels:
        return None

    # Concatenate stem and ending
    combined = stem_jamo + ending_jamo

    # Apply FST
    fst = create_reu_irregular_fst()
    result = apply_fst(fst, combined)

    # If FST applied successfully, return result
    if result != combined:
        return result

    return None


def check_reu_irregular_fst(stem_jamo, ending_jamo, stem=None):
    """
    Check if 르 irregular rule should apply (FST version).

    Args:
        stem_jamo: Stem in jamo form
        ending_jamo: Ending in jamo form
        stem: Original stem in composed form (for dictionary check)

    Returns:
        bool: True if rule applies
    """
    # Check dictionary
    if stem and stem not in REU_IRREGULAR_STEMS:
        return False

    # Check if stem ends with 르
    if not stem_jamo.endswith('ㅡㄹ'):
        return False

    # Check if ending starts with vowel
    vowels = 'ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟㅢㅑㅕㅛㅠㅒㅖㅘㅝㅙㅞ'
    if not ending_jamo or ending_jamo[0] not in vowels:
        return False

    return True
