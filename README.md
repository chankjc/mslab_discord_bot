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
```bash
pip install -r requirements.txt
```

## prepare
- https://www.dokuwiki.org/devel:xmlrpc?fbclid=IwAR0la60ASMWJ8qhrqAqZDZZcelpKpOtN_2OkgicFQsxBU-D5MYP2I7Br7_s
- https://www.dokuwiki.org/xmlrpc
- https://www.dokuwiki.org/config:remoteuser
## run
```bash
./run.sh
```