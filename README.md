# xcpcio/board-data

![](https://img.shields.io/github/repo-size/XCPCIO/board-data.svg)
[![Deploy](https://github.com/XCPCIO/board-data/actions/workflows/deploy.yml/badge.svg)](https://github.com/XCPCIO/board-data/actions/workflows/deploy.yml)

## Run

```bash
# generate index firstly
cd origin-data/gen-index
pip install -r requirements.txt
bash gen_index.sh
cd ../..

# start a http server
./start.sh
```
