
from pwd import getpwuid
from collections import Counter

def count(l):
    return Counter(map(str, l))


def pilestr(pName, pile):
    string = ""
    string += pName
    string += "\n"

    for card, num in count(pile).items():
        string += str(num)
        string += " "
        string += str(card)
        string += "\n"

    string += "\n"
    return string 


def flatten(ls):
    val = []
    for l in ls:
        val.extend(l)
    return val

def get_username():
    return getpwuid( os.getuid() )[ 0 ]

