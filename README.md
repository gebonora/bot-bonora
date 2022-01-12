# Run
Use Python3 to run bot.py

An .env file with a bot 'discord_token' is needed

## !p or !play $song
- Searches Youtube for $song, adds the first found to the queue
- Starts or resumes playing of queue

*Example:* `!p 1979 mashing pumpkins`

## !s or !skip
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