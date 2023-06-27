### general

bloog 6/27/2023:
even though it says below that pixiv is the current focus, i'm currently twisting the nipples off of gallery-dl's artstation extractor with pycharm's debugger since the site doesn't require oauth or any actual login credentials. low hanging fruit. i'll probably go after kemono/coomer party next for the same reason.

### felthier.py
for scraping the furaffinity tor archive posted by !RestrainedRaptor.

og post: https://www.furaffinity.net/journal/6873564/

tor link: http://g6jy5jkx466lrqojcngbnksugrcfxsl562bzuikrka5rv7srgguqbjid.onion/fa/

update 5/27/2023:
- this scraper will now start tor by itself on windows provided tor browser is installed to its default directory on the desktop.
- the script will no longer function on linux or mac until their default tor locations are added to common/tor.py in the _BASE_PATH and _TOR_PATH dict constants.

known issues:
- on occasion the tor connection will error, usually during longer galleries. i don't know what the cause of this is. currently the scraper has to be restarted from this in a new command line.
- tor script needs modified to know the default location of tor on linux.
- script has no retry feature, this is because i haven't had a failure yet. i don't know what the error looks like.
- script doesn't handle nonexistant users.

## Future
planned scrapers:
- 600dpi
- artstation
- deviantart
- facebook
- generic (fandom.com/wiki, MSDN, wiki, etc)
- furaffinity
- kemono.party
- mangakatana
- minitokyo
- newgrounds
- pixiv <- current focus
- tumblr
- twitter
