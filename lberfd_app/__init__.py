import os
import discord

TOKEN = os.environ["lberfd_token"]

client = discord.Client()
from transformers import pipeline
g = pipeline('text-generation')

the_seed = []

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    meta = message.content.startswith('T ')
    print(repr(message.author))
    if message.author == client.user:
        return
    if not meta:
        the_seed.append(message.author.name+": "+ message.content)
        if len(the_seed) > 8:
            the_seed[:] = the_seed[1:]
        print(the_seed)

    if meta:
        context = message.content[2:]
        #TODO: auto : på context
        m2 = '\n'.join(the_seed) + '\n' + message.content[2:]
        # TODO: be dynamic. throw one away when too long usv
        maxlen = 700
        if len(m2) > maxlen:
            m2 = m2[-maxlen:]
        print("Y:", m2)
        c = g(m2, max_length=100)

        te = c[0]['generated_text']
        tote = te.replace('\xa0', '\n')
        tote = tote.replace(' \n', '\n')
        msg = 'R '+tote
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
