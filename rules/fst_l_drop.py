"""
FST implementation of ㄹ-drop (ㄹ탈락) rule.

Rules:
1. ㄹ drops before the pre-final ending '느' (선어말어미 '느')
   Example: 놀 + 는 → 노는
2. ㄹ drops before endings that require the epenthetic vowel '으'
   Example: 놀 + ㄴ → 논

Uses pynini FST to implement this transformation.
"""

import pynini
from rules.fst_utils import apply_fst, jamo_fst


def create_l_drop_fst():
    """
    Create FST for ㄹ-drop rule.

    Transforms stems ending in ㄹ when followed by:
    1. Endings starting with ㄴㅡ (느): ...ㄹㄴㅡ → ...ㄴㅡ
    2. Incomplete consonant endings: ...ㄹㄴ → ...ㄴ, ...ㄹㅂ → ...ㅂ

    Returns:
        pynini.Fst: L-drop FST
    """
    sigma_star = pynini.closure(jamo_fst)

    # Rule 1: ㄹ drops before ㄴㅡ (느-series)
    # Pattern: ㄹㄴㅡ → ㄴㅡ
    l_drop_neu = pynini.cdrewrite(
        pynini.cross("ㄹㄴㅡ", "ㄴㅡ"),
        "",
        "",
        sigma_star
    )

    # Rule 2: ㄹ drops before incomplete consonants (ㄴ, ㅂ, ㅅ, ㅁ)
    # These consonants are used with epenthetic ㅡ
    # Patterns: ㄹㄴ → ㄴ, ㄹㅂ → ㅂ, ㄹㅅ → ㅅ, ㄹㅁ → ㅁ
    l_drop_n = pynini.cdrewrite(
        pynini.cross("ㄹㄴ", "ㄴ"),
        "",
        "",
        sigma_star
    )

    l_drop_b = pynini.cdrewrite(
        pynini.cross("ㄹㅂ", "ㅂ"),
        "",
        "",
        sigma_star
    )

    l_drop_s = pynini.cdrewrite(
        pynini.cross("ㄹㅅ", "ㅅ"),
        "",
        "",
        sigma_star
    )

    l_drop_m = pynini.cdrewrite(
        pynini.cross("ㄹㅁ", "ㅁ"),
        "",
        "",
        sigma_star
    )

    # Compose all rules
    result = pynini.compose(
        l_drop_neu,
        pynini.compose(
            l_drop_n,
            pynini.compose(
                l_drop_b,
                pynini.compose(l_drop_s, l_drop_m)
            )
        )
    ).optimize()

    return result


def apply_l_drop_fst(stem_jamo, ending_jamo):
    """
    Apply ㄹ-drop FST transformation.

    Args:
        stem_jamo: Stem in jamo form (e.g., 'ㄴㅗㄹ' for 놀)
        ending_jamo: Ending in jamo form (e.g., 'ㄴㅡ' for 는)

    Returns:
        str: Transformed result in jamo form, or None if rule doesn't apply
    """
    # Check if stem ends with ㄹ
    if not stem_jamo.endswith('ㄹ'):
        return None

    # Check if ending matches ㄹ-drop conditions
    valid_endings = ['ㄴㅡ', 'ㄴ', 'ㅂ', 'ㅅ', 'ㅁ']
    matches = False
    for end in valid_endings:
        if ending_jamo.startswith(end):
            matches = True
            break

    if not matches:
        return None

    # Concatenate stem and ending
    combined = stem_jamo + ending_jamo

    # Apply FST
    fst = create_l_drop_fst()
    result = apply_fst(fst, combined)

    # If FST applied successfully, return result
    if result != combined:
        return result

    return None


def check_l_drop_fst(stem_jamo, ending_jamo):
    """
    Check if ㄹ-drop rule should apply (FST version).

    Args:
        stem_jamo: Stem in jamo form
        ending_jamo: Ending in jamo form

    Returns:
        bool: True if rule applies
    """
    # Check if stem ends with ㄹ
    if not stem_jamo.endswith('ㄹ'):
        return False

    # Check if ending starts with valid patterns
    valid_endings = ['ㄴㅡ', 'ㄴ', 'ㅂ', 'ㅅ', 'ㅁ']
    for end in valid_endings:
        if ending_jamo.startswith(end):
            return True

    return False
