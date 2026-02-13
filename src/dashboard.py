import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os
import sys

# Constants
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
PYTHON_EXEC = sys.executable

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Dossier Database - Contributor Dashboard")
        self.root.geometry("600x500")

        # Style
        style = ttk.Style()
        style.theme_use('clam')

        # --- Header ---
        header_frame = ttk.Frame(root, padding="10")
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Contributor Dashboard", font=("Helvetica", 16, "bold")).pack()
        ttk.Label(header_frame, text="Make sure you have set up your .env file first!", foreground="red").pack()

        # --- Batch Selection ---
        batch_frame = ttk.LabelFrame(root, text=" 1. Select Batch ", padding="10")
        batch_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(batch_frame, text="Batch ID (e.g. 001):").pack(side=tk.LEFT)
        self.batch_entry = ttk.Entry(batch_frame, width=10)
        self.batch_entry.pack(side=tk.LEFT, padx=5)
        self.batch_entry.insert(0, "001")

        # --- Actions ---
        action_frame = ttk.LabelFrame(root, text=" 2. Actions ", padding="10")
        action_frame.pack(fill=tk.X, padx=10, pady=5)

        self.btn_claim = ttk.Button(action_frame, text="✋ Claim Batch", command=self.claim_batch)
        self.btn_claim.pack(fill=tk.X, pady=2)
        
        self.btn_mine = ttk.Button(action_frame, text="⛏️ Start Mining", command=self.start_mining)
        self.btn_mine.pack(fill=tk.X, pady=2)

        self.btn_submit = ttk.Button(action_frame, text="🚀 Submit Work", command=self.submit_work)
        self.btn_submit.pack(fill=tk.X, pady=2)

        # --- Console ---
        console_frame = ttk.LabelFrame(root, text=" Logs ", padding="10")
        console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.console = scrolledtext.ScrolledText(console_frame, height=10, state='disabled', bg="black", fg="white", font=("Consolas", 9))
        self.console.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        self.console.config(state='normal')
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state='disabled')

    def run_command(self, command, cwd=PROJECT_ROOT):
        """Runs a command in a separate thread to keep UI responsive"""
        def target():
            self.log(f"> {command}")
            try:
                process = subprocess.Popen(
                    command, 
                    shell=True, 
                    cwd=cwd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Stream output
                for line in process.stdout:
                    self.root.after(0, self.log, line.strip())
                for line in process.stderr:
                    self.root.after(0, self.log, f"[ERR] {line.strip()}")
                
                process.wait()
                if process.returncode == 0:
                    self.root.after(0, self.log, "[DONE] Success")
                    self.root.after(0, lambda: messagebox.showinfo("Success", "Command completed successfully."))
                else:
                    self.root.after(0, self.log, f"[FAIL] Exited with code {process.returncode}")
                    self.root.after(0, lambda: messagebox.showerror("Error", "Command failed. Check logs."))

            except Exception as e:
                self.root.after(0, self.log, f"[EXCEPTION] {e}")

        threading.Thread(target=target, daemon=True).start()

    def claim_batch(self):
        batch = self.batch_entry.get().strip()
        if not batch: return
        
        # Chain of commands: Pull -> Run Script -> Add -> Commit -> Push
        script_path = os.path.join(SRC_DIR, "claim_batch.py")
        cmd = f'git pull origin main && "{PYTHON_EXEC}" "{script_path}" --batch {batch} && git add claims/ && git commit -m "Claim batch {batch}" && git push origin main'
        
        self.run_command(cmd)

    def start_mining(self):
        batch = self.batch_entry.get().strip()
        if not batch: return
        
        script_path = os.path.join(SRC_DIR, "dossier_miner.py")
        # Ensure dependencies are installed? We assume setup.bat ran.
        cmd = f'"{PYTHON_EXEC}" "{script_path}" --batch {batch}'
        self.run_command(cmd)

    def submit_work(self):
        batch = self.batch_entry.get().strip()
        if not batch: return
        
        cmd = f'git add data/processed/ && git commit -m "Processed batch {batch}" && git push origin main'
        self.run_command(cmd)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
