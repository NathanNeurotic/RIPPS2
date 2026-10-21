"""Fill the v1.1.1 psx-place bump (notes/psxplace111.txt) with the sounds Short's YouTube link.

    python psxplace_bump.py <short url>      writes notes/psxplace111-ready.txt (the BBCode body to paste)
"""
import re
import sys
from pathlib import Path

NOTES = Path(__file__).resolve().parent / 'notes'


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    m = re.search(r'(?:shorts/|youtu\.be/|[?&]v=)([A-Za-z0-9_-]{11})', sys.argv[1])
    if not m:
        sys.exit('not a YouTube link: %s' % sys.argv[1])
    t = (NOTES / 'psxplace111.txt').read_text(encoding='utf-8')
    body = t[t.index('[CENTER][SIZE=5]'):].replace('SHORT_ID', m.group(1))
    (NOTES / 'psxplace111-ready.txt').write_text(body, encoding='utf-8')
    print('notes/psxplace111-ready.txt: paste it as a reply in BBCode mode')


if __name__ == '__main__':
    main()
