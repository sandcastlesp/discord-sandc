import os
import discord

TOKEN = os.environ["sandc_token"]
brusig = os.environ.get("sandc_brus")
brus = bool(brusig)

client = discord.Client()

from .zst_maskin import ZstMaskin

maskin = ZstMaskin()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    content = message.content
    meta = False
    prefix = ""
    if content.strip() == "T":
        meta = True
    elif content.startswith('T '):
        meta = True
        prefix = content[2:]
    chan = str(message.channel)
    print(chan)
    if not meta:
        maskin.recv_message(chan, message.author.name, content)

    if meta or brus:
        #TODO: auto : på context
        prefix = message.content[2:] if meta else ""
        context, msg = maskin.signalera(chan, prefix=prefix)

        print("\n===============")
        print(context + "@@" + msg)
        if meta:
            await message.channel.send(prefix + msg)
        else:
            pass
            #print('\x16\x63')
            #print(msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
