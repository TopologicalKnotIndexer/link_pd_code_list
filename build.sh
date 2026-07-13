#!/bin/bash
set -euo pipefail

# Resolve the repository root, including invocation through a symbolic link.
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
cd "$SCRIPT_DIR"

mkdir -p ./data/pages ./data/plain
python3 ./scripts/delete_empty_files.py ./data

wget -O ./data/main.html https://katlas.org/wiki/The_Thistlethwaite_Link_Table_L2a1-L11n459
python3 ./scripts/regex_extractor.py ./data/main.html ./data/link_url_set.txt

process_url() {
    local url="$1"
    local pdf_file="./data/pages/${url##*/}.pdf"
    local text_file="./data/plain/${url##*/}.txt"
    echo "Processing $url"
    if [ ! -f "$pdf_file" ]; then
        wkhtmltopdf --javascript-delay 3000 "$url" "$pdf_file" >/dev/null 2>&1
    fi
    if [ ! -f "$text_file" ]; then
        python3 ./scripts/pdf_to_text.py "$pdf_file" -o "$text_file"
    fi
}
export -f process_url

parallel -j 30 process_url :::: ./data/link_url_set.txt
python3 ./scripts/extract_pdcode.py ./data/plain ./data/pd_code_list.txt
python3 ./scripts/validate_pd_code_list.py
