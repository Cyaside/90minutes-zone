## Apa itu Django AuthenticationForm? Jelaskan juga kelebihan dan kekurangannya.

Authentication bawaan django ini menangani proses autentikasi. Nah secara defaut juga (setidaknya di project ini) dia punya 2 field utama yaitu username sama password (ada juga email first name dan last name kalau mereferensikan dari user object tapi ketiga ini opsional) dan saat digunakan Authentication form lah yang bakal ngecek username dan cocokin password

Kelebihannya yaitu tadi dia builtin dari djangonya sendiri dan udah terintegrasi sama sistem auth djangonya selain itu juga udh ada validasi otomatis dan udh di hash juga disananya jadi gk perlu terlalu ribetin diri sendiri alias coding sendiri authenticationnya karena udh ada

Kekurangannya ya dia kadang kurang fleksibel buat custom field kita harus mengoverride authentication formnya dan secara default dia terikat dengan user model jadinya juga kita custom dengan field login tidak seperti biasanya ya perlu modif ulang

Referensi jawaban (https://docs.djangoproject.com/en/5.2/topics/auth/default/

https://docs.djangoproject.com/en/5.2/ref/contrib/auth/#django.contrib.auth.models.User)

## Apa perbedaan antara autentikasi dan otorisasi? Bagaiamana Django mengimplementasikan kedua konsep tersebut?

Kalau autentikasi ya dia menverifikasi identitas si pengguna kalau otorisasi dia nentuin hak akses si pengguna kemana aja

Django sendiri seperti yang dibilang tadi punya built in authentikasi yaitu django.contrib.auth dia punya komponen utama user mode, login/logout functions sama forms nah setelah user login django bisa mengecek permissiona dari user tadi dia ada grouping defaultnya yaitu is_authenticated, is_staff sama is_superuser
nah django sendiri bakal beri izin pada user/grup tadi gitu.

Referensi : (https://docs.djangoproject.com/en/5.2/ref/contrib/auth/#django.contrib.auth.models.User)

## Apa saja kelebihan dan kekurangan session dan cookies dalam konteks menyimpan state di aplikasi web?

Cookies ini itu data yang disimpen di browser client atau si user dan yang bakal dikirim ke server di setiap request http

Kelebihannya dia disimpan disisi client jadinya ngurangin bebas storage server, persisten, mudah digunain dan bisa diakses client side. Nah kekurangannya karena dia cleint side dia bisa kena XSS kalau tidak dienkrips/https selain itu dia juga nambah beban request dan bergantung ke client karena user bisa matiin cookies di broswernya

Session sendiri itu data state yang disimpan di server

Kelebihannya ya lebih aman dan ukurannya lebih besar bisa simpen lebih banyak data, selain itu ini sulit dimanipulasi dari sisi client. Minusnya tadi dia ngebebanin server, butuh mekanisme cleanup buat session yang expired dan kalau servernya banyak sessionnya harus dishare gitulah sama dia tetap bergantung sama cookie karena biasanya session ID disimpan di cookie

## Apakah penggunaan cookies aman secara default dalam pengembangan web, atau apakah ada risiko potensial yang harus diwaspadai? Bagaimana Django menangani hal tersebut?

Jawabannya ya secara default ya tidak aman karena dia punya risiko potensial seperti XSS dan Pencurian cookies (di sniffing) sama CSRF (malsuin request pake cookie korban)

Risiko ini bisa di tangani dengan pake HTTPonly flag ini buat mastiin cookie tidak bisa diakses lewat javascript, secure flag ini buat mastiin cookie hanya dikirim via HTTPS, sameSite flag buat batasin pengiriman cooki lintas situs, session signing dan hashing dan juga ada CSRF protection built-in ( yang {%csrf_token%})

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

Sama seperti tugas-tugas sebelumnya ya ini hanya mengikuti dari tugas tutorial namun tentu saja dengan modifikasi sesuai dari saya. Ya pertama kita alter dulu modelsnya nambahin si user karena kan kita butuh buat authenticationnya. Isi Webnya ya hanya bisa diakses kalau udh login (ada @login_required di create, add sama shows products) kalau misalnya yang buat show mw gk ush login tinggal ya cabut aja (bebas). dan ya buat bagian ini sebenernya gk terlalu beda sih pastiin aja urlsnya juga udh bener sisanya ya paling styling dikit abis itu juga ada filtering buat all products sama my products. Disini juga udh ditaruh informasi pengguna yang login sama last loginnya di footer.

## Akun dummy di web pws-nya

admintest1  
Passtest1

admintest2  
Passtest2
