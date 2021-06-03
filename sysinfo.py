import platform
import psutil

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
        
def get_sys(num_clients=None):
    uname = platform.uname()
    res = f"\nSystem: {uname.system}"
    res += f"\nNode Name: {uname.node}"
    res += f"\nRelease: {uname.release}"
    res += f"\nVersion: {uname.version}"
    res += f"\nMachine: {uname.machine}"
    res += f"\nProcessor: {uname.processor}"
    # if num_clients is not None:
    #     res += f"\nConnected clients: {num_clients}"

    res += "\n" + ("="*40) + "CPU Information" + "="*40 + ""

    res += f"\nPhysical cores: {psutil.cpu_count(logical=False)}"
    res += f"\nTotal cores: {psutil.cpu_count(logical=True)}"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    res += f"\nMax Frequency: {cpufreq.max:.2f}Mhz"
    res += f"\nMin Frequency: {cpufreq.min:.2f}Mhz"
    res += f"\nCurrent Frequency: {cpufreq.current:.2f}Mhz"
    # CPU usage
    res += "\nCPU Usage Per Core:\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        if i % 4 == 0:
            res += f"\nCore {i}: {percentage}%"
        else:
            res += f"\tCore {i}: {percentage}%"

    res += f"\nTotal CPU Usage: {psutil.cpu_percent()}%"

    # Memory Information
    res += "\n" + ("="*38) + "Memory Information" + "="*39 + "\n"
    # get the memory details
    svmem = psutil.virtual_memory()
    res += f"\nTotal: {get_size(svmem.total)}"
    res += f"\tAvailable: {get_size(svmem.available)}"
    res += f"\tUsed: {get_size(svmem.used)}"
    res += f"\tPercentage: {svmem.percent}% \n"
    res += "\n" + ("="*46) + "SWAP" + "="*45 + "\n"
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    res += f"\nTotal: {get_size(swap.total)}"
    res += f"\tFree: {get_size(swap.free)}"
    res += f"\tUsed: {get_size(swap.used)}"
    res += f"\tPercentage: {swap.percent}%"

    return res


if __name__ == "__main__":
    get_sys(0)