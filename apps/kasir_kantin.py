"""
apps/kasir_kantin.py - Aplikasi 1: Kasir Kantin
================================================
Mata Kuliah : Pemrograman Fungsional
Fungsi fplib yang digunakan:
1. autentikasi()
2. hitung_total()
3. format_rupiah()
4. filter_data()

Fitur:
- Login kasir dengan akun demo.
- Menampilkan daftar menu makanan dan minuman.
- Menyaring/mencari menu berdasarkan kategori (Makanan / Minuman).
- Memilih barang dan jumlah pembelian ke dalam keranjang.
- Menghitung subtotal, diskon otomatis jika belanja >= Rp50.000 (10%).
- Menghitung total pembayaran dengan hitung_total().
- Menampilkan struk transaksi belanja yang rapi dan terformat Rupiah.
"""

import os
import sys

# Menambahkan root project agar dapat mengimpor fplib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fplib import autentikasi, filter_data, format_rupiah, hitung_total

# Data Akun Demo Kasir
USERS_KASIR = {
    "kasir": "12345",
    "admin": "admin123",
}

# Data Menu Awal (Immutability dijaga selama komputasi)
DAFTAR_MENU = [
    {"id": "M01", "nama": "Nasi Goreng Spesial", "kategori": "Makanan", "harga": 15000},
    {"id": "M02", "nama": "Mie Ayam Bakso", "kategori": "Makanan", "harga": 13000},
    {"id": "M03", "nama": "Ayam Geprek Sambal Korek", "kategori": "Makanan", "harga": 17000},
    {"id": "M04", "nama": "Soto Ayam Lamongan", "kategori": "Makanan", "harga": 14000},
    {"id": "D01", "nama": "Es Teh Manis", "kategori": "Minuman", "harga": 4000},
    {"id": "D02", "nama": "Jus Alpukat", "kategori": "Minuman", "harga": 10000},
    {"id": "D03", "nama": "Kopi Susu Gula Aren", "kategori": "Minuman", "harga": 8000},
    {"id": "D04", "nama": "Air Mineral Dingin", "kategori": "Minuman", "harga": 3000},
]


def hitung_diskon(total_belanja: int) -> int:
    """
    Pure function untuk menghitung besaran diskon:
    Diskon 10% jika belanja >= Rp 50.000, selain itu 0.
    """
    if total_belanja >= 50000:
        return int(total_belanja * 0.10)
    return 0


def tampilkan_daftar_menu(menu_list):
    """Menampilkan daftar menu secara deklaratif."""
    print("\n" + "=" * 60)
    print(f"{'ID':<6} | {'NAMA MENU':<28} | {'KATEGORI':<10} | {'HARGA':>8}")
    print("-" * 60)
    for m in menu_list:
        print(f"{m['id']:<6} | {m['nama']:<28} | {m['kategori']:<10} | {format_rupiah(m['harga']):>8}")
    print("=" * 60)


def cari_menu_by_id(menu_list, menu_id):
    """Mencari item menu berdasarkan ID menggunakan filter_data (Higher-order)."""
    hasil = filter_data(menu_list, lambda item: item["id"].upper() == menu_id.strip().upper())
    return hasil[0] if hasil else None


def proses_transaksi(menu_list):
    """Memproses transaksi pembelian di kasir."""
    keranjang = []
    print("\n--- Transaksi Pembelian Baru ---")
    tampilkan_daftar_menu(menu_list)

    while True:
        menu_id = input("\nMasukkan ID Menu (atau ketik 'selesai' / 'batal'): ").strip()
        if menu_id.lower() == "selesai":
            break
        if menu_id.lower() == "batal":
            print(">> Transaksi dibatalkan.")
            return

        item = cari_menu_by_id(menu_list, menu_id)
        if not item:
            print("[!] Menu dengan ID tersebut tidak ditemukan. Silakan cek kembali.")
            continue

        try:
            qty_input = input(f"Jumlah untuk '{item['nama']}': ").strip()
            qty = int(qty_input)
            if qty <= 0:
                print("[!] Jumlah pembelian harus lebih dari 0.")
                continue
        except ValueError:
            print("[!] Masukkan angka yang valid untuk jumlah.")
            continue

        subtotal = item["harga"] * qty
        # Menambahkan data keranjang secara immutable style
        keranjang.append({
            "id": item["id"],
            "nama": item["nama"],
            "harga": item["harga"],
            "qty": qty,
            "subtotal": subtotal,
        })
        print(f">> Berhasil menambahkan {qty}x {item['nama']} ({format_rupiah(subtotal)}).")

    if not keranjang:
        print(">> Keranjang kosong. Tidak ada transaksi yang diproses.")
        return

    # MENGGUNAKAN fplib.hitung_total()
    daftar_subtotal = [item["subtotal"] for item in keranjang]
    gross_total = hitung_total(daftar_subtotal)
    diskon = hitung_diskon(gross_total)
    net_total = gross_total - diskon

    # Cetak Struk Pembayaran
    print("\n" + "=" * 50)
    print("           STRUK PEMBAYARAN KANTIN")
    print("=" * 50)
    for idx, item in enumerate(keranjang, 1):
        print(f"{idx}. {item['nama']}")
        print(f"   {item['qty']} x {format_rupiah(item['harga'])} = {format_rupiah(item['subtotal'])}")
    print("-" * 50)
    print(f"Subtotal        : {format_rupiah(gross_total)}")
    if diskon > 0:
        print(f"Diskon (10%)    : -{format_rupiah(diskon)}")
    print(f"TOTAL BAYAR     : {format_rupiah(net_total)}")
    print("=" * 50)

    # Input Pembayaran
    while True:
        bayar_input = input("Uang Diterima : Rp ").strip()
        try:
            uang_bayar = int(bayar_input)
            if uang_bayar < net_total:
                kurang = net_total - uang_bayar
                print(f"[!] Uang tidak cukup. Kurang {format_rupiah(kurang)}.")
                continue
            kembalian = uang_bayar - net_total
            print(f"Kembalian       : {format_rupiah(kembalian)}")
            print("=" * 50)
            print(">> Transaksi Berhasil! Terima kasih atas kunjungan Anda.\n")
            break
        except ValueError:
            print("[!] Harap masukkan nominal uang yang valid.")


def menu_kasir():
    """Menu utama aplikasi Kasir Kantin."""
    menu_aktif = list(DAFTAR_MENU)

    while True:
        print("\n" + "=" * 45)
        print("           SISTEM KASIR KANTIN")
        print("=" * 45)
        print("1. Tampilkan Semua Menu")
        print("2. Filter Menu Berdasarkan Kategori")
        print("3. Transaksi Baru (Pesan & Cetak Struk)")
        print("0. Keluar / Kembali ke Menu Utama")
        print("=" * 45)

        pilihan = input("Pilih menu (0-3): ").strip()

        if pilihan == "1":
            tampilkan_daftar_menu(menu_aktif)

        elif pilihan == "2":
            print("\nPilih Kategori Filter:")
            print("1. Makanan")
            print("2. Minuman")
            kat_pilihan = input("Pilihan (1/2): ").strip()
            if kat_pilihan == "1":
                # MENGGUNAKAN fplib.filter_data()
                hasil_filter = filter_data(menu_aktif, lambda m: m["kategori"] == "Makanan")
                print("\n[ Hasil Filter: Makanan ]")
                tampilkan_daftar_menu(hasil_filter)
            elif kat_pilihan == "2":
                hasil_filter = filter_data(menu_aktif, lambda m: m["kategori"] == "Minuman")
                print("\n[ Hasil Filter: Minuman ]")
                tampilkan_daftar_menu(hasil_filter)
            else:
                print("[!] Pilihan kategori tidak valid.")

        elif pilihan == "3":
            proses_transaksi(menu_aktif)

        elif pilihan == "0":
            print(">> Keluar dari Aplikasi Kasir Kantin.")
            break

        else:
            print("[!] Pilihan tidak valid. Silakan masukkan angka 0-3.")


def jalankan_kasir():
    """Titik masuk utama aplikasi Kasir Kantin dengan otentikasi mandiri."""
    print("\n" + "#" * 50)
    print("       SELAMAT DATANG DI KASIR KANTIN")
    print("#" * 50)
    print("Akun Demo: kasir / 12345")

    maks_percobaan = 3
    percobaan = 0

    while percobaan < maks_percobaan:
        username = input("Username : ").strip()
        password = input("Password : ").strip()

        # MENGGUNAKAN fplib.autentikasi()
        if autentikasi(username, password, USERS_KASIR):
            print(f"\n[+] Login Berhasil! Selamat bekerja, {username}.\n")
            menu_kasir()
            return
        else:
            percobaan += 1
            sisa = maks_percobaan - percobaan
            print(f"[-] Login Gagal! Username atau password salah. (Sisa percobaan: {sisa})")

    print("[!] Anda telah mencapai batas maksimal percobaan login. Kembali ke menu utama.")


if __name__ == "__main__":
    jalankan_kasir()
