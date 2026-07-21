# LOL BOT

----

- It's simple bot that fetch some information
- about summoner like (level, match history)

## Installation

1. Chrome browser should be installed.
2. python is installed with 3.11 at most don't use 3.12.
3. Install dependencies from `requirements.txt`.

> There file `Summoners.txt` that contains summoners info.
> 
> Info in this way
> 
> region (euw1, na1, eun1), name, tag
>  - For example: euw1 bezo 123
>
> Notes:
> - one summoner per line
> - blank lines are ignored
> - comment lines starting with `#` are ignored

go to [release](https://github.com/AbdullahSaidAbdeaaziz/LOL_BOT-/releases/tag/v1.0.0) to download `EXE` program.

### OUTPUT
- In `Summoners/` folder.
- The bot uses a bounded worker pool (default max 4) to avoid creating too many browser sessions at once.

### Contribution

- are welcome ping me with your `pull request`.