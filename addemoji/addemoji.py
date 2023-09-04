import random
import processing_message.openaiapi as openaiapi

def emoji_response(msg):
    keywords = "Giving the following sentence: " + msg + ", Which of the following emotions best match this sentence?\n\n"
    keywords += "0. hello\n"
    keywords += "1. laughter\n"
    keywords += "2. happy\n"
    keywords += "3. sad\n"
    keywords += "4. mad\n"
    keywords += "5. think\n"
    keywords += "6. love\n"
    keywords += "7. good\n"
    keywords += "8. sorry\n"
    keywords += "9. none of all\n"
    # print(keywords)
    keywords = [{"role":"user", "content": keywords}]
    sentiment = openaiapi.ChatCompletion(keywords).content.strip()  
    # print(sentiment)
    
    if "none" in sentiment:
        return None
    if "hello" in sentiment:
        emoji = Helloemoji()
    elif "laughter" in sentiment:
        emoji = Laughteremoji()
    elif "happy" in sentiment:
        emoji = Happyemoji()
    elif "sad" in sentiment:
        emoji = Sademoji()
    elif "mad" in sentiment:
        emoji = Mademoji()
    elif "think" in sentiment:
        emoji = Thinkemoji()
    elif "love" in sentiment:
        emoji = Loveemoji()
    elif "good" in sentiment:
        emoji = Goodemoji()
    elif "sorry" in sentiment:
        emoji = Sorryemoji()
    else:
        emoji = None
       
    return emoji


def Helloemoji():
    emoji = ["👐","👏","👋","🤙"]
    return random.choice(emoji)

def Laughteremoji():
    emoji = ["😄","😁","🤣","😂"]
    return random.choice(emoji)

def Happyemoji():
    emoji = ["😀","🙂","😗","😜"]
    return random.choice(emoji)

def Sademoji():
    emoji = ["😞","😕","😥","😰"]
    return random.choice(emoji)

def Mademoji():
    emoji = ["😡","🤬","😠","😤"]
    return random.choice(emoji)

def Thinkemoji():
    emoji = ["🤔","😯","🤨","🧐"]
    return random.choice(emoji)

def Loveemoji():
    emoji = ["😍","🥰","😘","😚"]
    return random.choice(emoji)

def Goodemoji():
    emoji = ["👍","👍🏻","👍🏽","👍🏾"]
    return random.choice(emoji)

def Sorryemoji():
    emoji = ["👎","👎🏼","👎🏽","👎🏾"]
    return random.choice(emoji)

