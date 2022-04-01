from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
from datetime import datetime
import json


def check_liquidations():
    print("Launching Binance Websocket Connection & awaiting new Liquidations...")
    
    nonce = 0
    
    binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com-futures")
    binance_websocket_api_manager.create_stream(['!forceOrder'], [{}])
    
    
    while (True):
        lick_stream = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        cycles = 5000000
        nonce += 1
        if nonce > cycles:
            nonce = 0
        if lick_stream:
            data = json.loads(lick_stream)
            try:
                symbol = data['data']['o']['s'][:-4]
                last = data['data']['o']['ap']
                amount = data['data']['o']['q']
                stamp = data['data']['E']
                lick_size = float(last) * float(amount)
                d1 = datetime.fromtimestamp(stamp / 1000)
                now = datetime.now()
                past = now - d1
                duration = past.total_seconds()
                if duration < 2:
                    print("---------------------------------------------------------------------------------")
                    print("Liquidation found for:", amount, "Contracts worth: $", lick_size, "on ", symbol)

            except KeyError:
                pass

check_liquidations()
