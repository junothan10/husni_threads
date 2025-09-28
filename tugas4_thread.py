#Husni Ayi Nurdin
#237006002 A


import time
import threading
import multiprocessing
from multiprocessing import Process, Queue, Manager

# Fungsi CPU-bound
def process_file(file_id):
    total = 0
    for i in range(10**5):
        total += i * i
    return file_id

# Stage 1: Loader Thread
def loader(file_list, q, n_workers_cpu):
    for file_id in file_list:
        q.put(file_id)
    # Kirim sinyal selesai sebanyak jumlah proses
    for _ in range(n_workers_cpu):
        q.put(None)

# Stage 2: Worker Process
def worker(q, results):
    while True:
        file_id = q.get()
        if file_id is None:
            break
        result = process_file(file_id)
        results.append(result)

# Pipeline Executor
def run_pipeline(n_loader_threads, n_workers_cpu, jumlah_file):
    file_list = [f"file_{i}" for i in range(jumlah_file)]
    
    # Gunakan multiprocessing-safe queue dan list
    q = multiprocessing.Queue()
    manager = multiprocessing.Manager()
    results = manager.list()

    start = time.time()

    # Jalankan loader threads
    loader_threads = []
    chunk_size = len(file_list) // n_loader_threads
    for i in range(n_loader_threads):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < n_loader_threads - 1 else len(file_list)
        chunk = file_list[start_idx:end_idx]
        t = threading.Thread(target=loader, args=(chunk, q, n_workers_cpu))
        loader_threads.append(t)
        t.start()

    # Jalankan worker processes
    processes = []
    for _ in range(n_workers_cpu):
        p = Process(target=worker, args=(q, results))
        processes.append(p)
        p.start()

    # Tunggu semua loader selesai
    for t in loader_threads:
        t.join()

    # Tunggu semua worker selesai
    for p in processes:
        p.join()

    end = time.time()

    waktu = round(end - start, 2)
    throughput = round(jumlah_file / waktu, 2)
    avg_latency = round(waktu / jumlah_file, 3)

    return waktu, throughput, avg_latency

# MAIN
def main():
    jumlah_file = 50
    n_loader_threads = 2  # Tetap
    cpu_worker_counts = [1, 2, 4, 8]
    hasil = []

    print("\n=== Menjalankan Pipeline ===")
    for n_workers in cpu_worker_counts:
        print(f"- Threads Loader: {n_loader_threads}, Workers CPU: {n_workers}")
        waktu, throughput, avg_latency = run_pipeline(n_loader_threads, n_workers, jumlah_file)
        hasil.append([n_loader_threads, n_workers, jumlah_file, waktu, throughput, avg_latency])
        print(f"[OK] Selesai kombinasi {n_loader_threads}T / {n_workers}P\n")

    # Cetak Tabel
    print("\n=== TABEL HASIL ===")
    print(f"{'Threads Loader':<15} {'Workers CPU':<12} {'Jumlah File':<13} {'Waktu (s)':<10} {'Throughput (file/s)':<22} {'Avg Latency (s)'}")
    for row in hasil:
        print(f"{row[0]:<15} {row[1]:<12} {row[2]:<13} {row[3]:<10} {row[4]:<22} {row[5]}")

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")  # penting untuk Windows
    main()
