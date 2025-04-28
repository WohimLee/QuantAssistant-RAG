import os
import re
import json
from pathlib import Path


def classify_document(md_text):
    """判断文档类型：API文档、日志、指引、其他"""
    if re.search(r'(函数|参数|返回)', md_text):
        return 'api_doc'
    elif re.search(r'(升级日志|版本升级)', md_text):
        return 'log_doc'
    elif re.search(r'(安装|快速开始|操作指引)', md_text):
        return 'guide_doc'
    else:
        return 'other_doc'


def split_api_doc(md_text):
    """按接口切分API文档"""
    pattern = r'(##\s+[^\n]+)(.*?)(?=\n##\s+|\Z)'
    matches = re.findall(pattern, md_text, flags=re.DOTALL)
    chunks = []
    for title, content in matches:
        api_name = title.replace('##', '').strip()
        chunk_content = (title + '\n' + content).strip()
        chunks.append((api_name, chunk_content))
    return chunks


def split_log_doc(md_text):
    """按每个版本升级切分日志文档"""
    pattern = r'(\*\*R\d{4}.*?升级\*\*)(.*?)(?=\n\*\*R\d{4}|\Z)'
    matches = re.findall(pattern, md_text, flags=re.DOTALL)
    chunks = []
    for title, content in matches:
        version = title.strip('**').split('版本')[0]
        chunk_content = (title + '\n' + content).strip()
        chunks.append((version, chunk_content))
    return chunks


def split_guide_doc(md_text):
    """按小节切分指引文档"""
    pattern = r'(##\s+[^\n]+)(.*?)(?=\n##\s+|\Z)'
    matches = re.findall(pattern, md_text, flags=re.DOTALL)
    chunks = []
    for title, content in matches:
        section_name = title.replace('##', '').strip()
        chunk_content = (title + '\n' + content).strip()
        chunks.append((section_name, chunk_content))
    return chunks


def split_other_doc(md_text):
    """简单固定长度切分其他文档"""
    chunk_size = 800
    chunks = []
    for i in range(0, len(md_text), chunk_size):
        chunks.append((f'chunk_{i//chunk_size}', md_text[i:i+chunk_size].strip()))
    return chunks

# ===== 主处理函数 =====

def process_markdown_files(input_dir, output_jsonl):
    Path(os.path.dirname(output_jsonl)).mkdir(parents=True, exist_ok=True)
    all_chunks = []

    for filename in os.listdir(input_dir):
        if not filename.endswith('.md'):
            continue

        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            md_text = f.read()

        doc_type = classify_document(md_text)
        module = filename.replace('.md', '')

        if doc_type == 'api_doc':
            splits = split_api_doc(md_text)
        elif doc_type == 'log_doc':
            splits = split_log_doc(md_text)
        elif doc_type == 'guide_doc':
            splits = split_guide_doc(md_text)
        else:
            splits = split_other_doc(md_text)

        for idx, (title, content) in enumerate(splits):
            chunk = {
                'id': f'{module}/{title.replace(" ", "_")}',
                'module': module,
                'section': title,
                'doc_type': doc_type,
                'content': content
            }
            all_chunks.append(chunk)

    # 写入JSONL
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')

    print(f'✅ 成功处理 {len(all_chunks)} 个chunk，输出到 {output_jsonl}')



if __name__ == '__main__':
    ROOT = "/Users/azen/Desktop/llm/QuantAssistant-RAG"
    INPUT_DIR = "data/量化云API文档说明/all"
    # 输出JSONL文件
    OUTPUT_JSONL = './output/chunks.jsonl'

    process_markdown_files(INPUT_DIR, OUTPUT_JSONL)
