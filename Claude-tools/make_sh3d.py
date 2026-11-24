#!/usr/bin/env python3
"""Packs a new Home.xml into a .sh3d, taking all models and textures from an existing .sh3d.
Drops the binary `Home` and `ContentDigests` entries so SH3D reads Home.xml.
Extra files (new models) can be added as <entry name>=<path>.
Usage: make_sh3d.py <existing.sh3d> <new Home.xml> <out.sh3d> [entry=path ...]"""
import zipfile, sys
src, xml, dst = sys.argv[1:4]
zi = zipfile.ZipFile(src); zo = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
zo.writestr('Home.xml', open(xml, 'rb').read())
for i in zi.infolist():
    if i.filename in ('Home', 'Home.xml', 'ContentDigests'): continue
    zo.writestr(i, zi.read(i.filename))
for a in sys.argv[4:]:
    n, p = a.split('=', 1); zo.writestr(n, open(p, 'rb').read())
zo.close()
