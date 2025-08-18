import asyncio
import tkinter as tk
from bleak import BleakScanner, BleakClient
import struct
import threading
from ui import HeartRateGUI


# UUIDs for Heart Rate Service and Characteristic
hrs_uuid = "0000180d-0000-1000-8000-00805f9b34fb"
hrm_uuid = "00002a37-0000-1000-8000-00805f9b34fb"





class MiBandHeartRateMonitor:
    def __init__(self):
        self.client = None
        self.running = False
        self.heart_rate = None
        self.gui_callback = None

    def set_gui_callback(self, callback):
        self.gui_callback = callback

    def notification_handler(self, sender, data):
        """Callback function for heart rate notifications"""
        flag = data[0]

        if flag & 0b00001:
            heart_rate_value = struct.unpack('>H', data[1:3])[0]
        else:
            heart_rate_value = data[1]

        self.heart_rate = heart_rate_value

        if self.gui_callback:
            self.gui_callback(heart_rate_value)

        print(f"HeartRateValue: {heart_rate_value}")

    async def connect(self):
        """Connect to the Mi Band device"""
        print("Scanning for heart rate devices...")

        devices = await BleakScanner.discover(
            service_uuids=[hrs_uuid],
            return_adv=True
        )

        if not devices:
            print("No heart rate devices found")
            return False
        for d in devices:
            info = devices[d][0]
            name = info.name
            print(name)
        for d in devices:
            info = devices[d][0]
            name = info.name
            if name == None:
                continue
            if "Band" in name:
                break
        if name == None:
            return False
        if "Band" not in name:
            return False
        device = info
        print(f"Found device: {device.name} ({device.address})")

        self.client = BleakClient(device)
        try:
            await self.client.connect()
            print(f"Connected to {device.name}")

            services = self.client.services
            heart_rate_service = services.get_service(hrs_uuid)
            if not heart_rate_service:
                print("Heart rate service not found")
                return False

            heart_rate_char = heart_rate_service.characteristics[0]
            if not heart_rate_char:
                print("Heart rate measurement characteristic not found")
                return False

            await self.client.start_notify(heart_rate_char, self.notification_handler)
            print("Subscribed to heart rate notifications")
            return True

        except Exception as e:
            print(f"Connection error: {e}")
            return False

    async def run(self):
        """Main loop for the heart rate monitor"""
        self.running = True
        while self.running:
            if not self.client or not self.client.is_connected:
                success = await self.connect()
                if not success:
                    print("Retrying in 5 seconds...")
                    await asyncio.sleep(1)
                    continue

            await asyncio.sleep(1)

    async def stop(self):
        """Stop the heart rate monitor"""
        self.running = False
        if self.client and self.client.is_connected:
            try:
                await self.client.stop_notify(hrm_uuid)
                await self.client.disconnect()
                print("Disconnected from device")
            except Exception as e:
                print(f"Error while disconnecting: {e}")


def run_monitor(monitor):
    """Run the heart rate monitor in a separate thread"""
    asyncio.run(monitor.run())


def main():
    root = tk.Tk()
    gui = HeartRateGUI(root)
    monitor = MiBandHeartRateMonitor()

    def update_gui(heart_rate=None):
        if heart_rate is not None:
            gui.update_heart_rate(heart_rate)

    monitor.set_gui_callback(update_gui)

    monitor_thread = threading.Thread(target=run_monitor, args=(monitor,), daemon=True)
    monitor_thread.start()

    def on_closing():
        print("Stopping...")
        monitor.running = False
        monitor_thread.join(timeout=2.0)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
