# USA-2022-Midterm-Election-Data-Engineering-Workflow

Sebuah Data Engineering Workflow untuk memproses hasil Data Pemilu Midterm AS 2022 agar membentuk model prediktif

Anggota Kelompok:
- Karunia Perjuangan M             20/456368/TK/50498
- Christina Angraeni Panellah  20/456840/TK/50664
- Azzahra Adine Divania             20/463595/TK/51587
- Vira Ayu Oktaviani                     20/460670/TK/51159
- Richard Harryson                      20/456378/TK/50508

Tutorial Install
1. Pastikan Anda menggunakan OS berbasis Linux atau bisa juga melalui WSL2
2. Pada terminal kesayangan Anda, masukkan ```git clone https://github.com/karuniaperjuangan/USA-2022-Midterm-Election-Data-Engineering-Workflow.git```
3. Ketik ```cd USA-2022-Midterm-Election-Data-Engineering-Workflow.git```
4. Ketik ```virtualenv venv``` untuk membuat environment baru. Jika gagal, install dulu lewat ```pip install virtualenv```
5. Ketik ```source venv/bin/activate``` untuk mengaktifkan environment venv
6. Ketik ```pip install -r requirements.txt``` untuk menginstall dependency yang dibutuhkan
7. Pada ```/home/<USERNAME>/.bashsrc``` tambahkan ```EXPORT AIRFLOW-HOME=<PATH REPO>``` di akhir
8. Ketik ```airflow db init``` lalu tambahkan akun dengan ```airflow users create --username admin --password your_password --firstname your_first_name --lastname your_last_name --role Admin --email your_email@some.com``` dan ubah sesuai identitas Anda
9. Ketik ```airflow scheduler```
10. Buka terminal baru, ulangi hanya langkah 3&5
11. Ketik ```airflow webserver```, buka ```https:\\localhost:8080```, login sesuai identitas pada nomor 8
12. Aktifkan semua DAGs yang berawalan dengan ```rekdat-```
13. Selamat, anda berhasil menyelesaikan proses ini. Semoga rekdat Anda mendapat A
