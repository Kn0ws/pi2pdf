import os
import sys
from pathlib import Path
from PIL import Image
from PyPDF2 import PdfMerger

class Pi2pdf:

    def __init__(self, input_path, image_quality, image_dpi):
        self.input_path = input_path
        self.image_quality = image_quality
        self.image_dpi = image_dpi

    def remove_trailing_slash(self, path):
        if(path.endswith('/')):
            return path[:-1]
        return path

    def get_image_files(self, folder_path):

        image_files = []
        print(folder_path + " のファイルを走査しています。しばらくお待ち下さい。")
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png','jpg', 'jpeg')):
                    image_files.append(os.path.join(root, file))
        print(folder_path + " のファイルを走査しました。")
        return image_files

    def build_pdf(self, image_files, parent_folder_path, folder):
        if not image_files:
            print(folder + "の画像ファイルが見つかりませんでした。")
            return
        print(folder + "をPDFに変換しています。しばらくお待ち下さい。")
        image_files.sort()  # ソートして順番を固定

        pdf_merger = PdfMerger()

        for image_file in image_files:
            image = Image.open(image_file)
            if image.mode in ("RGBA", "P"):  # RGBAモードやパレットモードをRGBに変換
                image = image.convert("RGB")
            
            pdf_path = image_file + ".pdf"
            image.save(pdf_path, "PDF", quality=self.image_quality, dpi=[self.image_dpi, self.image_dpi])
            pdf_merger.append(pdf_path)
            os.remove(pdf_path)  # 一時PDFを削除
        output_path = parent_folder_path + "/" + folder + ".pdf"
        pdf_merger.write(output_path)
        pdf_merger.close()
        print(f"PDFの作成が完了しました。: {output_path}")

    def make(self):
        parent_folder_path = self.remove_trailing_slash(self.input_path)
        subfolders = []
        for f in os.listdir(parent_folder_path):
            if os.path.isdir(parent_folder_path + "/" + f):
                subfolders.append(f)

        for folder in subfolders:
            image_files = self.get_image_files(parent_folder_path + "/" + folder)
            self.build_pdf(image_files, parent_folder_path, folder)
        
def custom_input(prompt, default_value):
    user_input = input(prompt)
    if not user_input:
        return default_value
    return user_input

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    args = sys.argv
    input_path = input("PDFに変換するフォルダ郡の親フォルダのパスを入力: ")
    if not input_path:
        print("※! パスを入力してください。")
        restart_program()
    
    print("画像の圧縮品質を指定します。\n数値が低い程圧縮品質が高くなり、ファイルサイズは小さくなります。圧縮品質が高いほど、画質は低くなります。\nデフォルトは100（非圧縮）です。")
    image_quality = int(custom_input("圧縮品質(100~1): ", 100))

    if image_quality < 1 or image_quality > 100:
        raise ValueError("圧縮品質は100~1の間で入力してください。")

    print("印刷解像度(DPI)を指定します。\nこれは、主にプリンター等での印刷時に使用される解像度です。解像度が低い程、ファイルサイズは小さくなります。\nデフォルト値は72(Web用)です。印刷を予定している場合は、300以上が推奨です。")
    image_dpi = custom_input("DPI値: ", 72)

    pi2pdf = Pi2pdf(input_path, image_quality, float(image_dpi))
    pi2pdf.make()