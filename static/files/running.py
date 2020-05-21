import xml.etree.ElementTree as ET
from urllib.request import urlopen
def check():
    act = 0
    tree = ET.parse(urlopen('http://www.p3rl4.me:81/riel/pi.xml'))
    for x in [1,2,3,4,5]:
        pidir='.//raspi'+str(x)
        on = tree.find(pidir).text
        if on == 'True':
            act=act+1
    return(act)
