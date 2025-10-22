import os
import subprocess
from pathlib import Path
from PyPDF2 import PdfReader  # pip install PyPDF2

# ===== 配置部分 =====
input_dir = Path("/home/buding/haqian/data/Sorted_files/docx")  # 输入目录
output_dir = Path("/home/buding/wohim/data/output/docx_res")    # 输出目录
if not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)
mineru_base = [
    "mineru",
    "-o", str(output_dir),
    "-b", "vlm-http-client",
    "-u", "http://127.0.0.1:30000",
    "--max-tokens", "768",
    "--image-max-long-side", "1024",
]



def parse_pdf():
    # ===== 获取 PDF 页数 =====
    def get_pdf_pages(file_path: Path) -> int:
        try:
            reader = PdfReader(str(file_path))
            return len(reader.pages)
        except Exception as e:
            print(f"⚠️ 无法读取页数: {file_path.name} ({e})")
            return 0

    # ===== 主逻辑 =====
    files = list(input_dir.glob("*.pdf"))  # 若需递归子目录，改为 rglob("*.pdf")
    print(f"共找到 {len(files)} 个 PDF 文件。")

    for i, file_path in enumerate(files, 1):
        num_pages = get_pdf_pages(file_path)
        print(f"[{i}/{len(files)}] 正在处理: {file_path.name} (共 {num_pages} 页)")
        
        cmd = mineru_base + ["-p", str(file_path)]
        try:
            result = subprocess.run(cmd, check=True)
            print(f"✅ 完成: {file_path.name}\n")
        except subprocess.CalledProcessError as e:
            print(f"❌ 处理失败: {file_path.name}")
            print(e.stderr)
            print("-" * 60)


if __name__ == "__main__":
    parse_pdf()

