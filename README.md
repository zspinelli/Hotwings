
### common.py
shared funtions between multiple scrapers.

### felthier.py
for scraping the furaffinity tor archive posted by !RestrainedRaptor.

og post: https://www.furaffinity.net/journal/6873564/

tor link: http://g6jy5jkx466lrqojcngbnksugrcfxsl562bzuikrka5rv7srgguqbjid.onion/fa/

update 5/27/2023
this scraper will now start tor by itself on windows provided tor browser is installed to its default directory on the desktop.
the script will no longer function on linux or mac until their default tor locations are added to common/tor.py in the _BASE_PATH and _TOR_PATH dict constants.

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
