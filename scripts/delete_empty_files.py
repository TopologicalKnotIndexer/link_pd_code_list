import os
import sys

def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python delete_empty_files.py <目录路径>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    
    # 验证目录是否存在
    if not os.path.isdir(target_dir):
        print(f"错误: 目录 '{target_dir}' 不存在")
        sys.exit(1)
    
    # 遍历目录中的所有文件
    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        
        # 跳过目录和隐藏文件
        if not os.path.isfile(file_path) or filename.startswith('.'):
            continue
        
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查内容是否为空或仅含一个换行符
            if content.strip() == '':
                print(f"删除: {file_path}")
                os.remove(file_path)
                
        except Exception as e:
            print(f"处理文件 '{file_path}' 时出错: {e}")

if __name__ == "__main__":
    main()