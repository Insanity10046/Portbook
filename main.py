import sys as M_SYS
import ibapi as M_IBAPI
import ib_insync as M_IBSYNC
# ---------------------------------------- #
#                  OBJECT1                 #
# ---------------------------------------- #

# ---------------------------------------- #
#                  CLASS                   #
# ---------------------------------------- #

# ---------------------------------------- #
#                 FUNCTION                 #
# ---------------------------------------- #
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


def LIST(PARAMETER: list) -> list:
    spec = {
        'name': 'list',
        'allowed_flags': {'-a_id', '--account_id', '-b_n', '--bucket_name'},
        'required_flags': {},
        'mutual_exclusive': [{'-a_id', '-p_id'}],
        'flag_value_constraint': {},
        'max_pos': 1,
        'allowed_positionals': {'account', 'position'}
    };
    flags, positionals = PARSE_FLAGS(PARAMETER);
    VALIDATE_ON_COMMAND(spec, flags, positionals);
    if flags:
        account = flags.get('-a_id') or flags.get('--account_id');
        bucket = flags.get('-b_n') or flags.get('--bucket_name');
        if account and (positionals[0] == 'position'):
            print('fr fr');

def ADD(PARAMETER: list) -> list:
    spec = {
        'name': 'add',
        'allowed_flags': {'--broker', '-b', '-u', '-p'},
        'required_flags': {},
        'mutual_exclusive': [{'-a_id', '-p_id'}],
        'flag_value_constraint': {},
        'max_pos': 1,
        'allowed_positionals': {'account', 'position'}
    };
    flags, positionals = PARSE_FLAGS(PARAMETER);
    VALIDATE_ON_COMMAND(spec, flags, positionals);
    
    if flags:
        CHECK_COMMAND_STRUCTURE(PARAMETER, spec['name']);

# ----------------- #
#     CALIBRATE     #
# ----------------- #
Commands = {
    "list": LIST,
    "add": ADD
};
# ---------------------------------------- #
#          FUNCTION CONTINUATION    a       #
def PARSE_ARGUEMENT(ARGUEMENTS: list) -> type:
    for arg in ARGUEMENTS[1:]:
        if arg in Commands:
            Commands[arg](BREAK_DOWN_PARAMETERS(PARAMETER=ARGUEMENTS, START=arg));

PARSE_ARGUEMENT(M_SYS.argv);
#print(M_SYS.argv);
