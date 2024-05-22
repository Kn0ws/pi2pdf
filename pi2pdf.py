import os
import sys
from pathlib import Path
from PIL import Image
from PyPDF2 import PdfMerger

class Pi2pdf:

    def __init__(self, input_path):
        self.input_path = input_path

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
            image.save(pdf_path, "PDF", resolution=100.0)
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
        
        
if __name__ == "__main__":
    args = sys.argv
    pi2pdf = Pi2pdf(args[1])
    pi2pdf.make()