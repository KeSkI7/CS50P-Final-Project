import psutil # pip install psutil 
def main():
    print(psutil.cpu_times())

def check_cpu():
    ...
if __name__ == "__main__":
    main()