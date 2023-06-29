### general

bloog 6/27/2023:
even though it says below that pixiv is the current focus, i'm currently twisting the nipples off of gallery-dl's artstation extractor with pycharm's debugger since the site doesn't require oauth or any login credentials to get everything. low hanging fruit. i'll probably go after kemono/coomer party next for the same reason.

### felthier.py
for scraping the furaffinity tor archive posted by !RestrainedRaptor.

- og post: https://www.furaffinity.net/journal/6873564/
- tor site: http://g6jy5jkx466lrqojcngbnksugrcfxsl562bzuikrka5rv7srgguqbjid.onion/fa/

update 6/29/2023:
- i fixed a thing that doesnt really matter related to download file naming.
- the script will now stop the tor process no matter how it exits.

known issues:
- on occasion the tor connection will error, usually during longer galleries. i don't know what causes this.
- tor script needs modified to know the default location of tor on linux.
- script has no retry feature, this is because i haven't had a failure yet. i don't know what the error looks like.
- script doesn't handle nonexistant users. will fail without reporting.

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
