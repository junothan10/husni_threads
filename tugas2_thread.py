#Husni Ayi Nurdin
#237006002 A

import time
from concurrent.futures import ProcessPoolExecutor

# Fungsi berat (CPU-bound)
def heavy(n):
    total = 0
    for i in range(10**6):
        total += i * i
    return total

# Eksekusi secara serial
def run_serial():
    start = time.time()
    for i in range(10):
        print(f"[Serial] Mulai proses ke-{i+1}")
        heavy(10**6)
        print(f"[Serial] Selesai proses ke-{i+1}")
    end = time.time()
    return end - start

# Eksekusi secara paralel dengan ProcessPoolExecutor
def run_parallel(n_process):
    start = time.time()
    print(f"[Parallel - {n_process} proses] Menjalankan proses...")
    with ProcessPoolExecutor(max_workers=n_process) as executor:
        executor.map(heavy, [10**6] * 10)
    end = time.time()
    return end - start

# Fungsi utama
def main():
    print("\n=== PROSES SERIAL ===")
    waktu_serial = run_serial()

    hasil = []
    hasil.append(["Serial", 1, round(waktu_serial, 2), "1.00x", "100%"])

    for n in [2, 4, 8]:
        print(f"\n=== PROSES PARALLEL ({n} proses) ===")
        waktu_paralel = run_parallel(n)
        speedup = waktu_serial / waktu_paralel
        efisiensi = (speedup / n) * 100
        hasil.append([
            f"{n} proses",
            n,
            round(waktu_paralel, 2),
            f"{speedup:.2f}x",
            f"{efisiensi:.0f}%"
        ])

    # Tampilkan Tabel
    print("\n=== TABEL HASIL ===")
    print(f"{'Mode':<12} {'Proses':<8} {'Waktu (s)':<10} {'Speedup':<10} {'Efisiensi'}")
    for row in hasil:
        print(f"{row[0]:<12} {row[1]:<8} {row[2]:<10} {row[3]:<10} {row[4]}")

if __name__ == "__main__":
    main()
