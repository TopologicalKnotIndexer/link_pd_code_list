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
    
    # 递归遍历目录
    for root, dirs, files in os.walk(target_dir):
        for filename in files:
            # 跳过隐藏文件
            if filename.startswith('.'):
                continue
                
            file_path = os.path.join(root, filename)
            
            try:
                # 读取文件内容
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                # 检查内容是否为空或仅含空白字符
                if content.strip() == b'':
                    print(f"删除: {file_path}")
                    os.remove(file_path)
                    
            except Exception as e:
                print(f"处理文件 '{file_path}' 时出错: {e}")

if __name__ == "__main__":
    main()
