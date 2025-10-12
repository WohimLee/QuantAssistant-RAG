import subprocess
from pathlib import Path
from PyPDF2 import PdfReader  # pip install PyPDF2

# ===== 配置部分 =====
input_dir = Path("/home/buding/wohim/data/PDF_Sorted/pdf/zh")  # 输入目录
output_dir = Path("/home/buding/wohim/data/output")             # 输出目录
mineru_base = [
    "mineru",
    "-o", str(output_dir),
    "-b", "vlm-http-client",
    "-u", "http://127.0.0.1:34343",
    "--max-tokens", "768",
    "--image-max-long-side", "1024",
]

# ===== 获取 PDF 页数 =====
def get_pdf_pages(pdf_path: Path) -> int:
    try:
        reader = PdfReader(str(pdf_path))
        return len(reader.pages)
    except Exception as e:
        print(f"⚠️ 无法读取页数: {pdf_path.name} ({e})")
        return 0

# ===== 主逻辑 =====
pdf_files = list(input_dir.glob("*.pdf"))  # 若需递归子目录，改为 rglob("*.pdf")
print(f"共找到 {len(pdf_files)} 个 PDF 文件。")

for i, pdf_path in enumerate(pdf_files, 1):
    num_pages = get_pdf_pages(pdf_path)
    print(f"[{i}/{len(pdf_files)}] 正在处理: {pdf_path.name} (共 {num_pages} 页)")
    
    cmd = mineru_base + ["-p", str(pdf_path)]
    try:
        result = subprocess.run(cmd, check=True)
        print(f"✅ 完成: {pdf_path.name}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ 处理失败: {pdf_path.name}")
        print(e.stderr)
        print("-" * 60)
