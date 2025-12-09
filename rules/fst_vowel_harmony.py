"""
Vowel harmony (모음조화) FST rules for Korean conjugation.

Uses pynini to implement vowel harmony as FST transformations.
"""

import pynini
from rules.fst_utils import apply_fst, bright_fst, dark_fst, create_substitution_fst, compose_fsts


def create_vowel_harmony_fst():
    """
    Create FST for vowel harmony transformation.

    Changes 어-series to 아-series based on the stem's last vowel.
    This FST is applied at the stem-ending boundary.

    Returns:
        pynini.Fst: Vowel harmony FST
    """
    # Create individual substitution rules
    # These will be selected based on the stem's vowel

    # For bright vowels (ㅏ, ㅗ): 어 → 아
    eo_to_a = create_substitution_fst("ㅓ", "ㅏ")
    yeo_to_ya = create_substitution_fst("ㅕ", "ㅑ")
    e_to_ae = create_substitution_fst("ㅔ", "ㅐ")

    # Compose all transformations
    bright_harmony = compose_fsts(eo_to_a, yeo_to_ya, e_to_ae)

    # For dark vowels: keep 어-series (identity FST)
    dark_harmony = pynini.closure(pynini.union(
        pynini.accep("ㅏ"), pynini.accep("ㅓ"), pynini.accep("ㅗ"), pynini.accep("ㅜ"),
        pynini.accep("ㅡ"), pynini.accep("ㅣ"), pynini.accep("ㅐ"), pynini.accep("ㅔ"),
        pynini.accep("ㅑ"), pynini.accep("ㅕ"), pynini.accep("ㅛ"), pynini.accep("ㅠ"),
        pynini.accep("ㅘ"), pynini.accep("ㅝ"), pynini.accep("ㅙ"), pynini.accep("ㅞ"),
        pynini.accep("ㅚ"), pynini.accep("ㅟ"), pynini.accep("ㅢ"),
        pynini.accep("ㄱ"), pynini.accep("ㄴ"), pynini.accep("ㄷ"), pynini.accep("ㄹ"),
        pynini.accep("ㅁ"), pynini.accep("ㅂ"), pynini.accep("ㅅ"), pynini.accep("ㅇ"),
        pynini.accep("ㅈ"), pynini.accep("ㅊ"), pynini.accep("ㅋ"), pynini.accep("ㅌ"),
        pynini.accep("ㅍ"), pynini.accep("ㅎ"), pynini.accep("ㄲ"), pynini.accep("ㄸ"),
        pynini.accep("ㅃ"), pynini.accep("ㅆ"), pynini.accep("ㅉ")
    ))

    return bright_harmony


def apply_vowel_harmony_fst(stem_jamo, ending_jamo, is_bright):
    """
    Apply vowel harmony FST based on stem's vowel type.

    Args:
        stem_jamo: Stem in jamo decomposed form
        ending_jamo: Ending in jamo decomposed form
        is_bright: True if stem has bright vowel (ㅏ, ㅗ)

    Returns:
        str: Harmonized ending in jamo form
    """
    if is_bright:
        harmony_fst = create_vowel_harmony_fst()
        return apply_fst(harmony_fst, ending_jamo)
    else:
        # Dark vowel: no change needed (어-series is default)
        return ending_jamo
