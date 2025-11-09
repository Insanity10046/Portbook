import sys; sys.path.append('..');
from module.command_modules import PARSE_FLAGS;
from module.command_modules import VALIDATE_ON_COMMAND;
from module.command_modules import CHECK_COMMAND_STRUCTURE
from module import data as M_DATA
import json as M_JSON
import os
def WRITE_ACCOUNT(data,account_name):
    print(os.listdir())
    with open(f"portfolio/accounts/{account_name}.json", "w") as json_file:
        M_JSON.dump(data, json_file);

def ADD_ACCOUNT(flags):
    platform = flags['-plat'].upper() or flags['--platform'].upper();
    broker = flags['-b'].upper() or flags['--broker'].upper();
    # sanitise input:
    M_DATA.VALIDATE_BROKER_AND_PLATFORM(broker,platform);
    # just a simple test, we'll eventually rework this part here to include functions and parts from other platforms as they have their own API
    # whether we use class or what not, is up to interpretation; right now we need a layout
    # we'll eventually split this aswell, apply system architecture
    get_user = flags['-u'] or flags['--user'];
    get_password = flags['-p'] or flags['--password'];
    if platform == "METATRADER5":
        connected, server_id = M_DATA.CONNECT_ACCOUNT(get_user, get_password,broker,platform,None);
        if connected:
            WRITE_ACCOUNT(
                {
                    "user": get_user,
                    "password": get_password,
                    "broker": broker,
                    "platform": platform,
                    "server_id": server_id
                },
                get_user
            )

def ADD(PARAMETER: list) -> list:
    spec = {
        'name': 'add',
        'allowed_flags': {'--broker', '-b', '-u', '-p', '--platform', '-plat'},
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
        if positionals[0] == 'account':
            ADD_ACCOUNT(flags);
        elif positionals[0] == 'position':
            ADD_POSITION(flags);
