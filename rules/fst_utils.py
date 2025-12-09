"""
FST utility functions for Korean verb conjugation using pynini.

Provides common FST building blocks for morphological rules.
"""

import pynini
from pynini.lib import rewrite


# Define Korean jamo (consonants and vowels)
CHOSUNG = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
JUNGSUNG = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
JONGSUNG = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"

# Create FST character classes
cho_fst = pynini.union(*[pynini.accep(c) for c in CHOSUNG])
jung_fst = pynini.union(*[pynini.accep(c) for c in JUNGSUNG])
jong_fst = pynini.union(*[pynini.accep(c) for c in JONGSUNG])

# Any jamo
jamo_fst = pynini.union(cho_fst, jung_fst, jong_fst)

# Bright vowels for vowel harmony (양성모음)
bright_vowels = "ㅏㅗㅑㅛㅘ"
bright_fst = pynini.union(*[pynini.accep(v) for v in bright_vowels])

# Dark vowels (음성모음)
dark_vowels = "ㅓㅜㅡㅣㅔㅐㅕㅠㅝㅞㅟㅢ"
dark_fst = pynini.union(*[pynini.accep(v) for v in dark_vowels])


def apply_fst(fst, input_str):
    """
    Apply an FST to an input string and return the result.

    Args:
        fst: pynini FST
        input_str: Input string

    Returns:
        str: Output string, or input if FST doesn't apply
    """
    try:
        output = rewrite.one_top_rewrite(input_str, fst)
        return output
    except rewrite.Error:
        # FST doesn't apply, return input unchanged
        return input_str


def compose_fsts(*fsts):
    """
    Compose multiple FSTs in sequence.

    Args:
        *fsts: Variable number of FSTs to compose

    Returns:
        pynini.Fst: Composed FST
    """
    if not fsts:
        return pynini.accep("")

    result = fsts[0]
    for fst in fsts[1:]:
        result = pynini.compose(result, fst).optimize()

    return result


def create_deletion_fst(to_delete):
    """
    Create an FST that deletes a specific string.

    Args:
        to_delete: String to delete

    Returns:
        pynini.Fst: Deletion FST
    """
    return pynini.cdrewrite(
        pynini.cross(to_delete, ""),
        "",  # Left context
        "",  # Right context
        pynini.closure(jamo_fst)
    ).optimize()


def create_substitution_fst(from_str, to_str, left_context="", right_context=""):
    """
    Create an FST that substitutes one string for another.

    Args:
        from_str: String to replace
        to_str: Replacement string
        left_context: Left context (optional)
        right_context: Right context (optional)

    Returns:
        pynini.Fst: Substitution FST
    """
    sigma_star = pynini.closure(jamo_fst)

    return pynini.cdrewrite(
        pynini.cross(from_str, to_str),
        left_context,
        right_context,
        sigma_star
    ).optimize()


def create_contraction_fst(pattern1, pattern2, result):
    """
    Create an FST for vowel contraction.

    Args:
        pattern1: First pattern (e.g., 'ㅗ')
        pattern2: Second pattern (e.g., 'ㅏ')
        result: Contracted result (e.g., 'ㅘ')

    Returns:
        pynini.Fst: Contraction FST
    """
    sigma_star = pynini.closure(jamo_fst)

    return pynini.cdrewrite(
        pynini.cross(pattern1 + pattern2, result),
        "",
        "",
        sigma_star
    ).optimize()
