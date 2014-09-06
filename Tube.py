import re
import urllib2
from bs4 import BeautifulSoup

WORDS = ["TUBE", "TRAIN", "UNDERGROUND", "DELAYS", "DELAY"]
URL = "http://cloud.tfl.gov.uk/TrackerNet/LineStatus"

def handle(text, mic, profile):
    mic.say("Tube information")
    matches = findDelays()
    if len(matches) > 0:
        output = ', '.join(matches)
        output = 'The following lines have delays: '+output
    else:
        output = 'Everything is awesome!'
    mic.say(output)

def findDelays():
    req = urllib2.Request(URL)
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page)
    matches = soup.find_all('status', cssclass='DisruptedService')
    if len(matches) > 0:
        lines = [m.find_parent('linestatus').line for m in matches]
        return set([line['name'] for line in lines])
    else:
        return []



def isValid(text):
    return bool(re.search(r"\b(tube|trains?|underground|delays?)\b", text, re.IGNORECASE))
