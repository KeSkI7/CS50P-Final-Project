import psutil # pip install psutil 
import argparse
import time
def main():

    parser = argparse.ArgumentParser(description="PC Helth Check")
    parser.add_argument("-c", "--cpu", default=80, help="Checks usage of CPU, If it is above 80(by default) or users input, then program alerts user", type=float)
    parser.add_argument("-r", "--ram", default=80, help="Checks usage of RAM, If it is above 80(by default) or users input, then program alerts user", type=float)
    args = parser.parse_args()

    if args.cpu >= 100:
        raise ValueError("Limit can't be above or equal 100%")
    elif args.cpu < 0:
        raise ValueError("Limit can't be below 0%")
    else:
        temp_check_cpu = check_cpu(args.cpu)
        temp_check_ram = check_ram(args.ram)
        print(f"{log_check_cpu(temp_check_cpu)}, where safe limit is {args.cpu}")
        print(f"{log_check_ram(temp_check_ram)}, where safe limit is {args.ram}")


def check_cpu(threscold):
    usage = psutil.cpu_percent(interval=1)
    return usage > threscold, usage

def log_check_cpu(values):
    if values[0]:
        return f"[WARN] CPU usage is {values[1]}"
    return f"[OK] CPU usage is {values[1]} at {time.strftime('%H:%M:%S %d %b %Y')}"

def check_ram(threscold):
    usage = psutil.virtual_memory().percent
    return usage > threscold, usage

def log_check_ram(values):
    if values[0]:
        return f"[WARN] RAM usage is {values[1]}"
    return f"[OK] RAM usage is {values[1]} at {time.strftime('%H:%M:%S %d %b %Y')}"


if __name__ == "__main__":
    main()
