from typing import Text
from .bot import Bot
from .components import (
    Text, Markdown, HTML
)

def test(token, user_id):
    bot = Bot(token)
    bot@user_id << Markdown("markdown:\n"+\
        f"{Markdown.bold('bold')}\n"+\
        f"{Markdown.italic('italic')}\n"+\
        f"{Markdown.underline('underline')}\n"+\
        f"{Markdown.link('google!', 'www.google.com')}\n"+\
        f"{Markdown.monospace('monospace')}\n"+\
        f"{Markdown.strikethrough('strikethrough')}"
    )
    bot@user_id << HTML("html:\n"+\
        f"{HTML.bold('bold')}\n"+\
        f"{HTML.italic('italic')}\n"+\
        f"{HTML.underline('underline')}\n"+\
        f"{HTML.link('google!', 'www.google.com')}\n"+\
        f"{HTML.monospace('monospace')}\n"+\
        f"{HTML.strikethrough('strikethrough')}"
    )
    # bot[:] << Text("Hello!")

if __name__ == "__main__":
    test(
        token = input("token:"),
        user_id = int(input("your user id:"))
    )