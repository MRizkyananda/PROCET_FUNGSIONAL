"""
apps/nilai_mahasiswa.py - Aplikasi 5: Nilai Mahasiswa
=====================================================
Mata Kuliah : Pemrograman Fungsional
Fungsi fplib yang digunakan:
1. autentikasi()
2. cari_data()
3. hitung_rata_rata()
4. filter_data()
5. hitung_persentase()

Fitur:
- Login dosen / mahasiswa (akun demo: dosen / 12345).
- Menampilkan daftar mahasiswa beserta nilai tugas, UTS, UAS, nilai akhir,
  grade huruf, dan status kelulusan.
- Mencari mahasiswa berdasarkan NIM atau Nama menggunakan cari_data().
- Menginput / memperbarui nilai komponen mahasiswa.
- Menyaring mahasiswa lulus / tidak lulus menggunakan higher-order function filter_data().
- Menampilkan papan peringkat (ranking) mahasiswa berdasarkan nilai tertinggi.
- Menghitung rata-rata nilai kelas menggunakan hitung_rata_rata().
- Menghitung persentase kelulusan kelas menggunakan hitung_persentase().
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

# Akun Demo Nilai Mahasiswa
USERS_NILAI = {
    "dosen": "12345",
    "mahasiswa": "12345",
    "admin": "admin123",
}

# Data Awal Nilai Mahasiswa
DATA_NILAI = [
    {"nim": "220101", "nama": "Ahmad Fauzi", "tugas": 85, "uts": 80, "uas": 90},
    {"nim": "220102", "nama": "Bunga Citra", "tugas": 75, "uts": 70, "uas": 78},
    {"nim": "220103", "nama": "Citra Lestari", "tugas": 90, "uts": 88, "uas": 92},
    {"nim": "220104", "nama": "Dimas Pratama", "tugas": 60, "uts": 55, "uas": 65},
    {"nim": "220105", "nama": "Eka Saputra", "tugas": 45, "uts": 50, "uas": 40},
]


def hitung_nilai_akhir(mhs):
    """
    Pure function: menghitung nilai akhir dengan bobot:
    Tugas 30%, UTS 30%, UAS 40%.
    """
    tugas = mhs.get("tugas", 0)
    uts = mhs.get("uts", 0)
    uas = mhs.get("uas", 0)
    return round((0.30 * tugas) + (0.30 * uts) + (0.40 * uas), 2)


def tentukan_grade(nilai_akhir):
    """Pure function: konversi nilai numerik ke grade huruf."""
    if nilai_akhir >= 85:
        return "A"
    elif nilai_akhir >= 75:
        return "B"
    elif nilai_akhir >= 60:
        return "C"
    elif nilai_akhir >= 50:
        return "D"
    return "E"


def tentukan_status(nilai_akhir):
    """Pure function: menentukan status kelulusan (standar >= 60.0)."""
    return "Lulus" if nilai_akhir >= 60.0 else "Tidak Lulus"


def transform_data_lengkap(mhs):
    """Pure function: menghasilkan dictionary representasi nilai yang lengkap."""
    akhir = hitung_nilai_akhir(mhs)
    return {
        "nim": mhs["nim"],
        "nama": mhs["nama"],
        "tugas": mhs["tugas"],
        "uts": mhs["uts"],
        "uas": mhs["uas"],
        "akhir": akhir,
        "grade": tentukan_grade(akhir),
        "status": tentukan_status(akhir),
    }


def tampilkan_tabel_nilai(daftar_mhs):
    """Menampilkan tabel nilai mahasiswa secara rapi."""
    print("\n" + "=" * 80)
    print(f"{'NIM':<8} | {'NAMA MAHASISWA':<22} | {'TGS':>4} | {'UTS':>4} | {'UAS':>4} | {'AKHIR':>6} | {'GRD':^4} | {'STATUS':<11}")
    print("-" * 80)
    for m in daftar_mhs:
        item = transform_data_lengkap(m)
        print(
            f"{item['nim']:<8} | {item['nama']:<22} | {item['tugas']:>4} | "
            f"{item['uts']:>4} | {item['uas']:>4} | {item['akhir']:>6.2f} | "
            f"{item['grade']:^4} | {item['status']:<11}"
        )
    print("=" * 80)


def cari_mahasiswa_nilai(data):
    """Mencari mahasiswa berdasarkan NIM atau Nama menggunakan cari_data()."""
    print("\nPilihan Pencarian Mahasiswa:")
    print("1. Berdasarkan NIM")
    print("2. Berdasarkan Nama")
    opsi = input("Pilih (1/2): ").strip()

    if opsi == "1":
        nim = input("Masukkan NIM: ").strip()
        # MENGGUNAKAN fplib.cari_data()
        hasil = cari_data(data, nim, "nim")
    elif opsi == "2":
        nama = input("Masukkan Nama: ").strip()
        # MENGGUNAKAN fplib.cari_data()
        hasil = cari_data(data, nama, "nama")
    else:
        print("[!] Pilihan tidak valid.")
        return

    if hasil:
        print(f"\n[+] Ditemukan {len(hasil)} mahasiswa:")
        tampilkan_tabel_nilai(hasil)
    else:
        print("[-] Mahasiswa tidak ditemukan.")


def input_nilai_mahasiswa(data):
    """Menginput atau memperbarui nilai mahasiswa."""
    print("\n--- Input / Perbarui Nilai Mahasiswa ---")
    nim = input("Masukkan NIM Mahasiswa: ").strip()

    # MENGGUNAKAN fplib.cari_data()
    mhs_list = cari_data(data, nim, "nim")
    if not mhs_list:
        print(f"[-] Mahasiswa dengan NIM '{nim}' tidak ditemukan.")
        return

    # Ambil referensi objek mahasiswa yang cocok
    target = next((m for m in data if m["nim"] == mhs_list[0]["nim"]), None)
    if not target:
        return

    print(f"Mahasiswa ditemukan: {target['nama']} (NIM: {target['nim']})")
    print(f"Nilai saat ini: Tugas={target['tugas']}, UTS={target['uts']}, UAS={target['uas']}")

    try:
        tugas_in = input("Nilai Tugas Baru (0-100): ").strip()
        uts_in = input("Nilai UTS Baru (0-100): ").strip()
        uas_in = input("Nilai UAS Baru (0-100): ").strip()

        tugas = float(tugas_in)
        uts = float(uts_in)
        uas = float(uas_in)

        if not (0 <= tugas <= 100 and 0 <= uts <= 100 and 0 <= uas <= 100):
            print("[!] Nilai harus berada dalam rentang 0 sampai 100.")
            return

        target["tugas"] = tugas
        target["uts"] = uts
        target["uas"] = uas

        akhir = hitung_nilai_akhir(target)
        grade = tentukan_grade(akhir)
        status = tentukan_status(akhir)
        print(f"\n[+] Nilai berhasil diperbarui!")
        print(f"    Nilai Akhir: {akhir} | Grade: {grade} | Status: {status}")

    except ValueError:
        print("[!] Harap masukkan nilai angka yang valid.")


def filter_kelulusan_mahasiswa(data):
    """Menyaring mahasiswa berdasarkan status kelulusan menggunakan filter_data()."""
    print("\n--- Filter Kelulusan Mahasiswa ---")
    print("1. Mahasiswa LULUS (Nilai Akhir >= 60)")
    print("2. Mahasiswa TIDAK LULUS (Nilai Akhir < 60)")
    opsi = input("Pilih (1/2): ").strip()

    if opsi == "1":
        # MENGGUNAKAN fplib.filter_data() dengan lambda higher-order
        lulus = filter_data(data, lambda m: hitung_nilai_akhir(m) >= 60.0)
        print(f"\n[ Daftar Mahasiswa LULUS ({len(lulus)} orang) ]")
        if lulus:
            tampilkan_tabel_nilai(lulus)
        else:
            print(">> Tidak ada mahasiswa yang lulus.")

    elif opsi == "2":
        # MENGGUNAKAN fplib.filter_data()
        tidak_lulus = filter_data(data, lambda m: hitung_nilai_akhir(m) < 60.0)
        print(f"\n[ Daftar Mahasiswa TIDAK LULUS ({len(tidak_lulus)} orang) ]")
        if tidak_lulus:
            tampilkan_tabel_nilai(tidak_lulus)
        else:
            print(">> Hebat! Tidak ada mahasiswa yang tidak lulus.")

    else:
        print("[!] Pilihan tidak valid.")


def peringkat_mahasiswa(data):
    """Menampilkan peringkat mahasiswa secara deklaratif terurut descending."""
    # Pendekatan fungsional: sorted() tidak mengubah data asli
    urutan = sorted(data, key=lambda m: hitung_nilai_akhir(m), reverse=True)

    print("\n" + "=" * 65)
    print("               PAPAN PERINGKAT NILAI MAHASISWA")
    print("=" * 65)
    print(f"{'RANK':<5} | {'NIM':<8} | {'NAMA MAHASISWA':<22} | {'AKHIR':>6} | {'GRADE':^5}")
    print("-" * 65)
    for rank, m in enumerate(urutan, 1):
        akhir = hitung_nilai_akhir(m)
        grade = tentukan_grade(akhir)
        print(f"{rank:<5} | {m['nim']:<8} | {m['nama']:<22} | {akhir:>6.2f} | {grade:^5}")
    print("=" * 65 + "\n")


def statistik_kelas(data):
    """Menghitung statistik kelas: rata-rata nilai kelas dan persentase kelulusan."""
    if not data:
        print(">> Data mahasiswa kosong.")
        return

    # List nilai akhir
    semua_nilai_akhir = [hitung_nilai_akhir(m) for m in data]

    # MENGGUNAKAN fplib.hitung_rata_rata()
    rata_kelas = hitung_rata_rata(semua_nilai_akhir)

    # Filter mahasiswa yang lulus
    # MENGGUNAKAN fplib.filter_data()
    mhs_lulus = filter_data(data, lambda m: hitung_nilai_akhir(m) >= 60.0)

    # MENGGUNAKAN fplib.hitung_persentase()
    persen_lulus = hitung_persentase(len(mhs_lulus), len(data))
    persen_gagal = hitung_persentase(len(data) - len(mhs_lulus), len(data))

    print("\n" + "=" * 55)
    print("               STATISTIK NILAI KELAS")
    print("=" * 55)
    print(f"Total Mahasiswa        : {len(data)} orang")
    print(f"Rata-rata Nilai Kelas  : {rata_kelas}")
    print(f"Jumlah Mahasiswa Lulus : {len(mhs_lulus)} orang ({persen_lulus}%)")
    print(f"Jumlah Tidak Lulus     : {len(data) - len(mhs_lulus)} orang ({persen_gagal}%)")
    print("=" * 55)


def menu_nilai():
    """Menu utama aplikasi Nilai Mahasiswa."""
    data_nilai = copy.deepcopy(DATA_NILAI)

    while True:
        print("\n" + "=" * 45)
        print("          SISTEM NILAI MAHASISWA")
        print("=" * 45)
        print("1. Tampilkan Daftar Seluruh Nilai")
        print("2. Cari Mahasiswa (NIM / Nama)")
        print("3. Input / Perbarui Nilai Mahasiswa")
        print("4. Filter Mahasiswa (Lulus / Tidak Lulus)")
        print("5. Papan Peringkat (Ranking)")
        print("6. Statistik Nilai & Kelulusan Kelas")
        print("0. Keluar / Kembali ke Menu Utama")
        print("=" * 45)

        pilihan = input("Pilih menu (0-6): ").strip()

        if pilihan == "1":
            tampilkan_tabel_nilai(data_nilai)
        elif pilihan == "2":
            cari_mahasiswa_nilai(data_nilai)
        elif pilihan == "3":
            input_nilai_mahasiswa(data_nilai)
        elif pilihan == "4":
            filter_kelulusan_mahasiswa(data_nilai)
        elif pilihan == "5":
            peringkat_mahasiswa(data_nilai)
        elif pilihan == "6":
            statistik_kelas(data_nilai)
        elif pilihan == "0":
            print(">> Keluar dari Aplikasi Nilai Mahasiswa.")
            break
        else:
            print("[!] Pilihan tidak valid. Silakan masukkan angka 0-6.")


def jalankan_nilai():
    """Titik masuk utama aplikasi Nilai Mahasiswa dengan otentikasi mandiri."""
    print("\n" + "#" * 50)
    print("      SELAMAT DATANG DI NILAI MAHASISWA")
    print("#" * 50)
    print("Akun Demo: dosen / 12345 (atau mahasiswa / 12345)")

    maks_percobaan = 3
    percobaan = 0

    while percobaan < maks_percobaan:
        username = input("Username : ").strip()
        password = input("Password : ").strip()

        # MENGGUNAKAN fplib.autentikasi()
        if autentikasi(username, password, USERS_NILAI):
            print(f"\n[+] Login Berhasil! Selamat datang, {username}.\n")
            menu_nilai()
            return
        else:
            percobaan += 1
            sisa = maks_percobaan - percobaan
            print(f"[-] Login Gagal! Username atau password salah. (Sisa percobaan: {sisa})")

    print("[!] Batas maksimal percobaan login tercapai. Kembali ke menu utama.")


if __name__ == "__main__":
    jalankan_nilai()
