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
DISCORD_CHANNEL =   # notification channel id 
MSLAB_ACCOUNT = ""   # your mslab wiki account
MSLAB_PASSWORD = ""   # your mslab wiki password
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

## run for test
```bash
./run.sh
```

## run as daemon (Todo, testing...)
```
# create .service first

./help_for_create_service.sh 
# if will help you create mslab_discord_bot.service


# link daemon to .service
# following command will create link from ~/.config/systemd/user/mslab_discord_bot.service -> mslab_discord_bot.service

systemctl --user link [/full/path/to/your/mslab_discord_bot.service]

# start
systemctl --user start mslab_discord_bot

# you can check daemon status
systemctl --user status mslab_discord_bot
```
```
# if you want to delete daemon
# following command delete ~/.config/systemd/user/mslab_discord_bot.service
systemctl --user disable mslab_discord_bot

```