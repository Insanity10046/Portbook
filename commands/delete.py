import sys; sys.path.append('..');
import os;
import shutil;
from module.command_modules import PARSE_FLAGS;
from module.command_modules import VALIDATE_ON_COMMAND;
from module.command_modules import CHECK_COMMAND_STRUCTURE;
from module import data as M_DATA;

def DELETE_BUCKET(flags):
    name = flags['-n'] or flags['--name'];
    bucket = f'portfolio/buckets/{name}'
    if not os.path.exists(bucket):
        print(f'bucket {name} does not exist');
        return None;
    try:
        os.rmdir(bucket)
        print(f"bucket {name} removed successfully")
    except OSError as error:
        print(error)
        print("bucket can not be removed")

def DELETE(PARAMETER: list) -> list:
    spec = {
            'name': 'delete',
            'allowed_flags': {'--name', '-n'},
            'required_flags': {},
            'mutual_exclusive': [{}],
            'flag_value_constraint': {},
            'max_pos': 1,
            'allowed_positionals': {'bucket', 'ledger'}
    };
    flags, positionals = PARSE_FLAGS(PARAMETER);
    VALIDATE_ON_COMMAND(spec,flags,positionals);
    if flags:
        CHECK_COMMAND_STRUCTURE(PARAMETER, spec['name']);
        if positionals[0] == 'bucket':
            DELETE_BUCKET(flags);

def CLOSE(PARAMETER: list) -> list:
    spec = {
            'name': 'open',
            'allowed_flags': {
                '--position_id', '-p_id', 
                '--account_id', '-a_id', 
                '--symbol', '-symb'
                },
            'required_flags': {},
            'mutual_exclusive': [],
            'max_pos': 1,
            'allowed_positionals': {'position'}
    }
    flags, positionals = PARSE_FLAGS(PARAMETER);
    VALIDATE_ON_COMMAND(spec,flags,positionals);
    if flags:
        if positionals[0] == 'position':
            M_DATA.CLOSE_POSITION(flags);
