import json
from libs.constants import *

media_settings_json = json.dumps([
    {'type': 'path',
     'title': 'Music path setting',
     'desc': 'Path to music files',
     'section': 'Media',
     'key': 'path'},
    {'type': 'bool',
     'title': 'MP3',
     'desc': 'Play .mp3 files?',
     'section': 'Media',
     'key': 'mp3'},
    {'type': 'bool',
     'title': 'M4A',
     'desc': 'Play .m4a files?',
     'section': 'Media',
     'key': 'm4a'},
    {'type': 'bool',
     'title': 'FLAC',
     'desc': 'Play FLAC files?',
     'section': 'Media',
     'key': 'flac'},
    {'type': 'bool',
     'title': 'Random',
     'desc': 'Play randomly from playlist?',
     'section': 'Media',
     'key': 'shuffle'}
])

obd2_settings_json = json.dumps([
    {'type': 'bool',
     'title': 'Enable',
     'desc': 'Enable OBD2?',
     'section': 'OBD2',
     'key': 'enable'},
    {'type': 'string',
     'title': 'OBD2 password',
     'desc': 'OBD2 password',
     'section': 'OBD2',
     'key': 'password'},
    {'type': 'options',
     'title': 'Baud rate',
     'desc': 'OBD2 port baud rate',
     'section': 'OBD2',
     'key': 'baud',
     'options': BAUDS
    },
    {'type': 'options',
     'title': 'Protocol',
     'desc': 'OBD2 protocol',
     'section': 'OBD2',
     'key': 'protocol',
     'options': list(PROTOCOLS_MAP.keys())
    },
    {'type': 'numeric',
     'title': 'vef',
     'desc': 'Engine volumetric efficiency',
     'section': 'OBD2',
     'key': 'vef'
    },
    {'type': 'numeric',
     'title': 'eds',
     'desc': 'Engine displacement',
     'section': 'OBD2',
     'key': 'eds'
    },
    {'type': 'numeric',
     'title': 'Timeout',
     'desc': 'Wait this time before quering OBD2',
     'section': 'OBD2',
     'key': 'time'
     }

])
