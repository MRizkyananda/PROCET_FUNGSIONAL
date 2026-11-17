"""
main.py - Pusat Navigasi Aplikasi Pemrograman Fungsional
========================================================
Tugas Besar : Pemrograman Fungsional Python
Tema        : Satu Library, Lima Aplikasi (fplib.py)

Menu Aplikasi:
1. Kasir Kantin
2. Presensi Kelas
3. Perpustakaan Mini
4. Keuangan Pribadi
5. Nilai Mahasiswa
0. Keluar
"""

import sys

from apps.kasir_kantin import jalankan_kasir
from apps.keuangan_pribadi import jalankan_keuangan
from apps.nilai_mahasiswa import jalankan_nilai
from apps.perpustakaan import jalankan_perpustakaan
from apps.presensi_kelas import jalankan_presensi


def cetak_header():
    """Menampilkan header selamat datang."""
    print("\n" + "=" * 60)
    print("      TUGAS BESAR PEMROGRAMAN FUNGSIONAL PYTHON")
    print("            SATU LIBRARY, LIMA APLIKASI")
    print("                 Library: fplib.py")
    print("=" * 60)


def menu_utama():
    """Menampilkan menu navigasi utama."""
    while True:
        cetak_header()
        print("PILIHAN APLIKASI:")
        print("  [1] Kasir Kantin")
        print("  [2] Presensi Kelas")
        print("  [3] Perpustakaan Mini")
        print("  [4] Keuangan Pribadi")
        print("  [5] Nilai Mahasiswa")
        print("  [0] Keluar")
        print("=" * 60)

        pilihan = input("Masukkan pilihan Anda (0-5): ").strip()

        if pilihan == "1":
            jalankan_kasir()
        elif pilihan == "2":
            jalankan_presensi()
        elif pilihan == "3":
            jalankan_perpustakaan()
        elif pilihan == "4":
            jalankan_keuangan()
        elif pilihan == "5":
            jalankan_nilai()
        elif pilihan == "0":
            print("\n" + "=" * 60)
            print("  Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            print("=" * 60 + "\n")
            sys.exit(0)
        else:
            print("\n[!] Pilihan tidak valid. Silakan pilih angka antara 0 sampai 5.")

        input("\n[ Tekan ENTER untuk kembali ke Menu Utama... ]")


if __name__ == "__main__":
    try:
        menu_utama()
    except KeyboardInterrupt:
        print("\n\n[!] Program dihentikan oleh pengguna. Sampai jumpa!")
        sys.exit(0)
