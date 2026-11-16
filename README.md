# Sistem Manajemen Perpustakaan

Aplikasi desktop untuk mengelola data buku dan anggota perpustakaan. Aplikasi dibuat dengan Python dan CustomTkinter, menggunakan MySQL untuk penyimpanan data, serta menerapkan pola Model-View-Controller (MVC).

## Struktur direktori

Kode aplikasi berada di direktori `modul 3`:

```text
modul 3/
|-- config/       # Konfigurasi dan koneksi database
|-- controller/   # Logika aplikasi dan penghubung model-view
|-- models/       # Akses data buku, anggota, dan pengguna
|-- views/        # Tampilan login dan halaman aplikasi
|-- tests/        # Pengujian autentikasi
|-- test/         # Pengujian model dan controller
|-- main.py       # Titik masuk aplikasi
`-- requirements.txt
```

## Instalasi dan konfigurasi

1. Pasang Python 3.11 atau lebih baru dan MySQL Server (misalnya melalui Laragon).
2. Buat database beserta tabel yang dipakai aplikasi:

   ```sql
   CREATE DATABASE perpustakaan;
   USE perpustakaan;

   CREATE TABLE buku (
       id_buku INT AUTO_INCREMENT PRIMARY KEY,
       judul VARCHAR(255) NOT NULL,
       penulis VARCHAR(255) NOT NULL,
       tahun_terbit SMALLINT NOT NULL
   );

   CREATE TABLE anggota (
       id_anggota INT AUTO_INCREMENT PRIMARY KEY,
       nama VARCHAR(255) NOT NULL,
       alamat TEXT
   );

   CREATE TABLE users (
       id_user INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(100) NOT NULL UNIQUE,
       password CHAR(64) NOT NULL,
       role VARCHAR(30) NOT NULL
   );
   ```

3. Buka terminal di root repositori lalu jalankan:

   ```powershell
   cd "modul 3"
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

4. Atur koneksi MySQL melalui environment variables berikut. Nilai di sebelah kanan adalah nilai default aplikasi.

   | Variabel | Default |
   | --- | --- |
   | `MYSQL_HOST` | `localhost` |
   | `MYSQL_USER` | `root` |
   | `MYSQL_PASSWORD` | kosong |
   | `MYSQL_DATABASE` | `perpustakaan` |
   | `MYSQL_PORT` | `3306` |

   Contoh pengaturan di PowerShell:

   ```powershell
   $env:MYSQL_HOST = "localhost"
   $env:MYSQL_USER = "root"
   $env:MYSQL_PASSWORD = "password-mysql-anda"
   $env:MYSQL_DATABASE = "perpustakaan"
   $env:MYSQL_PORT = "3306"
   ```

   Buat akun awal sebelum login. Jalankan dari direktori `modul 3` setelah environment database dikonfigurasi:

   ```powershell
   python -c "from models.user_model import UserModel; UserModel().register_user('admin', 'ganti-dengan-password-anda', 'admin')"
   ```

   Ganti username dan password contoh sesuai kebutuhan. Password disimpan oleh aplikasi sebagai hash SHA-256.

## Menjalankan aplikasi

Pastikan MySQL aktif dan environment variables sudah diatur, kemudian dari direktori `modul 3` jalankan:

```powershell
python main.py
```

Login menggunakan akun yang telah dibuat. Pengguna dengan role `admin` dapat mengelola buku dan anggota; role selain `admin` hanya dapat melihat data buku.

## Pengujian dan pemeriksaan kualitas

Dari direktori `modul 3`, jalankan:

```powershell
pytest -v
flake8 models/ controller/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

Workflow GitHub Actions menjalankan pemeriksaan flake8 sebelum pengujian pytest pada setiap push atau pull request ke branch `main`.
