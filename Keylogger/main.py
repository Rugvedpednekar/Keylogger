import subprocess
import tkinter as tk
from tkinter import messagebox

class SimpleKeyloggerScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Scanner")
        self.root.geometry("400x250")

        tk.Label(root, text="Keylogger Scanner", font=("Arial", 18, "bold")).pack(pady=20)

        self.running_process = None

        self.start_scan_btn = tk.Button(root, text="Run Keylogger Detector", font=("Arial", 14, "bold"), bg="green", fg="white", command=self.run_detector_gui)
        self.start_scan_btn.pack(pady=20)

        self.exit_btn = tk.Button(root, text="Exit", font=("Arial", 12, "bold"), bg="black", fg="white", command=self.exit_program)
        self.exit_btn.pack(pady=10)

    def run_detector_gui(self):
        """Launch the Keylogger Detector normally without asking to stop."""
        if self.running_process:
            messagebox.showwarning("Warning", "Keylogger Detector is already running.")
            return

        try:
            self.running_process = subprocess.Popen(["python", "keylogger_detector_gui.py"])
            messagebox.showinfo("Detector Started", "✅ Keylogger Detector is running.")
        
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to start Detector:\n{e}")

    def stop_detector(self):
        """Stop the detector if running."""
        if self.running_process:
            try:
                self.running_process.terminate()
                self.running_process = None
                messagebox.showinfo("Stopped", "✅ Keylogger Detector has been stopped.")
            except Exception as e:
                messagebox.showerror("Error", f"❌ Failed to stop Detector:\n{e}")

    def exit_program(self):
        """Exit the app safely."""
        if self.running_process:
            self.running_process.terminate()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleKeyloggerScanner(root)
    root.mainloop()
