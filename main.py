from bot.lolbot import LOL
from multiprocessing.pool import ThreadPool
from pyfiglet import figlet_format


def read_summoners_file():
    with open(r"Summoners.txt", "r") as sums:
        summoners = sums.readlines()
        return summoners


def get_summoner(region: str, name: str, tag: int or str):
    try:
        lol = LOL(region, name, tag)

        lol.update_stat()
        # lvl = lol.get_level_summoner()
        # last_match = lol.last_match_played()
        lol.output_summoner_info()

    except Exception as e:
        print(e)


def main():
    print(figlet_format("LOL Checker"), "Developer By https://github.com/AbdullahSaidAbdeaaziz")
    try:
        summoners = read_summoners_file()
        if not summoners:
            raise ValueError
        summoners = [summoner.split() for summoner in summoners]
        THREAD_SIZE = len(summoners)
        print("Fetching Summoners Data.....")
        with ThreadPool(THREAD_SIZE) as pool:
            for _ in pool.starmap(get_summoner, summoners):
                pass
    except ValueError:
        print("""
-----|No Summoner found in `Summoners.txt`|-----
- Please Adding Summoners in this format (region, name, tag)
([euw1, na1, eun1], bezo ..etc, 123 ..etc)

for example put in `Summoners.txt`:
euw1 bezo 123
na1 ton EUW
""")
    input("Enter to continue...")


if __name__ == '__main__':
    main()
