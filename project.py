import psutil # pip install psutil 
import argparse
import time
import sys
LOGS_FILE = None
def main():

    parser = argparse.ArgumentParser(description="PC Health Check Tool")
    parser.add_argument("-c", "--cpu", default=80, help="CPU usage alert threshold in % (Default: 80)", type=float)
    parser.add_argument("-r", "--ram", default=80, help="RAM usage alert threshold in % (Default: 80)", type=float)
    parser.add_argument("-d", "--disks", default=50, help="Checks every disk speed alert threshold in MB/s (Default: 50)", type=float)
    parser.add_argument("-t", "--times", default=4, help="Number of checks to perform (Default: 4). One check is 15 seconds.", type=int)
    parser.add_argument("-s", "--save", nargs="?", const="info.txt", help="Save logs to file (Default: info.txt)", type=str)
    args = parser.parse_args()

    global LOGS_FILE
    LOGS_FILE = args.save

    validate_percentage(args.cpu,"CPU")
    validate_percentage(args.ram, "RAM")

    if args.times > 0:
            write_and_save(f"--- Monitoring started: {args.times} cycles ---")

            for i in range(args.times):
                    start_time = time.time()
                    start_for_disk = psutil.disk_io_counters(perdisk=True)
                    temp_check_cpu = check_cpu(args.cpu)
                    temp_check_ram = check_ram(args.ram)
                    write_and_save(f"{log_check_component(temp_check_cpu, 'CPU')}, limit: {args.cpu:.2f}%")
                    write_and_save(f"{log_check_component(temp_check_ram, 'RAM')}, limit: {args.ram:.2f}%")
                    end_for_disk = psutil.disk_io_counters(perdisk=True)
                    end_time = time.time()
                    time_delta = end_time - start_time
                    temp_check_disks = check_disks_speed(start_for_disk, end_for_disk, time_delta)
                    log_check_disks_speed(temp_check_disks, args.disks)
                    if i+1 == args.times:
                        write_and_save("--- Monitoring finished ---")
                        break
                    write_and_save(f"-" * 40)
                    time.sleep(14)
    else:
        raise ValueError("Program must be executed at least 1 time!")

def write_and_save(text):
    print(text)
    if LOGS_FILE is not None:
        try:
            with open(LOGS_FILE, "a", newline="", encoding="utf-8") as file:
                file.write(text + "\n")
        except Exception as e:
            print(f"[Error] Could not save file {e}")

def validate_percentage(value, name):
    if value > 100 or value < 0:
        sys.exit(f"[Error] {name} limit must be between 0 and 100. Provided {value}")
    return True

def check_cpu(threshold):
    usage = psutil.cpu_percent(interval=1)
    return usage > threshold, usage

def log_check_component(values, name):
    if values[0]:
        return f"[WARN] {name} usage is {values[1]:.2f}% at {time.strftime('%H:%M:%S %d %b %Y')}"
    return f"[OK] {name} usage is {values[1]:.2f}% at {time.strftime('%H:%M:%S %d %b %Y')}"

def check_ram(threshold):
    usage = psutil.virtual_memory().percent
    return usage > threshold, usage

def check_disks_speed(start, end, duration):
    disks_info = []
    common_disks = set(start.keys()) & set(end.keys())
    common_disks = sorted(common_disks)

    for key in common_disks:
        read_bytes = (end[key].read_bytes - start[key].read_bytes) / duration
        write_bytes = (end[key].write_bytes - start[key].write_bytes) / duration
        
        read_mb = read_bytes / 1048576
        write_mb = write_bytes / 1048576
        current_disk = {}
        current_disk["name"] = key
        current_disk["read"] = read_mb
        current_disk["write"] = write_mb
        current_disk["total"] = read_mb + write_mb
        disks_info.append(current_disk)
    return disks_info

def log_check_disks_speed(disks, threshold):
    for disk in disks:
        if disk["total"] >= threshold:
            write_and_save(f"[WARN] Disk {disk['name']:<15} | Total usage is {disk['total']:6.2f} MB/s | {time.strftime('%H:%M:%S %d %b %Y')} | Read: {disk['read']:.2f} MB/s | Write: {disk['write']:.2f} MB/s")
        else:
            write_and_save(f"[OK] Disk {disk['name']:<15} | Total usage is {disk['total']:6.2f} MB/s | {time.strftime('%H:%M:%S %d %b %Y')} | Read: {disk['read']:.2f} MB/s | Write: {disk['write']:.2f} MB/s")
    return ""



if __name__ == "__main__":
    main()
