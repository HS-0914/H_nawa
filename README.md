# 🖥️ H_nawa - PC 부품 크롤링 & 견적 구성 서비스스

> **H_nawa**는 서버에서 크롤링된 부품 정보를 기반으로  
> 사용자가 원하는 조합으로 PC 견적을 구성할 수 있는 서비스스입니다.

---

## 주요 기능

### ✅ 주기적 크롤링

- Playwright를 활용해 다나와, 컴퓨존 쇼핑몰의 부품 정보를 주기적으로 수집
- 크롤링 결과는 JSON 파일로 저장되며 API를 통해 프론트엔드에 제공
- 크롤링 주기: 30분 간격

### ✅ 견적 구성 웹페이지

- 사용자가 좌측에서 카테고리를 선택하면 해당 부품 목록이 중앙에 표시
- 우측에는 선택한 부품들이 견적 리스트로 추가됨
- 합계 가격 자동 계산, 삭제 및 초기화 기능 제공
- 선택한 부품 정보는 로컬스토리지에 자동 저장되어 새로고침해도 복원됨

### ✅ 필터링 & 검색 기능

- 쇼핑몰별 필터링 (다나와만 보기 / 컴퓨존만 보기 등)
- 부품 이름 키워드 검색
- 가격 낮은순/높은순 정렬 기능 포함

---

## 💡 스택

| 구분        | 기술                                                                  |
| ----------- | --------------------------------------------------------------------- |
| 백엔드      | FastAPI                                                               |
| 크롤링      | Playwright + BeautifulSoup                                            |
| 프론트      | HTML + Tailwind CSS + JavaScript                                      |
| 배포        | Docker 기반 ~~(playwright install --with-deps 지원)~~(playwright오류) |
| 데이터 저장 | JSON 파일 기반 (카테고리별, 사이트별 저장)                            |

---

## 🗂 프로젝트 구조

```bash
📦 H_nawa
├── 📁 saved_data               # 크롤링된 결과 저장 (JSON)
│   └── CPU_0.json              # 예: 다나와 CPU 목록
│   └── CPU_1.json              # 예: 컴퓨존 CPU 목록
│
├── 📄 main.py                  # FastAPI 서버 + 주기적 크롤링
├── 📄 crawler.py               # 사이트별 크롤링 로직 정의
├── 📄 Dockerfile               # Docker 배포 환경 정의
├── 📄 index.html               # 메인 견적 웹페이지 (HTML + Tailwind + JS)
├── 📄 requirements.txt         # 의존성 패키지 목록
```

---

## 🖼️ 주요 화면 구성

- 카테고리/사이트 선택 (왼쪽) + 부품 리스트 (가운데) + 선택 견적 리스트 (오른쪽)

<img src="" width="600"/>

- 부품 검색 & 정렬 기능 포함

<img src="" width="600"/>

- 선택한 부품은 로컬스토리지에 저장되어 새로고침해도 유지됨

---

## 🐳 Docker 배포 (요약)

```bash
# Python 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Playwright 브라우저 엔진 설치
RUN playwright install --with-deps

# Uvicorn으로 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📌 기타

- 로컬에선 크롤링이 가능하지만 배포된 서버에서는 크롤링 에러(추후 수정정)
