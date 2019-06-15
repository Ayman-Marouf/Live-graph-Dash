from ws4py.client import WebSocketBaseClient
from ws4py.manager import WebSocketManager
from ws4py import format_addresses, configure_logger

logger = configure_logger()

m = WebSocketManager()

class EchoClient(WebSocketBaseClient):
    def handshake_ok(self):
        logger.info("Opening %s" % format_addresses(self))
        m.add(self)

    def received_message(self, msg):
        logger.info(str(msg))

if __name__ == '__main__':
    import time

    try:
        m.start()
        for i in range(500):
            client = EchoClient('ws://localhost:9000/ws')
            client.connect()

        logger.info("%d clients are connected" % i)

        while True:
            for ws in m.websockets.itervalues():
                if not ws.terminated:
                   break
            else:
                break
            time.sleep(3)
    except KeyboardInterrupt:
        m.close_all()
        m.stop()
        m.join()