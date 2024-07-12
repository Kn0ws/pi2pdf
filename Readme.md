# PI2PDF

PI2PDFは複数の画像を1つのPDFにまとめるスクリプトです。
指定した親フォルダ内のサブフォルダ毎にまとめられた複数の画像が、サブフォルダ名.pdfという形で出力されます。

Python3系

```bash
git clone https://github.com/kn0ws/pi2pdf.git
cd pi2pdf
pip install requirements.txt
```
以下のフォルダがあります。
```bash
sample
├── no1
│   ├── 1.png
│   ├── 2.png
│   └── 3.jpg
├── no2
│   ├── 1.png
│   ├── 2.png
│   └── 3.jpg
└── no3
    ├── 1.png
    ├── 2.png
    └── 3.jpg
```

以下のコマンドを実行します。

```bash
python pi2pdf.py

> PDFに変換するフォルダ郡の親フォルダのパスを入力: sample(相対パス) または /path/to/sample(絶対パス)
> 指定した親フォルダ内のフォルダのファイル名を5桁の数字に変更できます。\n「ファイル名_1.jpg」等を「00001.jpg」に変更することで、PDFを生成する際の並び順が正確になります。\n直接ファイル名を変更する為、ファイル名を変更しても問題の無いフォルダの場合に実行してください。
ファイル名を変更しますか？ Yes: y, No: n またはy以外のキーを入力してください。:
> 圧縮品質(100~1): (empty) または 100〜1の数値
> DPI値: (empty) または指定のDPI値
```

```bash
sample
├── no1
│   ├── 1.png
│   ├── 2.png
│   └── 3.jpg
├── no1.pdf ← New!
├── no2
│   ├── 1.png
│   ├── 2.png
│   └── 3.jpg
├── no2.pdf ← New!
├── no3
│   ├── 1.png
│   ├── 2.png
│   └── 3.jpg
└── no3.pdf ← New!
```
