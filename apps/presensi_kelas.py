"""
apps/presensi_kelas.py - Aplikasi 2: Presensi Kelas
===================================================
Mata Kuliah : Pemrograman Fungsional
Fungsi fplib yang digunakan:
1. autentikasi()
2. cari_data()
3. hitung_rata_rata()
4. filter_data()
5. hitung_persentase()

Fitur:
- Login mahasiswa / admin.
- Menampilkan daftar mahasiswa beserta rincian kehadiran.
- Mencari mahasiswa berdasarkan nama atau NIM dengan cari_data().
- Mencatat status kehadiran pertemuan baru (Hadir, Izin, Sakit, Alfa).
- Menampilkan rekap kehadiran (filter mahasiswa rajin / yang pernah alfa) dengan filter_data().
- Menghitung persentase kehadiran per individu dengan hitung_persentase().
- Menghitung rata-rata kehadiran seluruh kelas dengan hitung_rata_rata().
"""

import copy
import os
import sys

# Menambahkan root project agar dapat mengimpor fplib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fplib import (
    autentikasi,
    cari_data,
    filter_data,
    hitung_persentase,
    hitung_rata_rata,
)

# Akun Demo Presensi
USERS_PRESENSI = {
    "mahasiswa": "12345",
    "admin": "12345",
    "dosen": "12345",
}

# Data Awal Mahasiswa dan Riwayat Kehadiran
DATA_MAHASISWA = [
    {"nim": "220101", "nama": "Ahmad Fauzi", "kehadiran": ["Hadir", "Hadir", "Hadir", "Izin", "Hadir"]},
    {"nim": "220102", "nama": "Bunga Citra", "kehadiran": ["Hadir", "Sakit", "Hadir", "Hadir", "Hadir"]},
    {"nim": "220103", "nama": "Citra Lestari", "kehadiran": ["Hadir", "Hadir", "Alfa", "Izin", "Hadir"]},
    {"nim": "220104", "nama": "Dimas Pratama", "kehadiran": ["Hadir", "Hadir", "Hadir", "Hadir", "Hadir"]},
    {"nim": "220105", "nama": "Eka Saputra", "kehadiran": ["Alfa", "Sakit", "Alfa", "Hadir", "Izin"]},
]


def hitung_statistik_mahasiswa(mhs):
    """
    Pure function: menghitung rincian status kehadiran dan persentasenya.
    Menggunakan fplib.hitung_persentase().
    """
    kehadiran = mhs.get("kehadiran", [])
    total_pertemuan = len(kehadiran)
    hadir = sum(1 for status in kehadiran if status == "Hadir")
    izin = sum(1 for status in kehadiran if status == "Izin")
    sakit = sum(1 for status in kehadiran if status == "Sakit")
    alfa = sum(1 for status in kehadiran if status == "Alfa")

    # MENGGUNAKAN fplib.hitung_persentase()
    persen = hitung_persentase(hadir, total_pertemuan)

    return {
        "nim": mhs["nim"],
        "nama": mhs["nama"],
        "hadir": hadir,
        "izin": izin,
        "sakit": sakit,
        "alfa": alfa,
        "total": total_pertemuan,
        "persentase": persen,
    }


def tampilkan_daftar_rekap(data):
    """Menampilkan tabel rekap kehadiran mahasiswa."""
    print("\n" + "=" * 75)
    print(f"{'NIM':<8} | {'NAMA MAHASISWA':<22} | {'H':<3} | {'I':<3} | {'S':<3} | {'A':<3} | {'PERSEN':>8}")
    print("-" * 75)
    for m in data:
        stat = hitung_statistik_mahasiswa(m)
        print(
            f"{stat['nim']:<8} | {stat['nama']:<22} | {stat['hadir']:<3} | "
            f"{stat['izin']:<3} | {stat['sakit']:<3} | {stat['alfa']:<3} | {stat['persentase']:>7.2f}%"
        )
    print("=" * 75)
    print("Keterangan: H = Hadir, I = Izin, S = Sakit, A = Alfa\n")


def cari_mahasiswa_menu(data):
    """Mencari mahasiswa berdasarkan NIM atau Nama menggunakan cari_data()."""
    print("\nPilihan Pencarian:")
    print("1. Berdasarkan NIM")
    print("2. Berdasarkan Nama")
    opsi = input("Pilih (1/2): ").strip()

    if opsi == "1":
        nim = input("Masukkan NIM yang dicari: ").strip()
        # MENGGUNAKAN fplib.cari_data()
        hasil = cari_data(data, nim, "nim")
    elif opsi == "2":
        nama = input("Masukkan Nama yang dicari: ").strip()
        # MENGGUNAKAN fplib.cari_data()
        hasil = cari_data(data, nama, "nama")
    else:
        print("[!] Pilihan tidak valid.")
        return

    if hasil:
        print(f"\n[+] Ditemukan {len(hasil)} mahasiswa:")
        tampilkan_daftar_rekap(hasil)
    else:
        print("[-] Mahasiswa tidak ditemukan.")


def catat_presensi_baru(data):
    """Mencatat presensi untuk pertemuan baru."""
    print("\n--- Pencatatan Presensi Pertemuan Baru ---")
    pertemuan_ke = len(data[0]["kehadiran"]) + 1 if data else 1
    print(f"Mencatat Presensi Pertemuan ke-{pertemuan_ke}")
    print("Pilihan Status: (1) Hadir  (2) Izin  (3) Sakit  (4) Alfa")

    pilihan_map = {"1": "Hadir", "2": "Izin", "3": "Sakit", "4": "Alfa"}

    for m in data:
        while True:
            pilihan = input(f"Status untuk {m['nim']} - {m['nama']} [1/2/3/4]: ").strip()
            if pilihan in pilihan_map:
                status = pilihan_map[pilihan]
                # Menambahkan kehadiran secara terkontrol
                m["kehadiran"].append(status)
                break
            else:
                print("[!] Masukkan angka 1 sampai 4.")

    print(f"\n[+] Sukses mencatat presensi pertemuan ke-{pertemuan_ke} untuk seluruh mahasiswa!")


def rekap_dan_filter_kehadiran(data):
    """Menyaring mahasiswa menggunakan filter_data() dan menampilkan statistik."""
    print("\n--- Filter & Analisis Presensi ---")
    print("1. Filter Mahasiswa dengan Kehadiran Bermasalah (< 75%)")
    print("2. Filter Mahasiswa yang Pernah Alfa")
    print("3. Tampilkan Rata-rata Kehadiran Seluruh Kelas")
    opsi = input("Pilih menu (1-3): ").strip()

    if opsi == "1":
        # MENGGUNAKAN fplib.filter_data() dengan lambda predikat
        kurang_disiplin = filter_data(
            data,
            lambda m: hitung_statistik_mahasiswa(m)["persentase"] < 75.0
        )
        print(f"\n[ Mahasiswa dengan Kehadiran < 75% ({len(kurang_disiplin)} orang) ]")
        if kurang_disiplin:
            tampilkan_daftar_rekap(kurang_disiplin)
        else:
            print(">> Hebat! Semua mahasiswa memiliki kehadiran >= 75%.")

    elif opsi == "2":
        # MENGGUNAKAN fplib.filter_data()
        pernah_alfa = filter_data(
            data,
            lambda m: "Alfa" in m.get("kehadiran", [])
        )
        print(f"\n[ Mahasiswa yang Memiliki Catatan Alfa ({len(pernah_alfa)} orang) ]")
        if pernah_alfa:
            tampilkan_daftar_rekap(pernah_alfa)
        else:
            print(">> Tidak ada mahasiswa yang memiliki catatan Alfa.")

    elif opsi == "3":
        # MENGGUNAKAN fplib.hitung_rata_rata()
        semua_persen = [hitung_statistik_mahasiswa(m)["persentase"] for m in data]
        rata_rata = hitung_rata_rata(semua_persen)
        print("\n" + "=" * 50)
        print(f"Total Mahasiswa        : {len(data)} orang")
        print(f"Rata-rata Kehadiran    : {rata_rata}%")
        print("=" * 50)

    else:
        print("[!] Opsi tidak valid.")


def menu_presensi():
    """Menu utama aplikasi Presensi Kelas."""
    data_kelas = copy.deepcopy(DATA_MAHASISWA)

    while True:
        print("\n" + "=" * 45)
        print("          SISTEM PRESENSI KELAS")
        print("=" * 45)
        print("1. Tampilkan Daftar Mahasiswa & Rekap")
        print("2. Cari Mahasiswa (NIM / Nama)")
        print("3. Catat Presensi Pertemuan Baru")
        print("4. Filter Status & Analisis Rata-rata")
        print("0. Keluar / Kembali ke Menu Utama")
        print("=" * 45)

        pilihan = input("Pilih menu (0-4): ").strip()

        if pilihan == "1":
            tampilkan_daftar_rekap(data_kelas)
        elif pilihan == "2":
            cari_mahasiswa_menu(data_kelas)
        elif pilihan == "3":
            catat_presensi_baru(data_kelas)
        elif pilihan == "4":
            rekap_dan_filter_kehadiran(data_kelas)
        elif pilihan == "0":
            print(">> Keluar dari Aplikasi Presensi Kelas.")
            break
        else:
            print("[!] Pilihan tidak valid. Silakan masukkan angka 0-4.")


def jalankan_presensi():
    """Titik masuk utama aplikasi Presensi Kelas dengan otentikasi mandiri."""
    print("\n" + "#" * 50)
    print("      SELAMAT DATANG DI PRESENSI KELAS")
    print("#" * 50)
    print("Akun Demo: mahasiswa / 12345 (atau admin / 12345)")

    maks_percobaan = 3
    percobaan = 0

    while percobaan < maks_percobaan:
        username = input("Username : ").strip()
        password = input("Password : ").strip()

        # MENGGUNAKAN fplib.autentikasi()
        if autentikasi(username, password, USERS_PRESENSI):
            print(f"\n[+] Login Berhasil! Selamat datang, {username}.\n")
            menu_presensi()
            return
        else:
            percobaan += 1
            sisa = maks_percobaan - percobaan
            print(f"[-] Login Gagal! Username atau password salah. (Sisa percobaan: {sisa})")

    print("[!] Batas maksimal percobaan login tercapai. Kembali ke menu utama.")


if __name__ == "__main__":
    jalankan_presensi()
