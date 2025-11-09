import sys; sys.path.append('..');
import importlib as M_IMPORTS
import json as M_JSON;

available_brokers = ["IBKR", "GLOBAL_PRIME"];
available_platforms = {
        "METATRADER5": M_IMPORTS.import_module('module.platform.metatrader5')
}

def GET_PLATFORM_API(platform):
    return available_platforms[platform];

def VALIDATE_BROKER_AND_PLATFORM(broker, platform):
    if not broker in available_brokers:
        raise TypeError('Unavailable broker');
    if not platform in available_platforms:
        raise TypeError('Unavailable platform');

def CONNECT_ACCOUNT(user, password, broker, platform,server_id):
    platform = GET_PLATFORM_API(platform);
    connected,server_id = platform.CONNECT_ACCOUNT(user,password,server_id);
    return connected,server_id;

def GET_ACCOUNT_FROM_ACCOUNT_ID(account_id):
    data = None;
    with open(f'portfolio/accounts/{account_id}.json', 'r') as json_file:
        data = M_JSON.load(json_file);
    connected, server_id = CONNECT_ACCOUNT(data['user'],data['password'],data['broker'],data['platform'],data['server_id'])
    return connected, server_id, data;


def GET_POSITION(user, broker, platform, position_specific):
    platform = GET_PLATFORM_API(platform);
    positions = platform.GET_POSITION(user, position_specific);
    return positions;

def OPEN_POSITION(parameters):
    account_id = parameters['-a_id'] or parameters['--account_id'];
    connected, server_id, data = GET_ACCOUNT_FROM_ACCOUNT_ID(account_id);
    platform = GET_PLATFORM_API(data['platform']);
    request = {
            'symbol': parameters['--symbol'],
            'volume': parameters['--lot'],
            'type': parameters['--type'],
            'price': parameters['--price'],
            'deviation': parameters['--deviations'],
            'identifier': parameters['--identifier'],
            'comment': 'open financial position',
    };
    platform.OPEN_POSITION(parameters, request);

def CLOSE_POSITION(parameters):
    account_id = parameters['-a_id'] or parameters['--account_id'];
    connected, server_id, data = GET_ACCOUNT_FROM_ACCOUNT_ID(account_id);
    platform = GET_PLATFORM_API(data['platform']);
    platform.CLOSE_POSITION(parameters)
