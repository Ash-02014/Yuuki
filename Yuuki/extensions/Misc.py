import asyncio
import hikari
import lightbulb
from deep_translator import GoogleTranslator
from ..core import Yuuki
from ..utils import LANGUAGES, PINK, CYAN

class Misc(lightbulb.Plugin):
    def __init__(self):
        super().__init__("Miscellanous commands!", "Miscellaneous Utility commands@")
        self.bot: Yuuki

misc = Misc()

@misc.command
@lightbulb.command(name="ping", description="Get my ping in milliseconds!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.SlashContext) -> None:
    embed = hikari.Embed(description=f"My Ping is **{round(misc.bot.heartbeat_latency * 1000)}**ms!")
    await ctx.respond(embed=embed)

@misc.command
@lightbulb.command(name="uptime", description="Get my uptime!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def uptime(ctx: lightbulb.SlashContext) -> None:
    await ctx.respond(f"My Uptime -> `{misc.bot.uptime}`")

@misc.command
@lightbulb.option(name="language", description="The language to convert the text to!", required=True, autocomplete=True, type=str)
@lightbulb.option(name="source_language", description="The language to convert the text from!", required=True, autocomplete=True, type=str)
@lightbulb.option(name="text", description="The text to translate!", required=True, type=str)
@lightbulb.command(name="translate", description="Translate text to another language!", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def translate_text(ctx: lightbulb.SlashContext):
    language = ctx._options.get("language")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    def _():
        translator = GoogleTranslator(target=language)
        return translator.translate(ctx._options.get("text"))
    res = await loop.run_in_executor(None, _)
    
    embed = hikari.Embed(title="Translation Success!", description=f"**English** to **{language}**", colour=PINK).add_field("Translated text", res[:1000])
    await ctx.respond(embed=embed)

@translate_text.autocomplete("language", "source_language")
async def autocomplete_language(option: hikari.AutocompleteInteractionOption, interaction: hikari.AutocompleteInteraction):
    return [lang for lang in LANGUAGES if option.value in lang]

@misc.command
@lightbulb.command(name="supported_languages", description="Get all the supported languages for /translate", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def supported_langs(ctx: lightbulb.SlashContext):
    embed = hikari.Embed(title="Supported Languages", description=", ".join(LANGUAGES), colour=CYAN)
    await ctx.respond(embed=embed)

def load(bot: Yuuki):
    bot.add_plugin(misc)