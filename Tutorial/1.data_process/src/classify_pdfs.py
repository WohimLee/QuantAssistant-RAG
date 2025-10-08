import os
import shutil
from langdetect import detect
from PyPDF2 import PdfReader

SRC_FOLDER = "/home/buding/haqian/data/Quantitative Trading"
MIN_TEXT_LEN = 50
MAX_PAGES = 5

def extract_text_from_pdf(pdf_path, max_pages=MAX_PAGES):
    """只提取前 max_pages 页文本"""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            if i >= max_pages:
                break
            text += page.extract_text() or ""
    except Exception as e:
        print(f"无法读取文件 {pdf_path}: {e}")
    return text

def detect_language(text):
    """检测文本语言，返回 zh / en / unknown"""
    if not text or len(text.strip()) < MIN_TEXT_LEN:
        return "unknown"
    try:
        lang = detect(text)
        if lang.startswith("zh"):
            return "zh"
        elif lang == "en":
            return "en"
        else:
            return "unknown"
    except Exception:
        return "unknown"

def ensure_unique_path(dst_path):
    """若目标文件存在则自动重命名"""
    if not os.path.exists(dst_path):
        return dst_path
    base, ext = os.path.splitext(dst_path)
    idx = 1
    while True:
        candidate = f"{base} ({idx}){ext}"
        if not os.path.exists(candidate):
            return candidate
        idx += 1

def classify_files(src_folder):
    # 创建目标根目录，与源目录同级
    parent_dir = os.path.dirname(src_folder.rstrip(os.sep))
    dest_root = os.path.join(parent_dir, "PDF_Sorted")

    # 定义分类子文件夹
    folder_map = {
        "doc": os.path.join(dest_root, "doc"),
        "docx": os.path.join(dest_root, "docx"),
        "pdf_zh": os.path.join(dest_root, "pdf", "zh"),
        "pdf_en": os.path.join(dest_root, "pdf", "en"),
        "pdf_unknown": os.path.join(dest_root, "pdf", "unknown"),
        "xlsx": os.path.join(dest_root, "xlsx"),
        "csv": os.path.join(dest_root, "csv"),
    }

    # 创建所有目标文件夹
    for path in folder_map.values():
        os.makedirs(path, exist_ok=True)

    def is_under_dest(path):
        try:
            return os.path.commonpath([os.path.abspath(path), os.path.abspath(dest_root)]) == os.path.abspath(dest_root)
        except ValueError:
            return False

    # 遍历源目录
    for root, _, files in os.walk(src_folder):
        if is_under_dest(root):
            continue

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            src_path = os.path.join(root, file)

            if ext == ".pdf":
                print(f"正在分析 PDF: {src_path}")
                text = extract_text_from_pdf(src_path)
                lang = detect_language(text)

                if lang == "zh":
                    dst_dir = folder_map["pdf_zh"]
                elif lang == "en":
                    dst_dir = folder_map["pdf_en"]
                else:
                    dst_dir = folder_map["pdf_unknown"]
            elif ext == ".doc":
                dst_dir = folder_map["doc"]
            elif ext == ".docx":
                dst_dir = folder_map["docx"]
            elif ext == ".xlsx":
                dst_dir = folder_map["xlsx"]
            elif ext == ".csv":
                dst_dir = folder_map["csv"]
            else:
                continue  # 其他文件类型跳过

            dst_path = ensure_unique_path(os.path.join(dst_dir, file))
            try:
                shutil.copy2(src_path, dst_path)
                print(f"→ 复制到: {dst_path}")
            except Exception as e:
                print(f"复制失败 {src_path}: {e}")

if __name__ == "__main__":
    classify_files(SRC_FOLDER)
