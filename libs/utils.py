
# -*- coding: utf-8 -*-


def celsius_to_kelvin(cgrad):
    if cgrad != "None":
        kgrad = int(cgrad) + 273.15
    else:
        kgrad = 0
    return kgrad


def kelvin_to_celsius(kgrad):
    if kgrad != "None":
        cgrad = int(kgrad) - 273.15
    else:
        cgrad = 0
    return cgrad


def round_by(x, base=5):
    return int(base * round(float(x)/base))

def is_true(value):
    if str(value) in ['True',
                      'true',
                      'TRUE',
                      'Yes',
                      'yes',
                      'YES',
                      '1']:
        return True
    elif str(value) in ['False',
                        'FALSE',
                        'false',
                        'No',
                        'no',
                        'NO',
                        '0']:
        return False
    else:
        return None