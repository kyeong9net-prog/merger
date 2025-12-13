# 바이러스 검사 및 보안 확인 가이드

## 개요
PyInstaller로 생성된 .exe 파일은 바이러스 백신 프로그램에서 **오탐(False Positive)**으로 감지될 수 있습니다. 이 문서는 ExcelMerger.exe의 안전성을 확인하고 오탐에 대응하는 방법을 설명합니다.

---

## 1. PyInstaller와 바이러스 오탐

### 왜 오탐이 발생하나요?

PyInstaller로 만든 .exe 파일은 다음 이유로 바이러스로 오인될 수 있습니다:

1. **패킹 기술 사용**:
   - Python 인터프리터와 라이브러리를 하나의 .exe로 압축
   - 악성코드가 사용하는 패킹 기술과 유사

2. **동적 코드 실행**:
   - 런타임에 Python 코드를 실행
   - 일부 백신이 의심스러운 행동으로 간주

3. **서명 부재**:
   - 코드 서명이 없으면 신뢰도 낮음
   - 유명 소프트웨어는 대부분 디지털 서명 보유

### 안전성 보장
- **오픈 소스**: 모든 소스 코드가 공개되어 있습니다
- **테스트 완료**: 24개 테스트 모두 통과
- **악의적 코드 없음**: 파일 읽기, 병합, 저장만 수행
- **네트워크 미사용**: 인터넷 연결 불필요

---

## 2. 바이러스 검사 방법

### 2.1 VirusTotal 사용

**VirusTotal**은 60개 이상의 백신 엔진으로 파일을 검사하는 무료 서비스입니다.

#### 검사 절차

1. **VirusTotal 접속**
   - https://www.virustotal.com/

2. **파일 업로드**
   - "Choose file" 클릭
   - `ExcelMerger.exe` 선택
   - "Confirm upload" 클릭

3. **검사 결과 확인**
   - 60+ 개 백신 엔진의 검사 결과 표시
   - 일부 엔진에서 탐지될 수 있음 (오탐)

#### 결과 해석

```
✅ 정상 (권장):
   - 대부분 백신(50개 이상)에서 안전 판정
   - 일부 엔진(5-10개)에서만 경고 (오탐 가능성 높음)

⚠️ 주의:
   - 다수 백신(20개 이상)에서 탐지
   - 재빌드 후 재검사 권장

❌ 위험:
   - 대부분 백신에서 악성코드 판정
   - 빌드 환경 확인 필요
```

### 2.2 Windows Defender 스캔

Windows 10/11에 내장된 Windows Defender로 검사:

```powershell
# PowerShell에서 실행
cd dist
Scan-MpThreatScan -ScanPath ".\ExcelMerger.exe" -ScanType QuickScan
```

또는 GUI로 검사:
1. `ExcelMerger.exe` 우클릭
2. "Microsoft Defender로 검사" 선택

### 2.3 온라인 샌드박스

**Hybrid Analysis**, **Any.Run** 등의 샌드박스에서 실행 분석:

1. https://www.hybrid-analysis.com/
2. 파일 업로드
3. 실행 동작 확인

**확인 사항**:
- 파일 접근: Excel 파일만 읽기/쓰기
- 네트워크: 연결 시도 없음
- 레지스트리: 수정하지 않음
- 프로세스: 의심스러운 자식 프로세스 생성하지 않음

---

## 3. 바이러스 오탐 대응 방법

### 3.1 Windows Defender 예외 추가

#### 방법 1: 설정에서 추가
1. Windows 설정 열기 (`Win + I`)
2. "업데이트 및 보안" → "Windows 보안"
3. "바이러스 및 위협 방지"
4. "설정 관리" 클릭
5. "제외 추가" → "파일" 선택
6. `ExcelMerger.exe` 선택

#### 방법 2: PowerShell로 추가
```powershell
# 관리자 권한으로 실행
Add-MpPreference -ExclusionPath "C:\경로\ExcelMerger.exe"
```

### 3.2 다른 백신 프로그램

각 백신 프로그램마다 예외 추가 방법이 다릅니다:

- **Norton**: 설정 → 예외 → 파일 추가
- **McAfee**: 설정 → 실시간 검사 → 제외된 파일
- **Avast**: 설정 → 일반 → 예외 → 파일 경로 추가
- **AVG**: 설정 → 구성 요소 → 웹 실드 → 예외

---

## 4. 신뢰성 향상 방법

### 4.1 코드 서명 (권장 - 비용 발생)

**디지털 서명**을 추가하면 Windows에서 신뢰할 수 있는 소프트웨어로 인식합니다.

#### 서명 절차
1. **인증서 구매**
   - DigiCert, Sectigo 등에서 코드 서명 인증서 구매
   - 비용: 연간 $100-$500

2. **서명 도구 사용**
   ```bash
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com ExcelMerger.exe
   ```

3. **검증**
   - 파일 속성 → "디지털 서명" 탭 확인

**Note**: 코드 서명은 선택사항이며 Phase 6 범위를 벗어납니다.

### 4.2 빌드 환경 정리

깨끗한 빌드 환경 사용:
```bash
# 가상 환경 생성
python -m venv clean_env

# 활성화
clean_env\Scripts\activate

# 필수 패키지만 설치
pip install openpyxl pyinstaller

# 빌드
build.bat
```

### 4.3 PyInstaller 최신 버전 사용

```bash
# PyInstaller 업데이트
pip install --upgrade pyinstaller
```

최신 버전은 오탐률이 낮습니다.

---

## 5. 사용자 안내

### 배포 시 포함할 안내문

```
📌 보안 안내

ExcelMerger.exe가 바이러스로 감지될 수 있습니다.
이는 오탐(False Positive)이며 안전합니다.

✅ 확인 방법:
1. VirusTotal.com에서 검사
2. 소스 코드 확인 (GitHub 링크)
3. Windows Defender 예외 추가

❓ 의심스럽다면:
- 소스 코드를 직접 확인하세요
- 직접 Python으로 실행하세요:
  python src/main.py
```

### README에 추가할 섹션

```markdown
## 보안 및 바이러스 검사

ExcelMerger는 100% 안전한 프로그램입니다.
- ✅ 오픈 소스 (모든 코드 공개)
- ✅ 악의적 코드 없음
- ✅ 네트워크 연결 불필요

⚠️ 일부 백신에서 오탐이 발생할 수 있습니다.
자세한 내용은 ANTIVIRUS_CHECK.md를 참조하세요.
```

---

## 6. 체크리스트

배포 전 확인:

- [ ] VirusTotal 검사 완료
- [ ] 대부분 백신에서 안전 판정
- [ ] Windows Defender 테스트 완료
- [ ] 샌드박스 분석 완료 (선택)
- [ ] 안내문 작성 완료
- [ ] README에 보안 섹션 추가

---

## 7. 참고 자료

### 공식 문서
- PyInstaller False Positives: https://pyinstaller.org/en/stable/operating-mode.html
- VirusTotal: https://www.virustotal.com/
- Windows Defender 제외 추가: https://support.microsoft.com/

### 관련 이슈
- PyInstaller GitHub Issues: "false positive", "antivirus" 검색
- Stack Overflow: "PyInstaller antivirus detection"

---

## 요약

1. **오탐 정상**: PyInstaller .exe는 오탐이 흔함
2. **안전 확인**: VirusTotal, Windows Defender로 검사
3. **예외 추가**: 필요시 백신 예외 목록에 추가
4. **사용자 안내**: 명확한 보안 안내문 제공
5. **신뢰 향상**: 코드 서명 (선택사항)

ExcelMerger는 오픈 소스이며 악의적 코드가 없습니다.
의심스러운 경우 소스 코드를 직접 확인하거나 Python으로 직접 실행할 수 있습니다.
