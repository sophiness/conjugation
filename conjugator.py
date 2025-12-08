"""
Main Korean verb conjugator.

Implements the full branching logic from the flowchart:
1. Check ㄹ-drop rule first
2. If not ㄹ-drop, check 이다 conjugation
3. Determine ending type (incomplete consonant, consonant, vowel)
4. For vowel endings:
   - Check irregular tags (ㅅ, ㄷ, ㅂ, 러, ㅎ)
   - Check special stems (우, 여, 르)
   - Apply 으-drop
   - Apply regular conjugation with contractions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import get_final_consonant
from rules.l_drop import apply_l_drop, check_l_drop
from rules.ida import apply_ida_conjugation, check_ida
from rules.irregular_s import apply_s_irregular, check_s_irregular
from rules.irregular_d import apply_d_irregular, check_d_irregular
from rules.irregular_b import apply_b_irregular, check_b_irregular
from rules.irregular_reo import apply_reo_irregular, check_reo_irregular
from rules.irregular_h import apply_h_irregular, check_h_irregular
from rules.irregular_u import apply_u_irregular, check_u_irregular
from rules.irregular_yeo import apply_yeo_irregular, check_yeo_irregular
from rules.irregular_reu import apply_reu_irregular, check_reu_irregular
from rules.eu_drop import apply_eu_drop, check_eu_drop
from rules.regular import apply_regular_conjugation


class KoreanConjugator:
    """
    Korean verb conjugator following morphological rules.
    """

    def __init__(self):
        """Initialize the conjugator."""
        pass

    def conjugate(self, stem, ending, tag=None, prev_word=None):
        """
        Conjugate a Korean verb stem with an ending.

        Args:
            stem: Verb stem (어간)
            ending: Verb ending (어미)
            tag: Morphological tag (e.g., 'VV+ㅅ불규칙', 'VV', 'XSV')
            prev_word: Previous word (for 이다 conjugation)

        Returns:
            str: Conjugated form
        """
        if not stem or not ending:
            return stem if stem else ''

        # Step 1: Check ㄹ-drop rule (highest priority)
        if check_l_drop(stem, ending):
            result = apply_l_drop(stem, ending)
            if result:
                return result

        # Step 2: Check 이다 (copula) conjugation
        if check_ida(stem):
            result = apply_ida_conjugation(prev_word, stem, ending)
            if result:
                return result

        # Step 3: Determine ending type and branch accordingly
        # Check if ending starts with incomplete consonant (자소)
        if self._is_incomplete_consonant_ending(ending):
            # Incomplete consonant ending: handled by regular conjugation
            return apply_regular_conjugation(stem, ending)

        # Check if ending starts with consonant (complete syllable)
        if self._is_consonant_ending(ending):
            # Consonant ending: handled by regular conjugation
            return apply_regular_conjugation(stem, ending)

        # Step 4: Vowel ending - check irregulars and special cases
        if self._is_vowel_ending(ending):
            # Check irregular verb tags
            if tag and self._has_irregular_tag(tag):
                # Apply tagged irregular rules
                result = self._apply_tagged_irregular(stem, ending, tag)
                if result:
                    return result

            # Check special stems (우, 여, 르 irregulars)
            # Priority: 우 > 여 > 르 > 으-drop > regular

            # 우 irregular (푸다)
            if check_u_irregular(stem, ending):
                result = apply_u_irregular(stem, ending)
                if result:
                    return result

            # 여 irregular (하다)
            if check_yeo_irregular(stem, ending, tag):
                result = apply_yeo_irregular(stem, ending)
                if result:
                    return result

            # 르 irregular (흐르다, etc.)
            if check_reu_irregular(stem, ending):
                result = apply_reu_irregular(stem, ending)
                if result:
                    return result

            # 으-drop (쓰다, 크다, etc.)
            if check_eu_drop(stem, ending):
                result = apply_eu_drop(stem, ending)
                if result:
                    return result

            # Regular conjugation with contractions
            return apply_regular_conjugation(stem, ending)

        # Default: regular conjugation
        return apply_regular_conjugation(stem, ending)

    def _is_incomplete_consonant_ending(self, ending):
        """Check if ending starts with incomplete consonant (자소)."""
        if not ending:
            return False
        # Incomplete consonants are single jamo characters
        return len(ending) == 1 and ending in ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    def _is_consonant_ending(self, ending):
        """Check if ending starts with consonant (complete syllable)."""
        if not ending:
            return False
        first_char = ending[0]
        # Check if it's a Hangul syllable starting with consonant (not vowel)
        if ord(first_char) < ord('가'):
            return False
        # It's not a vowel jamo
        if first_char in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ']:
            return False
        # Check if the syllable starts with ㅇ (which represents vowel-initial)
        from utils import decompose
        cho, _, _ = decompose(first_char)
        return cho != 'ㅇ'

    def _is_vowel_ending(self, ending):
        """Check if ending starts with vowel."""
        if not ending:
            return False
        first_char = ending[0]
        # Check if it's a vowel jamo
        if first_char in ['ㅏ', 'ㅓ', 'ㅗ', 'ㅜ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅚ', 'ㅟ', 'ㅢ']:
            return True
        # Check if it's a Hangul syllable starting with ㅇ (vowel)
        if ord(first_char) >= ord('가'):
            from utils import decompose
            cho, _, _ = decompose(first_char)
            return cho == 'ㅇ'
        return False

    def _has_irregular_tag(self, tag):
        """Check if tag contains irregular marker."""
        irregular_markers = ['ㅅ불규칙', 'ㄷ불규칙', 'ㅂ불규칙', '러불규칙', 'ㅎ불규칙']
        return any(marker in tag for marker in irregular_markers)

    def _apply_tagged_irregular(self, stem, ending, tag):
        """Apply irregular conjugation based on tag."""
        if 'ㅅ불규칙' in tag or 'ㅅ' in tag:
            if check_s_irregular(stem, ending, tag):
                return apply_s_irregular(stem, ending)

        if 'ㄷ불규칙' in tag or 'ㄷ' in tag:
            if check_d_irregular(stem, ending, tag):
                return apply_d_irregular(stem, ending)

        if 'ㅂ불규칙' in tag or 'ㅂ' in tag:
            if check_b_irregular(stem, ending, tag):
                return apply_b_irregular(stem, ending)

        if '러불규칙' in tag or '러' in tag:
            if check_reo_irregular(stem, ending, tag):
                return apply_reo_irregular(stem, ending)

        if 'ㅎ불규칙' in tag or 'ㅎ' in tag:
            if check_h_irregular(stem, ending, tag):
                return apply_h_irregular(stem, ending)

        return None


# Convenience function
def conjugate(stem, ending, tag=None, prev_word=None):
    """
    Conjugate a Korean verb.

    Args:
        stem: Verb stem
        ending: Verb ending
        tag: Morphological tag (optional)
        prev_word: Previous word for 이다 (optional)

    Returns:
        str: Conjugated form

    Examples:
        >>> conjugate('먹', '어요')
        '먹어요'
        >>> conjugate('짓', '어', tag='VV+ㅅ불규칙')
        '지어'
        >>> conjugate('돕', '어', tag='VV+ㅂ불규칙')
        '도와'
    """
    conjugator = KoreanConjugator()
    return conjugator.conjugate(stem, ending, tag, prev_word)
