"""
ㅎ irregular (ㅎ불규칙) conjugation rule.

Rule: ㅎ drops before vowel endings, then contractions apply
- Adjectives with suffix -앟/-엏 (e.g., 파랗다)
- ㅎ drops: 파랗 + 아 → 파라 + 아
- Then contracts: 파라 + 아 → 파래

Special contraction patterns:
- ㅏ + ㅇ + ㅏ → ㅐ
- ㅓ + ㅇ + ㅓ → ㅔ

Note: Only adjectives (형용사) show this pattern.
좋다 is the only ㅎ-final adjective with regular conjugation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str, get_final_consonant, decompose, compose
from rules.vowel_harmony import apply_vowel_harmony
from rules.contraction import apply_h_irregular_contraction


def check_h_irregular(stem, ending, tag):
    """
    Check if ㅎ irregular rule should apply.

    Args:
        stem: Verb stem
        ending: Ending
        tag: Morphological tag

    Returns:
        bool: True if ㅎ irregular applies
    """
    # Check if stem ends with ㅎ
    if get_final_consonant(stem) != 'ㅎ':
        return False

    # 좋다 is regular, not irregular
    if stem == '좋':
        return False

    # Check if ending starts with a vowel
    if not ending or ending[0] not in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ', '아', '어', '오', '우', '으', '이', '애', '에', '외', '위', '의']:
        return False

    # Check tag for irregular marker
    if tag and 'ㅎ' in tag and '불규칙' in tag:
        return True

    # Default to irregular for ㅎ-final adjectives (except 좋다)
    return True


def apply_h_irregular(stem, ending):
    """
    Apply ㅎ irregular conjugation.

    Args:
        stem: Verb stem ending in ㅎ
        ending: Vowel-initial ending

    Returns:
        str: Conjugated form with ㅎ dropped and contractions
    """
    # Apply vowel harmony
    harmonized_ending = apply_vowel_harmony(stem, ending)

    # Remove ㅎ from stem
    last_char = stem[-1]
    cho, jung, jong = decompose(last_char)
    new_last_char = compose(cho, jung, '')
    new_stem = stem[:-1] + new_last_char

    # Decompose for contraction
    jamo_stem = decompose_str(new_stem)
    jamo_ending = decompose_str(harmonized_ending)

    # Combine
    jamo_combined = jamo_stem + jamo_ending

    # Apply ㅎ irregular contractions: ㅏㅇㅏ→ㅐ, ㅓㅇㅓ→ㅔ
    jamo_contracted = apply_h_irregular_contraction(jamo_combined)

    result = compose_str(jamo_contracted)

    return result
