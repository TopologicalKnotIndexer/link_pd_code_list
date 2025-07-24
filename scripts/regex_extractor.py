import re
import sys

def extract_patterns(file_path):
    """从文件中提取匹配的模式并去重"""
    pattern = r'("/wiki/L\d+(a|n)\d+")'
    unique_matches = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 查找所有匹配的内容
                matches = re.findall(pattern, line)
                unique_matches.update(matches)
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在。")
        return []
    except Exception as e:
        print(f"错误：读取文件时发生异常：{e}")
        return []
    
    # 将集合转换为列表并排序
    sorted_matches = sorted(unique_matches)
    return sorted_matches

def main():
    if len(sys.argv) != 3:
        print("用法：python regex_extractor.py <输入路径> <输出路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    patterns = extract_patterns(file_path)
    
    # 输出结果
    with open(sys.argv[2], "w") as fp:
        for pattern in patterns:
            fp.write("https://katlas.org" + pattern[0][1:-1] + "\n")

if __name__ == "__main__":
    main()
