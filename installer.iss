; Excel Merger Installer Script for Inno Setup
; Inno Setup 다운로드: https://jrsoftware.org/isdl.php

[Setup]
; 기본 정보
AppName=Excel Merger
AppVersion=1.0.0
AppPublisher=kyeong9net-prog
AppPublisherURL=https://github.com/kyeong9net-prog/merger
DefaultDirName={autopf}\ExcelMerger
DefaultGroupName=Excel Merger
; 출력 파일명
OutputBaseFilename=ExcelMerger_Setup
OutputDir=installer_output
; 압축 설정
Compression=lzma2
SolidCompression=yes
; Windows 버전
MinVersion=10.0
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
; 권한
PrivilegesRequired=lowest
; UI
WizardStyle=modern
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\ExcelMerger.exe

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "바탕화면에 바로가기 만들기"; GroupDescription: "추가 아이콘:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "빠른 실행 바로가기 만들기"; GroupDescription: "추가 아이콘:"; Flags: unchecked

[Files]
; 메인 실행 파일
Source: "dist\ExcelMerger.exe"; DestDir: "{app}"; Flags: ignoreversion
; 문서 파일들
Source: "USER_GUIDE.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "INSTALLATION.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "TROUBLESHOOTING.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}\docs"; Flags: ignoreversion

[Icons]
; 시작 메뉴
Name: "{group}\Excel Merger"; Filename: "{app}\ExcelMerger.exe"
Name: "{group}\사용자 가이드"; Filename: "{app}\docs\USER_GUIDE.md"
Name: "{group}\문제 해결"; Filename: "{app}\docs\TROUBLESHOOTING.md"
Name: "{group}\{cm:UninstallProgram,Excel Merger}"; Filename: "{uninstallexe}"
; 바탕화면 바로가기
Name: "{autodesktop}\Excel Merger"; Filename: "{app}\ExcelMerger.exe"; Tasks: desktopicon
; 빠른 실행 바로가기
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Excel Merger"; Filename: "{app}\ExcelMerger.exe"; Tasks: quicklaunchicon

[Run]
; 설치 후 프로그램 실행 옵션
Filename: "{app}\ExcelMerger.exe"; Description: "{cm:LaunchProgram,Excel Merger}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; 언인스톨시 삭제할 폴더
Type: filesandordirs; Name: "{app}"

[Code]
// 사용자 정의 설치 메시지
function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('Excel Merger 설치를 시작합니다.' + #13#10 + #13#10 +
         '이 프로그램은 여러 엑셀 파일을 하나로 병합합니다.' + #13#10 +
         'Python이나 Excel 설치가 필요하지 않습니다.',
         mbInformation, MB_OK);
end;

// 설치 완료 메시지
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('설치가 완료되었습니다!' + #13#10 + #13#10 +
           '시작 메뉴 또는 바탕화면에서 Excel Merger를 실행하세요.' + #13#10 +
           '사용 방법은 시작 메뉴의 "사용자 가이드"를 참고하세요.',
           mbInformation, MB_OK);
  end;
end;
