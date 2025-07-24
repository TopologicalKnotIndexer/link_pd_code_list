import PyPDF2
import argparse
import os

def pdf_to_text(pdf_path, text_path=None, output_encoding='utf-8'):
    """
    将 PDF 文件转换为文本文件
    
    参数:
    pdf_path (str): 输入 PDF 文件路径
    text_path (str, optional): 输出文本文件路径，默认为 PDF 同名文件
    output_encoding (str, optional): 输出文件编码，默认为 UTF-8
    """
    # 检查输入文件是否存在
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"输入文件不存在: {pdf_path}")
    
    # 如果未指定输出路径，使用与 PDF 相同的文件名（替换扩展名）
    if text_path is None:
        base_name = os.path.splitext(pdf_path)[0]
        text_path = f"{base_name}.txt"
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            # 创建 PDF 阅读器对象
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # 获取 PDF 页数
            num_pages = len(pdf_reader.pages)
            
            # 提取每一页的文本
            extracted_text = []
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if text:
                    extracted_text.append(text)
            
            # 合并所有页面的文本
            full_text = "\n\n".join(extracted_text)
            
            # 写入文本文件
            with open(text_path, 'w', encoding=output_encoding) as text_file:
                text_file.write(full_text)
                
            print(f"成功提取 {num_pages} 页内容到 {text_path}")
            return text_path
            
    except Exception as e:
        print(f"处理 PDF 时出错: {e}")
        return None

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='将 PDF 文件转换为文本文件')
    parser.add_argument('input_pdf', help='输入 PDF 文件路径')
    parser.add_argument('-o', '--output', help='输出文本文件路径', default=None)
    parser.add_argument('-e', '--encoding', help='输出文件编码', default='utf-8')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 执行转换
    output_file = pdf_to_text(args.input_pdf, args.output, args.encoding)
    
    if output_file:
        print(f"PDF 转换完成，文本已保存至: {output_file}")
    else:
        print("PDF 转换失败")
