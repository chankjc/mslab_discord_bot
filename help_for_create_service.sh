#!/usr/bin/env bash

file="mslab_discord_bot.service"
py=$(which python)
dir=$(pwd)
echo [Service] > $file
echo ExecStart=$py $dir/bot.py >> $file
