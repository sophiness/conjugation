"""
Utility functions for Korean character manipulation.
Handles decomposition and composition of Hangul syllables.
"""

# 한글 유니코드 범위: AC00-D7A3
HANGUL_BASE = 0xAC00
HANGUL_END = 0xD7A3

# 자모 유니코드 범위
JAMO_CHOSUNG_BASE = 0x1100  # ᄀ
JAMO_CHOSUNG_END = 0x1112   # ᄒ
JAMO_JUNGSUNG_BASE = 0x1161 # ᅡ
JAMO_JUNGSUNG_END = 0x1175  # ᅵ
JAMO_JONGSUNG_BASE = 0x11A8 # ᆨ
JAMO_JONGSUNG_END = 0x11C2  # ᇂ

# 호환용 자모 범위 (ㄱ-ㅎ, ㅏ-ㅣ)
COMPAT_JAMO_BASE = 0x3131
COMPAT_JAMO_END = 0x318E

# 초성, 중성, 종성 리스트
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 자모 인덱스 딕셔너리
CHOSUNG_DICT = {char: idx for idx, char in enumerate(CHOSUNG_LIST)}
JUNGSUNG_DICT = {char: idx for idx, char in enumerate(JUNGSUNG_LIST)}
JONGSUNG_DICT = {char: idx for idx, char in enumerate(JONGSUNG_LIST)}

def is_hangul(char):
    """Check if a character is a Hangul syllable."""
    if not char:
        return False
    code = ord(char)
    return HANGUL_BASE <= code <= HANGUL_END


def is_jamo(char):
    """Check if a character is a compatibility jamo (ㄱ-ㅎ, ㅏ-ㅣ)."""
    if not char:
        return False
    code = ord(char)
    return COMPAT_JAMO_BASE <= code <= COMPAT_JAMO_END


def is_consonant_jamo(char):
    """Check if a character is a consonant jamo (ㄱ-ㅎ)."""
    return char in CHOSUNG_LIST or char in JONGSUNG_LIST[1:]  # Exclude empty string


def is_vowel_jamo(char):
    """Check if a character is a vowel jamo (ㅏ-ㅣ)."""
    return char in JUNGSUNG_LIST


def decompose(char):
    """
    Decompose a Hangul syllable into jamo (chosung, jungsung, jongsung).

    Args:
        char: A single Hangul character

    Returns:
        tuple: (chosung, jungsung, jongsung)
    """
    if not is_hangul(char):
        return (char, '', '')

    code = ord(char) - HANGUL_BASE
    jongsung_idx = code % 28
    jungsung_idx = ((code - jongsung_idx) // 28) % 21
    chosung_idx = ((code - jongsung_idx) // 28) // 21

    return (CHOSUNG_LIST[chosung_idx],
            JUNGSUNG_LIST[jungsung_idx],
            JONGSUNG_LIST[jongsung_idx])


def compose(chosung, jungsung, jongsung=''):
    """
    Compose jamo into a Hangul syllable.

    Args:
        chosung: Initial consonant (초성)
        jungsung: Medial vowel (중성)
        jongsung: Final consonant (종성), optional

    Returns:
        str: Composed Hangul character
    """
    if chosung not in CHOSUNG_DICT or jungsung not in JUNGSUNG_DICT:
        return chosung + jungsung + (jongsung if jongsung else '')

    chosung_idx = CHOSUNG_DICT[chosung]
    jungsung_idx = JUNGSUNG_DICT[jungsung]
    jongsung_idx = JONGSUNG_DICT.get(jongsung, 0)

    code = HANGUL_BASE + (chosung_idx * 21 + jungsung_idx) * 28 + jongsung_idx
    return chr(code)


def decompose_str(text):
    """
    Decompose a string into a sequence of jamo.

    Args:
        text: Input string

    Returns:
        str: Jamo sequence
    """
    result = []
    for char in text:
        if is_hangul(char):
            cho, jung, jong = decompose(char)
            result.append(cho)
            result.append(jung)
            if jong:
                result.append(jong)
        else:
            result.append(char)
    return ''.join(result)


def compose_str(jamo_str):
    """
    Compose a jamo sequence into Hangul syllables.

    Args:
        jamo_str: Jamo sequence string

    Returns:
        str: Composed Hangul string
    """
    result = []
    i = 0

    while i < len(jamo_str):
        char = jamo_str[i]

        # Check if this is a chosung (initial consonant)
        if char in CHOSUNG_DICT:
            chosung = char
            i += 1

            # Get jungsung (medial vowel)
            if i < len(jamo_str) and jamo_str[i] in JUNGSUNG_DICT:
                jungsung = jamo_str[i]
                i += 1

                # Get jongsung (final consonant) if exists
                jongsung = ''
                if i < len(jamo_str) and jamo_str[i] in JONGSUNG_DICT and jamo_str[i] != '':
                    # Look ahead: if next char is a vowel, this consonant is chosung of next syllable
                    # Otherwise, it's jongsung of current syllable
                    if i + 1 < len(jamo_str) and jamo_str[i + 1] in JUNGSUNG_DICT:
                        # This consonant starts the next syllable
                        pass
                    else:
                        # This consonant ends the current syllable
                        jongsung = jamo_str[i]
                        i += 1

                result.append(compose(chosung, jungsung, jongsung))
            else:
                result.append(chosung)
        else:
            result.append(char)
            i += 1

    return ''.join(result)


def get_final_consonant(text):
    """
    Get the final consonant (jongsung) of the last character.

    Args:
        text: Input string

    Returns:
        str: Final consonant, empty string if none
    """
    if not text:
        return ''

    last_char = text[-1]
    if is_hangul(last_char):
        _, _, jong = decompose(last_char)
        return jong
    return ''


def has_final_consonant(text):
    """
    Check if the last character has a final consonant (받침).

    Args:
        text: Input string

    Returns:
        bool: True if has final consonant
    """
    return bool(get_final_consonant(text))


def get_vowel(text):
    """
    Get the last vowel (jungsung) from text.

    Args:
        text: Input string

    Returns:
        str: Last vowel character
    """
    if not text:
        return ''

    last_char = text[-1]
    if is_hangul(last_char):
        _, jung, _ = decompose(last_char)
        return jung
    return ''


def is_bright_vowel(vowel):
    """
    Check if a vowel is bright (양성 모음: ㅏ, ㅗ).

    Args:
        vowel: Vowel character

    Returns:
        bool: True if bright vowel
    """
    return vowel in ['ㅏ', 'ㅗ', 'ㅑ', 'ㅛ', 'ㅘ']


def is_dark_vowel(vowel):
    """
    Check if a vowel is dark (음성 모음: ㅓ, ㅜ, ㅡ, etc.).

    Args:
        vowel: Vowel character

    Returns:
        bool: True if dark vowel
    """
    return not is_bright_vowel(vowel)
