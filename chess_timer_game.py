# timer.py

import threading
import time

class ChessTimer:
    def __init__(self, time_per_turn=60):
        self.time_per_turn = time_per_turn
        self.remaining_time = time_per_turn
        self.timer_thread = None
        self.running = False
        self.on_timeout = None

    def start(self, callback=None):
        self.remaining_time = self.time_per_turn
        self.on_timeout = callback
        self.running = True
        self.timer_thread = threading.Thread(target=self._countdown, daemon=True)
        self.timer_thread.start()

    def _countdown(self):
        while self.remaining_time > 0 and self.running:
            print(f"Time left: {self.remaining_time} sec")  # Replace with GUI label update
            time.sleep(1)
            self.remaining_time -= 1
        if self.remaining_time <= 0 and self.running and self.on_timeout:
            self.on_timeout()

    def stop(self):
        self.running = False
        if self.timer_thread:
            self.timer_thread.join(timeout=1)
