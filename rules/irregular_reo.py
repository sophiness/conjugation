"""
러 irregular (러불규칙) conjugation rule.

Rule: Some verbs ending in 르 + vowel ending → 러
Example: 이르다 + 어 → 이르러 (not 이를어)

This is different from 르 irregular, which applies to most 르-final stems.
Only specific verbs follow this pattern (e.g., 이르다, 푸르다).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str, get_final_consonant
from rules.contraction import apply_reo_irregular_contraction


def check_reo_irregular(stem, ending, tag):
    """
    Check if 러 irregular rule should apply.

    Args:
        stem: Verb stem
        ending: Ending
        tag: Morphological tag

    Returns:
        bool: True if 러 irregular applies
    """
    # Check if stem ends with 르
    if get_final_consonant(stem) != '':
        # 르 is a vowel-final stem in Korean (르 = ㄹ+ㅡ)
        return False

    if not stem.endswith('르'):
        return False

    # Check if ending starts with a vowel
    if not ending or ending[0] not in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ', '아', '어', '오', '우', '으', '이', '애', '에', '외', '위', '의']:
        return False

    # Check tag for 러 irregular marker
    if tag and '러' in tag and '불규칙' in tag:
        return True

    return False


def apply_reo_irregular(stem, ending):
    """
    Apply 러 irregular conjugation.

    Args:
        stem: Verb stem ending in 르
        ending: Vowel-initial ending

    Returns:
        str: Conjugated form (르 → ㄹ + 러)
    """
    # Remove 르 from stem and add ㄹ
    base_stem = stem[:-1]

    # Decompose
    jamo_stem = decompose_str(base_stem)
    jamo_r = 'ㄹ'
    jamo_ending = decompose_str('러' + ending[1:] if len(ending) > 1 else '러')

    # Combine
    jamo_combined = jamo_stem + jamo_r + jamo_ending

    # Apply contraction to remove ㅇ placeholder
    jamo_contracted = apply_reo_irregular_contraction(jamo_combined)

    result = compose_str(jamo_contracted)

    return result
