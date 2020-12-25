import os
import discord

TOKEN = os.environ["sandc_token"]
brusig = os.environ.get("sandc_brus")
brus = bool(brusig)

client = discord.Client()

from .zst_maskin import ZstMaskin

maskin = ZstMaskin()
seen_chans = []
allowed_chans = []

def desc_chan(msg):
    return str(msg.channel)

def handle_message(msg):
    content = msg.content
    meta = False
    prefix = ""
    if content.strip() == "T":
        meta = True
    elif content.startswith('T '):
        meta = True
        prefix = content[2:]
    chan = desc_chan(msg)
    if not meta:
        maskin.recv_message(desc_chan(msg), msg.author.name, msg.content)
    prefix = content[2:] if meta else ""

    return meta, chan, prefix


@client.event
async def on_message(msg):
    if msg.author == client.user:
        print("FLAMS!!!")
        return
    meta, chan, prefix = handle_message(msg)
    # we do not want the bot to reply to itself
    if meta or brus:
        #TODO: auto : på context
        context, reply = maskin.signalera(chan, prefix=prefix)

        print("\n===============")
        print(context + "@@" + reply)
        if meta:
            await msg.channel.send(prefix + reply)
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
    
    print(client.guilds)
    for g in client.guilds:
        print(g)
        for c in g.channels:
            print(c)
            if not isinstance(c, discord.TextChannel):
                continue
            async for m in c.history(limit=50):
                if m.author == client.user:
                    print("CENCUR!!!")
                else:
                    print(m)
                    handle_message(m)

client.run(TOKEN)
