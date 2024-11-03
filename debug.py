from syndication.base import basicFeed

debug = []

debug.append(
    basicFeed("HackDay", "https://hackaday.com/blog/feed/")
)
debug.append(
    basicFeed("ItsFoss", "https://news.itsfoss.com/latest/rss/")
)
debug.append(
    basicFeed("LinuxMagazine", "https://www.linux-magazine.com/rss/feed/lmi_news")
)
debug.append(
    basicFeed("Lwn", "https://lwn.net/headlines/rss")
)
debug.append(
    basicFeed("Phoronix", "https://www.phoronix.com/rss.php")
)
debug.append(
    basicFeed("JeffGeerling", "https://www.jeffgeerling.com/blog.xml")
)


for contents in debug:
    contents.consume_feed()
    contents.parse_feed()
    print(contents.articles[0])