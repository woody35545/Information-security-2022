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
        # ETW를 역방향으로 통과할 때 정상적으로 작동하도록 하기 위해 코드 추가
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
        # 정방향으로 Wheel을 PASS 할 경우
        for i in range(0, len(SETTINGS['WHEELS'])):
            # 가장 오른쪽 Wheel부터 왼쪽 Wheel 방향 순서로 통과하도록 Wheel 설정
            wheel = SETTINGS['WHEELS'][(len(SETTINGS['WHEELS']) - 1)- i]
            
            # 현재 통과하는 Wheel의 position
            wheel_pos = SETTINGS['WHEEL_POS'][len(SETTINGS['WHEELS']) - 1 - i]
            
            # 현재 통과하는 Wheel의 wire
            wire = wheel['wire']

            if len(SETTINGS['WHEELS']) - 1 - i == 2:
                # 현재 통과중인 Wheel이 가장 오른쪽 Wheel 일 경우, ETW에서 통과한 값에 대응되는 index를 계산
                match_location = (wheel_pos + (ord(passed_result) - ord('A'))) % 26

            else:
                # 현재 통과중인 Wheel이 가장 오른쪽 Wheel이 아닐 경우, 이전 Wheel의 Position 정보를 이용해 대응되는 index를 계산
                previous_wheel_pos = SETTINGS['WHEEL_POS'][(len(SETTINGS['WHEELS']) - 1) - i + 1]
                
                # 바로 직전에 통과한 이전 Wheel에 대응되는 현재 Wheel에서의 위치 계산
                match_location = (((ord(passed_result) - ord('A')) - previous_wheel_pos) + wheel_pos )
                
                if match_location < 0:
                    # 연산 결과가 음수인 경우 26을 더해 음수가 나오지 않도록 함.
                    match_location = match_location + 26

                # 인덱스 값이 알파벳 전체 개수인 26을 넘지 않도록 match_location에 % 26을 연산해줌
                match_location = match_location % 26

            # 찾은 위치에 대응되는 Wire 값을 pass_result 변수에 할당
            passed_result = wire[match_location]


    elif reverse:
        # 역방향으로 Wheel을 Pass 할 경우
        for i in range(0, len(SETTINGS['WHEELS'])):
            # 가장 왼쪽 WHEEL부터 오른쪽 WHEEL 방향 순서로 통과하도록 wheel 설정
            wheel = SETTINGS['WHEELS'][i]
            # 현재 통과하는 WHEEL position
            wheel_pos = SETTINGS['WHEEL_POS'][i]
            # 현재 통과하는 WHEEL의 wire
            wire = wheel['wire']

            if i == 0:
                # 현재 통과중인 Wheel이 가장 왼쪽 Wheel 일 경우, UKW에서 통과한 값에 대응되는 index를 계산
                match_location = (wheel_pos + (ord(passed_result) - ord('A'))) % 26

            else:
                # 현재 통과중인 Wheel이 가장 오른쪽 Wheel이 아닐 경우, 이전 Wheel의 Position 정보를 이용해 대응되는 index를 계산
                previous_wheel_pos = SETTINGS['WHEEL_POS'][i-1]                
                
                # 바로 직전에 통과한 이전 Wheel에 대응되는 현재 Wheel에서의 위치 계산
                match_location = ((ord(passed_result) - ord('A')) - previous_wheel_pos) + wheel_pos

                if match_location < 0:
                # 구한 index가 음수일 경우, 26을 더해주어서 계산
                    match_location = match_location + 26
                # 인덱스 값이 알파벳 전체 개수인 26을 넘지 않도록 match_location에 % 26을 연산해줌
                match_location = match_location % 26

            # Wheel 통과방향이 역방향이므로 기존에 wire에 정의된 Mapping을 반대로 하여 passed_result에 할당
            for i in range(len(wire)):
                if wire[i] == chr(match_location + ord("A")):
                    passed_result = chr(i + ord("A"))

    return passed_result


# UKW
def pass_ukw(input):
    # 가장 왼쪽 WHEEL을 통과한 값에 대응하는 위치를 찾아서 match_location에 할당
    match_location = ord(input)-ord('A') - SETTINGS['WHEEL_POS'][0]
    if match_location < 0:
        # 음수가 나오지 않도록 알파벳 전체 개수인 26을 더해줌
        match_location = match_location + 26

    return SETTINGS["UKW"][match_location]


def rotate_wheel(opt='r'):
    # 단일 Wheel 회전함수
    # rotate_wheel()에서는 단일 Wheel의 회전 기능 자체만을 구현하였음. 
    # rotate_wheels() 함수에서 각 Wheel이 돌아가는 조건에 따라 적절하게 호출하여 사용함.
    if opt == 'r':
        # opt 값을 'r' 로 설정할 경우 가장 오른쪽 Wheel 회전
        # SETTING['WHEEL_POS'] 에서 가장 오른쪽 Wheel의 index는 2 이므로 idx=2로 설정
        idx = 2

    elif opt == 'm':
        # opt 값을 'r' 로 설정할 경우 중간 Wheel 회전
        # SETTING['WHEEL_POS'] 에서 가장 오른쪽 Wheel의 index는 1 이므로 idx=1로 설정
        idx = 1
        
    elif opt == 'l':
        # opt 값을 'l'로 설정할 경우 가장 왼쪽 Wheel 회전
        # SETTING['WHEEL_POS'] 에서 가장 왼쪽 Wheel의 index는 0 이므로 indx=0으로 설정
        idx = 0
    
    # SETTINGS['WHEEL_POS'][idx] 값을 하나 증가시켜서 할당하면 WHEEL이 회전한 것과 논리적으로 동일함.
    # 현재 WHEEL_POS 값에 1을 더한 후 % 26 연산을 통해 WHEEL_POS 값이 알파벳 전체의 개수인 26을 넘지않도록 함
    SETTINGS['WHEEL_POS'][idx] = (SETTINGS['WHEEL_POS'][idx] + 1) % 26


# Wheel Rotation
def rotate_wheels():
    global SETTINGS
    
    # 가장 오른쪽 Wheel의 현재 위치가 turn에 걸렸을 경우
    if SETTINGS['WHEEL_POS'][2] == SETTINGS['WHEELS'][2]['turn']:
        
        if SETTINGS['WHEEL_POS'][1] == SETTINGS['WHEELS'][1]['turn']:
        # 가장 오른쪽 Wheel의 현재 위치가 turn에 걸리고 중간 Wheel도 turn에 걸려있는 상태이면, 중간 Wheel과 왼쪽 Wheel 모두 회전시킴
            rotate_wheel(opt='l') # 앞서 구현한 rotate_wheel 함수에 'l' 인자를 주어 좌측 Wheel 회전

        # 가장 오른쪽 Wheel만 현재 위치가 turn에 걸려있는 경우 오른쪽 Wheel과 중간 Wheel만 회전시킴. 
        # 오른쪽 Wheel의 회전은 항상 일어나야 하므로 if문 밖에 선언하여 조건에 관계없이 rotate_wheel()이 호출되면 공통으로 일어나도록 함.
        rotate_wheel(opt='m') # 앞서 구현한 rotate_wheel 함수에 'm' 인자를 주어 중간 Wheel 회전

    elif SETTINGS['WHEEL_POS'][1] == SETTINGS['WHEELS'][1]['turn']:
        # 가장 오른쪽 Wheel의 현재 위치가 turn에 걸리고 중간 Wheel도 turn에 걸려있는 상태이면, 오른쪽 Wheel, 중간 Wheel, 왼쪽 Wheel을 모두 회전시킴
        # 오른쪽 Wheel의 회전은 항상 일어나야 하므로 if문 밖에 선언하여 조건에 관계없이 rotate_wheel()이 호출되면 공통으로 일어나도록 함.
        rotate_wheel(opt='m') # 앞서 구현한 rotate_wheel 함수에 'm' 인자를 주어 중간 Wheel 회전
        rotate_wheel(opt='l') # 앞서 구현한 rotate_wheel 함수에 'l' 인자를 주어 좌측 Wheel 회전

    # 가장 오른쪽 Wheel은 char 하나가 들어올 때마다 조건없이 항상 회전함
    rotate_wheel(opt='r')# 앞서 구현한 rotate_wheel 함수에 'r' 인자를 주어 우측 Wheel 회전

    pass


# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")


# Enigma Exec Start


apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

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
    print(encoded_ch, end = "")
