# MagicSquare 프로젝트 개발 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트명 | MagicSquare |
| 작성일 | 2026-05-18 |
| 보고서 버전 | 1.0 |
| 작성 기준 | `.cursorrules.yaml` |

---

## 1. 프로젝트 개요

MagicSquare는 **n×n 정사각 격자**에 1부터 n²까지의 정수를 중복 없이 배치하여, 모든 **행·열·대각선의 합이 동일한 마방진(magic square)** 을 생성·검증하는 Python 프로젝트이다.

### 1.1 목표

- 홀수 차수 마방진 생성 및 검증 (시아라스 방법 기본)
- 잘못된 입력에 대한 명시적 오류 처리
- ECB(Entity-Control-Boundary) 아키텍처 및 TDD 기반 개발

### 1.2 현재 범위

| 구분 | 상태 |
|------|------|
| 프로젝트 규칙 (`.cursorrules.yaml`) | 완료 |
| entity — `User` 엔티티 | 완료 |
| entity — `MagicSquare` / 알고리즘 | 미구현 |
| control 레이어 | 미구현 |
| boundary 레이어 (CLI/API) | 미구현 |

---

## 2. 아키텍처 (ECB 패턴)

### 2.1 레이어 정의

```
boundary  →  control  →  entity
 (I/O)      (use case)   (도메인)
```

| 레이어 | 역할 | 예시 경로 |
|--------|------|-----------|
| **boundary** | UI, API, CLI 등 외부 입출력 | `boundary/cli/main.py` |
| **control** | 비즈니스 로직·유스케이스 조율 | `control/generate_magic_square.py` |
| **entity** | 도메인 데이터·규칙·알고리즘 | `entity/user.py`, `entity/magic_square.py` |

### 2.2 의존성 규칙

- **허용**: boundary → control → entity (단방향)
- **금지**: entity → control/boundary, control → boundary, boundary → entity 직접 참조

---

## 3. 개발 규칙 요약 (`.cursorrules.yaml`)

### 3.1 코드 스타일

| 항목 | 규칙 |
|------|------|
| Python | 3.10+ |
| 스타일 | PEP8 엄격 준수 |
| 타입 힌트 | 모든 함수 파라미터·반환값 필수 |
| docstring | Google 스타일, public 메서드 필수 |
| 줄 길이 | 88 (Black 기준) |

### 3.2 TDD 3단계

| 단계 | 요약 |
|------|------|
| **red** | 실패하는 테스트 먼저 작성, 실패 확인 후 진행 |
| **green** | 최소 코드로 테스트 통과, 리팩터링 금지 |
| **refactor** | 동작 유지·구조 개선, 커버리지 80% 이상 유지 |

### 3.3 테스트

- 프레임워크: **pytest**
- 패턴: **AAA** (Arrange-Act-Assert)
- 커버리지 최소: **80%**
- 파일·함수 명명: `test_<module>.py`, `test_` 접두사

---

## 4. 구현 현황

### 4.1 User 엔티티 (`entity/user.py`)

마방진 애플리케이션 사용자를 표현하는 **불변 값 객체**이다.

#### 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `user_id` | `str` | 고유 식별자 (비어 있지 않음, 최대 64자) |
| `display_name` | `str` | 표시 이름 (2~50자) |
| `email` | `str \| None` | 선택 이메일 (형식 검증) |

#### public API

| 메서드 | 설명 |
|--------|------|
| `User.create(...)` | 검증 후 인스턴스 생성 |
| `with_display_name(name)` | 표시 이름 변경 복사본 반환 |
| `with_email(email)` | 이메일 변경·제거 복사본 반환 |

#### 도메인 예외

- `InvalidUserError` (`entity/exceptions.py`) — 검증 실패 시 발생

### 4.2 디렉터리 구조 (현재)

```
MagicSquare_12/
├── .cursorrules.yaml
├── pyproject.toml
├── entity/
│   ├── __init__.py
│   ├── exceptions.py
│   └── user.py
├── tests/
│   ├── conftest.py
│   └── entity/
│       └── test_user.py
└── report/
    └── MagicSquare_개발보고서.md
```

### 4.3 미구현 항목 (규칙상 계획)

```
boundary/          control/              entity/
├── cli/           ├── generate_*.py       ├── magic_square.py
└── api/           └── validate_*.py       ├── validators.py
                                              └── algorithms/siamese.py
```

---

## 5. 테스트 결과

### 5.1 실행 환경

- Python 3.13.7
- pytest 9.0.3, pytest-cov 7.1.0

### 5.2 실행 명령

```bash
cd c:\DEV\MagicSquare_12
pytest --cov=entity --cov=control --cov-report=term-missing
```

### 5.3 결과 요약

| 항목 | 결과 |
|------|------|
| 테스트 수 | 12 |
| 통과 | 12 |
| 실패 | 0 |
| entity 커버리지 | **100%** (목표 80% 충족) |

### 5.4 테스트 케이스 목록

| 클래스 | 테스트 | 검증 내용 |
|--------|--------|-----------|
| TestUserCreate | `test_create_valid_user_with_email` | 정상 생성 (이메일 포함) |
| TestUserCreate | `test_create_valid_user_without_email` | 정상 생성 (이메일 없음) |
| TestUserCreate | `test_empty_user_id_raises` | 빈 user_id 오류 |
| TestUserCreate | `test_user_id_too_long_raises` | user_id 길이 초과 |
| TestUserCreate | `test_display_name_too_short_raises` | display_name 최소 길이 미달 |
| TestUserCreate | `test_display_name_too_long_raises` | display_name 최대 길이 초과 |
| TestUserCreate | `test_invalid_email_raises` | 잘못된 이메일 형식 |
| TestUserCreate | `test_empty_email_string_raises` | 공백만 있는 이메일 |
| TestUserImmutability | `test_with_display_name_returns_new_instance` | 불변 업데이트 |
| TestUserImmutability | `test_with_email_returns_new_instance` | 이메일 변경 |
| TestUserImmutability | `test_with_email_none_clears_email` | 이메일 제거 |
| TestUserImmutability | `test_frozen_user_is_hashable` | frozen·hashable |

---

## 6. 규칙 준수 점검

| 규칙 | User 구현 | 비고 |
|------|-----------|------|
| ECB entity 레이어 배치 | ✅ | I/O·pytest 미사용 |
| type hints | ✅ | 전 메서드 적용 |
| Google docstring | ✅ | public 메서드 적용 |
| print / bare except 금지 | ✅ | 미사용 |
| 매직 넘버 | ✅ | `MIN_*`, `MAX_*` 상수화 |
| TDD | ✅ | 테스트 12건 동반 구현 |

---

## 7. 이슈 및 권고 사항

### 7.1 Cursor 규칙 파일 적용

- 현재 파일명: `.cursorrules.yaml`
- Cursor 공식 자동 로드: `.cursorrules` 또는 `.cursor/rules/*.mdc`
- **권고**: 에이전트가 규칙을 항상 참조하도록 `.cursor/rules/` 로 이전하거나 채팅에서 `@.cursorrules.yaml` 로 명시 참조

### 7.2 다음 개발 우선순위

1. `entity/magic_square.py` — 마방진 도메인 모델 및 magic constant
2. `entity/algorithms/siamese.py` — 홀수 차수 생성 알고리즘
3. `control/generate_magic_square.py` — 생성 유스케이스
4. `boundary/cli/main.py` — CLI 진입점

---

## 8. 결론

MagicSquare 프로젝트는 **ECB 아키텍처·TDD·엄격한 코드 스타일**을 정의한 `.cursorrules.yaml`을 기반으로 개발을 시작하였다. 현재 **entity 레이어의 `User` 엔티티**가 완료되었으며, 단위 테스트 12건 전부 통과 및 entity 커버리지 100%를 달성하였다. 마방진 핵심 기능(control·boundary·MagicSquare entity)은 후속 스프린트에서 동일 규칙으로 확장할 예정이다.

---

*본 보고서는 프로젝트 저장소 `c:\DEV\MagicSquare_12` 기준으로 작성되었다.*
