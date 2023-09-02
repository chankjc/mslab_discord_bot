# mslab_discord_bot

Meeting notification on MSLAB Discord server

## env
```bash
mv .env.example .env
vim .env
```
```
NOTIFY = 1  # notify on or off (1/0)
INTERVAL = 10   # check interval (minutes)
DISCORD_BOT_TOKEN = "" # discord bot
DISCORD_MEETINGTIME_NOTIFICATION_CHANNEL =   #  meeting notification channel id 
MSLAB_ACCOUNT = ""   # your mslab wiki account
MSLAB_PASSWORD = ""   # your mslab wiki password
OPENAI_CHAT_MODEL = "gpt-3.5-turbo"
OPENAI_API_KEY = ""
```

## install
pip
```bash
pip install -r requirements.txt
```
or \
poetry
```
poetry shell
poetry install
```

## prepare
- https://www.dokuwiki.org/devel:xmlrpc?fbclid=IwAR0la60ASMWJ8qhrqAqZDZZcelpKpOtN_2OkgicFQsxBU-D5MYP2I7Br7_s
- https://www.dokuwiki.org/xmlrpc
- https://www.dokuwiki.org/config:remoteuser
- Prepare for applications
    -   Meeting times notification
        -   create the releated database
```
./prepare.sh
``` 

## run for test
```bash
pytest
./run.sh
```

## run as daemon

1. create .service first
```bash
./help_for_create_service.sh 
```
2. link daemon to .service
```bash
systemctl --user link $PWD/mslab_discord_bot.service
```
3. start
```bash
systemctl --user start mslab_discord_bot
```
- you can check daemon status
```bash
# status
systemctl --user status mslab_discord_bot  
# stop
systemctl --user stop mslab_discord_bot  
# restart
systemctl --user restart mslab_discord_bot
```
- if you want to delete daemon
```bash
systemctl --user disable mslab_discord_bot
```
