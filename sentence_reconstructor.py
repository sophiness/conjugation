"""
Sentence reconstruction module using morphological analysis and conjugation rules.

This module integrates with Kiwi morphological analyzer to:
1. Analyze input sentences
2. Extract verb stem-ending pairs
3. Apply conjugation rules
4. Reconstruct the surface form

Usage:
    from sentence_reconstructor import reconstruct_sentence

    result = reconstruct_sentence("나는 밥을 먹었어요")
    print(result)  # 나는밥을먹었어요 (without spacing)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conjugator import conjugate

# Try to import real Kiwi
try:
    from kiwipiepy import Kiwi
    KIWI_AVAILABLE = True
except ImportError:
    KIWI_AVAILABLE = False
    print("Warning: Kiwi not installed. Using mock data for demonstration.")
    print("Install with: pip install kiwipiepy")


# Mock Kiwi output for demonstration when Kiwi is not available
class MockKiwi:
    """Mock Kiwi for demonstration purposes."""

    def __init__(self):
        self.examples = {
            "나는 밥을 먹었어요": [
                [('나', 'NP', 0, 1), ('는', 'JX', 1, 2)],
                [('밥', 'NNG', 3, 4), ('을', 'JKO', 4, 5)],
                [('먹', 'VV', 6, 7), ('었', 'EP', 7, 8), ('어요', 'EF', 8, 10)]
            ],
            "그는 학교에 갑니다": [
                [('그', 'NP', 0, 1), ('는', 'JX', 1, 2)],
                [('학교', 'NNG', 3, 5), ('에', 'JKB', 5, 6)],
                [('가', 'VV', 7, 8), ('ㅂ니다', 'EF', 8, 10)]
            ],
            "아이가 노는 모습이 예뻐요": [
                [('아이', 'NNG', 0, 2), ('가', 'JKS', 2, 3)],
                [('놀', 'VV', 4, 5), ('는', 'ETM', 5, 6)],
                [('모습', 'NNG', 7, 9), ('이', 'JKS', 9, 10)],
                [('예쁘', 'VA', 11, 13), ('어요', 'EF', 13, 15)]
            ]
        }

    def analyze(self, text):
        """Mock analyze method."""
        if text in self.examples:
            return [self.examples[text]]
        else:
            # Simple fallback
            return [[[('unknown', 'NNG', 0, len(text))]]]

    def tokenize(self, text):
        """Mock tokenize method - returns list of morphemes."""
        result = []
        if text in self.examples:
            for word_morphs in self.examples[text]:
                for morph in word_morphs:
                    result.append(morph)
        return result


def is_verb_tag(tag):
    """Check if a POS tag is a verb or adjective."""
    return tag in ['VV', 'VA', 'VX', 'VCP', 'VCN']


def is_ending_tag(tag):
    """Check if a POS tag is an ending."""
    return tag in ['EP', 'EF', 'EC', 'ETN', 'ETM']


def is_irregular_tag(tag):
    """Extract irregularity information from tag."""
    # Kiwi uses tags like 'VV+ㅅ불규칙', 'VA+ㅂ불규칙'
    if '+' in tag:
        parts = tag.split('+')
        if len(parts) > 1:
            return parts[1]
    return None


def reconstruct_sentence(text, use_real_kiwi=True):
    """
    Reconstruct sentence from morphological analysis.

    Args:
        text: Input sentence
        use_real_kiwi: If True, use real Kiwi (default: True)

    Returns:
        str: Reconstructed sentence without spacing
    """
    # Initialize analyzer
    if use_real_kiwi and KIWI_AVAILABLE:
        kiwi = Kiwi()
    else:
        if not KIWI_AVAILABLE:
            print("Note: Using mock data. Install Kiwi for real analysis: pip install kiwipiepy")
        kiwi = MockKiwi()

    # Analyze sentence
    result = kiwi.analyze(text)
    if not result or not result[0]:
        return text

    words = result[0]  # Get first analysis result

    # Reconstruct
    reconstructed_parts = []

    for word_morphs in words:
        word_result = []
        i = 0

        while i < len(word_morphs):
            morph, tag, start, end = word_morphs[i]

            # Check if this is a verb stem
            if is_verb_tag(tag):
                stem = morph
                stem_tag = tag

                # Collect all endings that follow
                endings = []
                j = i + 1
                while j < len(word_morphs) and is_ending_tag(word_morphs[j][1]):
                    endings.append(word_morphs[j])
                    j += 1

                # Apply conjugation rules for each ending
                current_form = stem
                for ending_morph, ending_tag, _, _ in endings:
                    # Get irregularity info
                    irreg = is_irregular_tag(stem_tag)
                    full_tag = stem_tag + ('+' + irreg if irreg else '')

                    # Conjugate
                    current_form = conjugate(current_form, ending_morph, tag=full_tag)

                word_result.append(current_form)
                i = j  # Skip processed endings
            else:
                # Non-verb morpheme: just append
                word_result.append(morph)
                i += 1

        reconstructed_parts.append(''.join(word_result))

    return ''.join(reconstructed_parts)


def demo():
    """Demonstration of sentence reconstruction."""
    print("=" * 70)
    print("Korean Sentence Reconstruction Demo")
    print("=" * 70)
    print()

    test_sentences = [
        "나는 밥을 먹었어요",
        "그는 학교에 갑니다",
        "아이가 노는 모습이 예뻐요"
    ]

    for sentence in test_sentences:
        # Try real Kiwi first
        reconstructed = reconstruct_sentence(sentence, use_real_kiwi=True)
        print(f"입력: {sentence}")
        print(f"출력: {reconstructed}")
        print()

    print("=" * 70)
    if not KIWI_AVAILABLE:
        print("Note: Using mock data. Install Kiwi for real analysis:")
        print("  pip install kiwipiepy")
    else:
        print("Using real Kiwi morphological analyzer")
    print("=" * 70)


if __name__ == '__main__':
    demo()
