from collections import defaultdict

from transformers import pipeline, AutoTokenizer, AutoModel
from transformers import GPT2LMHeadModel

class Rum:
    def __init__(r, kontext = 20):
        r.msg_hist = []
        r.kontext = kontext

    def putta(r, nick, msg):
        r.msg_hist.append((nick, msg))
        if len(r.msg_hist) > r.kontext:
            r.msg_hist = r.msg_hist[1:]

class ModellBygge:
    def __init__(m, name):
        modclass = GPT2LMHeadModel
        m.tokenizer = AutoTokenizer.from_pretrained(name)
        m.model = modclass.from_pretrained(name)

    def skrik(m, input, n=1):
        plen = len(input)
        datain = m.tokenizer.encode(input, return_tensors='pt')
        daout = m.model.generate(input_ids=datain, max_length=len(datain[0])+20)
        text = m.tokenizer.decode(daout[0])
        return text[plen:]

class ZstMaskin:
    def __init__(z):
        z.rumkatalog = defaultdict(Rum)
        z.globalrum = Rum(kontext=50)

        z.m = ModellBygge("gpt2-large")

    def recv_message(z, rum, nick, msg):
        z.rumkatalog[rum].putta(nick, msg)
        z.globalrum.putta(rum + "/" + nick, msg)

    def signalera(z, rum, nick=None, prefix="", generalize=False):
        if generalize:
            nick = rum + "/" + nick
            rum = None
        r = z.rumkatalog[rum] if rum else z.globalrum
        pretext = '\n'.join('{}: {}'.format(n, m) for (n, m) in r.msg_hist) + '\n'
        if nick:
            pretext = pretext + '{}: '.format(nick)
        pretext = pretext + prefix
        te = z.m.skrik(pretext)
        tote = te.replace('\xa0', '\n')
        tote = tote.replace(' \n', '\n')
        print(tote)
        return pretext, tote

if __name__ == '__main__':
    z = ZstMaskin()
    z.recv_message("general", "bfredl", "this is sparta")
    z.recv_message("general", "bfredl", "knuffas inte")
    print(z.signalera("general", "tinkzorg"))
    print(z.signalera("general", "tinkzorg", generalize=True))

