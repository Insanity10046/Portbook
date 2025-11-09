import sys; sys.path.append('..');
from module.command_modules import PARSE_FLAGS;
from module.command_modules import VALIDATE_ON_COMMAND;
from module import data as M_DATA;
import json as M_JSON;


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
            connected, server_id, data = M_DATA.GET_ACCOUNT_FROM_ACCOUNT_ID(account);
            if connected:
                positions = M_DATA.GET_POSITION(data['user'],data['broker'],data['platform'],None);
                print(positions)
