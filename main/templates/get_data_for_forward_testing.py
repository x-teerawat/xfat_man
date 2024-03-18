# from _libs import *
# from _funcs import *

import asyncio
import socketio

sio = socketio.AsyncClient()


@sio.on('connect', namespace='/stocks')
async def connect():
    print('connected to server')
    await sio.emit('subscribe', {'events': ['SQQQ']}, namespace='/stocks')


@sio.on('disconnect', namespace='/stocks')
async def disconnect():
    print('disconnected from server')


@sio.on('subscribe', namespace='/stocks')
def subscribe(message):
    # print(type(message))
    try:
        # print(message['payload'])
        print(message['payload']['stock'])
        print(message['payload']['open'])
        print(message['payload']['high'])
        print(message['payload']['low'])
        print(message['payload']['close'])
        print()
    except:
        pass

    # print(message['payload'].keys())

@sio.on('exception', namespace='/stocks')
def exception(message):
    print(message)


async def start_server():
    await sio.connect('wss://web-socket.techglobetrading.com/stocks', transports=['websocket'], namespaces=['/stocks'])
    await sio.wait()


if __name__ == '__main__':
    asyncio.run(start_server())

# def get_data_for_forward_testing(stock_name, train_date, test_date):
#     # Get, Prep, and Clean data
#     df = get_data(ticker=stock_name, unit="second", _from=train_date, to=test_date)
#     prepared_data = prepare_data(df)
#     cleaned_data = clean_data(prepared_data)

#     test_data = prepared_data[(prepared_data.index>=pd.to_datetime(test_date))*(prepared_data.index<pd.to_datetime(test_date)+relativedelta(days=1)*(prepared_data.index>=pd.to_datetime(str(test_date) + " " + "09:30:00"))*(prepared_data.index<=pd.to_datetime(str(test_date) + " " + "15:59:59")))]
#     test_data = test_data[["open", "high", "low", "close", "volume"]]
#     train_data = cleaned_data[cleaned_data.index<test_data.index[0]]

#     return train_data, test_data