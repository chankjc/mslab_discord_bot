#!/usr/bin/env bash

file="mslab_discord_bot.service"
py=$(which python)
dir=$(pwd)
echo [Service] > $file
echo WorkingDirectory=$dir >> $file
echo Environment=\"PATH=$PATH\" >> $file
echo ExecStart=$dir/run.sh >> $file
echo ExecStop=/bin/kill -2 \$MAINPID >> $file
