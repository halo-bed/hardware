from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from config import (
    PUBNUB_PUBLISH_KEY,
    PUBNUB_SUBSCRIBE_KEY,
    PUBNUB_UUID,
    PUBNUB_CHANNEL,
)


pnconfig = PNConfiguration()
pnconfig.publish_key = PUBNUB_PUBLISH_KEY
pnconfig.subscribe_key = PUBNUB_SUBSCRIBE_KEY
pnconfig.uuid = PUBNUB_UUID

pubnub = PubNub(pnconfig)


def publish_event(message: dict):
    pubnub.publish().channel(PUBNUB_CHANNEL).message(message).pn_async(
        lambda envelope, status: None
    )

