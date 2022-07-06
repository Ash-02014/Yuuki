from dataclasses import dataclass
from typing import Union
import hikari
import lightbulb
from typing import Any

EXTENSION_PATH = "./Yuuki/extensions"
CYAN = 0x03fccf
PINK = 0xff1fda

@dataclass
class Record:
    message_id: int
    user_id: int
    guild_id: int
    channel_id: int=None

@dataclass 
class UserRecord:
    user_id: int
    target_id: int

def find_content(event: hikari.MessageDeleteEvent, /) -> str:
    if event.old_message is None:
        content = "*Could not find any content*"
    
    elif event.old_message.content is None and event.old_message.attachments:
        content = "Contains attachment..."

    elif event.old_message.embeds:
        content = event.old_message.embeds[0].title or event.old_message.embeds[0].description

    else:
        content = event.old_message.content if event.old_message.content is not None and not event.old_message.content.isspace() else "*Could not find any content*"
        

    return content

async def get_attachment(message: hikari.Message, /) -> Union[None, bytes, hikari.Bytes]:
    if not message: return None
    if not message.attachments: return None
    return await message.attachments[0].read() if message.attachments[0].extension in ("png", "jpg", "jpeg") else None


def get_id(ctx: lightbulb.SlashContext, /) -> Union[None, str]:
    _content: str = ctx._options.get("id_or_link")
    if len(_content) == 18 and _content.isdigit(): message_id = _content

    elif len(_content) == 85 and not _content.isdigit() and _content.startswith("https://discord.com/channels/"): message_id = _content.split("/")[-1]

    else:
        return None
    
    return message_id

async def send_message(bot: Any, all_records: Union[Record, UserRecord], embed: hikari.Embed):
    for record in all_records:
        try: await (await bot.getch_user(record.user_id)).send(embed=embed)
        except (hikari.ForbiddenError, hikari.NotFoundError, hikari.BadRequestError): pass

LANGUAGES = ['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque', 'belarusian', 'bengali', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'estonian', 'filipino', 'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'kinyarwanda', 'korean', 'kurdish', 'kyrgyz', 'lao', 'latin', 'latvian', 'lithuanian', 'luxembourgish', 'macedonian', 'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 'mongolian', 'myanmar', 'nepali', 'norwegian', 'odia', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 'romanian', 'russian', 'samoan', 'scots gaelic', 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'tatar', 'telugu', 'thai', 'turkish', 'turkmen', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu']