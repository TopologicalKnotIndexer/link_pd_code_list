#!/bin/bash

# 使用 readlink -f 获取脚本的绝对路径（兼容符号链接）
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

# 切换到脚本所在目录
cd "$SCRIPT_DIR" || exit

# 如果目标目录不存在，那就创建他
mkdir -p ./data/pages
mkdir -p ./data/plain

# 获取主文件
wget -O ./data/main.html https://katlas.org/wiki/The_Thistlethwaite_Link_Table_L2a1-L11n459

# 提取所有扭结名称
python3 ./scripts/regex_extractor.py ./data/main.html ./data/link_url_set.txt

# 定义一个 Bash 函数
my_function() {
    echo "Processing $1"
    aim_file="./data/pages/${1##*/}.pdf"
    txt_file="./data/plain/${1##*/}.txt"
    if [ ! -f "$aim_file" ]; then
        echo "downloading ${1} ..."
        wkhtmltopdf --javascript-delay 3000 "${1}" "${aim_file}" >/dev/null 2>&1
    fi
    if [ ! -f "$txt_file" ]; then
        echo "extracting text ${1} ..."
        python3 ./scripts/pdf_to_text.py "${aim_file}" -o "${txt_file}"
    fi
    echo "Done with $1"
}

# 导出函数，使其在子 shell 中可用
export -f my_function

# 逐行读取文件并输出
cat ./data/link_url_set.txt |  parallel -j 30 my_function

# 从中提取 pd_code
python3 scripts/extract_pdcode.py ./data/plain/ ./data/pd_code_list.txt
