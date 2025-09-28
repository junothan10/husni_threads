#Husni Ayi Nurdin
#237006002 A


import threading
import time
import random

# Fungsi simulasi download (I/O bound)
def download_file(i, sec):
    print(f"[{i}] Mulai download... ({sec:.2f} detik)")
    time.sleep(sec)
    print(f"[{i}] Selesai download!")

# Mode Serial
def run_serial(jobs):
    start = time.time()
    for i, sec in jobs:
        download_file(i, sec)
    end = time.time()
    return end - start

# Mode Threaded
def run_threads(jobs, max_threads):
    threads = []
    start = time.time()

    for i, sec in jobs:
        t = threading.Thread(target=download_file, args=(i, sec))
        threads.append(t)
        t.start()

        # Kontrol jumlah thread aktif (batasi per batch)
        while threading.active_count() > max_threads:
            time.sleep(0.01)  # tunggu thread lain selesai

    for t in threads:
        t.join()

    end = time.time()
    return end - start

# Simulasi & Tabel Hasil
def main():
    # Buat 10 file dengan durasi acak (0.5–2.0 detik)
    random.seed(42)
    jobs = [(i, random.uniform(0.5, 2.0)) for i in range(10)]

    print("\n=== PROSES SERIAL ===")
    waktu_serial = run_serial(jobs)

    tabel = []
    tabel.append(["Serial", 10, round(waktu_serial, 2), "1.00x"])

    for n_thread in [2, 4, 8]:
        print(f"\n=== PROSES THREAD ({n_thread}) ===")
        waktu_thread = run_threads(jobs, max_threads=n_thread)
        speedup = waktu_serial / waktu_thread
        tabel.append([
            f"Threads ({n_thread})",
            10,
            round(waktu_thread, 2),
            f"{speedup:.2f}x"
        ])

    # Cetak Tabel
    print("\n=== TABEL HASIL ===")
    print(f"{'Mode':<15} {'Jumlah File':<12} {'Waktu (s)':<10} {'Speedup'}")
    for row in tabel:
        print(f"{row[0]:<15} {row[1]:<12} {row[2]:<10} {row[3]}")

if __name__ == "__main__":
    main()
