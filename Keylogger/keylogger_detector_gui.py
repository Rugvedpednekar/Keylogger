import psutil
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Suspicious keylogger indicators
suspicious_files = ["logs.txt", "keylogger.py"]
suspicious_processes = ["pynput", "hook", "logger"]

class KeyloggerDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Detector")
        self.root.geometry("500x400")

        self.label = tk.Label(root, text="Keylogger Detection System", font=("Arial", 14, "bold"))
        self.label.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.text_area.insert(tk.END, "Click 'Scan' to detect keyloggers...\n")
        self.text_area.config(state=tk.DISABLED)

        self.scan_button = tk.Button(root, text="Scan", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.scan_for_keyloggers)
        self.scan_button.pack(pady=5)

        self.remove_button = tk.Button(root, text="Remove Keyloggers", font=("Arial", 12, "bold"), bg="red", fg="white", command=self.remove_keyloggers)
        self.remove_button.pack(pady=5)

    def log_message(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state=tk.DISABLED)
        self.text_area.yview(tk.END)  # Auto-scroll

    def scan_for_keyloggers(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)  
        self.text_area.config(state=tk.DISABLED)

        detected_files = self.detect_keylogger_files()
        found_processes = self.detect_suspicious_processes()

        if detected_files or found_processes:
            self.log_message("⚠️ Keylogger Detected!\n")
            if detected_files:
                self.log_message(f"🔍 Suspicious Files Found: {', '.join(detected_files)}")
            if found_processes:
                self.log_message("🔍 Suspicious Processes Found:")
                for name, pid in found_processes:
                    self.log_message(f" - {name} (PID: {pid})")
        else:
            self.log_message("✅ No keyloggers detected.")

    def detect_keylogger_files(self):
        return [file for file in suspicious_files if os.path.exists(file)]

    def detect_suspicious_processes(self):
        found_processes = []
        for process in psutil.process_iter(['pid', 'name']):
            if any(suspicious in process.info['name'].lower() for suspicious in suspicious_processes):
                found_processes.append((process.info['name'], process.info['pid']))
        return found_processes

    def remove_keyloggers(self):
        detected_files = self.detect_keylogger_files()
        found_processes = self.detect_suspicious_processes()

        if detected_files or found_processes:
            self.log_message("\n🚨 Removing Detected Keyloggers...")

            # Delete suspicious files
            for file in detected_files:
                try:
                    os.remove(file)
                    self.log_message(f"✅ Deleted: {file}")
                except Exception as e:
                    self.log_message(f"❌ Failed to delete {file}: {e}")

            # Terminate suspicious processes
            for name, pid in found_processes:
                try:
                    psutil.Process(pid).terminate()
                    self.log_message(f"✅ Terminated process: {name} (PID: {pid})")
                except Exception as e:
                    self.log_message(f"❌ Failed to terminate {name}: {e}")

            messagebox.showinfo("Keylogger Removed", "All detected threats have been removed!")
        else:
            messagebox.showinfo("No Threats", "No keyloggers detected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerDetectorGUI(root)
    root.mainloop()
