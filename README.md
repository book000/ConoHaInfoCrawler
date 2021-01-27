# ConoHaInfoCrawler

Crawl the [ConoHa Control Panel Information](https://cp.conoha.jp/information.aspx) and notify to Discord of new information.

## Requirements

- Python 3.6+
- [requirements.txt](requirements.txt): `requests`, `beautifulsoup4`

## Installation

1. Clone from GitHub repository: `git clone https://github.com/book000/ConoHaInfoCrawler.git`
2. Install the dependency package from `requirements.txt`: `pip3 install -r -U requirements.txt`

## Configuration

- Rewrite `config.sample.json` and rename to `config.json`.
  - `discord_token`: Discord Bot token
  - `discord_channel`: Discord Send to channel ID

## Usage

```shell
cd /path/to/
python3 main.py
```

The `config.json` file in the current directory will be read, so change to the root directory of the project in advance before executing.


## Warning / Disclaimer

The developer is not responsible for any problems caused by the user using this project.

## License

The license for this project is [MIT License](LICENSE).
