"""
fplib.py - Library Pemrograman Fungsional Python
=================================================
Mata Kuliah : Pemrograman Fungsional
Deskripsi   : Kumpulan fungsi umum murni (pure functions) dengan pendekatan
              fungsional yang dapat digunakan kembali (reusable) oleh
              berbagai aplikasi.

Prinsip Pemrograman Fungsional yang diterapkan:
1. Pure Function:
   - Output semata-mata bergantung pada argumen input.
   - Tidak menghasilkan side-effect (tidak ada print/input/akses mutasi global).
2. Immutability:
   - Tidak memodifikasi struktur data (list/dict) asli.
   - Mengembalikan data baru atau salinan hasil transformasi.
3. Higher-Order Function:
   - Menerima fungsi sebagai argumen (contoh: filter_data).
4. Declarative Programming:
   - Menggunakan abstraksi bawaan seperti sum, filter, list comprehension.
"""

from typing import Any, Callable, Dict, Iterable, List, Optional, Union


def autentikasi(
    username: str,
    password: str,
    users: Union[Dict[str, Any], List[Dict[str, Any]]]
) -> bool:
    """
    Memeriksa kecocokan username dan password pada koleksi data pengguna.

    Parameter:
        username (str): Username yang dimasukkan pengguna.
        password (str): Password yang dimasukkan pengguna.
        users (dict | list): Koleksi pengguna dalam bentuk:
            - Dict sederhana: {"user": "pass"}
            - Dict detail: {"user": {"password": "pass", ...}}
            - List of dict: [{"username": "user", "password": "pass", ...}]

    Return:
        bool: True jika cocok, False jika tidak cocok atau input tidak valid.

    Karakteristik FP:
        - Pure Function: Tidak ada I/O (print/input), deterministik.
        - Immutability: Tidak mengubah objek users.
    """
    if not username or not password or not users:
        return False

    u_str = str(username).strip()
    p_str = str(password).strip()

    if isinstance(users, dict):
        user_val = users.get(u_str)
        if user_val is None:
            return False
        if isinstance(user_val, dict):
            return str(user_val.get("password", "")).strip() == p_str
        return str(user_val).strip() == p_str

    if isinstance(users, (list, tuple)):
        return any(
            isinstance(u, dict)
            and str(u.get("username", "")).strip() == u_str
            and str(u.get("password", "")).strip() == p_str
            for u in users
        )

    return False


def cari_data(
    data: Iterable[Dict[str, Any]],
    kata_kunci: Any,
    key: str
) -> List[Dict[str, Any]]:
    """
    Mencari data berdasarkan kata kunci pada atribut tertentu (key).

    Parameter:
        data (iterable of dict): Kumpulan data yang akan dicari.
        kata_kunci (any): Kata kunci pencarian (case-insensitive).
        key (str): Nama atribut/kunci pada dictionary.

    Return:
        list: List baru berisi elemen yang memenuhi kriteria pencarian.

    Karakteristik FP:
        - Pure Function: Menghasilkan list baru tanpa mengubah data asal.
        - Declarative: Menggunakan list comprehension.
    """
    if data is None or kata_kunci is None or key is None:
        return []

    keyword_str = str(kata_kunci).strip().lower()

    # List comprehension murni - tidak ada efek samping pada list asli
    return [
        item for item in data
        if isinstance(item, dict) and keyword_str in str(item.get(key, "")).lower()
    ]


def hitung_total(data: Iterable[Union[int, float]]) -> Union[int, float]:
    """
    Menghitung jumlah keseluruhan nilai numerik dalam kumpulan data.

    Parameter:
        data (iterable): Kumpulan angka (int atau float).

    Return:
        int | float: Total nilai numerik. Mengembalikan 0 jika data kosong.

    Karakteristik FP:
        - Pure Function & Declarative: Menggunakan built-in sum() yang ringkas
          dan bebas efek samping.
    """
    if not data:
        return 0

    try:
        # Pendekatan fungsional deklaratif
        return sum(data)
    except TypeError:
        # Mengabaikan elemen non-numerik secara aman
        return sum(x for x in data if isinstance(x, (int, float)))


def hitung_rata_rata(data: Iterable[Union[int, float]]) -> float:
    """
    Menghitung rata-rata dari kumpulan angka dengan penanganan data kosong.

    Parameter:
        data (iterable): Kumpulan angka.

    Return:
        float: Nilai rata-rata dibulatkan 2 desimal. Mengembalikan 0.0 jika kosong.

    Karakteristik FP:
        - Pure Function: Menghindari ZeroDivisionError tanpa memodifikasi data.
    """
    if not data:
        return 0.0

    valid_numbers = [x for x in data if isinstance(x, (int, float))]
    if not valid_numbers:
        return 0.0

    return round(sum(valid_numbers) / len(valid_numbers), 2)


def format_rupiah(nominal: Union[int, float, None]) -> str:
    """
    Mengubah angka numerik menjadi string berformat mata uang Rupiah standar.
    Contoh: 15000 -> "Rp15.000", 1500000 -> "Rp1.500.000".

    Parameter:
        nominal (int | float | None): Nilai yang akan diformat.

    Return:
        str: Representasi string dalam format Rupiah ("Rp...").

    Karakteristik FP:
        - Pure Function: Menghasilkan string baru tanpa mutasi nilai asli.
    """
    if nominal is None:
        return "Rp0"

    try:
        num = float(nominal)
    except (ValueError, TypeError):
        return "Rp0"

    is_negative = num < 0
    abs_int = int(round(abs(num)))
    # Format ribuan dengan titik sesuai standar Indonesia
    formatted = f"{abs_int:,}".replace(",", ".")

    if is_negative:
        return f"-Rp{formatted}"
    return f"Rp{formatted}"


def filter_data(
    data: Iterable[Any],
    kondisi: Callable[[Any], bool]
) -> List[Any]:
    """
    Higher-order function untuk menyaring data berdasarkan fungsi predikat.

    Parameter:
        data (iterable): Kumpulan data yang akan difilter.
        kondisi (callable): Fungsi predikat yang menerima satu elemen
                            dan mengembalikan True atau False.

    Return:
        list: List baru berisi data yang memenuhi kondisi.

    Karakteristik FP:
        - Higher-Order Function: Menerima fungsi (kondisi) sebagai parameter.
        - Immutability: Mengembalikan list baru tanpa mengubah data input.
    """
    if not data:
        return []

    if not callable(kondisi):
        return list(data)

    # Menggunakan fungsi bawaan filter() bergaya fungsional
    return list(filter(kondisi, data))


def hitung_persentase(
    nilai: Union[int, float],
    total: Union[int, float]
) -> float:
    """
    Menghitung persentase suatu nilai terhadap total secara aman.

    Parameter:
        nilai (int | float): Nilai bagian.
        total (int | float): Nilai total keseluruhan.

    Return:
        float: Persentase (0-100) dibulatkan 2 desimal.
               Mengembalikan 0.0 jika total <= 0 atau pembagian dengan nol.

    Karakteristik FP:
        - Pure Function: Penanganan pembagian dengan nol yang aman.
    """
    if not total or total <= 0:
        return 0.0

    try:
        hasil = (float(nilai) / float(total)) * 100.0
        return round(hasil, 2)
    except (ZeroDivisionError, ValueError, TypeError):
        return 0.0
