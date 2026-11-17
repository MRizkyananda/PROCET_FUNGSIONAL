"""
test_fplib.py - Unit Test untuk fplib.py
========================================
Pengujian komprehensif terhadap seluruh fungsi murni pada library fplib.py.
Mencakup pengujian fungsionalitas, edge cases, penanganan input tidak valid,
dan verifikasi prinsip immutability.
"""

import copy
import os
import sys
import unittest

# Menambahkan direktori project root ke sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fplib import (
    autentikasi,
    cari_data,
    hitung_total,
    hitung_rata_rata,
    format_rupiah,
    filter_data,
    hitung_persentase,
)


class TestFpLib(unittest.TestCase):

    # =========================================================================
    # 1. PENGUJIAN autentikasi()
    # =========================================================================
    def test_autentikasi_dict_sederhana_berhasil(self):
        users = {"kasir": "12345", "admin": "admin123"}
        self.assertTrue(autentikasi("kasir", "12345", users))
        self.assertTrue(autentikasi("admin", "admin123", users))

    def test_autentikasi_dict_detail_berhasil(self):
        users = {
            "dosen": {"password": "secret", "nama": "Dr. Dosen"},
            "mahasiswa": {"password": "mhs123", "nama": "Ahmad"},
        }
        self.assertTrue(autentikasi("dosen", "secret", users))
        self.assertTrue(autentikasi("mahasiswa", "mhs123", users))

    def test_autentikasi_list_dict_berhasil(self):
        users = [
            {"username": "anggota", "password": "12345", "role": "member"},
            {"username": "petugas", "password": "perpustakaan", "role": "staff"},
        ]
        self.assertTrue(autentikasi("anggota", "12345", users))
        self.assertTrue(autentikasi("petugas", "perpustakaan", users))

    def test_autentikasi_gagal_password_salah(self):
        users = {"kasir": "12345"}
        self.assertFalse(autentikasi("kasir", "salah_password", users))

    def test_autentikasi_gagal_username_tidak_ada(self):
        users = {"kasir": "12345"}
        self.assertFalse(autentikasi("hacker", "12345", users))

    def test_autentikasi_input_kosong_atau_none(self):
        users = {"kasir": "12345"}
        self.assertFalse(autentikasi("", "12345", users))
        self.assertFalse(autentikasi("kasir", "", users))
        self.assertFalse(autentikasi(None, "12345", users))
        self.assertFalse(autentikasi("kasir", None, users))
        self.assertFalse(autentikasi("kasir", "12345", {}))
        self.assertFalse(autentikasi("kasir", "12345", None))

    def test_autentikasi_immutability(self):
        users = {"kasir": "12345"}
        users_copy = copy.deepcopy(users)
        autentikasi("kasir", "12345", users)
        autentikasi("hacker", "wrong", users)
        self.assertEqual(users, users_copy, "Data users tidak boleh termutasi")

    # =========================================================================
    # 2. PENGUJIAN cari_data()
    # =========================================================================
    def setUp(self):
        self.sample_buku = [
            {"id": "B01", "judul": "Pemrograman Python Modern", "pengarang": "Rian"},
            {"id": "B02", "judul": "Struktur Data & Algoritma", "pengarang": "Siti"},
            {"id": "B03", "judul": "Prinsip Pemrograman Fungsional", "pengarang": "Budi"},
        ]

    def test_cari_data_berhasil(self):
        hasil = cari_data(self.sample_buku, "python", "judul")
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]["id"], "B01")

    def test_cari_data_case_insensitive(self):
        hasil_upper = cari_data(self.sample_buku, "FUNGSIONAL", "judul")
        hasil_lower = cari_data(self.sample_buku, "fungsional", "judul")
        self.assertEqual(hasil_upper, hasil_lower)
        self.assertEqual(len(hasil_upper), 1)

    def test_cari_data_multiple_matches(self):
        hasil = cari_data(self.sample_buku, "Pemrograman", "judul")
        self.assertEqual(len(hasil), 2)

    def test_cari_data_tidak_ditemukan(self):
        hasil = cari_data(self.sample_buku, "Kalkulus", "judul")
        self.assertEqual(hasil, [])

    def test_cari_data_key_tidak_ada(self):
        hasil = cari_data(self.sample_buku, "Python", "kategori_nonexistent")
        self.assertEqual(hasil, [])

    def test_cari_data_edge_cases(self):
        self.assertEqual(cari_data([], "Python", "judul"), [])
        self.assertEqual(cari_data(None, "Python", "judul"), [])
        self.assertEqual(cari_data(self.sample_buku, None, "judul"), [])
        self.assertEqual(cari_data(self.sample_buku, "Python", None), [])

    def test_cari_data_immutability(self):
        original = copy.deepcopy(self.sample_buku)
        hasil = cari_data(self.sample_buku, "Python", "judul")
        self.assertEqual(self.sample_buku, original, "Data asli tidak boleh berubah")
        self.assertIsNot(hasil, self.sample_buku, "Hasil harus berupa list baru")

    # =========================================================================
    # 3. PENGUJIAN hitung_total()
    # =========================================================================
    def test_hitung_total_bilangan_bulat(self):
        angka = [15000, 25000, 10000]
        self.assertEqual(hitung_total(angka), 50000)

    def test_hitung_total_bilangan_desimal(self):
        angka = [10.5, 20.25, 4.25]
        self.assertAlmostEqual(hitung_total(angka), 35.0)

    def test_hitung_total_negatif(self):
        angka = [1000, -300, 500]
        self.assertEqual(hitung_total(angka), 1200)

    def test_hitung_total_kosong(self):
        self.assertEqual(hitung_total([]), 0)
        self.assertEqual(hitung_total(()), 0)
        self.assertEqual(hitung_total(None), 0)

    def test_hitung_total_immutability(self):
        angka = [5000, 15000, 20000]
        angka_copy = list(angka)
        hitung_total(angka)
        self.assertEqual(angka, angka_copy, "Koleksi data asli tidak boleh termutasi")

    # =========================================================================
    # 4. PENGUJIAN hitung_rata_rata()
    # =========================================================================
    def test_hitung_rata_rata_normal(self):
        nilai = [80, 90, 70]
        self.assertEqual(hitung_rata_rata(nilai), 80.0)

    def test_hitung_rata_rata_pembulatan(self):
        nilai = [10, 20, 25]  # total = 55 / 3 = 18.333...
        self.assertEqual(hitung_rata_rata(nilai), 18.33)

    def test_hitung_rata_rata_satu_elemen(self):
        self.assertEqual(hitung_rata_rata([95]), 95.0)

    def test_hitung_rata_rata_kosong_tanpa_zerodivision(self):
        # Harus mengembalikan 0.0 tanpa melempar Exception
        self.assertEqual(hitung_rata_rata([]), 0.0)
        self.assertEqual(hitung_rata_rata(None), 0.0)

    def test_hitung_rata_rata_immutability(self):
        nilai = [85, 90, 75]
        nilai_copy = list(nilai)
        hitung_rata_rata(nilai)
        self.assertEqual(nilai, nilai_copy)

    # =========================================================================
    # 5. PENGUJIAN format_rupiah()
    # =========================================================================
    def test_format_rupiah_standar(self):
        self.assertEqual(format_rupiah(15000), "Rp15.000")
        self.assertEqual(format_rupiah(1500000), "Rp1.500.000")
        self.assertEqual(format_rupiah(750), "Rp750")

    def test_format_rupiah_nol(self):
        self.assertEqual(format_rupiah(0), "Rp0")

    def test_format_rupiah_negatif(self):
        self.assertEqual(format_rupiah(-25000), "-Rp25.000")

    def test_format_rupiah_float(self):
        self.assertEqual(format_rupiah(15000.4), "Rp15.000")
        self.assertEqual(format_rupiah(15000.8), "Rp15.001")

    def test_format_rupiah_invalid_input(self):
        self.assertEqual(format_rupiah(None), "Rp0")
        self.assertEqual(format_rupiah("tidak_valid"), "Rp0")

    # =========================================================================
    # 6. PENGUJIAN filter_data()
    # =========================================================================
    def test_filter_data_higher_order(self):
        transaksi = [
            {"tipe": "Pemasukan", "nominal": 500000},
            {"tipe": "Pengeluaran", "nominal": 150000},
            {"tipe": "Pemasukan", "nominal": 200000},
        ]
        # Predikat menggunakan lambda murni
        pemasukan = filter_data(transaksi, lambda t: t["tipe"] == "Pemasukan")
        self.assertEqual(len(pemasukan), 2)
        self.assertTrue(all(t["tipe"] == "Pemasukan" for t in pemasukan))

    def test_filter_data_tidak_ada_yang_cocok(self):
        angka = [1, 3, 5, 7]
        genap = filter_data(angka, lambda x: x % 2 == 0)
        self.assertEqual(genap, [])

    def test_filter_data_kosong_dan_invalid(self):
        self.assertEqual(filter_data([], lambda x: True), [])
        self.assertEqual(filter_data([1, 2, 3], None), [1, 2, 3])

    def test_filter_data_immutability(self):
        data = [10, 20, 30, 40]
        data_copy = list(data)
        hasil = filter_data(data, lambda x: x > 25)
        self.assertEqual(data, data_copy, "Data asli tidak boleh termutasi")
        self.assertIsNot(hasil, data, "Hasil harus list baru")
        self.assertEqual(hasil, [30, 40])

    # =========================================================================
    # 7. PENGUJIAN hitung_persentase()
    # =========================================================================
    def test_hitung_persentase_normal(self):
        self.assertEqual(hitung_persentase(50, 200), 25.0)
        self.assertEqual(hitung_persentase(100, 100), 100.0)
        self.assertEqual(hitung_persentase(1, 3), 33.33)

    def test_hitung_persentase_pembagian_nol_aman(self):
        # Harus mengembalikan 0.0 tanpa ZeroDivisionError
        self.assertEqual(hitung_persentase(50, 0), 0.0)
        self.assertEqual(hitung_persentase(0, 0), 0.0)

    def test_hitung_persentase_input_negatif_atau_kosong(self):
        self.assertEqual(hitung_persentase(10, -50), 0.0)
        self.assertEqual(hitung_persentase(None, 100), 0.0)
        self.assertEqual(hitung_persentase(50, None), 0.0)


if __name__ == "__main__":
    unittest.main()
