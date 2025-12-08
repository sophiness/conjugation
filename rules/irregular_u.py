"""
우 irregular (우불규칙) conjugation rule.

Rule: Only applies to '푸다'
- 푸 + 어 → 퍼 (not 푸어)

This is a very specific irregular pattern for a single verb.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_u_irregular(stem, ending):
    """
    Check if 우 irregular rule should apply.

    Args:
        stem: Verb stem
        ending: Ending

    Returns:
        bool: True if 우 irregular applies (only for 푸)
    """
    # Only applies to 푸
    if stem != '푸':
        return False

    # Only applies to 어-series endings
    if not ending or not ending.startswith('어'):
        return False

    return True


def apply_u_irregular(stem, ending):
    """
    Apply 우 irregular conjugation.

    Args:
        stem: Verb stem (should be '푸')
        ending: 어-series ending

    Returns:
        str: Conjugated form (푸 → 퍼)
    """
    if not check_u_irregular(stem, ending):
        return None

    # 푸 + 어 → 퍼
    result = '퍼' + ending[1:]  # Remove 어 from beginning of ending

    return result
