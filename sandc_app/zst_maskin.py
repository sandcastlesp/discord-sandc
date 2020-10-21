from collections import defaultdict

from transformers import pipeline

class Rum:
    def __init__(r, kontext = 20):
        r.msg_hist = []
        r.kontext = kontext

    def putta(r, nick, msg):
        r.msg_hist.append((nick, msg))
        if len(r.msg_hist) > r.kontext:
            r.msg_hist = r.msg_hist[1:]

class ZstMaskin:
    def __init__(z):
        z.rumkatalog = defaultdict(Rum)
        z.globalrum = Rum(kontext=50)
        z.g = pipeline('text-generation')

    def recv_message(z, rum, nick, msg):
        z.rumkatalog[rum].putta(nick, msg)
        z.globalrum.putta(rum + "/" + nick, msg)

    def signalera(self, rum, nick=None, prefix="", generalize=False):
        if generalize:
            nick = rum + "/" + nick
            rum = None
        r = z.rumkatalog[rum] if rum else z.globalrum
        pretext = '\n'.join('{}: {}'.format(n, m) for (n, m) in r.msg_hist) + '\n'
        if nick:
            pretext = pretext + '{}: '.format(nick)
        pretext = pretext + prefix
        c = z.g(pretext, max_length=120)
        te = c[0]['generated_text']
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


