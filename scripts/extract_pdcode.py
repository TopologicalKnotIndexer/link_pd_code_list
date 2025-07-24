import os
import re
import sys

def process_pdcode(s:str):
    lis = [item.strip() for item in s.split("X") if item.strip() != ""]
    ans = []
    for item in lis:
        if len(item) == 4:
            ans.append([int(ch) for ch in item])
        else:
            assert item.find(",") != -1
            ans.append([int(x) for x in item.split(",")])
    return ans

def main():
    # 检查命令行参数
    if len(sys.argv) != 3:
        print("用法: python extract_pdcode.py <输入文件夹> <输出文件>")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_file = sys.argv[2]
    
    # 验证输入文件夹是否存在
    if not os.path.isdir(input_folder):
        print(f"错误: 文件夹 '{input_folder}' 不存在")
        sys.exit(1)
    
    # 定义正则表达式模式
    pattern = r'((X(\s)*([\d,\s]+))+)'
    
    try:
        # 编译正则表达式
        regex = re.compile(pattern, re.DOTALL)
        
        # 打开输出文件
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # 遍历文件夹中的所有文件
            for filename in os.listdir(input_folder):
                # 只处理 .txt 文件
                if filename.endswith('.txt'):
                    file_path = os.path.join(input_folder, filename)
                    
                    try:
                        # 读取文件内容
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                        
                        # 查找所有匹配项
                        matches = regex.finditer(content)
                        
                        # 处理匹配结果
                        for match in matches:
                            # 获取完整匹配内容
                            full_match = match.group(0)
                            
                            # 移除所有空白字符
                            cleaned_match = process_pdcode(re.sub(r'\s', '', full_match))
                            
                            # 写入输出文件
                            outfile.write(f"{filename[:-4]}:{cleaned_match}\n")
                    
                    except Exception as e:
                        print(f"处理文件 '{filename}' 时出错: {e}")
    
    except Exception as e:
        print(f"执行过程中出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()