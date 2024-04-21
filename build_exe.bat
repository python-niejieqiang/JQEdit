@echo off
REM 检查系统是否安装 Python
python --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python 未安装，请先安装 Python。
    pause
    exit /b
)

REM 检查系统是否安装 PyInstaller
pyinstaller --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller 未安装，请先安装 PyInstaller。
    pause
    exit /b
)

REM 检查系统是否安装 Inno Setup
if exist "C:\Program Files (x86)\Inno Setup 6\Compil32.exe" (
    echo Inno Setup 已安装。
) else if exist "C:\Program Files\Inno Setup 6\Compil32.exe" (
    echo Inno Setup 已安装。
) else (
    echo Inno Setup 未安装，请先安装 Inno Setup。
    pause
    exit /b
)

REM 检测完毕，开始打包exe

echo python,pyinstaller已经安装，即将打包成exe...
python -m venv venv
echo 创建虚拟环境
call venv\Scripts\activate
echo 激活虚拟环境成功
timeout /t 1 > nul
:: pyinstaller -D -w --icon="resources\JQEdit.ico" --add-data="resources\*;resources" JQEdit.py
pyinstaller --clean JQEdit.spec
echo 打包完成
timeout /t 2 > nul
echo 开始执行精简程序：
timeout /t 1 > nul
set count = 0
del dist\JQEdit\_internal\libcrypto-3.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\libcrypto-3.dll
set count = 0
del dist\JQEdit\_internal\select.pyd
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\select.pyd
del dist\JQEdit\_internal\unicodedata.pyd
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\unicodedata.pyd
del dist\JQEdit\_internal\VCRUNTIME140.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\VCRUNTIME140.dll
del dist\JQEdit\_internal\VCRUNTIME140_1.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\VCRUNTIME140_1.dll
del dist\JQEdit\_internal\_bz2.pyd
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\_bz2.pyd
del dist\JQEdit\_internal\_decimal.pyd
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\_decimal.pyd
del dist\JQEdit\_internal\_hashlib.pyd
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\_hashlib.pyd
del dist\JQEdit\_internal\_lzma.pyd
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\_lzma.pyd
del dist\JQEdit\_internal\_socket.pyd
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\_socket.pyd
del dist\JQEdit\_internal\PySide6\MSVCP140.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\MSVCP140.dll
del dist\JQEdit\_internal\PySide6\MSVCP140_1.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\MSVCP140_1.dll
del dist\JQEdit\_internal\PySide6\MSVCP140_2.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\MSVCP140_2.dll
del dist\JQEdit\_internal\PySide6\opengl32sw.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\opengl32sw.dll
del dist\JQEdit\_internal\PySide6\Qt6Network.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\Qt6Network.dll
del dist\JQEdit\_internal\PySide6\Qt6OpenGL.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\Qt6OpenGL.dll
del dist\JQEdit\_internal\PySide6\Qt6Pdf.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\Qt6Pdf.dll
del dist\JQEdit\_internal\PySide6\Qt6Qml.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\Qt6Qml.dll
del dist\JQEdit\_internal\PySide6\Qt6QmlModels.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\Qt6QmlModels.dll
del dist\JQEdit\_internal\PySide6\Qt6Quick.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\Qt6Quick.dll
del dist\JQEdit\_internal\PySide6\Qt6Svg.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\Qt6Svg.dll
del dist\JQEdit\_internal\PySide6\Qt6VirtualKeyboard.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\Qt6VirtualKeyboard.dll
del dist\JQEdit\_internal\PySide6\QtNetwork.pyd
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\QtNetwork.pyd
del dist\JQEdit\_internal\PySide6\VCRUNTIME140.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\VCRUNTIME140.dll
del dist\JQEdit\_internal\PySide6\VCRUNTIME140_1.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\VCRUNTIME140_1.dll
del dist\JQEdit\_internal\PySide6\plugins\generic\qtuiotouchplugin.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\generic\qtuiotouchplugin.dll
del dist\JQEdit\_internal\PySide6\plugins\iconengines\qsvgicon.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\iconengines\qsvgicon.dll
del dist\JQEdit\_internal\PySide6\plugins\imageformats\qgif.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\imageformats\qgif.dll
del dist\JQEdit\_internal\PySide6\plugins\imageformats\qicns.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\imageformats\qicns.dll
del dist\JQEdit\_internal\PySide6\plugins\imageformats\qico.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\imageformats\qico.dll
del dist\JQEdit\_internal\PySide6\plugins\imageformats\qjpeg.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\imageformats\qjpeg.dll
del dist\JQEdit\_internal\PySide6\plugins\imageformats\qpdf.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\imageformats\qpdf.dll
del dist\JQEdit\_internal\PySide6\plugins\imageformats\qsvg.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\imageformats\qsvg.dll
del dist\JQEdit\_internal\PySide6\plugins\imageformats\qtga.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\imageformats\qtga.dll
del dist\JQEdit\_internal\PySide6\plugins\imageformats\qtiff.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\imageformats\qtiff.dll
del dist\JQEdit\_internal\PySide6\plugins\imageformats\qwbmp.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\imageformats\qwbmp.dll
del dist\JQEdit\_internal\PySide6\plugins\imageformats\qwebp.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\imageformats\qwebp.dll
del dist\JQEdit\_internal\PySide6\plugins\networkinformation\qnetworklistmanager.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\networkinformation\qnetworklistmanager.dll
del dist\JQEdit\_internal\PySide6\plugins\platforminputcontexts\qtvirtualkeyboardplugin.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\platforminputcontexts\qtvirtualkeyboardplugin.dll
del dist\JQEdit\_internal\PySide6\plugins\platforms\qdirect2d.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\platforms\qdirect2d.dll
del dist\JQEdit\_internal\PySide6\plugins\platforms\qminimal.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\platforms\qminimal.dll
del dist\JQEdit\_internal\PySide6\plugins\platforms\qoffscreen.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\platforms\qoffscreen.dll
del dist\JQEdit\_internal\PySide6\plugins\tls\qcertonlybackend.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\tls\qcertonlybackend.dll
del dist\JQEdit\_internal\PySide6\plugins\tls\qopensslbackend.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\tls\qopensslbackend.dll
del dist\JQEdit\_internal\PySide6\plugins\tls\qschannelbackend.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\plugins\tls\qschannelbackend.dll
del dist\JQEdit\_internal\PySide6\translations\qtbase_ar.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_ar.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_bg.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_bg.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_ca.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_ca.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_cs.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_cs.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_da.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_da.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_de.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_de.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_en.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_en.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_es.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_es.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_fa.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_fa.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_fi.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_fi.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_fr.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_fr.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_gd.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_gd.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_he.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_he.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_hr.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_hr.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_hu.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_hu.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_it.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_it.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_ja.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_ja.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_ko.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_ko.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_lv.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_lv.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_nl.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_nl.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_nn.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_nn.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_pl.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_pl.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_pt_BR.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_pt_BR.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_ru.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_ru.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_sk.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_sk.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_tr.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_tr.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_uk.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_uk.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_zh_CN.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_zh_CN.qm
del dist\JQEdit\_internal\PySide6\translations\qtbase_zh_TW.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qtbase_zh_TW.qm
del dist\JQEdit\_internal\PySide6\translations\qt_ar.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_ar.qm
del dist\JQEdit\_internal\PySide6\translations\qt_bg.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_bg.qm
del dist\JQEdit\_internal\PySide6\translations\qt_ca.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_ca.qm
del dist\JQEdit\_internal\PySide6\translations\qt_cs.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_cs.qm
del dist\JQEdit\_internal\PySide6\translations\qt_da.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_da.qm
del dist\JQEdit\_internal\PySide6\translations\qt_de.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_de.qm
del dist\JQEdit\_internal\PySide6\translations\qt_en.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_en.qm
del dist\JQEdit\_internal\PySide6\translations\qt_es.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_es.qm
del dist\JQEdit\_internal\PySide6\translations\qt_fa.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_fa.qm
del dist\JQEdit\_internal\PySide6\translations\qt_fi.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_fi.qm
del dist\JQEdit\_internal\PySide6\translations\qt_fr.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_fr.qm
del dist\JQEdit\_internal\PySide6\translations\qt_gd.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_gd.qm
del dist\JQEdit\_internal\PySide6\translations\qt_gl.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_gl.qm
del dist\JQEdit\_internal\PySide6\translations\qt_he.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_he.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_ar.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_ar.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_bg.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_bg.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_ca.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_ca.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_cs.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_cs.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_da.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_da.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_de.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_de.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_en.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_en.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_es.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_es.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_fr.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_fr.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_gl.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_gl.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_hr.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_hr.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_hu.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_hu.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_it.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_it.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_ja.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_ja.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_ko.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_ko.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_nl.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_nl.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_nn.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_nn.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_pl.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_pl.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_pt_BR.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_pt_BR.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_ru.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_ru.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_sk.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_sk.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_sl.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_sl.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_tr.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_tr.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_uk.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_uk.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_zh_CN.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_zh_CN.qm
del dist\JQEdit\_internal\PySide6\translations\qt_help_zh_TW.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_help_zh_TW.qm
del dist\JQEdit\_internal\PySide6\translations\qt_hr.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_hr.qm
del dist\JQEdit\_internal\PySide6\translations\qt_hu.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_hu.qm
del dist\JQEdit\_internal\PySide6\translations\qt_it.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_it.qm
del dist\JQEdit\_internal\PySide6\translations\qt_ja.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_ja.qm
del dist\JQEdit\_internal\PySide6\translations\qt_ko.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_ko.qm
del dist\JQEdit\_internal\PySide6\translations\qt_lt.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_lt.qm
del dist\JQEdit\_internal\PySide6\translations\qt_lv.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_lv.qm
del dist\JQEdit\_internal\PySide6\translations\qt_nl.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_nl.qm
del dist\JQEdit\_internal\PySide6\translations\qt_nn.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_nn.qm
del dist\JQEdit\_internal\PySide6\translations\qt_pl.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_pl.qm
del dist\JQEdit\_internal\PySide6\translations\qt_pt_BR.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_pt_BR.qm
del dist\JQEdit\_internal\PySide6\translations\qt_pt_PT.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_pt_PT.qm
del dist\JQEdit\_internal\PySide6\translations\qt_ru.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_ru.qm
del dist\JQEdit\_internal\PySide6\translations\qt_sk.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_sk.qm
del dist\JQEdit\_internal\PySide6\translations\qt_sl.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_sl.qm
del dist\JQEdit\_internal\PySide6\translations\qt_sv.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_sv.qm
del dist\JQEdit\_internal\PySide6\translations\qt_tr.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_tr.qm
del dist\JQEdit\_internal\PySide6\translations\qt_uk.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_uk.qm
del dist\JQEdit\_internal\PySide6\translations\qt_zh_CN.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_zh_CN.qm
del dist\JQEdit\_internal\PySide6\translations\qt_zh_TW.qm
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\PySide6\translations\qt_zh_TW.qm
del dist\JQEdit\_internal\shiboken6\MSVCP140.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\shiboken6\MSVCP140.dll
del dist\JQEdit\_internal\shiboken6\VCRUNTIME140.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\shiboken6\VCRUNTIME140.dll
del dist\JQEdit\_internal\shiboken6\VCRUNTIME140_1.dll
set /a count+=1
echo 已经删除：del dist\JQEdit\_internal\shiboken6\VCRUNTIME140_1.dll

REM 删除 _internal\PySide6\plugins\styles 目录下的所有 .dll 文件
del /q dist\JQEdit\_internal\PySide6\plugins\styles\*.dll
set /a count+=1
echo 已经删除：del /q dist\JQEdit\_internal\PySide6\plugins\styles\*.dll

REM 计算删除的文件数量并输出信息

echo 精简了 %count% 个文件。
timeout /t 2 > nul
echo 准备将vista风格文件复制到程序目录
timeout /t 2 > nul
REM 复制当前目录中的 qwindowsvistastyle.dll 到 _internal\PySide6\plugins\styles 目录
copy qwindowsvistastyle.dll dist\JQEdit\_internal\PySide6\plugins\styles
timeout /t 2 > nul
echo 瘦身完成，开始封装安装包
timeout /t 2 > nul
Compil32 /cc inno_setup.iss
timeout /t 2 > nul
echo 安装包制作完成