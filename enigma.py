from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I": {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}


def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))

    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)


# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input


# ETW
def pass_etw(input, reverse=False):
    if reverse:
        diff = ord(input) - ord('A') - SETTINGS['WHEEL_POS'][2]
        idx = ord(SETTINGS["ETW"][0]) - ord('A')+ diff
        if idx < 0:
            idx = idx + 26
        return SETTINGS["ETW"][idx]

    return SETTINGS["ETW"][ord(input) - ord('A')]


# Wheels
def pass_wheels(input, reverse=False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    passed_result = input
    if not reverse:
        for i in range(0, len(SETTINGS['WHEELS'])):
            wheel = SETTINGS['WHEELS'][(len(SETTINGS['WHEELS']) - 1)- i]
            wheel_pos = SETTINGS['WHEEL_POS'][len(SETTINGS['WHEELS']) - 1 - i]
            wire = wheel['wire']

            if len(SETTINGS['WHEELS']) - 1 - i == 2:
                match_location = (wheel_pos + (ord(passed_result) - ord('A'))) % 26

            else:
                previous_wheel_pos = SETTINGS['WHEEL_POS'][(len(SETTINGS['WHEELS']) - 1) - i + 1]
                match_location = (((ord(passed_result) - ord('A')) - previous_wheel_pos) + wheel_pos )
                if match_location < 0:
                    match_location = match_location + 26
                match_location = match_location % 26

            passed_result = wire[match_location]


    elif reverse:
        for i in range(0, len(SETTINGS['WHEELS'])):
            wheel = SETTINGS['WHEELS'][i]
            wheel_pos = SETTINGS['WHEEL_POS'][i]
            wire = wheel['wire'] # Reverse Mapping 해야함

            if i == 0:
                match_location = (wheel_pos + (ord(passed_result) - ord('A'))) % 26

            else:
                previous_wheel_pos = SETTINGS['WHEEL_POS'][i-1]
                match_location = ((ord(passed_result) - ord('A')) - previous_wheel_pos) + wheel_pos
                if match_location < 0:
                    match_location = match_location + 26
                match_location = match_location % 26

            # Reverse Mapping
            for i in range(len(wire)):
                if wire[i] == chr(match_location + ord("A")):
                    passed_result = chr(i + ord("A"))

    return passed_result


# UKW
def pass_ukw(input):
    match_location = ord(input)-ord('A') - SETTINGS['WHEEL_POS'][0]
    if match_location < 0:
        match_location = match_location + 26

    return SETTINGS["UKW"][match_location]


def rotate_wheel(opt='r'):
    if opt == 'r':
        idx = 2
    elif opt == 'm':
        idx = 1
    elif opt == 'l':
        idx = 0

    SETTINGS['WHEEL_POS'][idx] = (SETTINGS['WHEEL_POS'][idx] + 1) % 26


# Wheel Rotation
def rotate_wheels():
    global SETTINGS

    if SETTINGS['WHEEL_POS'][2] == SETTINGS['WHEELS'][2]['turn']:
        if SETTINGS['WHEEL_POS'][1] == SETTINGS['WHEELS'][1]['turn']:
            rotate_wheel(opt='l')
        rotate_wheel(opt='m')

    elif SETTINGS['WHEEL_POS'][1] == SETTINGS['WHEELS'][1]['turn']:
        rotate_wheel(opt='m')
        rotate_wheel(opt='l')

    rotate_wheel(opt='r')
    pass

"""
# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")개
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")
"""

# Enigma Exec Start
plaintext = "A"*1000
ukw_select = "B"
wheel_select = "III II I"
wheel_pos_select = "A A A"
plugboard_setup = "AA"

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

count = 0
for ch in plaintext:

    rotate_wheels()

    encoded_ch = ch
    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse=True)
    encoded_ch = pass_etw(encoded_ch, reverse=True)

    encoded_ch = pass_plugboard(encoded_ch)
    count = count + 1

    if count % 5 == 0:
        print(encoded_ch, end = " ")
    else:
        print(encoded_ch, end = "")
    if count % 35 == 0:
        print("")
