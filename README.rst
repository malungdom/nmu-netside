Norsk Målungdom netside v4
==========================

Dette er kjeldefilene til netstaden til Norsk Målungdom.  Den er bygd på den
statiske sidegeneratoren Lektor.

Lokal innstallasjon og oppsett
------------------------------

Du må ha Python installert. Du kan installera lektor til din eigen maskin ved
hjelp av `pip`. For å ikkje installera lektor på heile maskina kan du bruka
virtualenv for å laga deg ein eige Python-miljø berre for lektor:

    $ virtualenv env
    $ source env/bin/activate  # Aktiver miljøet (environment)
    $ pip install lektor  # Installer lektor

No kan du byggja netsida:

    $ lektor server

Du skal nå kunna gå til http://127.0.0.1:5000 og sjå sida.  Når du gjer
endringar so vil lektor bygga prosjektet på ny, og du kan gjera ei omlasting i
netlesaren din for å sjå resultatet av endringane du gjorde.

Lukke til!

Få endringane ut på netsida
---------------------------

For å få endringane til å visast på http://ny.malungdom.no/ so må du lasta det
opp til tenaren.  Det kan du gjera ved denne lektor kommandoen (pass på at du
har aktivert virtualenv):

    $ lektor deploy production
