from src.blacklist_check import *
from urlextract import URLExtract
from re import sub


def checkMgs(userMessage, THROW_IF_MESSAGE_CONSIST_URL, DELETE_URL_FROM_MESSAGE):
    if THROW_IF_MESSAGE_CONSIST_URL:
        urlExtract = URLExtract()
        urls = urlExtract.find_urls(userMessage)

        print(urls)
        if len(urls) > 0:
            userMessage = "THROW_THIS_MESSAGE"
            return userMessage

    if len(THROW_IF_MESSAGE_CONSIST_WORDS) > 0:
        for word in THROW_IF_MESSAGE_CONSIST_WORDS:
            if word in userMessage:
                userMessage = "THROW_THIS_MESSAGE"
                return userMessage

    if DELETE_URL_FROM_MESSAGE:
        urlExtract = URLExtract()
        urls = urlExtract.find_urls(userMessage)

        if len(urls) > 0:
            for url in urls:
                if url in userMessage:
                    userMessage = userMessage.replace(url, "")

    if len(FORWARD_IF_MESSAGE_CONSIST_WORDS) > 0:
        found = False
        for word in FORWARD_IF_MESSAGE_CONSIST_WORDS:
            if word in userMessage:
                found = True
                userMessage = blacklistCheck(userMessage)
                break
            else:
                continue

        if not found:
            userMessage = "THROW_THIS_MESSAGE"

    else:
        userMessage = blacklistCheck(userMessage)

    userMessage = sub(' +', ' ', userMessage)
    return userMessage

def find_index_of_channel(findIndexOf, findIndexIn):
    for i in range(len(findIndexIn)):
        if str(findIndexOf) in str(findIndexIn[i]):
            return i