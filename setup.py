from cx_Freeze import setup, Executable
import os

base = None
# desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
executables = [Executable(
    script="main.py", base=base, icon="league.ico", target_name="LOL-Checker"
)]

packages = ["selenium", "prettytable", "pyfiglet"]
include_files = ['Summoners.txt']
if os.path.exists('chromedriver.exe'):
    include_files.append('chromedriver.exe')

options = {
    'build_exe': {
        'packages': packages,
        'include_files': include_files

    },
}

setup(
    name="LOL_CHECKER",
    options=options,
    version="1.0",
    description="It's bot that parse information about specific name in account",
    executables=executables
)
