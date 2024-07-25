import socket
from threading import Thread
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog, Text, END
from flask import Flask, send_from_directory

# Flask app setup
app = Flask(__name__)

@app.route('/system_build_folder/<path:filename>', methods=['GET'])
def download_file(filename):
    directory = ftp_server_gui.directory.get()  # Path to the build folder
    return send_from_directory(directory, filename)

# Function to get the local IP address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.254.254.254', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

class FlaskAppWrapper(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.running = False

    def run(self):
        self.running = True
        app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')

    def stop(self):
        if self.running:
            # This is a placeholder for actual shutdown logic
            # In reality, you would need a way to stop the Flask app properly
            self.running = False

class FTPServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("HTTP/HTTPS Py Flask Server")

        self.flask_app = FlaskAppWrapper()

        self.label = Label(master, text="Flask Server Configuration")
        self.label.pack()

        self.ip_label = Label(master, text="Server IP")
        self.ip_label.pack()
        self.ip_address = StringVar(value=get_ip_address())
        self.ip_entry = Entry(master, textvariable=self.ip_address, state='readonly')
        self.ip_entry.pack()

        self.directory_label = Label(master, text="Directory")
        self.directory_label.pack()
        self.directory = StringVar()
        self.directory_entry = Entry(master, textvariable=self.directory, state='readonly')
        self.directory_entry.pack()

        self.browse_button = Button(master, text="Browse", command=self.browse_directory)
        self.browse_button.pack()

        self.start_button = Button(master, text="Start Server", command=self.start_server)
        self.start_button.pack()

        self.stop_button = Button(master, text="Stop Server", command=self.stop_server, state="disabled")
        self.stop_button.pack()

        self.status_text = Text(master, height=4, wrap='word')
        self.status_text.pack()

        # Footer
        self.footer_label = Label(master, text="dev by meen", font=("Arial", 8))
        self.footer_label.pack(side='bottom', pady=10)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory.set(directory)

    def start_server(self):
        if not self.directory.get():
            self.status_text.config(state='normal')
            self.status_text.delete(1.0, END)
            self.status_text.insert(END, "Please select a directory before starting the server.")
            self.status_text.config(state='disabled')
            return

        if not self.flask_app.is_alive():
            self.flask_app = FlaskAppWrapper()
            self.flask_app.start()
            local_ip = self.ip_address.get()
            status_message = f"Server running on:\n* https://127.0.0.1:5000\n* https://{local_ip}:5000"
            self.status_text.config(state='normal')
            self.status_text.delete(1.0, END)
            self.status_text.insert(END, status_message)
            self.status_text.config(state='disabled')
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")

    def stop_server(self):
        self.flask_app.stop()
        self.status_text.config(state='normal')
        self.status_text.delete(1.0, END)
        self.status_text.insert(END, "Server stopped.")
        self.status_text.config(state='disabled')
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

if __name__ == "__main__":
    root = Tk()
    ftp_server_gui = FTPServerGUI(root)
    root.mainloop()
