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
    summoners = read_summoners_file()
    summoners = [summoner.split() for summoner in summoners]
    SIZE_THREADS = len(summoners)
    print("Fetching Summoners Data.....")
    with ThreadPool(SIZE_THREADS) as pool:
        for _ in pool.starmap(get_summoner, summoners):
            pass

    # for summoner in summoners:
    #     region, name, tag = summoner.split()
    #     print(f"{name}#{tag}")
    #     print("Fetching Summoner is data....")
    #     get_summoner(region, name, tag)
    #     print("Done fetching Summoner")


if __name__ == '__main__':
    main()
