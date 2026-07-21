import os

from .constants import OUTPUT_DIR


def write_summoner_output_file(summoner_name, active_status, output_text):
    path_folder = OUTPUT_DIR
    if not os.path.exists(path_folder):
        os.makedirs(path_folder)

    status_folder = fr"{path_folder}/{active_status}s"
    if not os.path.exists(status_folder):
        os.makedirs(status_folder)

    output_path = fr"{status_folder}/{summoner_name}.txt"
    with open(output_path, "w") as file:
        file.write(output_text)

    return output_path
