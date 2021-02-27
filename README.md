# Deprecated do not use, use bilara-data instead

SuttaCentral no longer uses Pootle or the PO format, all our translations are in JSon form in the bilara-data repo.

# Pootle FS git repository

**Note: the data in this repo is not meant for publication! It is a straight dump from Pootle and includes unfinished texts. Go [here](https://github.com/suttacentral/sc-data/tree/master/po_text) for the latest published files from pootle.**

This repository is intended to be used as the backend for Pootle FS
at the moment the data is placeholder because the Pootle FS git plugin
is rather buggy. The Pootle FS basic functionality seems to work okay
so maybe we could use Pootle FS to write to the file system then
do a manual git commit & push.

In any case, once this repository is linked to Pootle it should
be considered strictly "READ ONLY" unless you know exactly
what you're doing. It is for Pootle to manage and push updates to
it is possible to make changes to the repository and push them through
to Pootle but this requires running a management command for Pootle
and may cause merge conflicts requiring manual resolution.

## Folder Structure

Pootle FS allows using arbitary paths (to an extent) with variable
substitution, with the path template being defined per project.

A Pootle project itself can have multiple translation languages
it has one original language.

We will use a project path like this:

`<division>/<language>/<path>/<filename>.<ext>`

(Note that in Pootle FS <path> expands to any number of subdirectories)

With an actual file being like this:  

`dn/en/dn1.po`

or this:

`an/en/an1/an1.1.po`

## Getting additional info

A po file wont tell you the original language. But from the path we can
immediately see the translation language and the division and sutta uid
from either of those we can derive the root language (i.e. dn is pali).

The author is trickier: a po file doesn't include the author or should
I say Pootle doesn't automatically add that information to the po
metadata.

info.json
```
{
    "pi": {"author": "ms",
            "blurb": "Pali texts from Mahasangiti edition"},
    "en": {"author": "sujato",
            "blurb": "The latest and bested english translations by Bhante Sujato"}
}
```

In the future we could consider add a .po file specifically for filling
in such metadata.

## Using these files

The files are in the form we use them to pull into SuttaCentral. For the sutta translations, the original language and translation segments are accompanied by HTML, and a straight HTML version can be readily reconstructed. Please feel free to use the translation files as you wish. 

The translations also contain many notes. These are mere marginal scribbles intended to help translators, and are not meant for publication.
