"""
FST implementation of 여 irregular (여불규칙) conjugation.

Rule: Applies to '하다' verbs
- 하 + 어 series → 해 series
- Examples: 하 + 어 → 해, 하 + 았다 → 했다

Uses pynini FST to implement this transformation.
"""

import pynini
from rules.fst_utils import apply_fst, create_substitution_fst, compose_fsts, jamo_fst


def create_yeo_irregular_fst():
    """
    Create FST for 여 irregular conjugation.

    Transforms: 하 + 어-series → 해 + series
                하 + 아-series → 해 + series

    The FST operates at the stem-ending boundary:
    - ㅎㅏㅇㅓ → ㅎㅐ (하 + 어 → 해)
    - ㅎㅏㅇㅏ → ㅎㅐ (하 + 아 → 해)

    Returns:
        pynini.Fst: Yeo-irregular FST
    """
    # Create transformations for 하 + 어/아 → 해

    sigma_star = pynini.closure(jamo_fst)

    # Transform: ㅎㅏㅇㅓ → ㅎㅐ (하 + 어 → 해)
    ha_eo_to_hae = pynini.cdrewrite(
        pynini.cross("ㅎㅏㅇㅓ", "ㅎㅐ"),
        "",
        "",
        sigma_star
    )

    # Transform: ㅎㅏㅇㅏ → ㅎㅐ (하 + 아 → 해)
    ha_a_to_hae = pynini.cdrewrite(
        pynini.cross("ㅎㅏㅇㅏ", "ㅎㅐ"),
        "",
        "",
        sigma_star
    )

    # Compose both transformations
    yeo_irregular_fst = compose_fsts(ha_eo_to_hae, ha_a_to_hae).optimize()

    return yeo_irregular_fst


def apply_yeo_irregular_fst(stem_jamo, ending_jamo):
    """
    Apply 여 irregular FST transformation.

    Args:
        stem_jamo: Stem in jamo form (e.g., 'ㅎㅏ')
        ending_jamo: Ending in jamo form (e.g., 'ㅇㅓ', 'ㅇㅏ')

    Returns:
        str: Transformed result in jamo form, or None if rule doesn't apply
    """
    # Only apply to 하 (ㅎㅏ) + 어/아-series
    if stem_jamo != 'ㅎㅏ':
        return None

    if not (ending_jamo.startswith('ㅇㅓ') or ending_jamo.startswith('ㅇㅏ')):
        return None

    # Concatenate stem and ending
    combined = stem_jamo + ending_jamo

    # Apply FST
    fst = create_yeo_irregular_fst()
    result = apply_fst(fst, combined)

    # If FST applied successfully, return result
    if result != combined:
        return result

    return None


def check_yeo_irregular_fst(stem_jamo, ending_jamo, tag=None):
    """
    Check if 여 irregular rule should apply (FST version).

    Args:
        stem_jamo: Stem in jamo form
        ending_jamo: Ending in jamo form
        tag: Morphological tag (VV or XSV)

    Returns:
        bool: True if rule applies
    """
    # Only applies to 하
    if stem_jamo != 'ㅎㅏ':
        return False

    # Only applies to 어/아-series
    if not (ending_jamo.startswith('ㅇㅓ') or ending_jamo.startswith('ㅇㅏ')):
        return False

    # Check tag if provided
    if tag and tag not in ['VV', 'XSV']:
        return False

    return True
