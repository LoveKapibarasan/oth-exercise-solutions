#!/bin/bash

WEB_SESSION="$1"
if [ -z "$1" ]; then
    echo "Usage: $0 <WEB_SESSION_ID>"
    exit 1
fi

sudo apt update && sudo apt install -y git python3-pip python3-venv
git clone git@github.com:LoveKapibarasan/kifs.git

if [ ! -d "kifs" ]; then
    git clone git@github.com:LoveKapibarasan/kifs.git
fi

cd kifs || exit
echo "WEB_SESSION=$WEB_SESSION" > .env

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Usage: python swars_crawler.py [start] [end] [game_type]
python3 swars_crawler.py 1000 1500 sb
# Usage: python3 kif_downloader.py [input_jsonl]
python3 kif_downloader.py games_sb.jsonl