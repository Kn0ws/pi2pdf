import os
import sys
from pathlib import Path
from PIL import Image
from PyPDF2 import PdfMerger
from multiprocessing import Pool
import rename

class Pi2pdf:

    def __init__(self, is_rename, input_path, image_quality, image_dpi):
        self.is_rename = is_rename
        self.input_path = input_path
        self.image_quality = image_quality
        self.image_dpi = image_dpi

    def remove_trailing_slash(self, path):
        if(path.endswith('/')):
            return path[:-1]
        return path
    
    def split_image_if_wide(self, image_path):
        # 画像を開く
        with Image.open(image_path) as img:
            width, height = img.size
            
            # 縦横比を測定
            if width > height:
                # 横長の場合、画像を縦半分に分割
                left_half = img.crop((0, 0, width // 2, height))
                right_half = img.crop((width // 2, 0, width, height))
                
                # 元のファイル名と拡張子を取得
                base_name, ext = os.path.splitext(image_path)
                
                # 新しいファイル名を作成
                left_half_path = f"{base_name}b{ext}"
                right_half_path = f"{base_name}a{ext}"
                
                # 分割した画像を保存
                left_half.save(left_half_path)
                right_half.save(right_half_path)

                # 元のファイルを削除
                os.remove(image_path)
                
                print(f"画像を分割しました: {left_half_path}, {right_half_path}")
            else:
                print(f"画像は縦長または正方形です: {image_path}")

    def get_image_files(self, folder_path):

        image_files = []
        print(folder_path + " のファイルを走査しています。しばらくお待ち下さい。")
        

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png','jpg', 'jpeg')):
                    image_path = os.path.join(root, file)
                    # 画像を開く
                    with Image.open(image_path) as img:
                        width, height = img.size
                        
                        # 縦横比を測定
                        if width > height:
                            # 横長の場合、画像を縦半分に分割
                            left_half = img.crop((0, 0, width // 2, height))
                            right_half = img.crop((width // 2, 0, width, height))
                            
                            # 元のファイル名と拡張子を取得
                            base_name, ext = os.path.splitext(image_path)
                            
                            # 新しいファイル名を作成
                            left_half_path = f"{base_name}b{ext}"
                            right_half_path = f"{base_name}a{ext}"
                            
                            # 分割した画像を保存
                            left_half.save(left_half_path)
                            right_half.save(right_half_path)

                            # 元のファイルを削除
                            os.remove(image_path)
                            
                            print(f"画像を分割しました: {left_half_path}, {right_half_path}")
                            image_files.append(left_half_path)
                            image_files.append(right_half_path)
                        else:
                            print(f"画像は縦長または正方形です: {image_path}")
                            image_files.append(image_path)

                    # image_files.append(os.path.join(root, file))
        print(folder_path + " のファイルを走査しました。")
        return image_files

    def build_pdf(self, args):
        image_files, parent_folder_path, folder = args
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
            image.save(
                pdf_path,
                "PDF",
                quality=self.image_quality,
                dpi=[self.image_dpi, self.image_dpi]
            )
            pdf_merger.append(pdf_path)
            os.remove(pdf_path)  # 一時PDFを削除
        output_path = parent_folder_path + "/" + folder + ".pdf"
        pdf_merger.write(output_path)
        pdf_merger.close()
        print(f"PDFの作成が完了しました。: {output_path}")

    def make(self):
        parent_folder_path = self.remove_trailing_slash(self.input_path)
        subfolders = []
        dirs = [file for file in os.listdir(parent_folder_path) if not file.startswith('.')]
        for f in dirs:
            if self.is_rename:
                rename.FileRenamer(parent_folder_path + "/" + f).rename_files()
            if os.path.isdir(parent_folder_path + "/" + f):
                subfolders.append(f)

        pool = Pool()
        args_list = [(
            self.get_image_files(parent_folder_path + "/" + folder),
            parent_folder_path,
            folder
        ) for folder in subfolders]
        pool.map(self.build_pdf, args_list)
        pool.close()
        pool.join()
        
def custom_input(prompt, default_value):
    user_input = input(prompt)
    if not user_input:
        return default_value
    return user_input

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    
        
    input_path = input("PDFに変換するフォルダ郡の親フォルダのパスを入力: ")
    if not input_path:
        print("※! パスを入力してください。")
        restart_program()

    print("指定した親フォルダ内のフォルダのファイル名を5桁の数字に変更できます。\n「ファイル名_1.jpg」等を「00001.jpg」に変更することで、PDFを生成する際の並び順が正確になります。\n直接ファイル名を変更する為、ファイル名を変更しても問題の無いフォルダの場合に実行してください。")
    exec_rename = input("ファイル名を変更しますか？ Yes: y, No: n またはy以外のキーを入力してください。: ")
    if exec_rename.lower() == 'y':
        is_rename = True
    else:
        is_rename = False
    

    
    print("画像の圧縮品質を指定します。\n数値が低い程圧縮品質が高くなり、ファイルサイズは小さくなります。圧縮品質が高いほど、画質は低くなります。\nデフォルトは100（非圧縮）です。")
    image_quality = int(custom_input("2. 圧縮品質(100~1): ", 100))

    if image_quality < 1 or image_quality > 100:
        raise ValueError("圧縮品質は100~1の間で入力してください。")

    print("印刷解像度(DPI)を指定します。\nこれは、主にプリンター等での印刷時に使用される解像度です。解像度が低い程、ファイルサイズは小さくなります。\nデフォルト値は72(Web用)です。印刷を予定している場合は、300以上が推奨です。")
    image_dpi = custom_input("3. DPI値: ", 72)

    pi2pdf = Pi2pdf(is_rename, input_path, image_quality, float(image_dpi))
    pi2pdf.make()