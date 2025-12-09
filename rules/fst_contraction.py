"""
FST implementation of contraction (축약) rules.

Handles various vowel contraction patterns:
1. Regular contractions: ㅣ+ㅓ→ㅕ, ㅜ+ㅓ→ㅝ, ㅗ+ㅏ→ㅘ
2. Same vowel repetition: V+ㅇ+V→V
3. ㅂ irregular contractions: ㅗ+ㅏ→ㅘ, ㅜ+ㅓ→ㅝ
4. 러 irregular contractions: ㄹ+ㅇ+vowel → ㄹ+vowel
5. ㅎ irregular contractions: ㅏ+ㅇ+ㅏ→ㅐ, ㅓ+ㅇ+ㅓ→ㅔ
6. 이다 contractions: 이+ㅓ→ㅕ, 이+ㅔ→ㅖ, 이+ㅑ→ㅑ

Uses pynini FST to implement these transformations.
"""

import pynini
from rules.fst_utils import apply_fst, create_substitution_fst, compose_fsts, jamo_fst


def create_regular_contraction_fst():
    """
    Create FST for regular contraction rules.

    Patterns:
    - ㅣㅇㅓ → ㅕ
    - ㅜㅇㅓ → ㅝ
    - ㅗㅇㅏ → ㅘ
    - ㅣㅓ → ㅕ (without ㅇ)
    - ㅜㅓ → ㅝ (without ㅇ)
    - ㅗㅏ → ㅘ (without ㅇ)
    - V+ㅇ+V → V (same vowel repetition)

    Returns:
        pynini.Fst: Regular contraction FST
    """
    sigma_star = pynini.closure(jamo_fst)

    # Create individual contraction rules

    # Same vowel repetition with ㅇ: V + ㅇ + V → V
    same_vowel_rules = []
    for vowel in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ']:
        rule = pynini.cdrewrite(
            pynini.cross(f"{vowel}ㅇ{vowel}", vowel),
            "", "",
            sigma_star
        )
        same_vowel_rules.append(rule)

    # Vowel contractions with ㅇ
    i_eo_to_yeo = pynini.cdrewrite(
        pynini.cross("ㅣㅇㅓ", "ㅕ"),
        "", "",
        sigma_star
    )

    u_eo_to_wo = pynini.cdrewrite(
        pynini.cross("ㅜㅇㅓ", "ㅝ"),
        "", "",
        sigma_star
    )

    o_a_to_wa = pynini.cdrewrite(
        pynini.cross("ㅗㅇㅏ", "ㅘ"),
        "", "",
        sigma_star
    )

    # Direct vowel contractions (without ㅇ)
    i_eo_direct = pynini.cdrewrite(
        pynini.cross("ㅣㅓ", "ㅕ"),
        "", "",
        sigma_star
    )

    u_eo_direct = pynini.cdrewrite(
        pynini.cross("ㅜㅓ", "ㅝ"),
        "", "",
        sigma_star
    )

    o_a_direct = pynini.cdrewrite(
        pynini.cross("ㅗㅏ", "ㅘ"),
        "", "",
        sigma_star
    )

    # Compose all rules
    all_rules = same_vowel_rules + [
        i_eo_to_yeo, u_eo_to_wo, o_a_to_wa,
        i_eo_direct, u_eo_direct, o_a_direct
    ]

    result = all_rules[0]
    for rule in all_rules[1:]:
        result = pynini.compose(result, rule)

    return result.optimize()


def create_b_irregular_contraction_fst():
    """
    Create FST for ㅂ irregular contraction rules.

    After ㅂ → 오/우 transformation:
    - ㅗㅏ → ㅘ
    - ㅜㅓ → ㅝ

    Returns:
        pynini.Fst: B-irregular contraction FST
    """
    sigma_star = pynini.closure(jamo_fst)

    o_a_to_wa = pynini.cdrewrite(
        pynini.cross("ㅗㅏ", "ㅘ"),
        "", "",
        sigma_star
    )

    u_eo_to_wo = pynini.cdrewrite(
        pynini.cross("ㅜㅓ", "ㅝ"),
        "", "",
        sigma_star
    )

    return pynini.compose(o_a_to_wa, u_eo_to_wo).optimize()


def create_reo_irregular_contraction_fst():
    """
    Create FST for 러 irregular contraction rules.

    Pattern: ㄹ + ㅇ + vowel → ㄹ + vowel

    Returns:
        pynini.Fst: Reo-irregular contraction FST
    """
    sigma_star = pynini.closure(jamo_fst)

    # Create rules for each vowel
    vowels = ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ']

    rules = []
    for vowel in vowels:
        rule = pynini.cdrewrite(
            pynini.cross(f"ㄹㅇ{vowel}", f"ㄹ{vowel}"),
            "", "",
            sigma_star
        )
        rules.append(rule)

    result = rules[0]
    for rule in rules[1:]:
        result = pynini.compose(result, rule)

    return result.optimize()


def create_h_irregular_contraction_fst():
    """
    Create FST for ㅎ irregular contraction rules.

    After ㅎ deletion:
    - ㅏㅇㅏ → ㅐ
    - ㅓㅇㅓ → ㅔ

    Returns:
        pynini.Fst: H-irregular contraction FST
    """
    sigma_star = pynini.closure(jamo_fst)

    a_a_to_ae = pynini.cdrewrite(
        pynini.cross("ㅏㅇㅏ", "ㅐ"),
        "", "",
        sigma_star
    )

    eo_eo_to_e = pynini.cdrewrite(
        pynini.cross("ㅓㅇㅓ", "ㅔ"),
        "", "",
        sigma_star
    )

    return pynini.compose(a_a_to_ae, eo_eo_to_e).optimize()


def create_ida_contraction_fst():
    """
    Create FST for 이다 (copula) contraction rules.

    - ㅇㅣㅓ → ㅇㅕ
    - ㅇㅣㅔ → ㅇㅖ
    - ㅇㅣㅑ → ㅇㅑ

    Returns:
        pynini.Fst: Ida contraction FST
    """
    sigma_star = pynini.closure(jamo_fst)

    i_eo_to_yeo = pynini.cdrewrite(
        pynini.cross("ㅇㅣㅓ", "ㅇㅕ"),
        "", "",
        sigma_star
    )

    i_e_to_ye = pynini.cdrewrite(
        pynini.cross("ㅇㅣㅔ", "ㅇㅖ"),
        "", "",
        sigma_star
    )

    i_ya_to_ya = pynini.cdrewrite(
        pynini.cross("ㅇㅣㅑ", "ㅇㅑ"),
        "", "",
        sigma_star
    )

    return compose_fsts(i_eo_to_yeo, i_e_to_ye, i_ya_to_ya)


def apply_contraction_fst(jamo_str, contraction_type='regular'):
    """
    Apply contraction FST to a jamo string.

    Args:
        jamo_str: Decomposed jamo string
        contraction_type: Type of contraction ('regular', 'b_irregular', 'reo_irregular',
                         'h_irregular', 'ida')

    Returns:
        str: Contracted jamo string
    """
    if contraction_type == 'regular':
        fst = create_regular_contraction_fst()
    elif contraction_type == 'b_irregular':
        fst = create_b_irregular_contraction_fst()
    elif contraction_type == 'reo_irregular':
        fst = create_reo_irregular_contraction_fst()
    elif contraction_type == 'h_irregular':
        fst = create_h_irregular_contraction_fst()
    elif contraction_type == 'ida':
        fst = create_ida_contraction_fst()
    else:
        return jamo_str

    return apply_fst(fst, jamo_str)
