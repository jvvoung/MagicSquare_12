# MagicSquare C++ Cursor 룰 개발 보고서

| 항목 | 내용 |
|------|------|
| 프로젝트명 | MagicSquare |
| 문서 구분 | C++ Cursor 규칙 도입 (별도 보고서) |
| 작성일 | 2026-05-18 |
| 보고서 버전 | 1.0 |
| 작성 기준 | `.cursorrules`, `.cursor/rules/*.mdc` |
| 관련 보고서 | `MagicSquare_개발보고서.md` (Python 구현 현황, v1.0) |

---

## 1. 작업 개요

Python 기반 MagicSquare_개선 프로젝트의 Cursor 룰 구조를 참고하여, **C++17·CMake·GoogleTest** 기준의 Cursor 규칙 체계를 `MagicSquare_12`에 도입하였다.

### 1.1 작업 범위

| 작업 | 상태 |
|------|------|
| `.cursor/rules/*.mdc` 5종 작성 | ✅ 완료 |
| `.cursorrules` 통합 (yaml 제거) | ✅ 완료 |
| C++ 소스·CMake 구현 | ⬜ 미착수 (규칙만 정의) |

### 1.2 참고 구조 (Python → C++)

| Python (참고) | C++ (본 프로젝트) |
|---------------|-------------------|
| `magicsquare-python-code-style.mdc` | `magicsquare-cpp-code-style.mdc` |
| pytest, `test_*.py` | GoogleTest, `test_*.cpp` |
| PEP8, Black, type hints | Google C++ Style, clang-format/tidy, Doxygen |
| `entity/*.py` | `include/magicsquare/entity/*.hpp` + `src/` |

---

## 2. 생성된 규칙 파일

### 2.1 루트

| 파일 | 역할 |
|------|------|
| `.cursorrules` | 프로젝트 전체 규칙 (단일 원본, Cursor 자동 로드) |

> **변경**: 기존 `.cursorrules` + `.cursorrules.yaml` 이중 구성을 **`.cursorrules` 하나**로 통합하고 `.cursorrules.yaml`은 삭제함.

### 2.2 `.cursor/rules/` (mdc)

| 파일 | alwaysApply | globs | 내용 |
|------|-------------|-------|------|
| `magicsquare-project.mdc` | true | — | 개요·도메인·범위 |
| `magicsquare-ecb-architecture.mdc` | false | `include/`, `src/` | ECB·의존성·디렉터리 |
| `magicsquare-cpp-code-style.mdc` | false | `*.hpp`, `*.cpp` | 네이밍·헤더·Doxygen |
| `magicsquare-tdd-testing.mdc` | false | `tests/**` | red/green/refactor·GoogleTest |
| `magicsquare-forbidden.mdc` | true | — | 금지 패턴·AI 동작 |

### 2.3 디렉터리 구조 (규칙상 목표)

```
MagicSquare_12/
├── .cursorrules
├── .cursor/rules/              # magicsquare-*.mdc
├── CMakeLists.txt              # (미작성)
├── include/magicsquare/
│   ├── entity/
│   ├── control/
│   └── boundary/
├── src/
│   ├── entity/algorithms/
│   ├── control/
│   └── boundary/cli/
└── tests/
    ├── entity/
    ├── control/
    └── boundary/
```

---

## 3. 규칙 요약

### 3.1 ECB 아키텍처

```
boundary  →  control  →  entity
```

- **허용**: boundary → control → entity
- **금지**: 역방향 의존, boundary → entity 직접 include

### 3.2 코드 스타일 (C++)

- C++17, Google C++ Style Guide
- `clang-format`, `clang-tidy`, 줄 길이 100
- public API: Doxygen (`///`)

### 3.3 TDD·테스트

| 단계 | 요약 |
|------|------|
| red | `tests/` 실패 테스트 먼저 |
| green | 최소 구현만 |
| refactor | 동작 유지, 커버리지 80%+ |

- 실행: `ctest --output-on-failure`
- 필수 케이스: n=1,3,5 / n≤0·짝수 오류 / magic constant·중복 검증

### 3.4 주요 금지 패턴

| 금지 | 대안 |
|------|------|
| entity/control `std::cout`, `printf` | boundary 출력 |
| 매직 넘버 | `magic_constant(order)` |
| boundary → entity 직접 include | control use case |
| public API without test | red에서 `test_*.cpp` 먼저 |

---

## 4. Python 프로토타입과의 관계

| 구분 | Python (`MagicSquare_개발보고서.md`) | C++ (본 문서) |
|------|--------------------------------------|---------------|
| 구현 | `entity/user.py` 등 존재 | 소스 미착수 |
| 규칙 파일 | `.cursorrules.yaml` (보고서 v1.0 기준) | `.cursorrules` + mdc |
| 테스트 | pytest 12건 통과 | GoogleTest 예정 |

Python 코드는 도메인·TDD 검증용 프로토타입으로 유지하며, C++ 구현 시 동일 ECB·TDD 원칙을 적용한다.

---

## 5. 이슈 및 권고

### 5.1 보고서 분리

- **Python 구현 현황**: `report/MagicSquare_개발보고서.md` (v1.0, 변경 없음)
- **C++ Cursor 룰**: `report/MagicSquare_C++_커서룰_개발보고서.md` (본 문서)

### 5.2 다음 단계

1. `CMakeLists.txt` + GoogleTest 연동
2. `entity/magic_square.hpp` — magic constant
3. `siamese.cpp` — 홀수 차수 생성
4. control·boundary 레이어 순차 구현

---

## 6. 결론

MagicSquare_12에 **C++ 전용 Cursor 규칙** (`.cursorrules` + mdc 5종)을 도입하였다. 기존 Python 개발 보고서는 별도 파일로 유지하며, C++ 소스 구현은 후속 작업으로 진행한다.

---

*본 보고서는 `c:\DEV\MagicSquare_12` 저장소 기준으로 작성되었다.*
