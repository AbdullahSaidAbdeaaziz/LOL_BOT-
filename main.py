from bot.lolbot import LOL


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
    # print(figlet_format("LOL Checker"), "Developer By https://github.com/AbdullahSaidAbdeaaziz")
    summoners = read_summoners_file()
    print(summoners)

    for summoner in summoners:
        region, name, tag = summoner.split()
        get_summoner(region, name, tag)


if __name__ == '__main__':
    main()
