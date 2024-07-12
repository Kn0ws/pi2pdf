import os
from os import listdir
import re

class FileRenamer:
    def __init__(self,folder_path):
        self.folder_path = folder_path

    def list_files(self):
        try:
            # os.listdir()を使用してフォルダ内のファイル一覧を取得。
            # ファイル名がピリオドで始まる隠しファイルを除外
            files = [file for file in listdir(self.folder_path) if not file.startswith('.')]
            return files
        except FileNotFoundError:
            print("指定されたフォルダが見つかりません。")
            return []
    
    def rename_files(self):
        files = self.list_files()
        for file in files:
            # ファイルの拡張子を取得
            _, ext = os.path.splitext(file)
            # 拡張子が.jpg, .png, .jpegのいずれかであるか確認
            if ext.lower() in ['.jpg', '.png', '.jpeg']:
                # ファイル名から数字部分を抽出
                match = re.search(r'\d+', file)
                if match:
                    # 数字部分を基に新しいファイル名を生成
                    new_name = f"{int(match.group()):05}{ext}"  # 拡張子を保持
                    old_path = os.path.join(self.folder_path, file)
                    new_path = os.path.join(self.folder_path, new_name)
                    try:
                        os.rename(old_path, new_path)
                        print(f"「{file}」→「{new_name}」に変更しました。")
                    except FileNotFoundError:
                        print(f"{file}が見つかりませんでした。")
            else:
                # 拡張子が指定されたもの以外の場合はスキップ
                print(f"{file}は対象外の拡張子の為、スキップしました。")