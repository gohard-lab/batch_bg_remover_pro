# 📸 Batch BG Remover Pro (Workflow Edition)

[![GitHub stars](https://img.shields.io/github/stars/gohard-lab/batch_bg_remover_pro?style=social)](https://github.com/gohard-lab/batch_bg_remover_pro)

**AI 기반 대량 배경 제거 도구의 결정판.** 이 프로젝트는 글로벌 커뮤니티의 실제 사용자 피드백을 바탕으로, 단순한 AI 기능을 넘어 실제 업무 현장(이커머스, 사진 촬영 등)의 워크플로우 효율을 극대화하기 위해 제작되었습니다.

---

## ✨ Key Features (V2.0 Update)

### [KOR] 주요 기능
* **📂 폴더 구조 미러링**: 원본 폴더의 계층 구조를 결과물 폴더에 그대로 복제하여 파일 정리 시간을 획기적으로 줄여줍니다.
* **🎨 커스텀 캔버스 및 배경색**: 투명 배경뿐만 아니라 화이트, 블랙 등 원하는 배경색(#HEX)과 특정 캔버스 크기(예: 1000x1000)를 지정할 수 있습니다.
* **⚠️ 스마트 에러 관리**: 배경 제거가 불완전하거나 실패한 파일은 자동으로 `_review_needed` 폴더로 격리하여 수동 검토를 돕습니다.
* **📊 작업 통계 리포트**: 작업 시간, 성공 여부, 하드웨어 효율 등을 담은 `process_stats.csv` 파일을 생성합니다.

---

## 🚀 Quick Start

본 프로젝트는 최신 파이썬 생태계의 표준인 **`uv`**를 사용하여 의존성을 관리합니다.

```bash
# Repository 클론
git clone [https://github.com/gohard-lab/batch_bg_remover_pro.git](https://github.com/gohard-lab/batch_bg_remover_pro.git)
cd batch_bg_remover_pro

# 의존성 설치 및 실행
uv sync
uv run main.py
```

## ⭐ Support the Project
개발자를 응원해 주세요
이 프로그램이 여러분의 소중한 퇴근 시간을 앞당겨 주었나요? 소스코드만 조용히 가져가는 '체리피커'가 되기보다, 개발자의 땀과 노력에 대한 최소한의 예의로 GitHub Star⭐ 한 번만 눌러주세요. 여러분의 양심적인 클릭 한 번이 더 나은 무료 도구를 지속적으로 만드는 힘이 됩니다.

## 📝 Notice
※ 본 프로그램은 더 나은 서비스 제공과 에러 수정을 위해 익명화된 최소한의 사용 통계(기능 클릭 수 등)를 수집합니다. 개인 식별 정보는 일절 수집하지 않으니 안심하고 사용하셔도 됩니다.

## 🔗 Links
YouTube Channel: [잡학다식 개발자 PolymathDev](https://www.youtube.com/@PolymathDev_KR)

Developer GitHub: [gohard-lab](https://github.com/gohard-lab)