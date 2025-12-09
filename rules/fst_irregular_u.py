"""
FST implementation of 우 irregular (우불규칙) conjugation.

Rule: Only applies to '푸다'
- 푸 + 어 → 퍼 (not 푸어)

Uses pynini FST to implement this transformation.
"""

import pynini
from rules.fst_utils import apply_fst, compose_fsts, jamo_fst


def create_u_irregular_fst():
    """
    Create FST for 우 irregular conjugation.

    Transforms: 푸 + 어-series → 퍼 + 어-series

    The FST operates at the stem-ending boundary:
    - Input: ㅍㅜ|ㅇㅓ (stem boundary ending, | marks boundary)
    - Output: ㅍㅓ|ㅇㅓ (changed ㅜ → ㅓ, removed first ㅇㅓ)

    Returns:
        pynini.Fst: U-irregular FST
    """
    # Create FST that transforms: ㅍㅜㅇㅓ → ㅍㅓ
    # This handles: 푸 + 어 → 퍼

    # Pattern: ㅍㅜ followed by ㅇㅓ → ㅍㅓ
    pu_eo_to_peo = pynini.cross("ㅍㅜㅇㅓ", "ㅍㅓ")

    # For other 어-series endings (었, 어요, etc.)
    # ㅍㅜㅇㅓ... → ㅍㅓ...
    sigma_star = pynini.closure(jamo_fst)

    u_irregular_fst = pynini.cdrewrite(
        pynini.cross("ㅍㅜㅇㅓ", "ㅍㅓ"),
        "",  # Left context
        "",  # Right context
        sigma_star
    ).optimize()

    return u_irregular_fst


def apply_u_irregular_fst(stem_jamo, ending_jamo):
    """
    Apply 우 irregular FST transformation.

    Args:
        stem_jamo: Stem in jamo form (e.g., 'ㅍㅜ')
        ending_jamo: Ending in jamo form (e.g., 'ㅇㅓ')

    Returns:
        str: Transformed result in jamo form, or None if rule doesn't apply
    """
    # Only apply to 푸 (ㅍㅜ) + 어-series
    if stem_jamo != 'ㅍㅜ':
        return None

    if not ending_jamo.startswith('ㅇㅓ') and not ending_jamo.startswith('ㅇㅏ'):
        return None

    # Concatenate stem and ending
    combined = stem_jamo + ending_jamo

    # Apply FST
    fst = create_u_irregular_fst()
    result = apply_fst(fst, combined)

    # If FST applied successfully, return result
    if result != combined:
        return result

    return None


def check_u_irregular_fst(stem_jamo, ending_jamo):
    """
    Check if 우 irregular rule should apply (FST version).

    Args:
        stem_jamo: Stem in jamo form
        ending_jamo: Ending in jamo form

    Returns:
        bool: True if rule applies
    """
    return stem_jamo == 'ㅍㅜ' and (
        ending_jamo.startswith('ㅇㅓ') or ending_jamo.startswith('ㅇㅏ')
    )
