# README

聞き取りやすい音声スピードの調査システム.

## アプリケーション化(windows前提)

``` sh
$ cd path/to/src
$ python makeapp.py
```

## Usage

- dist/sounds に音声ファイルを設置
- dist/connect.exe からアプリ起動

## Tree

``` sh
$ tree .
.
├── README.md
├── requirements.txt
└── src
    ├── bug_fix.py    # pyinstaller + PyQtのバグ解消
    ├── connect.py    # 実行
    ├── connect.spec  # exe化用設定
    ├── dist          # 成果物の出力先
    │   ├── README.md
    │   ├── result.json
    │   └── sounds
    │       └── strings.wav
    ├── makeapp.py    # 成果物の作成
    ├── result.json
    ├── sound.py
    ├── sounds
    │   └── strings.wav
    └── static        # ui ファイル
        └── ui_files
            ├── fin.ui
            ├── guide.ui
            ├── menu.ui
            ├── result.ui
            ├── settings.ui
            └── test.ui
```
