This is placeholder data because right now the Pootle FS git plugin
is rather buggy. The Pootle FS basic functionality seems to work okay
so maybe we could use Pootle FS to write to the file system then
do a manual git commit & push.

## Folder Structure

Pootle FS allows using arbitary paths (to an extent) with variable
substitution, with the path template being defined per project.


We need 4 critical pieces of information for knowing what a po file
is to the used for:

1. The author
2. The root (original) langauge
3. The translation language
4. The uid


So we could use a path template like this:

`<author>/<translation_language>/<root_langauge>/<path>/<uid>.<ext>`

Author and root language don't form part of Pootle FS path templates
so an actual project might have a Pootle FS template like this:

`sujato/<language>/pi/<path>/<filename>.<ext>`

With an actual file being like this:  
`sujato/en/pi/dn/dn1.po`

