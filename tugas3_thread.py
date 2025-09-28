#Husni Ayi Nurdin
#237006002 A

import time
import threading
from concurrent.futures import ProcessPoolExecutor

# === Simulasi I/O-bound (sleep) ===
import random
def download_file(i, sec):
    time.sleep(sec)

def run_io_serial(jobs):
    start = time.time()
    for i, sec in jobs:
        download_file(i, sec)
    return time.time() - start

def run_io_threads(jobs):
    threads = []
    start = time.time()
    for i, sec in jobs:
        t = threading.Thread(target=download_file, args=(i, sec))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.time() - start

def run_io_processes(jobs):
    def wrapper(sec):
        time.sleep(sec)
    start = time.time()
    with ProcessPoolExecutor() as executor:
        executor.map(wrapper, [sec for _, sec in jobs])
    return time.time() - start

# === Simulasi CPU-bound ===
def heavy(n):
    total = 0
    for i in range(10**6):
        total += i * i
    return total

def run_cpu_serial():
    start = time.time()
    for _ in range(10):
        heavy(10**6)
    return time.time() - start

def run_cpu_threads():
    threads = []
    start = time.time()
    for _ in range(10):
        t = threading.Thread(target=heavy, args=(10**6,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.time() - start

def run_cpu_processes():
    start = time.time()
    with ProcessPoolExecutor() as executor:
        executor.map(heavy, [10**6] * 10)
    return time.time() - start

# === Main Program ===
def main():
    random.seed(42)
    jobs = [(i, random.uniform(0.5, 2.0)) for i in range(10)]

    print("=== I/O-BOUND ===")
    io_serial = run_io_serial(jobs)
    io_threads = run_io_threads(jobs)
    io_processes = run_io_processes(jobs)

    print("=== CPU-BOUND ===")
    cpu_serial = run_cpu_serial()
    cpu_threads = run_cpu_threads()
    cpu_processes = run_cpu_processes()

    # Hitung speedup
    io_speedup_threads = io_serial / io_threads
    io_speedup_processes = io_serial / io_processes

    cpu_speedup_threads = cpu_serial / cpu_threads
    cpu_speedup_processes = cpu_serial / cpu_processes

    print("\n=== TABEL HASIL ===")
    print(f"{'Jenis Aplikasi':<15} {'Serial (s)':<12} {'Threads (s)':<12} {'Processes (s)':<14} {'Speedup Threads':<17} {'Speedup Processes'}")
    print(f"{'I/O-Bound':<15} {io_serial:<12.2f} {io_threads:<12.2f} {io_processes:<14.2f} {io_speedup_threads:<17.2f} {io_speedup_processes:.2f}")
    print(f"{'CPU-Bound':<15} {cpu_serial:<12.2f} {cpu_threads:<12.2f} {cpu_processes:<14.2f} {cpu_speedup_threads:<17.2f} {cpu_speedup_processes:.2f}")

if __name__ == "__main__":
    main()
