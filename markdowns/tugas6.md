## Apa perbedaan antara synchronous request dan asynchronous request?

synchornous jenis permintaan yang memblokir browser sampai operasi selesai dimana artinya browser nunggu respon dari server, javascript berhenti sementara dan tidak bisa jalanin kode lain.

sementara, asynchronous jenis permintaan jenis permintaan yang tidak blokir browser. javascript tetap bisa jalanin perintah lain dan halaman tetap bisa digunakan oleh pengguna

source : https://stackoverflow.com/questions/16715380/what-is-the-difference-between-asynchronous-and-synchronous-http-request

## Bagaimana AJAX bekerja di Django (alur request–response)?

misal pertama pengguna melakukan "action" di halaman web seperti menekan tombol login atau sesuatu gitu nah nanti bakal kekriim permintaan AJAX ke django misalnya dengan fetch() dan lalu dimana django bakal menerima dan memproses permintaan (misalnya di views.py) yang mana django bakal mengirimkan respon tersebut (biasanya berupa JSON object) yang lalu setelahnya javascript menerima data dari server dan halaman diperbarui

## Apa keuntungan menggunakan AJAX dibandingkan render biasa di Django?

Keuntungannya tidak perlu reload seluruh halaman bisa bagian tertentu saja dan AJAX ini lebih cepat dan efisien karena hanya mengirim data penting bukan seluruh HTML halaman dan terakhir tergantung bagaimana kita mengimplementnya ajax bisa juga ningkatin user experience

## Bagaimana cara memastikan keamanan saat menggunakan AJAX untuk fitur Login dan Register di Django?

Sama seperti biasanya caranya bisa memakai CSRF Token, Menggunakan HTTPS, Validasi data (seperti biasa) dan terakhir gunakan django authentication sistem (daripada buat sendiri) dan masih banyak lagi sebenarnya

## Bagaimana AJAX mempengaruhi pengalaman pengguna (User Experience) pada website?

Ajax dapat membuat website terasa lebih cepat, interaktif dan responsif karena dapat memperbarui data di sebagian halaman tanpa membuat seluruh halaman dan ini berpengaruh dari sisi kecepatan dan kenyaman interaksi pengguna
