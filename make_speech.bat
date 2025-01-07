@echo off
chcp 65001
set INPUT_FOLDER=.\work\Grreka_Jelly
set INPUT_FILE=%INPUT_FOLDER%\dialogue.json
set OUTPUT_FOLDER=.\work\Grreka_Jelly\mp3

echo python make_speech\main.py %INPUT_FILE% %OUTPUT_FOLDER%
