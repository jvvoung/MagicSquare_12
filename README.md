# MagicSquare

n×n 정사각 격자에 1부터 n²까지의 정수를 중복 없이 배치하여, 모든 **행·열·대각선의 합**이 동일한 **마방진(magic square)** 을 생성·검증하는 프로젝트입니다.

[ECB(Entity-Control-Boundary)](.cursor/rules/magicsquare-ecb-architecture.mdc) 아키텍처와 **TDD**를 기반으로 개발합니다.

## 목표

| 구분 | 내용 |
|------|------|
| 생성 | 홀수 차수 마방진 (시아라스 방법, Siamese method) |
| 검증 | magic constant, 값 범위, 중복 여부 |
| 오류 처리 | n ≤ 0, 짝수 n 등 잘못된 입력에 대한 명시적 예외 |

## 도메인 용어

| 용어 | 정의 |
|------|------|
| **order** | 마방진 차수 n (격자 한 변 길이) |
| **magic constant** | 행·열·대각선 공통 합: `n × (n² + 1) / 2` |
| **Siamese method** | 홀수 차수 마방진 생성 알고리즘 |

## 요구 사항

- Python 3.10 이상
- [pytest](https://docs.pytest.org/) (테스트)
- [pytest-cov](https://pytest-cov.readthedocs.io/) (커버리지, 선택)

## 빠른 시작

```bash
# 저장소 루트에서
cd MagicSquare_12

# 가상 환경 (권장)
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS

pip install pytest pytest-cov

# 테스트 실행
pytest

# 커버리지 (목표 80% 이상)
pytest --cov=entity --cov=control --cov-report=term-missing
```

## 아키텍처 (ECB)

```
boundary  →  control  →  entity
 (I/O)      (use case)   (도메인)
```

| 레이어 | 역할 | 예시 경로 |
|--------|------|-----------|
| **entity** | 도메인 모델·규칙·알고리즘 | `entity/user.py`, `entity/magic_square.py` (예정) |
| **control** | 유스케이스 조율 | `control/generate_magic_square.py` (예정) |
| **boundary** | CLI·API 등 입출력 | `boundary/cli/main.py` (예정) |

**의존 방향**: boundary → control → entity (단방향만 허용)

자세한 규칙은 [`.cursorrules`](.cursorrules) 및 [`.cursor/rules/`](.cursor/rules/)를 참고하세요.

## 구현 현황

| 모듈 | 상태 | 설명 |
|------|------|------|
| `entity/user.py` | ✅ 완료 | 불변 `User` 값 객체, 검증·예외 처리 |
| `entity/magic_square.py` | ⏳ 예정 | 마방진 도메인 모델 |
| `entity/algorithms/siamese.py` | ⏳ 예정 | 홀수 차수 생성 |
| `control/` | ⏳ 예정 | 생성·검증 유스케이스 |
| `boundary/` | ⏳ 예정 | CLI 진입점 |

## 디렉터리 구조

```
MagicSquare_12/
├── README.md
├── pyproject.toml
├── .cursorrules
├── entity/                 # 도메인 레이어
│   ├── exceptions.py
│   └── user.py
├── tests/
│   ├── conftest.py
│   └── entity/
│       └── test_user.py
├── control/                # (예정)
├── boundary/               # (예정)
└── Report/                  # 개발 보고서
```

## 개발 규칙 요약

- **TDD**: red → green → refactor (`tests/`에 실패 테스트를 먼저 작성)
- **스타일**: PEP 8, 타입 힌트, Google 스타일 docstring, 줄 길이 88 (Black)
- **테스트**: AAA 패턴, `test_<module>.py` 명명, 커버리지 80% 이상
- **금지**: entity/control에서 `print`·파일 I/O, boundary에서 entity 직접 import 등

## User 엔티티 (현재 API)

```python
from entity.user import User

user = User.create(
    user_id="user-001",
    display_name="Magic Fan",
    email="fan@example.com",
)

updated = user.with_display_name("Square Master")
```

검증 실패 시 `entity.exceptions.InvalidUserError`가 발생합니다.

## 관련 문서

- [MagicSquare 개발 보고서](Report/MagicSquare_개발보고서.md) — 구현 현황·테스트 결과
- [MagicSquare C++ 커서룰 개발 보고서](Report/MagicSquare_C++_커서룰_개발보고서.md) — C++ 마이그레이션 규칙 참고

## 라이선스

라이선스는 저장소 소유자가 지정합니다.
