@echo off
REM ���ϵͳ�Ƿ�װ Python
python --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python δ��װ�����Ȱ�װ Python��
    pause
    exit /b
)
REM ���ϵͳ�Ƿ�װ PyInstaller
pyinstaller --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller δ��װ�����Ȱ�װ PyInstaller��
    pause
    exit /b
)
REM ���ϵͳ�Ƿ�װ Inno Setup
if exist "C:\Program Files (x86)\Inno Setup 6\Compil32.exe" (
    echo Inno Setup �Ѱ�װ��
) else if exist "C:\Program Files\Inno Setup 6\Compil32.exe" (
    echo Inno Setup �Ѱ�װ��
) else (
    echo Inno Setup δ��װ�����Ȱ�װ Inno Setup��
    pause
    exit /b
)
REM �����ϣ���ʼ���exe
echo python,pyinstaller�Ѿ���װ�����������exe...
python -m venv venv
echo �������⻷��
call venv\Scripts\activate
echo �������⻷���ɹ�
timeout /t 1 > nul
::pyinstaller -D -w --icon="resources\JQEdit.ico" --add-data="resources\*;resources" JQEdit.py
pyinstaller --clean JQEdit.spec
echo ������
timeout /t 2 > nul
echo ��ʼִ�о������
timeout /t 1 > nul
set count = 0
del dist\JQEdit\libcrypto-1_1.dll
echo ɾ����dist\JQEdit\libcrypto-1_1.dll
set /a count+=1
del dist\JQEdit\libssl-1_1.dll
echo ɾ����dist\JQEdit\libssl-1_1.dll
set /a count+=1
del dist\JQEdit\select.pyd
echo ɾ����dist\JQEdit\select.pyd
set /a count+=1
del dist\JQEdit\unicodedata.pyd
echo ɾ����dist\JQEdit\unicodedata.pyd
set /a count+=1
del dist\JQEdit\VCRUNTIME140.dll
echo ɾ����dist\JQEdit\VCRUNTIME140.dll
set /a count+=1
del dist\JQEdit\VCRUNTIME140_1.dll
echo ɾ����dist\JQEdit\VCRUNTIME140_1.dll
set /a count+=1
del dist\JQEdit\_bz2.pyd
echo ɾ����dist\JQEdit\_bz2.pyd
set /a count+=1
del dist\JQEdit\_hashlib.pyd
echo ɾ����dist\JQEdit\_hashlib.pyd
set /a count+=1
del dist\JQEdit\_lzma.pyd
echo ɾ����dist\JQEdit\_lzma.pyd
set /a count+=1
del dist\JQEdit\_socket.pyd
echo ɾ����dist\JQEdit\_socket.pyd
set /a count+=1
del dist\JQEdit\_ssl.pyd
echo ɾ����dist\JQEdit\_ssl.pyd
set /a count+=1
del dist\JQEdit\PySide6\MSVCP140.dll
echo ɾ����dist\JQEdit\PySide6\MSVCP140.dll
set /a count+=1
del dist\JQEdit\PySide6\MSVCP140_1.dll
echo ɾ����dist\JQEdit\PySide6\MSVCP140_1.dll
set /a count+=1
del dist\JQEdit\PySide6\MSVCP140_2.dll
echo ɾ����dist\JQEdit\PySide6\MSVCP140_2.dll
set /a count+=1
del dist\JQEdit\PySide6\opengl32sw.dll
echo ɾ����dist\JQEdit\PySide6\opengl32sw.dll
set /a count+=1
del dist\JQEdit\PySide6\Qt6Network.dll
echo ɾ����dist\JQEdit\PySide6\Qt6Network.dll
set /a count+=1
del dist\JQEdit\PySide6\Qt6OpenGL.dll
echo ɾ����dist\JQEdit\PySide6\Qt6OpenGL.dll
set /a count+=1
del dist\JQEdit\shiboken6\MSVCP140.dll
echo ɾ����dist\JQEdit\shiboken6\MSVCP140.dll
set /a count+=1
del dist\JQEdit\PySide6\Qt6Pdf.dll
echo ɾ����dist\JQEdit\PySide6\Qt6Pdf.dll
set /a count+=1
del dist\JQEdit\shiboken6\VCRUNTIME140_1.dll
echo ɾ����dist\JQEdit\shiboken6\VCRUNTIME140_1.dll
set /a count+=1
del dist\JQEdit\PySide6\Qt6Qml.dll
echo ɾ����dist\JQEdit\PySide6\Qt6Qml.dll
set /a count+=1
del dist\JQEdit\PySide6\Qt6QmlModels.dll
echo ɾ����dist\JQEdit\PySide6\Qt6QmlModels.dll
set /a count+=1
del dist\JQEdit\PySide6\Qt6Quick.dll
echo ɾ����dist\JQEdit\PySide6\Qt6Quick.dll
set /a count+=1
del dist\JQEdit\PySide6\Qt6Svg.dll
echo ɾ����dist\JQEdit\PySide6\Qt6Svg.dll
set /a count+=1
del dist\JQEdit\PySide6\Qt6VirtualKeyboard.dll
echo ɾ����dist\JQEdit\PySide6\Qt6VirtualKeyboard.dll
set /a count+=1
del dist\JQEdit\PySide6\QtNetwork.pyd
echo ɾ����dist\JQEdit\PySide6\QtNetwork.pyd
set /a count+=1
del dist\JQEdit\PySide6\VCRUNTIME140_1.dll
echo ɾ����dist\JQEdit\PySide6\VCRUNTIME140_1.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\generic\qtuiotouchplugin.dll
echo ɾ����dist\JQEdit\PySide6\plugins\generic\qtuiotouchplugin.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\iconengines\qsvgicon.dll
echo ɾ����dist\JQEdit\PySide6\plugins\iconengines\qsvgicon.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\imageformats\qgif.dll
echo ɾ����dist\JQEdit\PySide6\plugins\imageformats\qgif.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\imageformats\qicns.dll
echo ɾ����dist\JQEdit\PySide6\plugins\imageformats\qicns.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\imageformats\qico.dll
echo ɾ����dist\JQEdit\PySide6\plugins\imageformats\qico.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\imageformats\qjpeg.dll
echo ɾ����dist\JQEdit\PySide6\plugins\imageformats\qjpeg.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\imageformats\qpdf.dll
echo ɾ����dist\JQEdit\PySide6\plugins\imageformats\qpdf.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\imageformats\qsvg.dll
echo ɾ����dist\JQEdit\PySide6\plugins\imageformats\qsvg.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\imageformats\qtga.dll
echo ɾ����dist\JQEdit\PySide6\plugins\imageformats\qtga.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\imageformats\qtiff.dll
echo ɾ����dist\JQEdit\PySide6\plugins\imageformats\qtiff.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\imageformats\qwbmp.dll
echo ɾ����dist\JQEdit\PySide6\plugins\imageformats\qwbmp.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\imageformats\qwebp.dll
echo ɾ����dist\JQEdit\PySide6\plugins\imageformats\qwebp.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\networkinformation\qnetworklistmanager.dll
echo ɾ����dist\JQEdit\PySide6\plugins\networkinformation\qnetworklistmanager.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\platforminputcontexts\qtvirtualkeyboardplugin.dll
echo ɾ����dist\JQEdit\PySide6\plugins\platforminputcontexts\qtvirtualkeyboardplugin.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\platforms\qdirect2d.dll
echo ɾ����dist\JQEdit\PySide6\plugins\platforms\qdirect2d.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\platforms\qminimal.dll
echo ɾ����dist\JQEdit\PySide6\plugins\platforms\qminimal.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\platforms\qoffscreen.dll
echo ɾ����dist\JQEdit\PySide6\plugins\platforms\qoffscreen.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\tls\qcertonlybackend.dll
echo ɾ����dist\JQEdit\PySide6\plugins\tls\qcertonlybackend.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\tls\qopensslbackend.dll
echo ɾ����dist\JQEdit\PySide6\plugins\tls\qopensslbackend.dll
set /a count+=1
del dist\JQEdit\PySide6\plugins\tls\qschannelbackend.dll
echo ɾ����dist\JQEdit\PySide6\plugins\tls\qschannelbackend.dll
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_ar.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_ar.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_bg.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_bg.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_ca.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_ca.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_cs.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_cs.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_da.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_da.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_de.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_de.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_en.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_en.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_es.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_es.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_fa.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_fa.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_fi.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_fi.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_fr.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_fr.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_gd.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_gd.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_he.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_he.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_hr.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_hr.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_hu.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_hu.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_it.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_it.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_ja.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_ja.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_ko.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_ko.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_lv.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_lv.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_nl.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_nl.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_nn.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_nn.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_pl.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_pl.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_pt_BR.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_pt_BR.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_ru.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_ru.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_sk.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_sk.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_tr.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_tr.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_uk.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_uk.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_zh_CN.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_zh_CN.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qtbase_zh_TW.qm
echo ɾ����dist\JQEdit\PySide6\translations\qtbase_zh_TW.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_ar.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_ar.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_bg.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_bg.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_ca.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_ca.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_cs.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_cs.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_da.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_da.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_de.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_de.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_en.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_en.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_es.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_es.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_fa.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_fa.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_fi.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_fi.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_fr.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_fr.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_gd.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_gd.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_gl.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_gl.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_he.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_he.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_ar.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_ar.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_bg.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_bg.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_ca.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_ca.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_cs.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_cs.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_da.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_da.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_de.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_de.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_en.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_en.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_es.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_es.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_fr.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_fr.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_gl.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_gl.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_hr.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_hr.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_hu.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_hu.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_it.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_it.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_ja.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_ja.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_ko.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_ko.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_nl.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_nl.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_nn.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_nn.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_pl.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_pl.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_pt_BR.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_pt_BR.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_ru.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_ru.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_sk.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_sk.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_sl.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_sl.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_tr.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_tr.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_uk.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_uk.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_zh_CN.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_zh_CN.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_help_zh_TW.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_help_zh_TW.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_hr.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_hr.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_hu.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_hu.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_it.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_it.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_ja.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_ja.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_ko.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_ko.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_lt.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_lt.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_lv.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_lv.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_nl.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_nl.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_nn.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_nn.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_pl.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_pl.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_pt_BR.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_pt_BR.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_pt_PT.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_pt_PT.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_ru.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_ru.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_sk.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_sk.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_sl.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_sl.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_sv.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_sv.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_tr.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_tr.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_uk.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_uk.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_zh_CN.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_zh_CN.qm
set /a count+=1
del dist\JQEdit\PySide6\translations\qt_zh_TW.qm
echo ɾ����dist\JQEdit\PySide6\translations\qt_zh_TW.qm
set /a count+=1
REM ����ɾ�����ļ������������Ϣ
echo ������ %count% ���ļ���
timeout /t 2 > nul
echo ׼����vista����ļ����Ƶ�����Ŀ¼
timeout /t 2 > nul
REM ���Ƶ�ǰĿ¼�е� qwindowsvistastyle.dll �� _internal\PySide6\plugins\styles Ŀ¼
copy qwindowsvistastyle.dll dist\JQEdit\PySide6\plugins\styles
timeout /t 2 > nul
echo ������ɣ���ʼ��װ��װ��
timeout /t 2 > nul
Compil32 /cc inno_setup.iss
timeout /t 2 > nul
echo ��װ���������