# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(

    ['JQEdit.py'],
    pathex=[],
    binaries=[],
    datas=[('resources\\*', 'resources')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "nntplib",
        "timeit",
        "winsound",
        "winreg",
        "html",
        "socket",
        "socketserver",
        "ensurepip",
        "configparser",
        "pip",
        "hashlib",
        "csv",
        "unicodedata",
        "pydoc_data",
        "email",
        "numpy",
        "jedi",
        "json",
        "cchardet",
        "PIL",
        "psutil",
        "tk",
        "ipython",
        "tcl",
        "tcl8",
        "tornado",
        "matplotlib",
        "scipy",
        "setuptools",
        "hook",
        "distutils",
        "site",
        "hooks",
        "tornado",
        "PIL",
        "PyQt4",
        "PyQt5",
        "pydoc",
        "Pygments",
        "pythoncom",
        "pytz",
        "pywintypes",
        "sqlite3",
        "pyz",
        "pandas",
        "sklearn",
        "scapy",
        "scrapy",
        "sympy",
        "kivy",
        "pyramid",
        "opencv",
        "tensorflow",
        "pipenv",
        "pattern",
        "mechanize",
        "beautifulsoup4",
        "requests",
        "wxPython",
        "pygi",
        "pillow",
        "pygame",
        "pyglet",
        "flask",
        "django",
        "pylint",
        "pytube",
        "odfpy",
        "mccabe",
        "pilkit",
        "six",
        "json",
        "wrapt",
        "astroid",
        "isort"
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='JQEdit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['resources\\JQEdit.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='JQEdit',
)