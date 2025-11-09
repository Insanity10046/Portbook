def FLAG_PARAMETER(FLAG: str) -> None:
    if ':' in FLAG or '=' in FLAG:
        name, val = FLAG.split(':') or FLAG.split('=');
        #name = name.lstrip('-');
        ##print(name);
        return name, val;
    else:
        return FLAG, None;

def IS_FLAG(ARG: str) -> None:
    if ARG.startswith('-'):
        return True;
    return False;

def PARSE_FLAGS(ARG: list) -> None:
    flag_list = {};
    positional_list = [];
    for flag in ARG:
        if IS_FLAG(ARG=flag):
            name, value = FLAG_PARAMETER(FLAG=flag);
            flag_list[name] = value if value else True;
        else:
            positional_list.append(flag);
    return flag_list, positional_list;

def CHECK_COMMAND_STRUCTURE(ARGUEMENTS: str, COMMAND:str):
    for arg in ARGUEMENTS:
        if IS_FLAG(arg):
            raise TypeError(f"For command '{COMMAND}': positionals must come before flags");
            return False;
        else:
            break;
    return True;

def VALIDATE_ON_COMMAND(SPEC: list, FLAG_LIST: list, POSITIONAL_LIST: list) -> bool:
    for flag in FLAG_LIST.keys():
        if not flag in SPEC['allowed_flags']:
            raise TypeError(
                "Flag " + flag + " is not allowed for command " + SPEC['name']
            );
    m_count = 0;
    used_flags = [];
    for groups in SPEC['mutual_exclusive']:
        for flag in groups:
            if flag in FLAG_LIST:
                m_count+=1;
                used_flags.append(flag);
        if m_count > 1:
            raise TypeError('Not allowed flags together')
    p_count = 0;
    for pos in POSITIONAL_LIST:
        ##print(pos)
        p_count+=1;
        if not pos in SPEC['allowed_positionals']:
            raise TypeError('unkown positional');
    if p_count > SPEC['max_pos']:
        raise TypeError('Too much positionals')
    return True;

def BREAK_DOWN_PARAMETERS(PARAMETER: list, START: str) -> list:
    return PARAMETER[PARAMETER.index(START)+1:]
