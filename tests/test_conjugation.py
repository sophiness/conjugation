"""
Test cases for Korean verb conjugation.

Tests all conjugation patterns:
1. Regular conjugation
2. ㄹ-drop
3. 으-drop
4. Irregulars: ㅅ, ㄷ, ㅂ, 러, ㅎ, 우, 여, 르
5. 이다 conjugation
6. Vowel harmony
7. Contractions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conjugator import conjugate


def test_regular_conjugation():
    """Test regular conjugation."""
    print("=== Regular Conjugation ===")

    tests = [
        ('먹', '어요', None, '먹어요'),
        ('먹', '는다', None, '먹는다'),
        ('먹', '었다', None, '먹었다'),
        ('살', '고', None, '살고'),
        ('울', '고', None, '울고'),
        ('잡', 'ㄴ', None, '잡은'),  # With epenthetic ㅡ
    ]

    for stem, ending, tag, expected in tests:
        result = conjugate(stem, ending, tag)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stem} + {ending} = {result} (expected: {expected})")


def test_l_drop():
    """Test ㄹ-drop rule."""
    print("\n=== ㄹ-Drop Rule ===")

    tests = [
        ('놀', '는', None, '노는'),
        ('놀', 'ㄴ', None, '논'),
        ('살', '는', None, '사는'),
        ('만들', '는', None, '만드는'),
    ]

    for stem, ending, tag, expected in tests:
        result = conjugate(stem, ending, tag)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stem} + {ending} = {result} (expected: {expected})")


def test_eu_drop():
    """Test 으-drop rule."""
    print("\n=== 으-Drop Rule ===")

    tests = [
        ('쓰', '어', None, '써'),
        ('크', '어', None, '커'),
        ('크', '었다', None, '컸다'),
        ('쓰', '었다', None, '썼다'),
    ]

    for stem, ending, tag, expected in tests:
        result = conjugate(stem, ending, tag)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stem} + {ending} = {result} (expected: {expected})")


def test_s_irregular():
    """Test ㅅ irregular."""
    print("\n=== ㅅ Irregular ===")

    tests = [
        ('짓', '어', 'VV+ㅅ불규칙', '지어'),
        ('낫', '아', 'VV+ㅅ불규칙', '나아'),
        ('잇', '어', 'VV+ㅅ불규칙', '이어'),
    ]

    for stem, ending, tag, expected in tests:
        result = conjugate(stem, ending, tag)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stem} + {ending} = {result} (expected: {expected})")


def test_d_irregular():
    """Test ㄷ irregular."""
    print("\n=== ㄷ Irregular ===")

    tests = [
        ('듣', '어', 'VV+ㄷ불규칙', '들어'),
        ('걷', '어', 'VV+ㄷ불규칙', '걸어'),
        ('묻', '어', 'VV+ㄷ불규칙', '물어'),  # 묻다 (to ask)
    ]

    for stem, ending, tag, expected in tests:
        result = conjugate(stem, ending, tag)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stem} + {ending} = {result} (expected: {expected})")


def test_b_irregular():
    """Test ㅂ irregular."""
    print("\n=== ㅂ Irregular ===")

    tests = [
        ('돕', '아', 'VV+ㅂ불규칙', '도와'),
        ('돕', '어', 'VV+ㅂ불규칙', '도와'),
        ('아름답', '어', 'VA+ㅂ불규칙', '아름다워'),
        ('춥', '어', 'VA+ㅂ불규칙', '추워'),
    ]

    for stem, ending, tag, expected in tests:
        result = conjugate(stem, ending, tag)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stem} + {ending} = {result} (expected: {expected})")


def test_h_irregular():
    """Test ㅎ irregular."""
    print("\n=== ㅎ Irregular ===")

    tests = [
        ('파랗', '아', 'VA+ㅎ불규칙', '파래'),
        ('빨갛', '아', 'VA+ㅎ불규칙', '빨개'),
        ('하얗', '아', 'VA+ㅎ불규칙', '하얘'),
    ]

    for stem, ending, tag, expected in tests:
        result = conjugate(stem, ending, tag)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stem} + {ending} = {result} (expected: {expected})")


def test_reu_irregular():
    """Test 르 irregular."""
    print("\n=== 르 Irregular ===")

    tests = [
        ('흐르', '어', None, '흘러'),
        ('부르', '어', None, '불러'),
        ('모르', '아', None, '몰라'),
        ('다르', '아', None, '달라'),
    ]

    for stem, ending, tag, expected in tests:
        result = conjugate(stem, ending, tag)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stem} + {ending} = {result} (expected: {expected})")


def test_u_irregular():
    """Test 우 irregular (푸다)."""
    print("\n=== 우 Irregular (푸다) ===")

    tests = [
        ('푸', '어', None, '퍼'),
        ('푸', '었다', None, '펐다'),
    ]

    for stem, ending, tag, expected in tests:
        result = conjugate(stem, ending, tag)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stem} + {ending} = {result} (expected: {expected})")


def test_yeo_irregular():
    """Test 여 irregular (하다)."""
    print("\n=== 여 Irregular (하다) ===")

    tests = [
        ('하', '어', 'VV', '해'),
        ('하', '어요', 'VV', '해요'),
        ('하', '았다', 'VV', '했다'),
    ]

    for stem, ending, tag, expected in tests:
        result = conjugate(stem, ending, tag)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stem} + {ending} = {result} (expected: {expected})")


def test_ida_conjugation():
    """Test 이다 conjugation."""
    print("\n=== 이다 Conjugation ===")

    tests = [
        # With final consonant
        ('이', '다', None, '학생', '이다'),
        ('이', '었다', None, '학생', '이었다'),

        # Without final consonant
        ('이', '었다', None, '나무', '였다'),
        ('이', '어서', None, '나무', '여서'),
        ('이', '에요', None, '나무', '예요'),
        ('이', '야', None, '나무', '야'),
    ]

    for stem, ending, tag, prev_word, expected in tests:
        result = conjugate(stem, ending, tag, prev_word)
        status = "✓" if result == expected else "✗"
        print(f"{status} {prev_word} + {stem} + {ending} = {prev_word + result} (expected: {prev_word + expected})")


def test_vowel_harmony():
    """Test vowel harmony."""
    print("\n=== Vowel Harmony ===")

    tests = [
        ('먹', '어요', None, '먹어요'),  # Dark vowel → 어
        ('가', '아요', None, '가요'),    # Bright vowel → 아 (with contraction)
        ('보', '아요', None, '봐요'),    # Bright vowel → 아 (with contraction)
    ]

    for stem, ending, tag, expected in tests:
        result = conjugate(stem, ending, tag)
        status = "✓" if result == expected else "✗"
        print(f"{status} {stem} + {ending} = {result} (expected: {expected})")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Korean Verb Conjugation Tests")
    print("=" * 50)

    test_regular_conjugation()
    test_l_drop()
    test_eu_drop()
    test_s_irregular()
    test_d_irregular()
    test_b_irregular()
    test_h_irregular()
    test_reu_irregular()
    test_u_irregular()
    test_yeo_irregular()
    test_ida_conjugation()
    test_vowel_harmony()

    print("\n" + "=" * 50)
    print("Tests completed!")
    print("=" * 50)


if __name__ == '__main__':
    run_all_tests()
