import os
import pynvml

def update_status():
    pynvml.nvmlInit()
    device_count = pynvml.nvmlDeviceGetCount()
    gpu_statue = []

    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        gpu_information = {
            "gpu_name" : pynvml.nvmlDeviceGetName(handle), # name
            "gpu_utilization_rates" : pynvml.nvmlDeviceGetUtilizationRates(handle).gpu, # %
            "memory_utilization_rates" : pynvml.nvmlDeviceGetUtilizationRates(handle).memory, # %
            "total_memory" : pynvml.nvmlDeviceGetMemoryInfo(handle).total / (1024 * 1024 * 1024),  # in GB
            "used_memory" : pynvml.nvmlDeviceGetMemoryInfo(handle).used / (1024 * 1024  * 1024),  # in GB
            "free_memory" : pynvml.nvmlDeviceGetMemoryInfo(handle).free / (1024 * 1024  * 1024),  # in GB
            "temperature" : pynvml.nvmlDeviceGetTemperature(handle, 0), # °C
            "fan_speed" : pynvml.nvmlDeviceGetFanSpeed(handle), # %
            "power_usage" : pynvml.nvmlDeviceGetPowerUsage(handle) / 1000, # W
            "power_limit" : pynvml.nvmlDeviceGetEnforcedPowerLimit(handle) / 1000, # W
        }
        gpu_statue.append((i, gpu_information))
    
    pynvml.nvmlShutdown()
    response = "**Server: Joule** \n"
    for index, gpu in enumerate(gpu_statue):
        response += gpu_status_to_string(gpu[1], index)

    cmd = "ssh cuda6 bash < ./workstation/nv.sh  > ./log/cuda6_gpu.log"
    os.system(cmd)
    with open("./log/cuda6_gpu.log", "r") as f:
        result = f.read()
        response += result
    return response

def gpu_status_to_string(gpu_statue, index):
    gpu_templete = f"""```ansi
GPU {index}: [2;33m{gpu_statue['gpu_name']}[0m
    Utilization:
        GPU [2;34m{gpu_statue['gpu_utilization_rates']:.2f}[0m %, Memory bandwidth [2;34m{gpu_statue['memory_utilization_rates']:.2f}[0m %
    Memory:
        Total [2;32m{gpu_statue['total_memory']:.2f}[0m GB, Used [2;32m{gpu_statue['used_memory']:.2f}[0m GB, 
        Free [2;32m{gpu_statue['free_memory']:.2f}[0m GB
    Temperature:
            [2;31m{gpu_statue['temperature']:.2f}[0m °C
    Fan speed:
            [0;2m[0;36m{gpu_statue['fan_speed']:.2f}[0m %[0m
    Power:
        Usage: [2;35m{gpu_statue['power_usage']:.2f}[0m W, Limit: [2;35m{gpu_statue['power_limit']:.2f}[0m W
```

"""
    return gpu_templete


if __name__ == "__main__":
    print(update_status())
