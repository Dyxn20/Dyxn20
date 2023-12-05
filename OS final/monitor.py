import psutil
import GPUtil


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
    return f"Sent: {network.bytes_sent} bytes, Received: {network.bytes_recv} bytes"


def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append(
            f"GPU {gpus.index(gpu) + 1}: {gpu.name}, Driver: {gpu.driver}")
    return gpu_info


def main():
    try:
        while True:
            cpu_usage = get_cpu_usage()
            memory_usage = get_memory_usage()
            disk_usage = get_disk_usage()
            network_usage = get_network_usage()
            gpu_info = get_gpu_info()

            print(f"CPU Usage: {cpu_usage}%")
            print(f"Memory Usage: {memory_usage}%")
            print(f"Disk Usage: {disk_usage}%")
            print(f"Network Usage: {network_usage}")
            print("GPU Information:")
            for info in gpu_info:
                print(info)
            print("\n")

    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()
