import sys; sys.path.append('..');
from module.command_modules import PARSE_FLAGS;
from module.command_modules import VALIDATE_ON_COMMAND;
from module import data as M_DATA;
from module.graph.candlestick_graph import GRAPH_CANDLESTICK;

def GET(PARAMETER: list) -> list:
    spec = {
            'name': 'get',
            'allowed_flags': {'-s', '--stock', '-p', '--period'},
            'required_flags': {'-s'},
            'mutual_exclusive': [],
            'flag_value_constraint': {},
            'max_pos': 1,
            'allowed_positionals': {'price'}
    };
    flags, positionals = PARSE_FLAGS(PARAMETER);
    VALIDATE_ON_COMMAND(spec, flags, positionals);
    if flags:
        stock = flags.get('-s') or flags.get('--stock');
        period = flags.get('-p') or flags.get('--period');
        if not period:
            period = '5d';
        GRAPH_CANDLESTICK(stock, period);
