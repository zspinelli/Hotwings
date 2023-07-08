### general

bloog jul/8/2023:
i added a missing 'not' to stdargs. now it wont complain about not having an output dir.
the artstation scraper is going well. its very uncomplicated now being decoupled from the rest of gallery-dl.

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
