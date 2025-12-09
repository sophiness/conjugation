# Korean Verb Conjugation System (한국어 용언 활용 시스템)

Python으로 구현한 한국어 용언 활용 규칙 시스템입니다. 형태소 분석기(Kiwi) 출력을 기반으로 어간과 어미를 결합하여 올바른 활용형을 생성합니다.

## 주요 기능

### 지원하는 활용 규칙

#### 1. 규칙 활용
- **ㄹ탈락**: 놀 + 는 → 노는
- **으탈락**: 쓰 + 어 → 써
- **모음조화**: 먹 + 어요 → 먹어요, 가 + 아요 → 가요
- **모음축약**: 보 + 아 → 봐, 가 + 아 → 가
- **매개모음**: 잡 + ㄴ → 잡은

#### 2. 불규칙 활용 (어간의 불규칙)
- **ㅅ불규칙**: 짓 + 어 → 지어
- **ㄷ불규칙**: 듣 + 어 → 들어
- **ㅂ불규칙**: 돕 + 아 → 도와, 아름답 + 어 → 아름다워
- **ㅎ불규칙**: 파랗 + 아 → 파래

#### 3. 특수 어간 처리
- **우불규칙**: 푸 + 어 → 퍼 (푸다만 해당)
- **여불규칙**: 하 + 어 → 해 (하다 계열)
- **르불규칙**: 흐르 + 어 → 흘러, 부르 + 어 → 불러

#### 4. 이다 활용
- 받침 있음: 학생 + 이다 → 학생이다
- 받침 없음: 나무 + 이었다 → 나무였다

## 설치

```bash
git clone <repository-url>
cd conjugation
pip install -r requirements.txt
```

**의존성:**
- `pynini`: FST 규칙 구현
- `kiwipiepy`: 형태소 분석기 (문장 복원용)

**참고**: 의존성 설치 없이도 기본 활용 기능은 사용 가능 (mock 모드)

## 사용법

### 기본 사용 (어간 + 어미)

```python
from conjugator import conjugate

# 규칙 활용
result = conjugate('먹', '어요')  # 먹어요
result = conjugate('살', '아요')  # 살아요

# ㄹ탈락
result = conjugate('놀', '는')    # 노는

# 으탈락
result = conjugate('쓰', '어')    # 써

# 불규칙 활용 (태그 지정 필요)
result = conjugate('짓', '어', tag='VV+ㅅ불규칙')  # 지어
result = conjugate('듣', '어', tag='VV+ㄷ불규칙')  # 들어
result = conjugate('돕', '아', tag='VV+ㅂ불규칙')  # 도와

# 특수 어간
result = conjugate('푸', '어')    # 퍼 (우불규칙)
result = conjugate('하', '어', tag='VV')  # 해 (여불규칙)
result = conjugate('흐르', '어')  # 흘러 (르불규칙)

# 이다 활용
result = conjugate('이', '었다', prev_word='나무')  # 였다

# 자음 자모로 시작하는 어미 (모아쓰기 자동 처리)
result = conjugate('가', 'ㅂ니다')  # 갑니다
result = conjugate('먹', 'ㅂ니다')  # 먹습니다
result = conjugate('가', 'ㄹ까요')  # 갈까요
```

### 문장 복원 (Kiwi 형태소 분석기 통합)

```python
from sentence_reconstructor import reconstruct_sentence

# 완전한 문장 입력 → 형태소 분석 → 활용 규칙 적용 → 복원
result = reconstruct_sentence("나는 밥을 먹었어요")
print(result)  # 나는밥을먹었어요 (띄어쓰기 없음)

result = reconstruct_sentence("그는 학교에 갑니다")
print(result)  # 그는학교에갑니다
```

**참고**: Kiwi 설치 필요 (`pip install kiwipiepy`), 설치 안 되어 있으면 mock 데이터 사용

### 예제 실행

```bash
# 기본 사용 예제
python examples/basic_usage.py

# 테스트 실행
python tests/test_conjugation.py
```

## 프로젝트 구조

```
conjugation/
├── README.md                    # 프로젝트 문서
├── requirements.txt             # 의존성 패키지 (선택적)
├── utils.py                     # 한글 자모 분해/조합 유틸리티
├── conjugator.py                # 메인 활용기 (분기 로직)
├── sentence_reconstructor.py    # 문장 복원 시스템 (Kiwi 통합)
├── data/
│   └── reu_irregular_stems.txt  # 르불규칙 어간 사전
├── rules/                       # 활용 규칙 모듈
│   ├── __init__.py
│   ├── fst_utils.py             # FST 공통 유틸리티 (pynini)
│   ├── fst_vowel_harmony.py     # FST 모음조화
│   ├── vowel_harmony.py         # 모음조화 (Python)
│   ├── contraction.py           # 축약 규칙
│   ├── l_drop.py                # ㄹ탈락
│   ├── eu_drop.py               # 으탈락
│   ├── ida.py                   # 이다 활용
│   ├── irregular_s.py           # ㅅ불규칙
│   ├── irregular_d.py           # ㄷ불규칙
│   ├── irregular_b.py           # ㅂ불규칙
│   ├── irregular_h.py           # ㅎ불규칙
│   ├── irregular_reo.py         # 러불규칙
│   ├── irregular_reu.py         # 르불규칙
│   ├── irregular_u.py           # 우불규칙
│   ├── irregular_yeo.py         # 여불규칙
│   └── regular.py               # 규칙 활용
├── tests/
│   └── test_conjugation.py      # 테스트 케이스
└── examples/
    └── basic_usage.py           # 사용 예제
```

## 활용 규칙 적용 순서 (Flowchart)

```
입력 (어간 + 어미)
    ↓
1. ㄹ탈락 검사
    ↓ (적용 안됨)
2. 이다 검사
    ↓ (아님)
3. 어미 유형 판별
    ├─ 불완전자음어미 → 모아쓰기
    ├─ 자음어미 → 단순결합 또는 매개모음
    └─ 모음어미
        ↓
    4. 불규칙 태그 검사 (ㅅ, ㄷ, ㅂ, 러, ㅎ)
        ↓ (없음)
    5. 특수 어간 검사
        ├─ 우불규칙 (푸다)
        ├─ 여불규칙 (하다)
        └─ 르불규칙 (사전 기반)
            ↓ (해당 없음)
    6. 으탈락 검사
        ↓ (해당 없음)
    7. 규칙 활용 + 모음조화 + 축약
```

## 기술 세부사항

### 구현 방식
- **하이브리드 구조**: Python 분기 처리 + pynini FST 규칙
- **FST 규칙**: 각 형태소 규칙을 pynini FST로 구현 (완전 구현 완료)
- **모듈화 설계**: 각 규칙을 독립적인 모듈로 분리하여 관리
- **어간-어미 경계**: FST는 어간과 어미의 경계에서만 적용

### FST 구현 모듈
모든 활용 규칙이 FST로 구현되었습니다:

**기본 규칙 (FST):**
- `rules/fst_vowel_harmony.py` - 모음조화 FST
- `rules/fst_l_drop.py` - ㄹ탈락 FST
- `rules/fst_eu_drop.py` - 으탈락 FST
- `rules/fst_contraction.py` - 축약 규칙 FST
- `rules/fst_regular.py` - 규칙 활용 FST

**불규칙 활용 (FST):**
- `rules/fst_irregular_s.py` - ㅅ불규칙 FST
- `rules/fst_irregular_d.py` - ㄷ불규칙 FST
- `rules/fst_irregular_b.py` - ㅂ불규칙 FST
- `rules/fst_irregular_h.py` - ㅎ불규칙 FST
- `rules/fst_irregular_reo.py` - 러불규칙 FST

**특수 어간 (FST):**
- `rules/fst_irregular_u.py` - 우불규칙 FST (푸다)
- `rules/fst_irregular_yeo.py` - 여불규칙 FST (하다)
- `rules/fst_irregular_reu.py` - 르불규칙 FST

**Python 버전 (호환성):**
각 FST 모듈에는 대응하는 Python 버전이 존재합니다 (`rules/*.py` without `fst_` prefix).
Python 버전은 pynini 설치가 불가능한 환경에서 fallback으로 사용됩니다.

### 한글 처리
- 한글 자모 분해/조합: `utils.py`
- 유니코드 기반 초성/중성/종성 처리
- 자모 문자열로 변환 후 규칙 적용

### 모음조화
- 양성모음 (ㅏ, ㅗ) → 아 계열
- 음성모음 (ㅓ, ㅜ, ㅡ) → 어 계열

### 축약 규칙
- 규칙활용: ㅣ+ㅓ→ㅕ, ㅜ+ㅓ→ㅝ, ㅗ+ㅏ→ㅘ
- 예외: 기-, 미-, 비-, 띠- 어간은 축약 안함
- ㅂ불규칙: ㅗ+ㅏ→ㅘ, ㅜ+ㅓ→ㅝ
- ㅎ불규칙: ㅏ+ㅇ+ㅏ→ㅐ, ㅓ+ㅇ+ㅓ→ㅔ

### 불규칙 활용 우선순위
1. 태그 기반 불규칙 (ㅅ, ㄷ, ㅂ, 러, ㅎ)
2. 우불규칙 (푸다)
3. 여불규칙 (하다)
4. 르불규칙 (사전 기반)
5. 으탈락
6. 규칙활용

## 제한사항

- Kiwi 형태소 분석기 출력 형식 기준
- 일부 불규칙 활용은 태그 필요 (ㅅ, ㄷ, ㅂ, 러, ㅎ)
- 르불규칙은 사전 기반 (완전하지 않을 수 있음)
- 구현하지 않은 규칙:
  - 주다 불규칙 (Kiwi에서 별도 처리)
  - 아니하다 불규칙 (Kiwi에서 별도 처리)
  - 거라/너라/오 불규칙 (특수 명령형)

## 참고문헌

- 한국어 용언 활용 규칙
- Kiwi 형태소 분석기 태그셋
- 국립국어원 표준국어대사전

## 라이선스

MIT License

## 기여

이슈와 풀 리퀘스트를 환영합니다!
