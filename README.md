# Run
Use Python3 to run bot.py
a .env with a bot 'discord_token' is needed

## !p o !play
- If URL sent, enqueues and plays it
- Else if text is sent, searches for it, enqueues and plays it
- Resumes playing of queue

## !s o !skip
- Skips to the next queue entry

## !erase
- Deletes queue and all downloaded files

## !pause
- Pauses

## !leave
- Removes bot from voice channel

## !join
- Adds bot to voice channel

# Heroku dependencies

Add the following buildpacks to the heroku app:

- https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest
- https://github.com/xrisk/heroku-opus