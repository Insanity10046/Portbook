import MetaTrader5 as M_T5
import pandas as M_PD
import time

def CONNECT_ACCOUNT(user, password, server_id):
    server_id = input('Enter server id:') if not server_id else server_id;
    M_T5.initialize();
    connected = M_T5.login(int(user), password, server_id);
    return connected, server_id;

def ADJUST_DATAFRAME_POSITIONS(dataframe):
    dataframe = dataframe.drop(columns=[
        'time_msc',
        'comment',
        'external_id',
        'time_update',
        'time_update_msc',
        'magic',
        'identifier',
        'reason',
        'swap',
        ]
    )
    return dataframe;

def HANDLE_TRADE_ACTION_REQUEST(order_type):
    if order_type == M_T5.ORDER_TYPE_BUY or order_type == M_T5.ORDER_TYPE_SELL:
        return M_T5.TRADE_ACTION_DEAL;
    if order_type == M_T5.ORDER_TYPE_BUY_LIMIT or order_type == M_T5.ORDER_TYPE_SELL_LIMIT:
        print('test');
        return M_T5.TRADE_ACTION_PENDING;

def GET_PRICE(order_type, symbol):
    if order_type == M_T5.ORDER_TYPE_BUY or order_type == M_T5.ORDER_TYPE_BUY_LIMIT:
        return M_T5.symbol_info_tick(symbol).ask;
    if order_type == M_T5.ORDER_TYPE_SELL or order_type == M_T5.ORDER_TYPE_SELL_LIMIT:
        return M_T5.symbol_info_tick(symbol).bid;

def GET_INVERSE_ORDER_TYPE(order_type):
    if order_type == M_T5.ORDER_TYPE_BUY:
        return M_T5.ORDER_TYPE_SELL;
    if order_type == M_T5.ORDER_TYPE_SELL:
        return M_T5.ORDER_TYPE_BUY;

def HANDLE_ORDER_PRICE(order_price, order_type, symbol):
    if order_price == 'current':
        return GET_PRICE(order_type, symbol);
    return float(order_price);

def HANDLE_ORDER_TYPE(order_type):
    if order_type == 'buy':
        return M_T5.ORDER_TYPE_BUY;
    if order_type == 'sell':
        return M_T5.ORDER_TYPE_SELL;
    if order_type == 'buy_limit':
        return M_T5.ORDER_TYPE_BUY_LIMIT;
    if order_type == 'sell_limit':
        return M_T5.ORDER_TYPE_SELL_LIMIT;
    return None;

def HANDLE_TIME_AND_FILLINGS(order_type):
    type_time = M_T5.ORDER_TIME_GTC;
    if order_type == M_T5.ORDER_TYPE_BUY or order_type == M_T5.ORDER_TYPE_SELL:
        type_filling =  M_T5.ORDER_FILLING_IOC;
    if order_type == M_T5.ORDER_TYPE_BUY_LIMIT or order_type == M_T5.ORDER_TYPE_SELL_LIMIT:
        type_filling = M_T5.ORDER_FILLING_RETURN;
    return type_time, type_filling;

def HANDLE_OPEN_REQUEST(request):
    request['magic'] = int(request.pop('identifier'));
    request['type'] = HANDLE_ORDER_TYPE(request['type']);
    request['action'] = HANDLE_TRADE_ACTION_REQUEST(request['type']);
    request['type_time'], request['type_filling'] = HANDLE_TIME_AND_FILLINGS(request['type']);
    request['price'] = HANDLE_ORDER_PRICE(request['price'], request['type'], request['symbol']);
    request['volume'] = float(request['volume']);
    request['deviation'] = int(request['deviation']);
    return request;

def GET_POSITION(user, position_specific):
    if M_T5.initialize():
        positions = M_T5.positions_get();
        if positions is None:
            print("No positions found, or error code =", M_T5.last_error())
        elif len(positions) > 0:
            df = M_PD.DataFrame(list(positions), columns=positions[0]._asdict().keys());
            df['time'] = M_PD.to_datetime(df['time'], unit='s')
            return ADJUST_DATAFRAME_POSITIONS(df);
    M_T5.shutdown();

def GET_POSITION_BY_TICKET(identifier):
    identifier = int(identifier);
    position = M_T5.positions_get(ticket=identifier);
    if position and len(position) > 0:
        position = position[0];
    if position:
        current_price = GET_PRICE(position.type, position.symbol);
        request = {
                "action": M_T5.TRADE_ACTION_DEAL,
                "position": position.ticket,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": GET_INVERSE_ORDER_TYPE(position.type),
                "price": current_price,
                "deviation": 20,
                "magic": 100320,
                "comment": "closed position from portbook",
                'type_time': M_T5.ORDER_TIME_GTC,
                'type_filling': M_T5.ORDER_FILLING_IOC
        }
        return request;
    position = M_T5.orders_get(ticket=identifier);
    if position and len(position) > 0:
        position = position[0];
    if position:
        request = {
                "action": M_T5.TRADE_ACTION_REMOVE,
                "order": position.ticket,
                "comment": "closed position from portbook"
        }
        return request;

def SEND_ORDERS(request):
    result = M_T5.order_send(request);
    if not result:
        print(f'No results, last error encountered: {M_T5.last_error()}');
        print(f'the payload used: {request}');
        return None;
    if result.retcode != M_T5.TRADE_RETCODE_DONE:
        print("order send failed, retcode={}".format(result.retcode));
        print(request);
    else:
        print("order sent successfully, position_ticket =", result.order);
    #M_T5.shutdown();

def OPEN_POSITION(parameters, request):
    if M_T5.initialize():
        request = HANDLE_OPEN_REQUEST(request);
        SEND_ORDERS(request);

def CLOSE_ALL_TRADES(symbol):
    positions = M_T5.positions_get(symbol=symbol);
    if positions:
        for position in positions:
            request = GET_POSITION_BY_TICKET(position.ticket);
            SEND_ORDERS(request);
    positions = M_T5.orders_get(symbol=symbol);
    if positions:
        for position in positions:
            request = GET_POSITION_BY_TICKET(position.ticket);
            SEND_ORDERS(request);

def CLOSE_POSITION(parameters):
    if M_T5.initialize():
        ticket = parameters.get('--position_id') or parameters.get('-p_id');
        if ticket:
            request = GET_POSITION_BY_TICKET(ticket);
            SEND_ORDERS(request);
        else:
            symbol = parameters['--symbol'] or parameters['-symb'];
            CLOSE_ALL_TRADES(symbol);
            

