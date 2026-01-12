from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

class PubNubClient:
    def __init__(self, publish_key: str, subscribe_key: str, uuid: str, token: str):
        pnconfig = PNConfiguration()
        pnconfig.publish_key = publish_key
        pnconfig.subscribe_key = subscribe_key
        pnconfig.uuid = uuid

        pnconfig.auth_key = token

        self.pubnub = PubNub(pnconfig)

    def publish(self, channel: str, message: dict):
        self.pubnub.publish().channel(channel).message(message).pn_async(lambda e, s: None)

    def subscribe(self, channel: str, on_message):
        class Listener(SubscribeCallback):
            def message(self, pubnub, event):
                msg = event.message
                if isinstance(msg, dict):
                    on_message(msg)

        self.pubnub.add_listener(Listener())
        self.pubnub.subscribe().channels([channel]).execute()

    def stop(self):
        try:
            self.pubnub.stop()
        except Exception:
            pass

