# LOL BOT

Simple bot that fetches League of Legends summoner information (level, match history, and more).

## Quick install (uv)

1. Install [uv](https://docs.astral.sh/uv/).
2. Make sure Chrome is installed.
3. From the project root, install dependencies:
   ```bash
   uv sync
   ```

## Run

```bash
uv run python main.py
```

You can also run through the script entrypoint:

```bash
uv run lol-checker
```

## `Summoners.txt` format

Each line must be:

`region name tag`

Supported regions: `euw1`, `na1`, `eun1`

Example:

```txt
euw1 bezo 123
na1 ton EUW
```

Notes:
- One summoner per line
- Blank lines are ignored
- Lines starting with `#` are ignored

## Output

- Files are saved in the `Summoners/` folder.
- The bot uses a bounded worker pool (default max 4).

## Windows EXE

Download the prebuilt executable from [releases](https://github.com/AbdullahSaidAbdeaaziz/LOL_BOT-/releases/tag/v1.0.0).

## Contribution

PRs are welcome.