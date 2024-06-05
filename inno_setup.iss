; �ű��� Inno Setup �ű��� ���ɣ�
; �йش��� Inno Setup �ű��ļ�����ϸ��������İ����ĵ���

#define MyAppName "JQEdit"
#define MyAppVersion "0.7.2"
#define MyAppPublisher "niejieqiang"
#define MyAppURL "469063190@qq.com"
#define MyAppExeName "JQEdit.exe"
#define MyAppAssocName "txt�ļ�"
#define MyAppAssocExt ".txt"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
; ע: AppId��ֵΪ������ʶ��Ӧ�ó���
; ��ҪΪ������װ����ʹ����ͬ��AppIdֵ��
; (��Ҫ�����µ� GUID�����ڲ˵��е�� "����|���� GUID"��)
AppId={{0B56641D-F6A6-4472-8BB7-BF357D675837}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
ChangesAssociations=yes
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; ������ȡ��ע�ͣ����ڷǹ���װģʽ�����У���Ϊ��ǰ�û���װ����
;PrivilegesRequired=lowest
OutputDir=D:\Ѹ������\JQEdit\
OutputBaseFilename=JQEdit_setup
SetupIconFile=C:\Program Files (x86)\Inno Setup 6\SetupClassicIcon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkablealone

[Files]
Source: "D:\Ѹ������\JQEdit\dist\JQEdit\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Ѹ������\JQEdit\dist\JQEdit\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; ע��: ��Ҫ���κι���ϵͳ�ļ���ʹ�á�Flags: ignoreversion��

[Registry]         
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".txt"; ValueData: ""; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".py"; ValueData: ""; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".bat"; ValueData: ""; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".sh"; ValueData: ""; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".pl"; ValueData: ""; Flags: uninsdeletekey        
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".xml"; ValueData: ""; Flags: uninsdeletekey         
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".json"; ValueData: ""; Flags: uninsdeletekey    
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".c"; ValueData: ""; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".ini"; ValueData: ""; Flags: uninsdeletekey

Root: HKA; Subkey: "Software\Classes\.txt"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocKey}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\.py"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocKey}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\.bat"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocKey}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\.sh"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocKey}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\.pl"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocKey}"; Flags: uninsdeletekey 
Root: HKA; Subkey: "Software\Classes\.json"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocKey}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\.c"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocKey}"; Flags: uninsdeletekey  
Root: HKA; Subkey: "Software\Classes\.ini"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocKey}"; Flags: uninsdeletekey

; ��������ʹ�Ҽ��˵����ܹ�ִ�б༭������
Root: HKCR; Subkey: "*\shell\�� JQEdit�༭\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Flags: uninsdeletekey
; ���ͼ��·��
Root: HKCR; Subkey: "*\shell\�� JQEdit�༭"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\resources\JQEdit.ico"; Flags: uninsdeletekey


Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Tasks]
Name: addPath; Description: "��������ӵ�Path��������"

[Code]
function ShouldAddToPath: Boolean;
begin
  // ���ظ�ѡ���״̬��True��ʾѡ�У�False��ʾδѡ��
  Result := WizardForm.TasksList.Checked[0];
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer; // ����ResultCode����
begin
  // ��"��װ"����֮��ִ����ӵ�PATH���������Ĳ���
  if CurStep = ssPostInstall then
  begin
    // �����ѡ��ѡ�У���ִ����ӵ�PATH���������Ĳ���
    if ShouldAddToPath then
    begin
      // ִ����ӵ�PATH���������Ĳ���
      Exec('cmd.exe', '/c setx PATH "%PATH%;"' + ExpandConstant('{app}'), '', SW_HIDE,
        ewWaitUntilTerminated, ResultCode);
    end;
  end;
end;

const
  UninstallRegKey = 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{{0B56641D-F6A6-4472-8BB7-BF357D675837}}';

function InitializeSetup(): Boolean;
var
  UninstallString: string;
  ResultCode: Integer;
begin
  Result := True;

  // ����Ƿ��Ѱ�װ�ɰ汾
  if RegQueryStringValue(HKLM, UninstallRegKey, 'UninstallString', UninstallString) or
     RegQueryStringValue(HKCU, UninstallRegKey, 'UninstallString', UninstallString) then
  begin
    // ȥ��ж���ַ����е����ţ���ΪCmdLine�������ܰ�������
    UninstallString := RemoveQuotes(UninstallString);

    // ȷ�������ҵ�������Ч��·��
    if FileExists(ExtractFilePath(UninstallString)) then
    begin
      Log('���־ɰ汾����������ж�س���: ' + UninstallString);
      // ����ж�س���
      Exec(UninstallString, '/SILENT', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      if ResultCode <> 0 then
      begin
        MsgBox('ж�ؾɰ汾ʧ�ܣ����ֶ�ж�غ����ԡ��������: ' + IntToStr(ResultCode), mbError, MB_OK);
        Result := False;
      end;
    end else
    begin
      Log('ж�س���·����Ч');
    end;
  end else
  begin
    Log('δ�ҵ��ɰ汾��ж����Ϣ');
  end;

  Result := Result and (ResultCode = 0); // ȷ��ֻ����ж�سɹ���ż�����װ
end;