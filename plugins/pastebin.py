# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

# Some credits to catUB

import os
import re
import json
import aiohttp
import requests

from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text

#Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "content-type": "application/json",
}

#Pastebins
async def p_paste(message, extension=None):
    siteurl = "https://pasty.lus.pm/api/v1/pastes"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        purl = (
            f"https://pasty.lus.pm/{response['id']}.{extension}"
            if extension
            else f"https://pasty.lus.pm/{response['id']}.txt"
        )
        return {
            "url": purl,
            "raw": f"https://pasty.lus.pm/{response['id']}/raw",
            "bin": "Pasty",
        }
    return {"error": "Unable to reach pasty.lus.pm"}


async def s_paste(message, extension="txt"):
    siteurl = "https://spaceb.in/api/v1/documents/"
    try:
        response = requests.post(
            siteurl, data={"content": message, "extension": extension}
        )
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        if response["error"] != "" and response["status"] < 400:
            return {"error": response["error"]}
        return {
            "url": f"https://spaceb.in/{response['payload']['id']}",
            "raw": f"{siteurl}{response['payload']['id']}/raw",
            "bin": "Spacebin",
        }
    return {"error": "Unable to reach spacebin."}


async def c_paste(message, extension=None):
    siteurl = "http://catbin.up.railway.app/documents"
    data = {"content": message}
    try:
        response = requests.post(url=siteurl, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        purl = (
            f"http://catbin.up.railway.app/{response['key']}.{extension}"
            if extension
            else f"http://catbin.up.railway.app/{response['key']}"
        )
        return {
            "url": purl,
            "raw": f"http://catbin.up.railway.app/raw/{response['key']}",
            "bin": "Dog",
        }
    return {"error": "Unable to reach dogbin."}
    
    
@friday_on_cmd(['pasty'],
    cmd_help={
    "help": "paste to pasty",
    "example": "{ch}pasty",
    })
async def pasty(client, message):
    pablo = await edit_or_reply(message, "`Pasting to Pasty.....`")
    tex_t = get_text(message)
    message_s = tex_t
    if not tex_t:
        if not message.reply_to_message:
            await pablo.edit("`Reply To File / Give Me Text To Paste!`")
            return
        if not message.reply_to_message.text:
            file = await message.reply_to_message.download()
            m_list = open(file, "r").read()
            message_s = m_list
            os.remove(file)
        else:
            message_s = message.reply_to_message.text

    ext = "py"
    x = await p_paste(message_s, ext)
    p_link = x["url"]
    p_raw = x["raw"]

    pasted = f"**Pasted to Pasty**\n**Link:** [Pasty]({p_link})\n**Raw Link:** [Raw]({p_raw})"
    await pablo.edit(pasted, disable_web_page_preview=True)


@friday_on_cmd(['space'],
    cmd_help={
    "help": "paste to Spacebin",
    "example": "{ch}space",
    })
async def space_bin(client, message):
    pablo = await edit_or_reply(message, "`Pasting to Spacebin.....`")
    tex_t = get_text(message)
    message_s = tex_t
    if not tex_t:
        if not message.reply_to_message:
            await pablo.edit("`Reply To File / Give Me Text To Paste!`")
            return
        if not message.reply_to_message.text:
            file = await message.reply_to_message.download()
            m_list = open(file, "r").read()
            message_s = m_list
            os.remove(file)
        else:
            message_s = message.reply_to_message.text

    ext = "py"
    x = await s_paste(message_s, ext)
    s_link = x["url"]
    s_raw = x["raw"]

    pasted = f"**Pasted to Spacebin**\n**Link:** [Spacebin]({s_link})\n**Raw Link:** [Raw]({s_raw})"
    await pablo.edit(pasted, disable_web_page_preview=True)

@friday_on_cmd(['cbin'],
    cmd_help={
    "help": "paste to Catbin",
    "example": "{ch}cbin",
    })
async def cat_bin(client, message):
    pablo = await edit_or_reply(message, "`Pasting to Catbin.....`")
    tex_t = get_text(message)
    message_s = tex_t
    if not tex_t:
        if not message.reply_to_message:
            await pablo.edit("`Reply To File / Give Me Text To Paste!`")
            return
        if not message.reply_to_message.text:
            file = await message.reply_to_message.download()
            m_list = open(file, "r").read()
            message_s = m_list
            os.remove(file)
        else:
            message_s = message.reply_to_message.text

    ext = "py"
    x = await c_paste(message_s, ext)
    c_link = x["url"]
    c_raw = x["raw"]

    pasted = f"**Pasted to Catbin**\n**Link:** [Catbin]({c_link})\n**Raw Link:** [Raw]({c_raw})"
    await pablo.edit(pasted, disable_web_page_preview=True)

@friday_on_cmd(['haste'],
    cmd_help={
        "help": "Paste to Hastebin.",
        "example": "{ch}haste (reply to file or text)"
})
async def haste_bin(client, message):
    pablo = await edit_or_reply(message, "`Pasting to Hastebin.....`")
    tex_t = get_text(message)
    message_s = tex_t
    if not tex_t:
        if not message.reply_to_message:
            await pablo.edit("`Reply To File / Give Me Text To Paste!`")
            return
        if not message.reply_to_message.text:
            file = await message.reply_to_message.download()
            m_list = open(file, "r").read()
            message_s = m_list
            os.remove(file)
        else:
            message_s = message.reply_to_message.text

    link = "https://www.toptal.com/developers/hastebin/documents"

    async with aiohttp.ClientSession() as session:
        req = await session.post(link, data=message_s)
        resp = await req.json()
    key = resp.get("key")
    url = f"https://www.toptal.com/developers/hastebin/{key}"
    raw = f"https://www.toptal.com/developers/hastebin/raw/{key}"

    output = f"**Pasted to Hastebin**\n**Link:** [Hastebin]({url})\n**Raw Link:** [Raw]({raw})"
    await pablo.edit(output, disable_web_page_preview=True)
