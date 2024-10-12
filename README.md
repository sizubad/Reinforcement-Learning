# UTS Reinforcement Learning
# Kelompok 1
| Nama                       | NPM       |
| ----------------------     | :--------:|
| Nanditha Nabiilah Putri    | G1A021001 | 
| Siti Zubaidah	             | G1A021002 |
| Elisa                      | G1A021008 | 

# Penerapan DDQN dalam game 2048
![Overview Banner!](https://github.com/sizubad/Reinforcement-Learning/blob/main/2048.png)
Papan permainan 2048 adalah grid 4 * 4 dengan semua nilai adalah bilangan bulat pangkat 2. Pengguna memiliki a
maksimal 4 tindakan yang tersedia untuk setiap giliran, yaitu menggeser ke kiri, atas, bawah, atau kanan.<br />
Katakanlah kita memilih untuk menggeser ke kanan. Apa yang terjadi selanjutnya adalah bahwa semua ubin di kisi-kisi akan bergeser ke kanan, sebanyak mungkin. Selain itu, jika dalam prosesnya, sebuah angka bertabrakan dengan
dengan angka itu sendiri, keduanya akan digabungkan dengan menjumlahkannya. Terakhir, Anda juga akan melihat nomor baru muncul secara acak, disalah satu sel kisi yang kosong, angkanya selalu 2 atau 4.<br />
Demikian pula, jika Anda menggeser ke bawah sekarang, semua petak di kisi akan bergeser sejauh mungkin ke bawah.
sejauh yang dimungkinkan dalam kisi ini. Penggabungan juga akan dilakukan, jika ada, dan Anda juga akan melihat
baru akan muncul seperti sebelumnya.a <br />
Permainan akan terus berlanjut hingga Anda kehabisan langkah, atau ketika petak terbesar di papan adalah 2048. A
banyak permainan yang memungkinkan Anda untuk terus bermain setelah Anda mendapatkan 2048, dan kami juga akan mengasumsikan hal yang sama untuk permainan yang akan dimainkan agen kami.a <br />
<br />Untuk mencoba demo model di komputer Anda, kloning repo dan ketik perintah berikut di terminal:
```
python demo.py
```
# Referensi
1. https://github.com/brianspiering/rl-course/tree/main/08_deep_q_learning
2. https://github.com/jyotipmahes/2048_RL_Project

