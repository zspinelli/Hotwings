### general

blog jul/10/2023:
i made a bunch of changes to my development copy of the program. i'm going to do another "total replacement" type of update when i post the artstation scraper.
it will accompany some deduplication code and a new utility script for the felthier site that should benefit any hardheaded datahoarders.

### felthier.py
for scraping the furaffinity tor archive posted by !RestrainedRaptor.

- og post: https://www.furaffinity.net/journal/6873564/
- tor site: http://g6jy5jkx466lrqojcngbnksugrcfxsl562bzuikrka5rv7srgguqbjid.onion/fa/

update jun/29/2023:
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
- artstation <- current focus
- deviantart
- facebook
- generic (fandom.com/wiki, MSDN, wiki, etc)
- furaffinity
- kemono.party
- mangakatana
- minitokyo
- newgrounds
- pixiv
- tumblr
- twitter
