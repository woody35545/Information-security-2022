from copy import deepcopy
from ctypes import ArgumentError

WHEELS = {
    "I": {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "state": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "state": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "state": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "turn": 21
    }
}
def get_mapping(wheel, reverse = False):
    wire = wheel['wire']
    res = {}
    if reverse == False:
        for i in range(len(wire)):
            res[chr(ord('A') + i)] = wire[i]
    elif reverse:
        for i in range(len(wire)):
            res[wire[i]] = chr(ord('A') + i)
    return res


def index_of(input_str, elemnt_to_find):
    for i in range(len(input_str)):
        if input_str[i] == elemnt_to_find:
            return i

# Enigma Components
ETW =  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


WHEELS = {
    "I": {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "state": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "state": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "state": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
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
        match_loc = index_of(SETTINGS['WHEELS'][2]['state'], input)
        return SETTINGS["ETW"][match_loc]



    return SETTINGS["ETW"][ord(input) - ord('A')]


# Wheels
def pass_wheels(input, reverse=False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    encrypted = input

    for i in range(0, len(SETTINGS['WHEELS'])):
        if reverse:
            wheel = SETTINGS['WHEELS'][i]
            cur_state = wheel['state']
            if wheel == SETTINGS['WHEELS'][0]:
                prev_state = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            else:
                prev_state = SETTINGS['WHEELS'][i-1]['state']

        elif not reverse:
            wheel = SETTINGS['WHEELS'][2-i]
            cur_state = wheel['state']
            if wheel == SETTINGS['WHEELS'][(len(SETTINGS['WHEELS'])-1)]:
                prev_state = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # SETTING['ETW']['state']
            else:
                prev_state = SETTINGS['WHEELS'][2-i+1]['state']
        temp = encrypted
        wire = wheel['wire']

        if reverse:
            match_char = cur_state[index_of(prev_state, encrypted)]
            mapping = get_mapping(wheel,reverse = True)

            encrypted = mapping[match_char]

        elif not reverse:
            mapping = get_mapping(wheel)
            match_char = cur_state[index_of(prev_state, encrypted)]
            encrypted = mapping[match_char]


    return encrypted


# UKW
def pass_ukw(input):

    return SETTINGS["UKW"][ord(input) - ord('A')]


# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics
    rotate_wheel()
    if SETTINGS['WHEELS'][2]['state'][-1] == chr(ord('A') + SETTINGS['WHEELS'][2]['turn']):
        rotate_wheel(opt='m')
    if SETTINGS['WHEELS'][1]['state'][-1] == chr(ord('A') + SETTINGS['WHEELS'][1]['turn']):
        rotate_wheel(opt='l')
    pass

def rotate_wheel(opt = 'r'):
    global SETTINGS
    if opt == 'r':
        wheel_idx = 2
    elif opt == 'm':
        wheel_idx = 1
    elif opt == 'l':
        wheel_idx = 0
    wheel = SETTINGS['WHEELS'][wheel_idx]
    state = str(wheel['state'])
    SETTINGS['WHEELS'][wheel_idx]['state'] = state[1:len(state)] + str(state[0])
    return None

# Enigma Exec Start
"""
plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")
"""


plaintext = "A"*40
ukw_select = "B"
wheel_select = "III II I"
wheel_pos_select = "A A A"
plugboard_setup = "AA"
apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)



for ch in plaintext:
    rotate_wheels()
    #print("\nRIGHT WHEEL = " + SETTINGS["WHEELS"][2]['state'])
    encoded_ch = ch
    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse=True)
    encoded_ch = pass_etw(encoded_ch, reverse=True)
    encoded_ch = pass_plugboard(encoded_ch)
    print(encoded_ch, end='')


