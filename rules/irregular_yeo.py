"""
여 irregular (여불규칙) conjugation rule.

Rule: Applies to '하다' verbs
- 하 + 어 series → 해 series
- Examples: 하 + 어 → 해, 하 + 었다 → 했다

This applies to:
- Verb stem '하' (VV)
- Verbal suffix '하' (XSV)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_yeo_irregular(stem, ending, tag=None):
    """
    Check if 여 irregular rule should apply.

    Args:
        stem: Verb stem
        ending: Ending
        tag: Morphological tag (VV or XSV)

    Returns:
        bool: True if 여 irregular applies (only for 하)
    """
    # Only applies to 하
    if stem != '하':
        return False

    # Only applies to 어-series endings
    if not ending or not (ending.startswith('어') or ending.startswith('아')):
        return False

    # Check tag if provided (should be VV or XSV)
    if tag and tag not in ['VV', 'XSV']:
        return False

    return True


def apply_yeo_irregular(stem, ending):
    """
    Apply 여 irregular conjugation.

    Args:
        stem: Verb stem (should be '하')
        ending: 어/아-series ending

    Returns:
        str: Conjugated form (하 + 어 → 해)
    """
    if stem != '하':
        return None

    # Transform 어 series to 해 series
    result = ending.replace('어', '애', 1)  # Only replace first occurrence
    result = '해' if result.startswith('애') else '하' + result

    # Special handling for common patterns
    if ending.startswith('어'):
        # 하 + 어 → 해
        result = '해' + ending[1:]
    elif ending.startswith('아'):
        # 하 + 아 → 해
        result = '해' + ending[1:]

    return result
