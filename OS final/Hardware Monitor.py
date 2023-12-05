import tkinter as tk
from PIL import Image, ImageTk
import psutil
import os
import platform
import datetime

# Function to retrieve hardware information
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent

def get_network_usage():
    network = psutil.net_io_counters()
    return f"Sent: {network.bytes_sent} bytes Received: {network.bytes_recv} bytes"

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return f"Battery: {battery.percent}% - {'Charging' if battery.power_plugged else 'Discharging'}"
    return "Battery information not available"

def get_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            for entry in temps["coretemp"]:
                if "Package" in entry.label:
                    return entry.current
    except Exception as e:
        print(f"Error retrieving CPU temperature: {e}")
    return None

def get_os_info():
    return f"OS: {platform.platform()}"

def get_boot_time():
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(boot_time_timestamp)
    return f"Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}"

def get_running_processes():
    return f"Running Processes: {len(psutil.pids())}"

# Function to handle button clicks and show enlarged box
def button_click(label_text):
    result = f"{label_text} Usage Information:\n"
    if label_text == "CPU":
        result += f"{get_cpu_usage()}%\n"
        temperature = get_cpu_temperature()
        if temperature:
            result += f"CPU Temperature: {temperature}°C\n"
        else:
            result += "CPU Temperature: N/A\n"
    elif label_text == "Memory":
        result += f"{get_memory_usage()}%\n"
    elif label_text == "Disk":
        result += f"{get_disk_usage()}%\n"
    elif label_text == "Network":
        result += f"{get_network_usage()}\n"
    elif label_text == "Battery":
        result += f"{get_battery_info()}\n"
    elif label_text == "OS":
        result += f"{get_os_info()}\n"
    elif label_text == "Boot":
        result += f"{get_boot_time()}\n"
    elif label_text == "Processes":
        result += f"{get_running_processes()}\n"

    # Clear the canvas
    canvas.delete("all")

    # Create a text box on the canvas
    text_id = canvas.create_text(150, 75, anchor='center', text=result, width=250, justify='center', font=('Comic Sans MS', 15))
    bbox = canvas.bbox(text_id)
    expanded_bbox = (bbox[0] - 5, bbox[1] - 5, bbox[2] + 5, bbox[3] + 5)
    canvas.create_rectangle(expanded_bbox, outline='black', width=3)

def sleep_system():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")  # Command to put system to sleep

def restart_system():
    os.system("shutdown /r /t 0")  # Command to restart system

def shutdown_system():
    os.system("shutdown /s /t 0")  # Command to shutdown system

# Create the main window
root = tk.Tk()
root.title("Hardware Monitor")

# Set background color for the window
root.configure(bg='lightgray')

# Create a dictionary mapping labels to their corresponding images
images = {
    "CPU": "images/cpu.png",
    "Memory": "images/memory.png",
    "Disk": "images/disk.jpg",
    "Network": "images/network.png",
    "Battery": "images/battery.png",
    "OS": "images/os.png",
    "Boot": "images/boot.png",
    "Processes": "images/processes.png"
}

# Load images and resize them with ANTIALIAS resampling
image_buttons = {}
for label_text, image_path in images.items():
    img = Image.open(image_path)
    img = img.resize((50, 50), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(img)
    button = tk.Button(root, image=image, compound='top', command=lambda text=label_text: button_click(text))
    button.image = image
    image_buttons[label_text] = button

# Create a list of labels for CPU, Memory, Disk, Network, Battery, OS, Boot Time, and Processes
labels = [tk.Label(root, text=label_text, anchor='w', font=('Comic Sans MS', 12), bg='lightgray') for label_text in images.keys()]
for label in labels:
    label.grid(padx=(10, 5), pady=5, sticky='w')

# Create a canvas for displaying enlarged box
canvas = tk.Canvas(root, width=300, height=270, bg='lightgray', highlightthickness=0)
canvas.grid(row=0, column=2, rowspan=len(images), padx=10, pady=5, sticky='w')

# Layout using grid
for i, (button, label) in enumerate(zip(image_buttons.values(), labels)):
    button.grid(row=i, column=0, padx=10, pady=5, sticky='w')
    label.grid(row=i, column=1, padx=10, pady=5, sticky='w')

# Create buttons for sleep, restart, and shutdown
sleep_button = tk.Button(root, text="Sleep", command=sleep_system)
restart_button = tk.Button(root, text="Restart", command=restart_system)
shutdown_button = tk.Button(root, text="Shutdown", command=shutdown_system)

# Place sleep, restart, and shutdown buttons in the window
sleep_button.grid(row=len(images), column=0, padx=10, pady=5, sticky='w')
restart_button.grid(row=len(images), column=1, padx=10, pady=5, sticky='w')
shutdown_button.grid(row=len(images), column=2, padx=10, pady=5, sticky='w')

# Run the main event loop
root.mainloop()
