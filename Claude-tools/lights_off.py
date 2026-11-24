#!/usr/bin/env python3
"""Day variant: switch off the v13 lights (name starts with 'Light:'), except the spots in the windowless hall, corridor and laundry. Usage: lights_off.py in.xml out.xml"""
import sys, xml.etree.ElementTree as ET
t=ET.parse(sys.argv[1]); n=0
for l in t.getroot().iter('light'):
    if (l.get('name') or '').startswith('Light:') and 'spot' not in l.get('name'): l.set('power','0'); n+=1
t.write(sys.argv[2],encoding='UTF-8',xml_declaration=True); print('lights off:',n)
