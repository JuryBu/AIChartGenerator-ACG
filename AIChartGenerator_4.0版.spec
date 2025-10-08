# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('web', 'web'),
        ('说明图片', '说明图片'),
        ('字体', '字体'),
        ('config.json', '.'),
        ('settings.json', '.'),
        ('help_content.json', '.'),
        ('navigator_history.json', '.'),
        ('requirements_core.txt', '.'),
        ('requirements_heavy.txt', '.'),
        ('read_file_content.py', '.'),
        ('download_models.py', '.'),
        ('font_manager_window.py', '.'),
        ('help_window.py', '.'),
        ('navigator.py', '.'),
        ('version_check.py', '.'),
        ('preview_window.py', '.'),
        ('utils.py', '.'),
        ('webview_apis.py', '.'),
        ('config_manager.py', '.'),
        ('agent.py', '.'),
        ('rag_handler.py', '.'),
        ('llm_service.py', '.'),
        ('config.py', '.'),
        ('constants.py', '.'),
        ('create_preview.py', '.'),
    ],
    hiddenimports=[
        # --- 清理并保留了核心功能的 hiddenimports ---
        'pymdownx', 'pymdownx.highlight', 'pymdownx.superfences', 'pymdownx.inlinehilite',
        'pymdownx.details', 'pymdownx.tabbed', 'pymdownx.tasklist', 'pymdownx.magiclink',
        'pymdownx.betterem', 'pymdownx.tilde', 'pymdownx.caret', 'pymdownx.mark',
        'pymdownx.smartsymbols', 'pymdownx.critic', 'pymdownx.keys',
        'PyQt5.QtSvg', 'PyQt5.QtPrintSupport',
        'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageFont', 'PIL.ImageFilter',
        'PIL.JpegImagePlugin', 'PIL.PngImagePlugin',
        'lxml._elementpath', 'pkg_resources.extern'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pandas', 'numpy', 'scipy', 'pyarrow', 'polars', 'tensorflow', 'torch',
        'torchvision', 'torchaudio', 'sklearn', 'xgboost', 'lightgbm', 'optuna',
        'accelerate', 'bitsandbytes', 'transformers', 'sentence_transformers',
        'faiss', 'jieba', 'thefuzz', 'rank_bm25', 'gensim', 'matplotlib',
        'seaborn', 'plotly', 'cv2', 'SQLAlchemy', 'biopython', 'rdkit',
        'weasyprint', 'fitz'
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    [],
    name='AIChartGenerator_4.0版',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets\\icons\\app_icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AIChartGenerator_4.0版'
)
