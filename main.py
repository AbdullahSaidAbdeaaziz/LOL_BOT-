from bot.lolbot import LOL
from bot.output import write_summoner_output_file
from bot.parser import parse_summoners_lines
from bot.constants import MAX_WORKERS
from multiprocessing.pool import ThreadPool
from pyfiglet import figlet_format
from selenium.common.exceptions import WebDriverException, TimeoutException
import logging


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
LOGGER = logging.getLogger(__name__)


def read_summoners_file():
    with open(r"Summoners.txt", "r") as sums:
        return sums.readlines()


def get_summoner(region: str, name: str, tag: str):
    try:
        with LOL(region, name, tag) as lol:
            lol.update_stat()
            table = lol.output_summoner_info()
            write_summoner_output_file(lol.summoner_name, lol.active, table.get_string())
    except (TimeoutException, WebDriverException, ValueError) as exc:
        LOGGER.error("Failed to fetch %s#%s (%s): %s", name, tag, region, exc)


def main():
    print(figlet_format("LOL Checker"), "Developer By https://github.com/AbdullahSaidAbdeaaziz")
    try:
        parsed_summoners = parse_summoners_lines(read_summoners_file())
        if not parsed_summoners:
            raise ValueError
        thread_size = min(MAX_WORKERS, len(parsed_summoners))
        print("Fetching Summoners Data.....")
        with ThreadPool(thread_size) as pool:
            pool.starmap(
                get_summoner,
                [(summoner.region, summoner.name, summoner.tag) for summoner in parsed_summoners],
            )
    except (ValueError, OSError):
        print("""
-----|No Summoner found in `Summoners.txt`|-----
- Please Adding Summoners in this format (region, name, tag) and keep one summoner per line
([euw1, na1, eun1], bezo ..etc, 123 ..etc)
- Empty lines and lines starting with # are ignored

for example put in `Summoners.txt`:
euw1 bezo 123
na1 ton EUW
""")
    input("Enter to continue...")


if __name__ == '__main__':
    main()
