import subprocess
import tkinter as tk
from tkinter import messagebox

class KeyloggerControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger & Detection Control Panel")
        self.root.geometry("500x400")
        self.root.configure(bg="#1e1e2f")

        self.running_process = None  # Store the subprocess

        # Title
        tk.Label(root, text="🛡️ Keylogger Control Panel", 
                 font=("Helvetica", 18, "bold"), bg="#1e1e2f", fg="#ffffff").pack(pady=20)

        # Buttons
        self.start_keylogger_btn = self.create_button("▶ Run Keylogger", "#d9534f", self.run_keylogger)
        self.start_keylogger_btn.pack(pady=10)

        self.start_detector_btn = self.create_button("🧠 Run Detector", "#5cb85c", self.run_detector)
        self.start_detector_btn.pack(pady=10)

        self.stop_btn = self.create_button("⛔ Stop Running Process", "#f0ad4e", self.stop_program, tk.DISABLED)
        self.stop_btn.pack(pady=15)

        self.exit_btn = self.create_button("🚪 Exit", "#292b2c", root.quit)
        self.exit_btn.pack(pady=10)

    def create_button(self, text, color, command, state=tk.NORMAL):
        return tk.Button(
            self.root,
            text=text,
            font=("Verdana", 12, "bold"),
            bg=color,
            fg="white",
            activebackground="#333",
            activeforeground="white",
            command=command,
            relief=tk.RAISED,
            bd=3,
            width=25,
            state=state
        )

    def run_keylogger(self):
        if self.running_process:
            messagebox.showwarning("Already Running", "Please stop the current process before starting another.")
            return
        self.running_process = subprocess.Popen(["python", "keylogger_gui.py"])
        self.stop_btn.config(state=tk.NORMAL)
        messagebox.showinfo("Success", "Keylogger is now running.")

    def run_detector(self):
        if self.running_process:
            messagebox.showwarning("Already Running", "Please stop the current process before starting another.")
            return
        self.running_process = subprocess.Popen(["python", "keylogger_detector_gui.py"])
        self.stop_btn.config(state=tk.NORMAL)
        messagebox.showinfo("Success", "Keylogger Detector is now running.")

    def stop_program(self):
        if self.running_process:
            self.running_process.terminate()
            self.running_process = None
            self.stop_btn.config(state=tk.DISABLED)
            messagebox.showinfo("Stopped", "The running program has been terminated.")
        else:
            messagebox.showwarning("No Process", "No program is currently running.")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerControlPanel(root)
    root.mainloop()
