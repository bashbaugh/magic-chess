import dbus
import time

from ble_gatt_server.advertisement import Advertisement
from ble_gatt_server.service import Application, Service, Characteristic, Descriptor

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

CHESSBOARD_SVC_UUID = "00000001-502e-4e1d-b821-ae2488aa4202"

PING_CHRC_UUID = "00000002-502e-4e1d-b821-ae2488aa4202" # read
BOARDSTATE_CHRC_UUID = "00000003-502e-4e1d-b821-ae2488aa4202" # read, notify
STARTGAME_CHRC_UUID = "00000004-502e-4e1d-b821-ae2488aa4202" # write
UPDATESETTINGS_CHRC_UUID = "00000005-502e-4e1d-b821-ae2488aa4202" # read, write

class ChessboardAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("magic-chessboard")
        self.include_tx_power = True

class ChessboardService(Service):
    def __init__(self, index):
        Service.__init__(self, index, CHESSBOARD_SVC_UUID, True)
        self.add_characteristic(PingCharacteristic(self))
        # self.add_characteristic(BoardStateCharacteristic(self))

class PingCharacteristic(Characteristic):
    def __init__(self, service):
        Characteristic.__init__(self, PING_CHRC_UUID,["read", "write"], service)
        self.add_descriptor(Descriptor("2901", "Ping", ["read"], self))

    def ReadValue(self, options):
        return self.encode_value("hello" + str(time.time()))

    def WriteValue(self, value, options):
        print(str(value))

class BleApplication(Application):
    def __init__(self):
        Application.__init__(self)
        self.add_service(ChessboardService(0))
        self.register()

        # Register advertisements
        board_ad = ChessboardAdvertisement(0)
        board_ad.register()
