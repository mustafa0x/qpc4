# /// script
# dependencies = [
#   "html_sanitizer",
#   "beautifulsoup4",
#   "regex"
# ]
# ///
import sys
from pathlib import Path
import regex as re

def apply_repls(text, repls):
    for r in repls:
        text = re.sub(r[1], r[2], text) if r[0] else text.replace(r[1], r[2])
    return text

repls = [
    (1, r'', ''),

    # in `<span style="font-family:KFGQPC_Uthman_Taha_Naskh_H;color:#8E3B17">[1-128]<br/></span>`
    (0, r'<br/>', ''),

    (1, r'(?m)(?<=<span[^>]+>)\s*([^<]+?)\s*(?=</span>)', r'\1'),
    # ;color:black
    (0, r';color:black', ''),
    (0, r'family: ', 'family:'),
    # remove `/* Style Definitions */` to the end of the </style> tag
    (1, r'/\* Style Definitions \*/[^<]+', ''),
    # remove all colors
    (1, r';? ?color:[^;">]+', ''),
    (1, r'(?m)^ +', ''),
    (1, r'\n\n+', '\n'),
    (0, '</style>', r'p {direction:rtl;unicode-bidi:bidi-override}</style>'),
    (1, '<span style="font-family:KFGQPC_Uthman_Taha_Naskh_H.*?>', '<br><br>'),
    # remove span tag with KFGQPC_Uthman_Taha_Naskh_H font
    (1, r'<span style="font-family:KFGQPC_Uthman_Taha_Naskh_H;color:[^"]+">[^<]*</span>', ''),

    # font-family:QCF4_Hafs_26_W
    # src: url(https://fonts.nuqayah.com/qcf4/QCF4_Hafs_25_W.woff2);
    # Search for Font Family and add after it the source URL replacing the file number 
    (1, r'(font-family:QCF4_Hafs_(\d+)_W;)', r'\1 src: url(https://fonts.nuqayah.com/qcf4/QCF4_Hafs_\2_W.woff2);'),
    # 0xf100
]

file_path = sys.argv[1]
path = Path(file_path)

output_path = path.with_stem(f"{path.stem}-clean")
output_path.write_text(apply_repls(path.read_text(), repls))
