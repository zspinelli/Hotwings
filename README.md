### general

blog: aug/8/2023:
the artstation scraper is nearly finished and fully functional. video downloads are supported through yt-dlp. it will be a bit before i post the update. i made huge changes to everything that should make the arguments system far more robust and simpler to use in future scrapers. the name collector utility script for felthier has been postponed. im finishing an experiment with a different approach to the feltheir scraper itself to hopefully enable removing beautifulsoup from the parsing process to remove whatever overhead it creates and reduce the number of dependencies.

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
- flikr
- generic (fandom.com/wiki, MSDN, wiki, etc)
- furaffinity
- kemono.party
- minitokyo
- newgrounds
- pixiv
- tumblr
- twitter
