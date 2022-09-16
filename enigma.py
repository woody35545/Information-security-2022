from copy import deepcopy
from ctypes import ArgumentError

DEBUG_MODE = False
def debug_msg(msg):
    if DEBUG_MODE:
        print("[DEBUG] " + msg)

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
def pass_etw(input):
    debug_msg(input)
    debug_msg(f"[pass_etw] >> ord(input) - ord('A') = {ord(input) - ord('A')}")
    debug_msg("[pass_etw] >> SETTINGS[\"ETW\"][ord(input) - ord('A')] = " + str(SETTINGS["ETW"][ord(input) - ord('A')]))

    return SETTINGS["ETW"][ord(input) - ord('A')]


# Wheels
def pass_wheels(input, reverse=False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    encrypted = input
    debug_msg("encrypted = " + str(input))
    if reverse:
        for wh in SETTINGS['WHEELS']:
            #print(wh['wire'])
            encrypted = wh['wire'][ord(wh['wire'][ord(encrypted) - ord('A')]) - ord('A')]
            debug_msg("[pass_wheels] >> encrypted = wh['wire'][ord(wh['wire'][ord(encrypted) - ord('A')]) - ord('A')]: " + str(encrypted))
    elif not reverse:
        for i in range(0, len(SETTINGS['WHEELS'])):

            encrypted = SETTINGS['WHEELS'][2-i]['wire'][ord(encrypted) - ord('A')]
            debug_msg("[pass_wheels] >> encrypted = wh['wire'][ord(encrypted) - ord('A')] = " + str(encrypted))

    return encrypted


# UKW
def pass_ukw(input):
    debug_msg(f"[pass_ukw] >> ord(input) - ord('A') = {ord(input) - ord('A')}")
    debug_msg("[pass_ukw] >> SETTINGS[\"UKW\"][ord(input) - ord('A')] = " + str(SETTINGS["UKW"][ord(input) - ord('A')]))

    return SETTINGS["UKW"][ord(input) - ord('A')]


# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics
    rotate_right_wheel()
    if SETTINGS['WHEELS'][1]['wire'][0] == SETTINGS['WHEELS'][1]['turn']:
        rotate_middle_wheel()
    if SETTINGS['WHEELS'][0]['wire'][0] == SETTINGS['WHEELS'][0]['turn']:
        rotate_left_wheel()
    pass

def rotate_left_wheel():
    global SETTINGS
    debug_msg("LEFT WHEEL's wire= " + str(SETTINGS['WHEELS'][0]['wire']))
    wire = str(SETTINGS['WHEELS'][0]['wire'])
    rotated_wire = wire[1:len(wire)] + str(wire[0])
    SETTINGS['WHEELS'][0]['wire'] = rotated_wire
    #print(str(SETTINGS['WHEELS'][0]['wire']))
    return None

def rotate_middle_wheel():
    middle_wheel = SETTINGS['WHEELS'][1]
    wire = str(middle_wheel['wire'])
    debug_msg("MIDDLE WHEEL's wire= " + str(wire))
    rotated_wire = wire[1:len(wire)] + str(wire[0])
    SETTINGS['WHEELS'][1]['wire'] = rotated_wire
    #print(str(SETTINGS['WHEELS'][1]['wire']))
    return None

def rotate_right_wheel():
    debug_msg("RIGHT WHEEL's wire= " + str(SETTINGS['WHEELS'][2]['wire']))
    wire = str(SETTINGS['WHEELS'][2]['wire'])
    rotated_wire = wire[1:len(wire)] + str(wire[0])
    SETTINGS['WHEELS'][2]['wire'] = rotated_wire
    #print(str(SETTINGS['WHEELS'][2]['wire']))
    return None


# Enigma Exec Start
"""
plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")
"""


plaintext = "AAA"
ukw_select = "B"
wheel_select = "III II I"
wheel_pos_select = "A A A"
plugboard_setup = "AA"
apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)
print(SETTINGS['WHEELS'])

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse=True)
    encoded_ch = pass_plugboard(encoded_ch)
    print("결과: " , end = " ")
    print(encoded_ch, end='')

    print("")
