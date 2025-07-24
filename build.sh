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

# 逐行读取文件并输出
while IFS= read -r line; do
    aim_file="./data/pages/${line##*/}.pdf"
    txt_file="./data/plain/${line##*/}.txt"
    if [ ! -f "$aim_file" ]; then
        echo "downloading ${line} ..."
        wkhtmltopdf --javascript-delay 2000 "${line}" "${aim_file}"
    fi
    if [ ! -f "$txt_file" ]; then
        python3 ./scripts/pdf_to_text.py "${aim_file}" -o "${txt_file}"
    fi
done < "./data/link_url_set.txt"
