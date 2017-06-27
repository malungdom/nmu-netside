Norsk Målungdom netside v4
==========================

Dette er kjeldefilene til netstaden til Norsk Målungdom.  Den er bygd på den
statiske sidegeneratoren Lektor.

Lokal installasjon og oppsett
-----------------------------

.. highlight:: console

Dersom du brukar Windows, kan du fylgja ein `videogaid for oppsett`_. Resten
går ut i frå at du brukar Linux.

.. _`videogaid for oppsett`: https://www.youtube.com/watch?v=7TuBEDSeXRk

Du må ha Python installert. Du kan installera lektor til din eigen maskin ved
hjelp av `pip`. For å ikkje installera lektor på heile maskina kan du bruka
virtualenv for å laga deg ein eige Python-miljø berre for lektor::

  $ virtualenv env
  $ source env/bin/activate  # Aktiver miljøet (environment)
  $ pip install lektor  # Installer lektor

No kan du byggja netsida::

  $ lektor server

Du skal nå kunna gå til http://127.0.0.1:5000 og sjå sida.  Når du gjer
endringar so vil lektor bygga prosjektet på ny, og du kan gjera ei omlasting i
netlesaren din for å sjå resultatet av endringane du gjorde.

Lukke til!

Få endringane ut på netsida
---------------------------

For å få endringane til å visast på https://malungdom.no/ so må du lasta dei
opp til tenaren. Det gjer du ganske enkelt ved å pusha til GitHub, når
endringane landar i `master` vil dei automatisk gå til test-sida. Der kan du
trykka på 'Publiser' so kjem endringane på netsida.

Om du ikkje har tilgang, lag ein pull request på GitHub so tek ein av oss
endringa di inn.
