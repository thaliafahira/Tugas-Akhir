1. Containers
Glass Panel (Floating Card): Efek glassmorphism (semi-transparan dengan blur) warna dasarnya diatur di mobile/src/constants/colors.ts (variabel ULTRA.glass). Penggunaannya bisa Anda lihat pada "Profile Pill" di bagian atas file mobile/app/(pelari)/home.tsx atau pada mobile/src/components/organisms/ActiveDashboard.tsx.
Bottom Sheet / Swipeable Drawer: Komponen laci tarik ini kodenya difokuskan di file mobile/src/components/organisms/InactiveDashboard.tsx menggunakan library luar bernama @gorhom/bottom-sheet.
Stat Card: Kartu-kartu yang menampilkan informasi ringkas (seperti Pace, Waktu, Jarak) dibuat menjadi komponen mandiri (Molecule) di mobile/src/components/molecules/MetricItem.tsx yang kemudian dipanggil ke dalam Active Dashboard.

2. Action (Tombol)
Primary, Secondary, Danger, dan FAB: Semua variasi tombol ini disatukan dan diatur kodenya di dalam file atom mobile/src/components/atoms/Button.tsx. Komponen ini biasanya menerima props variant untuk mengubah warna dan gayanya sesuai dengan tabel desain Anda.

3. Indikator Status & Progres
Status Chip (Running, Finished, dsb): Kode untuk label pil warna-warni ini ada di mobile/src/components/atoms/Badge.tsx. Kedipan (pulsing glow) untuk status active/running juga diatur di dalam file tersebut atau dari style turunannya.
Leg Progress Bar: Jika sudah diimplementasi, komponen stat bar panjang biasanya diletakkan bersama di Dashboard atau sebagai molecule terpisah.
Avatar Pelari: Komponen lingkaran dengan inisial dan warna unik pelari ini kodenya ada di mobile/src/components/atoms/Avatar.tsx.

4. Komponen Peta
Runner Marker, Checkpoint Marker, & Route Line: Semua urusan peta (garis rute hijau terang yang bersinar, marker wajik untuk CP, dan lingkaran glow untuk pelari) murni dikoding menggunakan HTML & CSS murni yang disuntikkan ke Leaflet di dalam file mobile/src/components/organisms/MapViewer.tsx (pada fungsi buildHtml).