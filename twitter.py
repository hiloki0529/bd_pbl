# -*- coding: utf-8 -*-

import tweepy


def twp():
        access_token = "760907401885212672-g7mYRfDEs4SsdpKsHOFcNNQuNmalXF8"
        access_token_secret = "1hEAhKmXZBkr0ZLYHJO4nI3yt9PZp9aI7FrytjldY7EAm"
        api_key = "GgxHcBZmJbn47e165jvnB2019"
        api_secret = "XwjhdEOoJQ9jVhePy6DBVdGTaKsQifwDxzRs16MGC6odtUWkUT"
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)

def send_DM(id,text):
    api = twp()
    api.send_direct_message(user = id,text = text)

if __name__ == '__main__':
    send_DM("Billie_Of_East", "hey,yo")
