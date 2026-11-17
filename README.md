# PROJECT TUGAS BESAR PEMROGRAMAN FUNGSIONAL PYTHON
## Satu Library, Lima Aplikasi (`fplib.py`)

Proyek ini dibangun untuk memenuhi tugas besar mata kuliah **Pemrograman Fungsional**. Inti dari proyek ini adalah arsitektur modular yang berpusat pada satu library buatan sendiri bernama `fplib.py`. Library ini menyediakan fungsi-fungsi umum murni bergaya pemrograman fungsional (*functional programming*) yang digunakan kembali (*reusable*) oleh lima aplikasi konsol (CLI) yang berbeda.

---

## 1. Deskripsi & Tujuan Project

### Deskripsi
Proyek ini mengintegrasikan lima aplikasi berbasis terminal ke dalam satu repositori dengan fondasi fungsional bersama. Kelima aplikasi tersebut mencakup domain kasir ritel, administrasi perkuliahan, manajemen perpustakaan, pencatatan finansial personal, hingga pengolahan nilai akademik.

### Tujuan Pembuatan Library `fplib.py`
1. **Pemisahan Logika & Tampilan (Separation of Concerns)**: Memisahkan komputasi data murni ke dalam library independen tanpa tercampur dengan operasi input/output (I/O).
2. **Reusabilitas Kode (Code Reusability)**: Mencegah duplikasi fungsi logika yang sering dipakai ulang oleh berbagai modul aplikasi.
3. **Penerapan Prinsip Fungsional**: Memastikan fungsi bersifat deterministik (*pure functions*), tidak menghasilkan efek samping (*side-effects*), serta menjamin integritas data melalui *immutability*.

---

## 2. Struktur Folder Project

```text
project_pemrograman_fungsional/
│
├── fplib.py               # Library utama fungsi-fungsi fungsional murni
├── main.py                # Titik masuk utama / pusat navigasi aplikasi
├── README.md              # Dokumentasi lengkap proyek
├── requirements.txt       # Daftar dependensi Python
│
├── apps/                  # Direktori lima aplikasi mandiri
│   ├── __init__.py
│   ├── kasir_kantin.py    # Aplikasi 1: Kasir Kantin
│   ├── presensi_kelas.py  # Aplikasi 2: Presensi Kelas
│   ├── perpustakaan.py    # Aplikasi 3: Perpustakaan Mini
│   ├── keuangan_pribadi.py# Aplikasi 4: Keuangan Pribadi
│   └── nilai_mahasiswa.py # Aplikasi 5: Nilai Mahasiswa
│
└── tests/                 # Unit testing
    ├── __init__.py
    └── test_fplib.py      # Pengujian komprehensif fplib.py
```

---

## 3. Matriks Pemetaan Fungsi Library ke Aplikasi

Setiap fungsi di dalam `fplib.py` digunakan oleh minimal 3 aplikasi dan maksimal 5 aplikasi. Berikut adalah tabel pemetaan aktual:

| Fungsi | Kasir Kantin | Presensi Kelas | Perpustakaan | Keuangan Pribadi | Nilai Mahasiswa | Total Pemakaian |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `autentikasi` | ✓ | ✓ | ✓ | ✓ | ✓ | 5 |
| `cari_data` | - | ✓ | ✓ | - | ✓ | 3 |
| `hitung_total` | ✓ | - | ✓ | ✓ | - | 3 |
| `hitung_rata_rata` | - | ✓ | - | ✓ | ✓ | 3 |
| `format_rupiah` | ✓ | - | ✓ | ✓ | - | 3 |
| `filter_data` | ✓ | ✓ | - | - | ✓ | 3 |
| `hitung_persentase` | - | ✓ | - | ✓ | ✓ | 3 |

---

## 4. Penjelasan Setiap Fungsi di `fplib.py`

### 1. `autentikasi(username, password, users)`
- **Deskripsi**: Memeriksa kecocokan identitas pengguna (username dan password) terhadap kumpulan data pengguna.
- **Karakteristik FP**: Pure function tanpa efek samping (tidak ada `print` maupun `input`). Menangani dictionary sederhana, dictionary bersarang, maupun list of dictionaries secara aman.
- **Digunakan oleh**: Seluruh 5 aplikasi (Kasir, Presensi, Perpustakaan, Keuangan, Nilai).

### 2. `cari_data(data, kata_kunci, key)`
- **Deskripsi**: Mencari elemen data berdasarkan pencocokan substring kata kunci pada atribut/kunci tertentu secara *case-insensitive*.
- **Karakteristik FP**: Mengembalikan koleksi baru tanpa merusak list atau dictionary sumber (*immutability*).
- **Digunakan oleh**: Presensi Kelas, Perpustakaan Mini, Nilai Mahasiswa.

### 3. `hitung_total(data)`
- **Deskripsi**: Menjumlahkan keseluruhan nilai numerik dalam koleksi data.
- **Karakteristik FP**: Menerapkan pendekatan deklaratif menggunakan fungsi bawaan `sum()`, aman dari data kosong (mengembalikan 0).
- **Digunakan oleh**: Kasir Kantin, Perpustakaan Mini, Keuangan Pribadi.

### 4. `hitung_rata_rata(data)`
- **Deskripsi**: Menghitung nilai rata-rata dari kumpulan angka dan membulatkannya ke 2 angka di belakang koma.
- **Karakteristik FP**: Pure function yang aman dari pembagian dengan nol (*ZeroDivisionError*) saat list kosong (mengembalikan `0.0`).
- **Digunakan oleh**: Presensi Kelas, Keuangan Pribadi, Nilai Mahasiswa.

### 5. `format_rupiah(nominal)`
- **Deskripsi**: Mengonversi nilai numerik (int/float) menjadi representasi string berformat mata uang Rupiah Indonesia (contoh: `15000` $\rightarrow$ `"Rp15.000"`).
- **Karakteristik FP**: Pure function tanpa mutasi angka sumber, menangani angka negatif dan nilai desimal.
- **Digunakan oleh**: Kasir Kantin, Perpustakaan Mini, Keuangan Pribadi.

### 6. `filter_data(data, kondisi)`
- **Deskripsi**: Menyaring sekumpulan elemen data berdasarkan fungsi predikat yang diberikan.
- **Karakteristik FP**: Merupakan *Higher-Order Function* yang menerima parameter fungsi (`kondisi`). Menghasilkan list baru secara murni tanpa memodifikasi list input.
- **Digunakan oleh**: Kasir Kantin, Presensi Kelas, Nilai Mahasiswa.

### 7. `hitung_persentase(nilai, total)`
- **Deskripsi**: Menghitung proporsi persentase suatu nilai terhadap total (skala 0 - 100%).
- **Karakteristik FP**: Pure function dengan pengamanan bawaan terhadap pembagian dengan nol (*zero division safe*).
- **Digunakan oleh**: Presensi Kelas, Keuangan Pribadi, Nilai Mahasiswa.

---

## 5. Penjelasan Lima Aplikasi

### Aplikasi 1: Kasir Kantin (`apps/kasir_kantin.py`)
- **Peran**: Sistem penjualan kantin berbasis terminal.
- **Fitur Utama**:
  - Login mandiri kasir.
  - Tampilkan seluruh menu makanan dan minuman.
  - Filter menu berdasarkan kategori (Makanan vs Minuman) dengan `filter_data()`.
  - Keranjang belanja interaktif dengan input kuantitas.
  - Perhitungan diskon otomatis 10% jika transaksi $\ge$ Rp50.000.
  - Perhitungan total transaksi menggunakan `hitung_total()`.
  - Format mata uang dan kembalian menggunakan `format_rupiah()`.
  - Cetak struk transaksi pembayaran.

### Aplikasi 2: Presensi Kelas (`apps/presensi_kelas.py`)
- **Peran**: Sistem pencatatan kehadiran mahasiswa di ruang kelas.
- **Fitur Utama**:
  - Login mandiri mahasiswa / admin.
  - Tampilkan daftar mahasiswa beserta riwayat kehadiran (Hadir, Izin, Sakit, Alfa).
  - Pencarian mahasiswa berdasarkan NIM atau Nama menggunakan `cari_data()`.
  - Pencatatan kehadiran pertemuan baru.
  - Filter mahasiswa dengan kehadiran kurang disiplin (< 75%) atau pernah alfa menggunakan `filter_data()`.
  - Hitung persentase kehadiran per mahasiswa dengan `hitung_persentase()`.
  - Hitung rata-rata kehadiran kelas dengan `hitung_rata_rata()`.

### Aplikasi 3: Perpustakaan Mini (`apps/perpustakaan.py`)
- **Peran**: Sistem peminjaman dan pengelolaan denda buku perpustakaan.
- **Fitur Utama**:
  - Login anggota atau petugas perpustakaan.
  - Tampilkan katalog buku beserta ketersediaan stok.
  - Cari judul buku secara *case-insensitive* dengan `cari_data()`.
  - Transaksi peminjaman buku dengan batas waktu peminjaman.
  - Pengembalian buku dan kalkulasi denda keterlambatan (Rp2.000 / hari terlambat).
  - Hitung total akumulasi denda perpustakaan menggunakan `hitung_total()`.
  - Tampilkan bukti denda dan rincian transaksi dengan `format_rupiah()`.

### Aplikasi 4: Keuangan Pribadi (`apps/keuangan_pribadi.py`)
- **Peran**: Aplikasi pelacak arus kas keuangan personal.
- **Fitur Utama**:
  - Login pengguna personal.
  - Tampilkan riwayat pemasukan dan pengeluaran.
  - Catat transaksi baru dengan kategori (Gaji, Makanan, Transportasi, dsb.).
  - Hitung total pemasukan dan total pengeluaran dengan `hitung_total()`.
  - Hitung sisa saldo (`total_pemasukan - total_pengeluaran`).
  - Hitung rata-rata pengeluaran per transaksi dengan `hitung_rata_rata()`.
  - Analisis persentase alokasi pengeluaran per kategori dengan `hitung_persentase()`.
  - Format seluruh nilai finansial dengan `format_rupiah()`.

### Aplikasi 5: Nilai Mahasiswa (`apps/nilai_mahasiswa.py`)
- **Peran**: Sistem pengolahan nilai akademik perkuliahan.
- **Fitur Utama**:
  - Login dosen pengampu.
  - Tampilkan tabel nilai lengkap (Tugas 30%, UTS 30%, UAS 40%, Nilai Akhir, Grade, Status).
  - Cari mahasiswa berdasarkan NIM atau Nama menggunakan `cari_data()`.
  - Input atau perbarui komponen nilai mahasiswa.
  - Filter mahasiswa Lulus (nilai $\ge$ 60) vs Tidak Lulus dengan `filter_data()`.
  - Urutkan peringkat (*ranking*) mahasiswa tertinggi ke terendah secara fungsional.
  - Hitung rata-rata nilai kelas dengan `hitung_rata_rata()`.
  - Hitung persentase kelulusan kelas dengan `hitung_persentase()`.

---

## 6. Penerapan Prinsip Pemrograman Fungsional

### 1. Pure Function (Fungsi Murni)
Setiap fungsi di dalam `fplib.py` tidak memiliki efek samping (*side-effects*):
- Tidak memanggil `print()` atau `input()`.
- Tidak melakukan akses modifikasi berkas (*file I/O*) atau variabel global.
- Menghasilkan output yang konsisten berdasarkan argumen input yang sama (*deterministik*).
- **Contoh pada `fplib.py`**:
  ```python
  def hitung_persentase(nilai, total):
      if not total or total <= 0:
          return 0.0
      return round((float(nilai) / float(total)) * 100.0, 2)
  ```

### 2. Immutability (Data Tidak Berubah)
Fungsi-fungsi tidak memodifikasi list atau dictionary asli yang dilewatkan sebagai argumen. Sebaliknya, dibuat koleksi baru atau salinan data saat transformasi dilakukan.
- **Contoh pada `fplib.py`**:
  ```python
  def cari_data(data, kata_kunci, key):
      keyword = str(kata_kunci).strip().lower()
      # Mengembalikan list baru tanpa mengubah data input asli
      return [
          item for item in data
          if isinstance(item, dict) and keyword in str(item.get(key, "")).lower()
      ]
  ```

### 3. Higher-Order Function (Fungsi Tingkat Tinggi)
Fungsi yang menerima fungsi lain sebagai argumen atau mengembalikan sebuah fungsi.
- **Contoh pada `fplib.py`**:
  `filter_data(data, kondisi)` menerima fungsi predikat `kondisi` untuk menyaring data:
  ```python
  def filter_data(data, kondisi):
      if not callable(kondisi):
          return list(data)
      return list(filter(kondisi, data))
  ```
- **Penerapan pada Aplikasi**:
  ```python
  # Lambda dilewatkan sebagai first-class citizen
  mahasiswa_lulus = filter_data(data, lambda m: hitung_nilai_akhir(m) >= 60.0)
  ```

### 4. Declarative Programming (Gaya Deklaratif)
Menyatakan *apa* hasil yang ingin dicapai daripada merinci langkah iteratif manual langkah demi langkah (*imperatif*). Mengoptimalkan fungsi bawaan Python seperti `sum()`, `filter()`, `map()`, serta *list comprehension*.
- **Contoh pada `fplib.py`**:
  ```python
  def hitung_total(data):
      if not data:
          return 0
      return sum(data)
  ```

---

## 7. Akun Demo untuk Login

Setiap aplikasi memiliki sistem autentikasi mandiri. Anda dapat menggunakan akun berikut untuk login:

| Aplikasi | Username Demo | Password Demo | Peran |
|---|---|---|---|
| **Kasir Kantin** | `kasir` | `12345` | Kasir Operasional |
| **Presensi Kelas** | `mahasiswa` | `12345` | Mahasiswa / Kelas |
| **Perpustakaan Mini** | `anggota` | `12345` | Anggota Perpustakaan |
| **Keuangan Pribadi** | `rizky` | `12345` | Pengguna Personal |
| **Nilai Mahasiswa** | `dosen` | `12345` | Dosen Pengampu |

---

## 8. Cara Instalasi & Menjalankan Project

### Prasyarat
- Python versi 3.8 atau lebih baru (direkomendasikan Python 3.10+).

### Langkah Menjalankan:
1. Buka terminal atau Command Prompt.
2. Navigasikan ke direktori project:
   ```bash
   cd project_pemrograman_fungsional
   ```
3. (Opsional) Pasang dependensi jika ingin menjalankan pengujian dengan pytest:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi utama:
   ```bash
   python main.py
   ```
   *(Atau di Windows: `py main.py`)*

### Menjalankan Unit Testing:
Untuk menguji seluruh fungsi di `fplib.py`:
```bash
python -m unittest tests/test_fplib.py -v
```
*(Atau: `py -m unittest discover -s tests -v`)*
