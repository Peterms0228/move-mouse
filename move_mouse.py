import pyautogui
import time
import threading
from datetime import datetime, timedelta

# Disable pyautogui's failsafe (move mouse to corner to stop)
# Remove this line if you want the failsafe enabled
# pyautogui.FAILSAFE = True

class MouseMover:
    def __init__(self):
        self.running = False
        self.moves_completed = 0
        self.next_move_time = None
        
    def move_mouse_quick(self):
        """Move mouse up 5px, then down 5px within 1 second"""
        # Get current mouse position
        x, y = pyautogui.position()
        
        print(f"\nMoving mouse...")
        
        # Move up 5 pixels in 0.05 seconds
        pyautogui.moveTo(x, y - 1, duration=0.05)
        
        # Move down 5 pixels in 0.05 seconds
        pyautogui.moveTo(x, y + 1, duration=0.05)
        
        # Press Shift key to prevent sleep (doesn't type anything)
        pyautogui.press('shift')
        
        self.moves_completed += 1
        print(f"Move complete! Total moves: {self.moves_completed}")
    
    def countdown_timer(self):
        """Display countdown until next move"""
        while self.running:
            if self.next_move_time:
                remaining = (self.next_move_time - datetime.now()).total_seconds()
                if remaining <= 0:
                    self.move_mouse_quick()
                    self.next_move_time = datetime.now() + timedelta(seconds=170)
                else:
                    mins = int(remaining // 60)
                    secs = int(remaining % 60)
                    print(f"\rNext move in: {mins:02d}:{secs:02d}", end="", flush=True)
            time.sleep(1)
    
    def start(self):
        """Start the mouse mover"""
        print("="*50)
        print("MOUSE MOVER STARTED")
        print("="*50)
        print("Press Ctrl+C to stop")
        print("Move mouse to top-left corner for emergency stop (if failsafe enabled)")
        print()
        
        self.running = True
        self.next_move_time = datetime.now() + timedelta(seconds=60)
        
        # Start countdown in separate thread
        timer_thread = threading.Thread(target=self.countdown_timer, daemon=True)
        timer_thread.start()
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the mouse mover"""
        self.running = False
        print("\n\n" + "="*50)
        print(f"STOPPED - Total moves completed: {self.moves_completed}")
        print("="*50)

if __name__ == "__main__":
    mover = MouseMover()
    mover.start()