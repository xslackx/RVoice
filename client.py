import re
import time
import os
from consume_feed import HackDay

debug: bool = True
skip_send: bool = True

if debug:
    rss = HackDay()
    rss.consume_feed()

    rss.parse_feed()
    if len(rss.articles) > 0:
        print("Found ", len(rss.articles)-1, "articles: \n")
        for index, article in enumerate(rss.articles):
            print(f"{index})", article["title"])
        print('\n')

    print("Did you like to see the description?\n[Y/n] ")
    user_choice = input()
    if user_choice == "Y" or user_choice == "y":
        print("Which: \n")
        user_choice = input()
    elif user_choice != "Y" or user_choice != "y":
        exit(1)

    if int(user_choice) <= len(rss.articles):
        print('\n\n\n')
        print("Title:", rss.articles[int(user_choice)]["title"])
        print("Date:", rss.articles[int(user_choice)]["pub_date"])
        print("Creator:", rss.articles[int(user_choice)]["creator"])
        print("Description:", rss.articles[int(user_choice)]["description"], '...')
        print('\n')
        print("Continue: ")
        hit = input()
        if not hit:
            if not skip_send:
                print(rss.send_feed("http://localhost:3636/tts/", rss.articles[int(user_choice)]))
            if skip_send:
                print(rss.articles[int(user_choice)])
                for stanzas in rss.articles[int(user_choice)]["content"]:
                    print(stanzas, '\n')
                    time.sleep(8.5)
        else:
            print('Bye!')