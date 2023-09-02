#!/usr/bin/env bash

# meeting time database
python ./database/create_meeting_times_database.py
echo "default_setting = [{\"role\":\"system\", \"content\": \"\"}]" > default_message.py

