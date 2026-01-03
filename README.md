# Paper Search MCP

arXiv, PubMed, bioRxiv, Sci-Hub(선택 사항) 등 다양한 소스에서 학술 논문을 검색 및 다운로드하고, **RAG(검색 증강 생성)를 통해 논문 내용에 대해 직접 질문할 수 있는** MCP(Model Context Protocol) 서버입니다. Claude Desktop과 같은 대규모 언어 모델(LLM)과 원활하게 통합되도록 설계되었습니다.

![PyPI](https://img.shields.io/pypi/v/paper-search-mcp.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
[![smithery badge](https://smithery.ai/badge/@openags/paper-search-mcp)](https://smithery.ai/server/@openags/paper-search-mcp)

---

## 목차

- [개요](#개요)
- [주요 기능](#주요-기능)
- [사용 가능한 도구 (Tools)](#사용-가능한-도구-tools)
- [설치 방법](#설치-방법)
  - [빠른 시작](#빠른-시작)
  - [개발용 설정](#개발용-설정)
- [기여하기](#기여하기)
- [데모](#데모)
- [라이선스](#라이선스)

---

## 개요

`paper-search-mcp`는 사용자가 다양한 플랫폼에서 학술 논문을 검색하고 다운로드할 수 있게 해주는 Python 기반 MCP 서버입니다. `search_arxiv`와 같은 검색 도구와 `download_arxiv`와 같은 다운로드 도구를 제공하여 연구자와 AI 기반 워크플로우에 이상적입니다.

새롭게 추가된 **RAG 엔진(Docling + FAISS)**을 통해, 단순히 파일을 내려받는 것을 넘어 **다운로드한 논문의 내용을 바탕으로 문맥에 맞는 질의응답**을 수행할 수 있습니다.

---

## 주요 기능

- **다중 소스 지원**: arXiv, PubMed, bioRxiv, medRxiv, Google Scholar, IACR ePrint Archive, Semantic Scholar 등에서 논문 검색 및 다운로드.
- **RAG 기반 심층 질의 (NEW)**:
  - **세션 관리**: 연구 주제별로 세션을 생성하여 문맥을 유지.
  - **Docling 통합**: PDF 문서를 구조적으로 정밀하게 파싱.
  - **벡터 검색**: `google/embeddinggemma-300M` 모델과 FAISS를 이용한 고성능 의미 검색.
- **표준화된 출력**: 모든 논문 데이터는 `Paper` 클래스를 통해 일관된 딕셔너리 형식으로 반환됩니다.
- **비동기 도구**: `httpx`를 사용하여 네트워크 요청을 효율적으로 처리합니다.
- **확장 가능한 설계**: `academic_platforms` 모듈을 확장하여 새로운 학술 플랫폼을 쉽게 추가할 수 있습니다.

---

## 사용 가능한 도구 (Tools)

`server.py`에 등록된 플랫폼별 검색(Search), 다운로드(Download), 읽기(Read) 도구 목록입니다.

| 플랫폼 | 검색 (Search) | 다운로드 (Download) | 읽기 (Read) |
| :--- | :--- | :--- | :--- |
| **arXiv** | `search_arxiv` | `download_arxiv` | `read_arxiv_paper` |
| **PubMed** | `search_pubmed` | ❌ (미지원) | ❌ (미지원) |
| **bioRxiv** | `search_biorxiv` | `download_biorxiv` | `read_biorxiv_paper` |
| **medRxiv** | `search_medrxiv` | `download_medrxiv` | `read_medrxiv_paper` |
| **Google Scholar** | `search_google_scholar` | ❌ | ❌ |
| **IACR ePrint** | `search_iacr` | `download_iacr` | `read_iacr_paper` |
| **Semantic Scholar** | `search_semantic` | `download_semantic` | `read_semantic_paper` |
| **CrossRef** | `search_crossref` | ❌ (미지원) | ❌ (미지원) |

> **참고**: `PubMed`와 `CrossRef`는 코드상에서 다운로드/읽기 시도 시 "지원하지 않음(NotImplemented)" 메시지를 반환합니다.

### RAG (지능형 질의) 도구

| 도구 이름 | 설명 |
| :--- | :--- |
| `rag_create_session` | 새로운 질의 세션을 생성하고 세션 ID를 반환합니다. |
| `rag_add_paper` | 지정된 논문(arXiv 등)을 다운로드하고 세션의 지식 베이스에 추가합니다. |
| `rag_query` | 세션에 추가된 논문들의 내용을 바탕으로 질문에 답변을 검색합니다. |
| `rag_list_sessions` | 활성화된 모든 세션 목록을 확인합니다. |
| `rag_delete_session` | 특정 세션을 삭제하고 리소스를 정리합니다. |

---

## 설치 방법

`uv` 또는 `pip`를 사용하여 설치할 수 있습니다.

### Smithery를 통한 설치

Claude Desktop용으로 [Smithery](https://smithery.ai/server/@openags/paper-search-mcp)를 통해 자동 설치하려면:

```bash
npx -y @smithery/cli install @openags/paper-search-mcp --client claude
```

### 빠른 시작

빠르게 서버를 실행하고 싶은 경우:

1. **패키지 설치**:

   ```bash
   uv add paper-search-mcp
   ```

2. **Claude Desktop 설정**:
   Mac의 경우 `~/Library/Application Support/Claude/claude_desktop_config.json`, Windows의 경우 `%APPDATA%\Claude\claude_desktop_config.json`에 설정을 추가합니다:

   ```json
   {
     "mcpServers": {
       "paper_search_server": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "/path/to/your/paper-search-mcp",
           "-m",
           "paper_search_mcp.server"
         ],
         "env": {
           "SEMANTIC_SCHOLAR_API_KEY": "" // 선택 사항: Semantic Scholar 기능 향상용
         }
       }
     }
   }
   ```

   > 주의: `/path/to/your/paper-search-mcp`를 실제 설치 경로로 변경하세요.

### 개발용 설정

코드를 수정하거나 기여하려는 경우:

1. **환경 설정**:

   ```bash
   # uv 설치 (없는 경우)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # 리포지토리 클론
   git clone https://github.com/openags/paper-search-mcp.git
   cd paper-search-mcp

   # 가상 환경 생성 및 활성화
   uv venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. **의존성 설치**:

   ```bash
   # 프로젝트를 편집 모드로 설치
   uv add -e .

   # 개발용 의존성 추가 (선택 사항)
   uv add pytest flake8
   ```

---

## 기여하기

기여는 언제나 환영합니다! 다음 절차를 따라주세요:

1. **리포지토리 포크 (Fork)**: GitHub에서 "Fork" 버튼을 클릭합니다.
2. **클론 및 설정**:

   ```bash
   git clone https://github.com/yourusername/paper-search-mcp.git
   cd paper-search-mcp
   pip install -e ".[dev]"
   ```

3. **변경 사항 작업**: `academic_platforms/`에 새 플랫폼을 추가하거나 `tests/`를 업데이트합니다.
4. **Pull Request 제출**: 변경 사항을 푸시하고 GitHub에서 PR을 생성합니다.

---

## 데모

<img src="docs\images\demo.png" alt="Demo" width="800">

---

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.

---

`paper-search-mcp`와 함께 즐거운 연구 되세요! 문제가 발생하면 GitHub 이슈를 열어주세요.
