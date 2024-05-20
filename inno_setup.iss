; 脚本由 Inno Setup 脚本向导 生成！
; 有关创建 Inno Setup 脚本文件的详细资料请查阅帮助文档！

#define MyAppName "JQEdit"
#define MyAppVersion "0.1.1"
#define MyAppPublisher "niejieqiang"
#define MyAppURL "469063190@qq.com"
#define MyAppExeName "JQEdit.exe"
#define MyAppAssocName "txt文件"
#define MyAppAssocExt ".txt"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
; 注: AppId的值为单独标识该应用程序。
; 不要为其他安装程序使用相同的AppId值。
; (若要生成新的 GUID，可在菜单中点击 "工具|生成 GUID"。)
AppId={{0B56641D-F6A6-4472-8BB7-BF357D675837}
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
; 以下行取消注释，以在非管理安装模式下运行（仅为当前用户安装）。
;PrivilegesRequired=lowest
OutputDir=D:\迅雷下载\JQEdit\
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
Source: "D:\迅雷下载\JQEdit\dist\JQEdit\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\迅雷下载\JQEdit\dist\JQEdit\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 注意: 不要在任何共享系统文件上使用“Flags: ignoreversion”

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

; 添加命令项，使右键菜单项能够执行编辑器程序
Root: HKCR; Subkey: "*\shell\用 JQEdit编辑\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Flags: uninsdeletekey
; 添加图标路径
Root: HKCR; Subkey: "*\shell\用 JQEdit编辑"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\resources\JQEdit.ico"; Flags: uninsdeletekey


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
Name: addPath; Description: "将程序添加到Path环境变量"

[Code]
function ShouldAddToPath: Boolean;
begin
  // 返回复选框的状态，True表示选中，False表示未选中
  Result := WizardForm.TasksList.Checked[0];
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer; // 声明ResultCode变量
begin
  // 在"安装"步骤之后执行添加到PATH环境变量的操作
  if CurStep = ssPostInstall then
  begin
    // 如果复选框被选中，则执行添加到PATH环境变量的操作
    if ShouldAddToPath then
    begin
      // 执行添加到PATH环境变量的操作
      Exec('cmd.exe', '/c setx PATH "%PATH%;"' + ExpandConstant('{app}'), '', SW_HIDE,
        ewWaitUntilTerminated, ResultCode);
    end;
  end;
end;
