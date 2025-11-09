import sys; sys.path.append('..');
import os;
from module.command_modules import PARSE_FLAGS;
from module.command_modules import VALIDATE_ON_COMMAND;
from module.command_modules import CHECK_COMMAND_STRUCTURE;
from module import data as M_DATA

def CREATE_BUCKET(flags):
    name = flags['-n'] or flags['--name'];
    bucket = f'portfolio/buckets/{name}'
    try:
        os.makedirs(bucket)
        print(f"bucket '{name}' created successfully.")
    except FileExistsError:
        print(f"One or more bucket '{name}' already exist.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def CREATE(PARAMETER: list) -> list:
    spec = {
            'name': 'create',
            'allowed_flags': {'--name', '-n'},
            'required_flags': {},
            'mutual_exclusive': [{'-a_id', '-p_id'}],
            'flag_value_constraint': {},
            'max_pos': 1,
            'allowed_positionals': {'bucket', 'ledger'}
    };
    flags, positionals = PARSE_FLAGS(PARAMETER);
    VALIDATE_ON_COMMAND(spec,flags,positionals);
    if flags:
        CHECK_COMMAND_STRUCTURE(PARAMETER, spec['name'])
        if positionals[0] == 'bucket':
            CREATE_BUCKET(flags);    

def OPEN(PARAMETER: list) -> list:
    spec = {
            'name': 'open',
            'allowed_flags': {
                '--account_id', '-a_id', 
                '--symbol', '-symb', 
                '--lot', '-l', 
                '--type', '-t', 
                '--price', '-p', 
                '--deviations', '-d', 
                '--identifier', '-i'
                },
            'required_flags': {},
            'mutual_exclusive': [],
            'max_pos': 1,
            'allowed_positionals': {'position'}
    };
    flags, positionals = PARSE_FLAGS(PARAMETER);
    VALIDATE_ON_COMMAND(spec,flags,positionals);
    if flags:
        if positionals[0] == 'position':
            M_DATA.OPEN_POSITION(flags);

            
