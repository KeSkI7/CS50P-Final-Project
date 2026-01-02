# PC Health Check Tool
#### Description:
This script monitors PC health by periodic checks on system resources.

- It checks **CPU** and **RAM** usage against a defined percentage threshold.
- It calculates **Disk Read/Write speeds** (MB/s) over a time interval.
- Alerts (`[WARN]`) or status updates (`[OK]`) are saved to a log file.

Logs are saved by default to `info.txt` in the same directory.

---

#### Requirements

- Python 3.6+
- External library: `psutil`

To install the dependency:
```bash
pip install psutil
```

#### Usage
1. Clone this repository or download the script.
2. (Optional) Run help to see available arguments.
```bash
python project.py --help
```
3. Run the script with default settings(CPU/RAM limit: 80%, Disk limit: 50MB/s, 4 cycles)
```bash
python project.py
```
4. Run with custom thresholds
```bash
python project.py -c 95 -r 70 -t 15 -s my_logs.txt
```

#### Example

Command:
```bash
python project.py -t 3
```
Console output:
```
--- Monitoring started: 3 cycles ---
[OK] CPU usage is 2.30% at 21:49:30 02 Jan 2026, limit: 80.00%
[OK] RAM usage is 54.60% at 21:49:30 02 Jan 2026, limit: 80.00%
[OK] Disk PhysicalDrive0  | Total usage is   0.00 MB/s | 21:49:30 02 Jan 2026 | Read: 0.00 MB/s | Write: 0.00 MB/s
[OK] Disk PhysicalDrive1  | Total usage is   0.00 MB/s | 21:49:30 02 Jan 2026 | Read: 0.00 MB/s | Write: 0.00 MB/s
[OK] Disk PhysicalDrive2  | Total usage is   0.00 MB/s | 21:49:30 02 Jan 2026 | Read: 0.00 MB/s | Write: 0.00 MB/s
----------------------------------------
[OK] CPU usage is 37.20% at 21:49:45 02 Jan 2026, limit: 80.00%
[OK] RAM usage is 57.70% at 21:49:45 02 Jan 2026, limit: 80.00%
[OK] Disk PhysicalDrive0  | Total usage is   1.31 MB/s | 21:49:45 02 Jan 2026 | Read: 0.68 MB/s | Write: 0.63 MB/s
[OK] Disk PhysicalDrive1  | Total usage is   0.00 MB/s | 21:49:45 02 Jan 2026 | Read: 0.00 MB/s | Write: 0.00 MB/s
[OK] Disk PhysicalDrive2  | Total usage is   0.00 MB/s | 21:49:45 02 Jan 2026 | Read: 0.00 MB/s | Write: 0.00 MB/s
----------------------------------------
[WARN] CPU usage is 100.00% at 21:50:00 02 Jan 2026, limit: 80.00%
[OK] RAM usage is 59.60% at 21:50:00 02 Jan 2026, limit: 80.00%
[WARN] Disk PhysicalDrive0  | Total usage is 107.89 MB/s | 21:50:00 02 Jan 2026 | Read: 18.58 MB/s | Write: 89.31 MB/s
[OK] Disk PhysicalDrive1  | Total usage is   0.00 MB/s | 21:50:00 02 Jan 2026 | Read: 0.00 MB/s | Write: 0.00 MB/s
[OK] Disk PhysicalDrive2  | Total usage is   0.00 MB/s | 21:50:00 02 Jan 2026 | Read: 0.00 MB/s | Write: 0.00 MB/s
--- Monitoring finished ---
```

#### Project Structure
```text
txt-to-bitwarden/
├─ info.txt             # Deafult log file (created after running -s)
├─ project.py           # Main Python script
├─ test_project.py      # Tests for the script
├─ requirements.txt     # pip-library to download
└─ README.md            # This file
```

## Notes

- Admin privileges might be required to see stats for some system disks.  
- Press `Ctrl + C` to stop the monitoring loop gracefully.

#### License 
MIT License