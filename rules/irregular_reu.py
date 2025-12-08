"""
르 irregular (르불규칙) conjugation rule.

Rule: Stems ending in 르 + vowel ending → ㅡ drops, ㄹ is added
- 흐르 + 어 → 흘러 (ㅡ drops, ㄹ added before 어)
- Pattern: 르 → ㄹ + ㄹ + vowel

This is different from 러 irregular. Most 르-final verbs follow this pattern.
Since Kiwi doesn't tag these, we maintain a dictionary of 르 irregular stems.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import decompose_str, compose_str
from rules.vowel_harmony import apply_vowel_harmony
from rules.contraction import apply_contraction


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


def check_reu_irregular(stem, ending):
    """
    Check if 르 irregular rule should apply.

    Args:
        stem: Verb stem
        ending: Ending

    Returns:
        bool: True if 르 irregular applies
    """
    # Check if stem is in the dictionary
    if stem not in REU_IRREGULAR_STEMS:
        return False

    # Check if stem ends with 르
    if not stem.endswith('르'):
        return False

    # Check if ending starts with a vowel
    if not ending or ending[0] not in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ', '아', '어', '오', '우', '으', '이', '애', '에', '외', '위', '의']:
        return False

    return True


def apply_reu_irregular(stem, ending):
    """
    Apply 르 irregular conjugation.

    Args:
        stem: Verb stem ending in 르
        ending: Vowel-initial ending

    Returns:
        str: Conjugated form (르 → ㄹ + ㄹ + ending)
    """
    # Apply vowel harmony
    harmonized_ending = apply_vowel_harmony(stem, ending)

    # Remove 르 from stem: 흐르 → 흐
    base_stem = stem[:-1]

    # Add ㄹ to base stem and ㄹ before ending
    # Pattern: 흐 + ㄹ + ㄹ + 어 → 흘러
    jamo_stem = decompose_str(base_stem)
    jamo_r1 = 'ㄹ'
    jamo_r2 = 'ㄹ'
    jamo_ending = decompose_str(harmonized_ending)

    # Combine: base + ㄹ + ㄹ + vowel
    jamo_combined = jamo_stem + jamo_r1 + jamo_r2 + jamo_ending

    # Compose back
    result = compose_str(jamo_combined)

    return result
