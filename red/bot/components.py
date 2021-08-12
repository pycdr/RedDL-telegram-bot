import html
from os import replace
import telebot
from .keyboards import Keyboard, NormalKeyboard
from math import ceil
from html import escape as html_escape


class Component:
    """
example:

comp = YourComponent(...)
comp = YourComponent(...) / YourKeyboard(...)
    """
    pass


class Text(Component):
    def __init__(self, text: str = "", keyboard=None):
        self.text = text
        self.keyboard = keyboard.generate() \
            if isinstance(keyboard, Keyboard) \
            else NormalKeyboard(keyboard).generate()

    def render(self, bot: telebot.TeleBot, **kwargs):
        for i in range(ceil(len(self.text)/4096)):
            bot.send_message(
                text=self.text[i*4096:(i+1)*4096],
                reply_markup=self.keyboard
                ** kwargs,
            )

    def __truediv__(self, keyboard: Keyboard):
        assert isinstance(
            keyboard, Keyboard
        ), "component keyboard must be from type <bot.Keyboard>"
        return Text(
            self.text,
            keyboard.generate()
        )

    def __add__(self, text):
        assert isinstance(
            text, (str, Text)), "(Text + Text) and (Text + str) are only supported"
        if isinstance(text, str):
            return Text(
                self.text + text,
                self.keyboard
            )
        else:  # type <Text>
            return Text(
                self.text + text.text,
                self.keyboard
            )

    def __str__(self) -> str:
        return self.text


class Markdown(Text):
    def render(self, bot: telebot.TeleBot, **kwargs):
        for i in range(ceil(len(self.text)/4096)):
            bot.send_message(
                text=self.text[i*4096:(i+1)*4096],
                **kwargs,
                reply_markup=self.keyboard,
                parse_mode="Markdown"
            )
    
    @staticmethod
    def plain(text):
        return text\
            .replace("*", "\\*")\
            .replace("_", "\\_")\
            .replace("\`", "\`")\
            .replace("[", "\\[")

    @staticmethod
    def bold(text: str): return f"*{Markdown.plain(text)}*"

    @staticmethod
    def italic(text: str): return f"_{Markdown.plain(text)}_"
    
    @staticmethod
    def link(text: str, link: str): return f"[{Markdown.plain(text)}]({link})"

    @staticmethod
    def monospace(text: str): return f"```\n{Markdown.plain(text)}\n```"

    @staticmethod
    def underline(text: str): return f"--{Markdown.plain(text)}--"

    @staticmethod
    def strikethrough(text: str): return f"~~{Markdown.plain(text)}~~"


class HTML(Text):
    def render(self, bot: telebot.TeleBot, **kwargs):
        for i in range(ceil(len(self.text)/4096)):
            bot.send_message(
                text=self.text[i*4096:(i+1)*4096],
                **kwargs,
                reply_markup=self.keyboard,
                parse_mode="Markdown"
            )
    
    @staticmethod
    def plain(text):
        return html_escape(text)

    @staticmethod
    def bold(text: str): return f"<b>{HTML.plain(text)}</b>"

    @staticmethod
    def italic(text: str): return f"<i>{HTML.plain(text)}</i>"
    
    @staticmethod
    def link(text: str, link: str): return f"<a href=\"{link}\">{HTML.plain(text)}]</a>"

    @staticmethod
    def code(text: str): return f"<code>{HTML.plain(text)}</code>"

    @staticmethod
    def underline(text: str): return f"<u>{HTML.plain(text)}</u>"

    @staticmethod
    def strikethrough(text: str): return f"<s>{HTML.plain(text)}</s>"


class Image(Component):
    def __init__(self, path: str, text: Text = Text(), keyboard=None):
        assert isinstance(
            text, Text), "<text> argument must be from type <Text> or <Markdown>"
        self.text = text.text if isinstance(
            text, Markdown) else Markdown.plain(text.text)
        self.photo_path = path
        self.keyboard = keyboard.generate() \
            if isinstance(keyboard, Keyboard) \
            else NormalKeyboard(keyboard).generate()

    def render(self, bot: telebot.TeleBot, **kwargs):
        bot.send_photo(
            photo=open(self.photo_path, 'rb'),
            caption=self.text[:1024],
            reply_markup=self.keyboard,
            parse_mode="Markdown",
            **kwargs
        )
        if len(self.text) > 1024:
            Markdown(self.text[1024:]).render(**kwargs)

    def __truediv__(self, keyboard: Keyboard):
        assert isinstance(
            keyboard, Keyboard
        ), "component keyboard must be from type <bot.Keyboard>"
        return Image(
            self.photo_path,
            self.text,
            keyboard.generate()
        )

    def __add__(self, text):
        assert isinstance(
            text, (str, Text)), "(Image + Text or Markdown) and (Image + str) are only supported"
        if isinstance(text, str):
            return Image(
                self.photo_path,
                self.text + text,
                self.keyboard
            )
        else:  # type <Text>
            return Image(
                self.photo_path,
                self.text + text.text,
                self.keyboard
            )


class File(Component):
    pass


class Audio(Component):
    pass


class Music(Component):
    pass
