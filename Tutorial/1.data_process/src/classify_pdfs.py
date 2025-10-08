import os
import shutil
from langdetect import detect
from PyPDF2 import PdfReader

'''
把拿到的一个包含中英文 pdf 的文件夹里面的 pdf
按照中文、英文分出来
'''

SRC_FOLDER = "/home/buding/haqian/data/Quantitative Trading"  # 要扫描的源目录
MIN_TEXT_LEN = 50  # 文本长度阈值，小于则视为未识别/扫描件
MAX_PAGES = 5      # 只读取前 N 页

def extract_text_from_pdf(pdf_path, max_pages=MAX_PAGES):
    """只提取前 max_pages 页文本"""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            if i >= max_pages:
                break
            # 某些页可能提取不到文本（如扫描件）
            page_text = page.extract_text() or ""
            text += page_text
    except Exception as e:
        print(f"无法读取文件 {pdf_path}: {e}")
    return text

def detect_language(text):
    """检测文本语言，优先识别中文/英文，其他返回 unknown"""
    if not text or len(text.strip()) < MIN_TEXT_LEN:
        return "unknown"
    try:
        lang = detect(text)  # 可能返回 'zh-cn','zh-tw','en','ja' 等
        if lang.startswith("zh"):
            return "zh"
        elif lang == "en":
            return "en"
        else:
            return "unknown"
    except Exception:
        return "unknown"

def ensure_unique_path(dst_path):
    """若目标文件已存在，自动追加计数避免覆盖"""
    if not os.path.exists(dst_path):
        return dst_path
    base, ext = os.path.splitext(dst_path)
    idx = 1
    while True:
        candidate = f"{base} ({idx}){ext}"
        if not os.path.exists(candidate):
            return candidate
        idx += 1

def classify_pdfs(src_folder):
    # 目标根目录：与源目录同级
    parent_dir = os.path.dirname(src_folder.rstrip(os.sep))
    dest_root = os.path.join(parent_dir, "PDF_Sorted")

    chinese_folder = os.path.join(dest_root, "Chinese_PDFs")
    english_folder = os.path.join(dest_root, "English_PDFs")
    unknown_folder = os.path.join(dest_root, "Unknown_PDFs")

    # 创建目标目录
    os.makedirs(chinese_folder, exist_ok=True)
    os.makedirs(english_folder, exist_ok=True)
    os.makedirs(unknown_folder, exist_ok=True)

    # 为了安全：不扫描目标根目录（尽管与源目录同级，仍加此判断以防万一）
    def is_under_dest(path):
        try:
            return os.path.commonpath([os.path.abspath(path), os.path.abspath(dest_root)]) == os.path.abspath(dest_root)
        except ValueError:
            return False

    for root, _, files in os.walk(src_folder):
        # 跳过目标目录（理论上不会走到，但以防软链接等情况）
        if is_under_dest(root):
            continue

        for file in files:
            if not file.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(root, file)
            print(f"正在分析: {pdf_path}")

            text = extract_text_from_pdf(pdf_path)
            lang = detect_language(text)

            if lang == "zh":
                target_dir = chinese_folder
                hint = "→ 复制到 Chinese_PDFs"
            elif lang == "en":
                target_dir = english_folder
                hint = "→ 复制到 English_PDFs"
            else:
                target_dir = unknown_folder
                hint = "→ 复制到 Unknown_PDFs（未识别或扫描件）"

            dst_path = ensure_unique_path(os.path.join(target_dir, file))
            try:
                shutil.copy2(pdf_path, dst_path)
                print(hint)
            except Exception as e:
                print(f"复制失败 {pdf_path} -> {dst_path}: {e}")

if __name__ == "__main__":
    classify_pdfs(SRC_FOLDER)
