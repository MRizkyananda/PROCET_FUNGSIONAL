"""
apps/perpustakaan.py - Aplikasi 3: Perpustakaan Mini
===================================================
Mata Kuliah : Pemrograman Fungsional
Fungsi fplib yang digunakan:
1. autentikasi()
2. cari_data()
3. hitung_total()
4. format_rupiah()

Fitur:
- Login anggota / admin.
- Menampilkan katalog buku beserta ketersediaan stok.
- Mencari buku berdasarkan judul menggunakan cari_data().
- Melakukan peminjaman buku baru.
- Menghitung denda keterlambatan pengembalian buku (denda per hari).
- Menghitung total seluruh denda perpustakaan menggunakan hitung_total().
- Menampilkan rincian biaya denda dalam format Rupiah dengan format_rupiah().
"""

import copy
import os
import sys

# Menambahkan root project agar dapat mengimpor fplib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fplib import autentikasi, cari_data, format_rupiah, hitung_total

# Akun Demo Perpustakaan
USERS_PERPUS = {
    "anggota": "12345",
    "admin": "12345",
    "petugas": "petugas123",
}

# Katalog Buku Awal
KATALOG_BUKU = [
    {"id": "B01", "judul": "Pemrograman Python Modern", "pengarang": "Rian Hidayat", "stok": 3},
    {"id": "B02", "judul": "Struktur Data & Algoritma", "pengarang": "Siti Nurhaliza", "stok": 2},
    {"id": "B03", "judul": "Prinsip Pemrograman Fungsional", "pengarang": "Budi Santoso", "stok": 4},
    {"id": "B04", "judul": "Basis Data Relasional & NoSQL", "pengarang": "Dewi Sartika", "stok": 1},
    {"id": "B05", "judul": "Kecerdasan Buatan Terapan", "pengarang": "Eko Prasetyo", "stok": 2},
]

# Riwayat Peminjaman Buku
DATA_PEMINJAMAN = [
    {"id_pinjam": "P01", "peminjam": "Andi", "id_buku": "B01", "judul": "Pemrograman Python Modern", "hari_terlambat": 3, "tarif_denda": 2000, "status": "Dipinjam"},
    {"id_pinjam": "P02", "peminjam": "Bella", "id_buku": "B03", "judul": "Prinsip Pemrograman Fungsional", "hari_terlambat": 0, "tarif_denda": 2000, "status": "Dipinjam"},
    {"id_pinjam": "P03", "peminjam": "Candra", "id_buku": "B02", "judul": "Struktur Data & Algoritma", "hari_terlambat": 5, "tarif_denda": 2000, "status": "Dipinjam"},
]


def hitung_denda_item(pinjam):
    """Pure function untuk menghitung denda satu transaksi peminjaman."""
    hari = pinjam.get("hari_terlambat", 0)
    tarif = pinjam.get("tarif_denda", 2000)
    return max(0, hari * tarif)


def tampilkan_katalog(katalog):
    """Menampilkan daftar buku di katalog."""
    print("\n" + "=" * 68)
    print(f"{'ID':<6} | {'JUDUL BUKU':<32} | {'PENGARANG':<18} | {'STOK':>4}")
    print("-" * 68)
    for b in katalog:
        print(f"{b['id']:<6} | {b['judul']:<32} | {b['pengarang']:<18} | {b['stok']:>4}")
    print("=" * 68)


def cari_buku_judul(katalog):
    """Mencari buku berdasarkan judul menggunakan cari_data()."""
    kata_kunci = input("\nMasukkan judul buku yang dicari: ").strip()
    if not kata_kunci:
        print("[!] Kata kunci tidak boleh kosong.")
        return

    # MENGGUNAKAN fplib.cari_data()
    hasil = cari_data(katalog, kata_kunci, "judul")
    if hasil:
        print(f"\n[+] Ditemukan {len(hasil)} buku dengan kata kunci '{kata_kunci}':")
        tampilkan_katalog(hasil)
    else:
        print(f"[-] Tidak ada buku yang cocok dengan judul '{kata_kunci}'.")


def pinjam_buku(katalog, peminjaman_list):
    """Memproses peminjaman buku."""
    print("\n--- Peminjaman Buku ---")
    tampilkan_katalog(katalog)

    id_buku = input("\nMasukkan ID Buku yang ingin dipinjam: ").strip().upper()
    buku = next((b for b in katalog if b["id"] == id_buku), None)

    if not buku:
        print("[!] Buku dengan ID tersebut tidak ditemukan.")
        return

    if buku["stok"] <= 0:
        print(f"[!] Maaf, stok buku '{buku['judul']}' sedang habis.")
        return

    nama_peminjam = input("Masukkan Nama Peminjam: ").strip()
    if not nama_peminjam:
        print("[!] Nama peminjam tidak boleh kosong.")
        return

    # Kurangi stok buku
    buku["stok"] -= 1
    new_id = f"P{len(peminjaman_list) + 1:02d}"
    transaksi = {
        "id_pinjam": new_id,
        "peminjam": nama_peminjam,
        "id_buku": buku["id"],
        "judul": buku["judul"],
        "hari_terlambat": 0,
        "tarif_denda": 2000,
        "status": "Dipinjam",
    }
    peminjaman_list.append(transaksi)

    print("\n" + "=" * 50)
    print("         BUKTI PEMINJAMAN BUKU")
    print("=" * 50)
    print(f"ID Transaksi : {new_id}")
    print(f"Peminjam     : {nama_peminjam}")
    print(f"Judul Buku   : {buku['judul']}")
    print(f"Batas Waktu  : 7 Hari")
    print(f"Tarif Denda  : {format_rupiah(2000)} / hari jika terlambat")
    print("=" * 50)
    print(">> Peminjaman berhasil dicatat!\n")


def kembalikan_buku(katalog, peminjaman_list):
    """Memproses pengembalian buku dan denda keterlambatan."""
    print("\n--- Pengembalian Buku & Cek Denda ---")
    aktif = [p for p in peminjaman_list if p["status"] == "Dipinjam"]
    if not aktif:
        print(">> Tidak ada buku yang sedang dipinjam.")
        return

    print("\nDaftar Peminjaman Aktif:")
    print("-" * 65)
    for p in aktif:
        print(f"ID: {p['id_pinjam']} | Peminjam: {p['peminjam']:<12} | Buku: {p['judul']}")
    print("-" * 65)

    id_pinjam = input("\nMasukkan ID Transaksi Pinjam: ").strip().upper()
    transaksi = next((p for p in aktif if p["id_pinjam"] == id_pinjam), None)

    if not transaksi:
        print("[!] ID Peminjaman tidak ditemukan.")
        return

    try:
        terlambat_input = input("Jumlah hari keterlambatan (0 jika tepat waktu): ").strip()
        hari_terlambat = max(0, int(terlambat_input))
    except ValueError:
        print("[!] Masukkan angka hari yang valid.")
        return

    transaksi["hari_terlambat"] = hari_terlambat
    transaksi["status"] = "Dikembalikan"

    # Kembalikan stok buku
    buku = next((b for b in katalog if b["id"] == transaksi["id_buku"]), None)
    if buku:
        buku["stok"] += 1

    denda = hitung_denda_item(transaksi)

    print("\n" + "=" * 50)
    print("       BUKTI PENGEMBALIAN BUKU")
    print("=" * 50)
    print(f"Peminjam     : {transaksi['peminjam']}")
    print(f"Judul Buku   : {transaksi['judul']}")
    print(f"Keterlambatan: {hari_terlambat} Hari")
    # MENGGUNAKAN fplib.format_rupiah()
    print(f"Total Denda  : {format_rupiah(denda)}")
    print("=" * 50)
    print(">> Buku berhasil dikembalikan. Terima kasih!\n")


def rekap_peminjaman_dan_denda(peminjaman_list):
    """Menampilkan rekap seluruh peminjaman dan total denda."""
    print("\n" + "=" * 78)
    print("                    REKAP PEMINJAMAN & DENDA")
    print("=" * 78)
    print(f"{'ID':<5} | {'PEMINJAM':<12} | {'JUDUL':<25} | {'STATUS':<12} | {'DENDA':>12}")
    print("-" * 78)

    daftar_denda = []
    for p in peminjaman_list:
        denda = hitung_denda_item(p)
        daftar_denda.append(denda)
        print(
            f"{p['id_pinjam']:<5} | {p['peminjam']:<12} | {p['judul'][:23]:<25} | "
            f"{p['status']:<12} | {format_rupiah(denda):>12}"
        )

    # MENGGUNAKAN fplib.hitung_total()
    total_denda_semua = hitung_total(daftar_denda)

    print("=" * 78)
    # MENGGUNAKAN fplib.format_rupiah()
    print(f"TOTAL DENDA KESELURUHAN : {format_rupiah(total_denda_semua)}")
    print(f"TOTAL TRANSAKSI         : {len(peminjaman_list)} transaksi")
    print("=" * 78 + "\n")


def menu_perpustakaan():
    """Menu utama aplikasi Perpustakaan Mini."""
    katalog = copy.deepcopy(KATALOG_BUKU)
    peminjaman = copy.deepcopy(DATA_PEMINJAMAN)

    while True:
        print("\n" + "=" * 45)
        print("         PERPUSTAKAAN MINI DIGITAL")
        print("=" * 45)
        print("1. Tampilkan Katalog Buku")
        print("2. Cari Buku (Berdasarkan Judul)")
        print("3. Peminjaman Buku")
        print("4. Pengembalian Buku & Cek Denda")
        print("5. Rekap Peminjaman & Total Denda")
        print("0. Keluar / Kembali ke Menu Utama")
        print("=" * 45)

        pilihan = input("Pilih menu (0-5): ").strip()

        if pilihan == "1":
            tampilkan_katalog(katalog)
        elif pilihan == "2":
            cari_buku_judul(katalog)
        elif pilihan == "3":
            pinjam_buku(katalog, peminjaman)
        elif pilihan == "4":
            kembalikan_buku(katalog, peminjaman)
        elif pilihan == "5":
            rekap_peminjaman_dan_denda(peminjaman)
        elif pilihan == "0":
            print(">> Keluar dari Aplikasi Perpustakaan Mini.")
            break
        else:
            print("[!] Pilihan tidak valid. Silakan masukkan angka 0-5.")


def jalankan_perpustakaan():
    """Titik masuk utama aplikasi Perpustakaan dengan otentikasi mandiri."""
    print("\n" + "#" * 50)
    print("    SELAMAT DATANG DI PERPUSTAKAAN MINI")
    print("#" * 50)
    print("Akun Demo: anggota / 12345 (atau admin / 12345)")

    maks_percobaan = 3
    percobaan = 0

    while percobaan < maks_percobaan:
        username = input("Username : ").strip()
        password = input("Password : ").strip()

        # MENGGUNAKAN fplib.autentikasi()
        if autentikasi(username, password, USERS_PERPUS):
            print(f"\n[+] Login Berhasil! Selamat membaca, {username}.\n")
            menu_perpustakaan()
            return
        else:
            percobaan += 1
            sisa = maks_percobaan - percobaan
            print(f"[-] Login Gagal! Username atau password salah. (Sisa percobaan: {sisa})")

    print("[!] Batas maksimal percobaan login tercapai. Kembali ke menu utama.")


if __name__ == "__main__":
    jalankan_perpustakaan()
