import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import psutil
import GPUtil

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

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append(f"GPU {gpus.index(gpu) + 1}: {gpu.name}, Driver: {gpu.driver}")
    return gpu_info

# Function to handle button clicks and show enlarged box
def button_click(label_text):
    result = f"{label_text} Usage Information:\n"
    if label_text == "CPU":
        result += f"{get_cpu_usage()}%"
    elif label_text == "Memory":
        result += f"{get_memory_usage()}%"
    elif label_text == "Disk":
        result += f"{get_disk_usage()}%"
    elif label_text == "Network":
        result += f"{get_network_usage()}"
    elif label_text == "GPU": 
        gpu_info = get_gpu_info()
        result += "\n"
        for info in gpu_info:
            result += f"{info}\n"

    # Clear the canvas
    canvas.delete("all")

    # Create a text box on the canvas
    text_id = canvas.create_text(150, 75, anchor='center', text=result, width=250, justify='center', font=('Comic Sans MS', 15))
    bbox = canvas.bbox(text_id)
    expanded_bbox = (bbox[0] - 5, bbox[1] - 5, bbox[2] + 5, bbox[3] + 5)  # Adjust the expansion values as needed
    canvas.create_rectangle(expanded_bbox, outline='black', width=3)  # Adjust the width as needed

# Create the main window
root = tk.Tk()
root.title("Hardware Monitor")

# Set background color for the window
root.configure(bg='lightgray')  # Change 'lightgray' to your desired color

# Create a dictionary mapping labels to their corresponding images
images = {
    "CPU": "images/cpu.png",
    "Memory": "images/memory.png",
    "Disk": "images/disk.jpg",
    "Network": "images/network.png",
    "GPU": "images/gpu.png"
}

# Load images and resize them with ANTIALIAS resampling
image_buttons = {}
for label_text, image_path in images.items():
    img = Image.open(image_path)
    img = img.resize((50, 50), Image.ANTIALIAS)  # Increase image size
    image = ImageTk.PhotoImage(img)
    button = tk.Button(root, image=image, compound='top', command=lambda text=label_text: button_click(text))
    button.image = image
    image_buttons[label_text] = button

# Create a list of labels for CPU, Memory, Disk, Network, and GPU
labels = [tk.Label(root, text=label_text, anchor='w', font=('Comic Sans MS', 12), bg='lightgray') for label_text in images.keys()]
for label in labels:
    label.grid(padx=(10, 5), pady=5, sticky='w')  # Set padding and alignment


# Create a canvas for displaying enlarged box
canvas = tk.Canvas(root, width=300, height=170, bg='lightgray', highlightthickness=0)
canvas.grid(row=0, column=2, rowspan=len(images), padx=10, pady=5, sticky='w')

# Layout using grid
for i, (button, label) in enumerate(zip(image_buttons.values(), labels)):
    button.grid(row=i, column=0, padx=10, pady=5, sticky='w')  # Set sticky to 'w'
    label.grid(row=i, column=1, padx=10, pady=5, sticky='w')  # Set sticky to 'w'

# Run the main event loop
root.mainloop()
