"""
apps/keuangan_pribadi.py - Aplikasi 4: Keuangan Pribadi
======================================================
Mata Kuliah : Pemrograman Fungsional
Fungsi fplib yang digunakan:
1. autentikasi()
2. hitung_total()
3. hitung_rata_rata()
4. format_rupiah()
5. hitung_persentase()

Fitur:
- Login pengguna (akun demo: rizky / 12345).
- Menampilkan seluruh catatan transaksi (Pemasukan & Pengeluaran).
- Mencatat transaksi pemasukan atau pengeluaran baru.
- Mengelompokkan transaksi berdasarkan kategori.
- Menghitung total pemasukan dan total pengeluaran dengan hitung_total().
- Menghitung saldo akhir (total pemasukan - total pengeluaran).
- Menghitung rata-rata nominal pengeluaran dengan hitung_rata_rata().
- Menghitung rasio pengeluaran terhadap pemasukan serta persentase alokasi
  kategori dengan hitung_persentase().
- Memformat seluruh nilai nominal dengan format_rupiah().
"""

import copy
from datetime import date
import os
import sys

# Menambahkan root project agar dapat mengimpor fplib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fplib import (
    autentikasi,
    format_rupiah,
    hitung_persentase,
    hitung_rata_rata,
    hitung_total,
)

# Akun Demo Keuangan Pribadi
USERS_KEUANGAN = {
    "rizky": "12345",
    "user": "12345",
}

# Data Awal Transaksi Keuangan
DATA_TRANSAKSI = [
    {"id": "T01", "tipe": "Pemasukan", "kategori": "Gaji", "deskripsi": "Gaji Pokok Bulanan", "nominal": 5000000, "tanggal": "2026-11-01"},
    {"id": "T02", "tipe": "Pemasukan", "kategori": "Freelance", "deskripsi": "Proyek Desain Web", "nominal": 1500000, "tanggal": "2026-11-05"},
    {"id": "T03", "tipe": "Pengeluaran", "kategori": "Makanan", "deskripsi": "Makan & Minum Harian", "nominal": 850000, "tanggal": "2026-11-07"},
    {"id": "T04", "tipe": "Pengeluaran", "kategori": "Transportasi", "deskripsi": "Bensin & Parkir", "nominal": 350000, "tanggal": "2026-11-09"},
    {"id": "T05", "tipe": "Pengeluaran", "kategori": "Kebutuhan", "deskripsi": "Belanja Bulanan & Listrik", "nominal": 1200000, "tanggal": "2026-11-10"},
    {"id": "T06", "tipe": "Pengeluaran", "kategori": "Hiburan", "deskripsi": "Langganan Streaming & Nonton", "nominal": 150000, "tanggal": "2026-11-12"},
]


def tampilkan_daftar_transaksi(daftar):
    """Menampilkan daftar transaksi dengan format tabel rapi."""
    print("\n" + "=" * 80)
    print(f"{'ID':<5} | {'TANGGAL':<10} | {'TIPE':<11} | {'KATEGORI':<14} | {'DESKRIPSI':<22} | {'NOMINAL':>14}")
    print("-" * 80)
    for t in daftar:
        tanda = "+" if t["tipe"] == "Pemasukan" else "-"
        # MENGGUNAKAN fplib.format_rupiah()
        nominal_str = f"{tanda}{format_rupiah(t['nominal'])}"
        print(
            f"{t['id']:<5} | {t['tanggal']:<10} | {t['tipe']:<11} | "
            f"{t['kategori']:<14} | {t['deskripsi'][:20]:<22} | {nominal_str:>14}"
        )
    print("=" * 80)


def catat_transaksi_baru(daftar):
    """Mencatat transaksi pemasukan atau pengeluaran baru."""
    print("\n--- Tambah Transaksi Baru ---")
    print("Pilih Tipe Transaksi:")
    print("1. Pemasukan (+)")
    print("2. Pengeluaran (-)")
    pilih_tipe = input("Pilih (1/2): ").strip()

    if pilih_tipe == "1":
        tipe = "Pemasukan"
        kategori_opsi = ["Gaji", "Freelance", "Investasi", "Hadiah", "Lainnya"]
    elif pilih_tipe == "2":
        tipe = "Pengeluaran"
        kategori_opsi = ["Makanan", "Transportasi", "Kebutuhan", "Hiburan", "Kesehatan", "Lainnya"]
    else:
        print("[!] Pilihan tipe tidak valid.")
        return

    print(f"\nPilih Kategori {tipe}:")
    for idx, k in enumerate(kategori_opsi, 1):
        print(f"{idx}. {k}")
    pilih_kat = input(f"Pilihan kategori (1-{len(kategori_opsi)}): ").strip()

    try:
        kat_idx = int(pilih_kat) - 1
        if 0 <= kat_idx < len(kategori_opsi):
            kategori = kategori_opsi[kat_idx]
        else:
            kategori = "Lainnya"
    except ValueError:
        kategori = "Lainnya"

    deskripsi = input("Deskripsi singkat: ").strip() or f"{tipe} {kategori}"

    try:
        nominal_input = input("Nominal transaksi: Rp ").strip()
        nominal = int(nominal_input)
        if nominal <= 0:
            print("[!] Nominal harus lebih besar dari 0.")
            return
    except ValueError:
        print("[!] Masukkan nominal angka yang valid.")
        return

    new_id = f"T{len(daftar) + 1:02d}"
    transaksi = {
        "id": new_id,
        "tipe": tipe,
        "kategori": kategori,
        "deskripsi": deskripsi,
        "nominal": nominal,
        "tanggal": str(date.today()),
    }
    daftar.append(transaksi)
    # MENGGUNAKAN fplib.format_rupiah()
    print(f"\n[+] Berhasil mencatat {tipe} sebesar {format_rupiah(nominal)}!")


def ringkasan_keuangan(daftar):
    """Menghitung dan menampilkan total pemasukan, pengeluaran, saldo, dan rata-rata."""
    # List comprehension murni untuk memisahkan nominal
    nominal_masuk = [t["nominal"] for t in daftar if t["tipe"] == "Pemasukan"]
    nominal_keluar = [t["nominal"] for t in daftar if t["tipe"] == "Pengeluaran"]

    # MENGGUNAKAN fplib.hitung_total()
    total_masuk = hitung_total(nominal_masuk)
    total_keluar = hitung_total(nominal_keluar)
    saldo = total_masuk - total_keluar

    # MENGGUNAKAN fplib.hitung_rata_rata()
    rata_keluar = hitung_rata_rata(nominal_keluar)

    # MENGGUNAKAN fplib.hitung_persentase()
    rasio_pengeluaran = hitung_persentase(total_keluar, total_masuk)

    print("\n" + "=" * 55)
    print("               RINGKASAN KEUANGAN")
    print("=" * 55)
    # MENGGUNAKAN fplib.format_rupiah()
    print(f"Total Pemasukan       : {format_rupiah(total_masuk)}")
    print(f"Total Pengeluaran     : {format_rupiah(total_keluar)}")
    print("-" * 55)
    print(f"Sisa Saldo            : {format_rupiah(saldo)}")
    print(f"Rata-rata Pengeluaran : {format_rupiah(rata_keluar)} / transaksi")
    print(f"Rasio Pengeluaran     : {rasio_pengeluaran}% dari pemasukan")
    print("=" * 55)


def analisis_kategori_pengeluaran(daftar):
    """Mengelompokkan pengeluaran berdasarkan kategori dan menghitung persentasenya."""
    pengeluaran = [t for t in daftar if t["tipe"] == "Pengeluaran"]
    if not pengeluaran:
        print(">> Belum ada data pengeluaran untuk dianalisis.")
        return

    # MENGGUNAKAN fplib.hitung_total()
    total_keluar = hitung_total([t["nominal"] for t in pengeluaran])

    # Mengelompokkan kategori secara deklaratif
    kategori_set = sorted(list({t["kategori"] for t in pengeluaran}))

    print("\n" + "=" * 62)
    print("               ALOKASI PENGELUARAN PER KATEGORI")
    print("=" * 62)
    print(f"{'KATEGORI':<18} | {'TOTAL PENGELUARAN':>18} | {'PERSENTASE':>12}")
    print("-" * 62)

    for kat in kategori_set:
        total_kat = hitung_total([t["nominal"] for t in pengeluaran if t["kategori"] == kat])
        # MENGGUNAKAN fplib.hitung_persentase()
        persen_kat = hitung_persentase(total_kat, total_keluar)
        # MENGGUNAKAN fplib.format_rupiah()
        print(f"{kat:<18} | {format_rupiah(total_kat):>18} | {persen_kat:>11.2f}%")

    print("=" * 62)
    print(f"{'TOTAL KESELURUHAN':<18} | {format_rupiah(total_keluar):>18} | {'100.00%':>12}")
    print("=" * 62 + "\n")


def menu_keuangan():
    """Menu utama aplikasi Keuangan Pribadi."""
    transaksi = copy.deepcopy(DATA_TRANSAKSI)

    while True:
        print("\n" + "=" * 45)
        print("      MANAJEMEN KEUANGAN PRIBADI")
        print("=" * 45)
        print("1. Tampilkan Riwayat Semua Transaksi")
        print("2. Catat Transaksi Baru (+ / -)")
        print("3. Ringkasan Saldo & Rata-rata")
        print("4. Analisis Pengeluaran per Kategori")
        print("0. Keluar / Kembali ke Menu Utama")
        print("=" * 45)

        pilihan = input("Pilih menu (0-4): ").strip()

        if pilihan == "1":
            tampilkan_daftar_transaksi(transaksi)
        elif pilihan == "2":
            catat_transaksi_baru(transaksi)
        elif pilihan == "3":
            ringkasan_keuangan(transaksi)
        elif pilihan == "4":
            analisis_kategori_pengeluaran(transaksi)
        elif pilihan == "0":
            print(">> Keluar dari Aplikasi Keuangan Pribadi.")
            break
        else:
            print("[!] Pilihan tidak valid. Silakan masukkan angka 0-4.")


def jalankan_keuangan():
    """Titik masuk utama aplikasi Keuangan Pribadi dengan otentikasi mandiri."""
    print("\n" + "#" * 50)
    print("    SELAMAT DATANG DI KEUANGAN PRIBADI")
    print("#" * 50)
    print("Akun Demo: rizky / 12345 (atau user / 12345)")

    maks_percobaan = 3
    percobaan = 0

    while percobaan < maks_percobaan:
        username = input("Username : ").strip()
        password = input("Password : ").strip()

        # MENGGUNAKAN fplib.autentikasi()
        if autentikasi(username, password, USERS_KEUANGAN):
            print(f"\n[+] Login Berhasil! Selamat datang kembali, {username}.\n")
            menu_keuangan()
            return
        else:
            percobaan += 1
            sisa = maks_percobaan - percobaan
            print(f"[-] Login Gagal! Username atau password salah. (Sisa percobaan: {sisa})")

    print("[!] Batas maksimal percobaan login tercapai. Kembali ke menu utama.")


if __name__ == "__main__":
    jalankan_keuangan()
