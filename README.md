##!p o !play
si recibe youtube url, pone la queue eso
else busca un video en youtube por el string y pone en la queue
pone a reproducir el primero si no hay args 

## !s o !skip
pasa a reproducir el siguiente de la queue

## !erase
borra la queue

## !pause
detiene la reproduccion

## !leave
lo echa del canal

##!bananero
reproduce un sonido random del bananero

# Heroku dependencies

Add the following buildpacks to the heroku app:

- https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest
- https://github.com/xrisk/heroku-opus