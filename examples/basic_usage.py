"""
Basic usage examples for Korean verb conjugation system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conjugator import conjugate


def basic_examples():
    """Basic conjugation examples."""
    print("=== Basic Conjugation Examples ===\n")

    # Regular verbs
    print("1. Regular verbs:")
    print(f"   먹다 (to eat): 먹 + 어요 = {conjugate('먹', '어요')}")
    print(f"   살다 (to live): 살 + 아요 = {conjugate('살', '아요')}")
    print(f"   울다 (to cry): 울 + 어요 = {conjugate('울', '어요')}")

    # ㄹ-drop
    print("\n2. ㄹ-drop:")
    print(f"   놀다 (to play): 놀 + 는 = {conjugate('놀', '는')}")
    print(f"   살다 (to live): 살 + ㄴ = {conjugate('살', 'ㄴ')}")

    # 으-drop
    print("\n3. 으-drop:")
    print(f"   쓰다 (to write): 쓰 + 어 = {conjugate('쓰', '어')}")
    print(f"   크다 (to be big): 크 + 었다 = {conjugate('크', '었다')}")


def irregular_examples():
    """Irregular conjugation examples."""
    print("\n=== Irregular Conjugation Examples ===\n")

    # ㅅ irregular
    print("1. ㅅ irregular:")
    print(f"   짓다 (to build): 짓 + 어 = {conjugate('짓', '어', 'VV+ㅅ불규칙')}")

    # ㄷ irregular
    print("\n2. ㄷ irregular:")
    print(f"   듣다 (to hear): 듣 + 어 = {conjugate('듣', '어', 'VV+ㄷ불규칙')}")

    # ㅂ irregular
    print("\n3. ㅂ irregular:")
    print(f"   돕다 (to help): 돕 + 아 = {conjugate('돕', '아', 'VV+ㅂ불규칙')}")
    print(f"   아름답다 (beautiful): 아름답 + 어 = {conjugate('아름답', '어', 'VA+ㅂ불규칙')}")

    # ㅎ irregular
    print("\n4. ㅎ irregular:")
    print(f"   파랗다 (to be blue): 파랗 + 아 = {conjugate('파랗', '아', 'VA+ㅎ불규칙')}")

    # 르 irregular
    print("\n5. 르 irregular:")
    print(f"   흐르다 (to flow): 흐르 + 어 = {conjugate('흐르', '어')}")
    print(f"   부르다 (to call): 부르 + 어 = {conjugate('부르', '어')}")

    # 우 irregular
    print("\n6. 우 irregular:")
    print(f"   푸다 (to scoop): 푸 + 어 = {conjugate('푸', '어')}")

    # 여 irregular
    print("\n7. 여 irregular:")
    print(f"   하다 (to do): 하 + 어 = {conjugate('하', '어', 'VV')}")
    print(f"   하다 (to do): 하 + 았다 = {conjugate('하', '았다', 'VV')}")


def tense_examples():
    """Tense conjugation examples."""
    print("\n=== Tense Conjugation Examples ===\n")

    stem = '먹'

    print("먹다 (to eat):")
    print(f"  Present: {conjugate(stem, '어요')}")
    print(f"  Past: {conjugate(stem, '었어요')}")
    print(f"  Future: {conjugate(stem, '을 거예요')}")
    print(f"  Progressive: {conjugate(stem, '고 있어요')}")


def formality_examples():
    """Formality level examples."""
    print("\n=== Formality Level Examples ===\n")

    stem = '가'

    print("가다 (to go):")
    print(f"  Informal: {conjugate(stem, '아')}")
    print(f"  Casual polite: {conjugate(stem, '아요')}")
    print(f"  Formal: {conjugate(stem, 'ㅂ니다')}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Korean Verb Conjugation System - Usage Examples")
    print("=" * 60)

    basic_examples()
    irregular_examples()
    tense_examples()
    formality_examples()

    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()
