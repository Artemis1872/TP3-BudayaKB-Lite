import csv
import os
import platform
import random
import pprint
import webbrowser

database = {}
kategori = ["namawarisanbudaya", "tipe", "provinsi", "referenceurl"]
salam = ['Peu na haba?', 'Hadia Duria?', 'Aha do kabar?', 'Camano kabo awak?', 'Cemane kabe?', 'Ba a kabanyo?',
         'Ape kaber?', 'Apo kabar?', 'Pedio Kabarnyo?', 'Dame pangabaran?', 'Api kabagh?', 'Nyow kabagh?',
         'Maye kabagh?', 'Pripun habare?', 'Kepriben kabare?', 'Kepriwe kabare?', 'Rika Kepriben kabare?',
         'Piye kabarmu?', 'Karabem pe leh?', 'Pripun kabare?', 'Kados pundi kabaripun?', 'Kelendai riko?',
         'Pimen kabare?', 'Napa habar?', 'Kayapa habar pian?', 'Aga kareba?', 'Sapunapi gatrane?', 'Punapi gatre?',
         'Brembe kabar?', 'Ngumbe kabarne?', 'Meluk rungan?', 'Bune haba?', 'Nara gerotelo?']
guide = """
IMPOR\t <file.csv>\tMengimpor data CSV ke Database, contoh: IMPOR file.csv
EKSPOR\t <file.csv>\tMengekspor data Database ke CSV, contoh: EKSPOR file.csv
CARINAMA <nama>\t\tMencari warisan budaya berdasarkan nama, contoh: CARINAMA Rendang
CARITIPE <tipe>\t\tMencari warisan budaya berdasarkan tipe, contoh: CARITIPE Makanan
CARIPROV <prov>\t\tMencari warisan budaya berdasarkan provinsi daerah asal, contoh: CARIPROV Bali
TAMBAH\t <data>\t\tMenambahkan warisan budaya ke Database,\n\t\t\tcontoh: TAMBAH Tari Legong;;;Tarian;;;Bali;;;www.baliprov.go.id
UPDATE\t <data>\t\tMemperbarui data warisan budaya,\n\t\t\tcontoh: UPDATE Tari Legong;;;Tarian;;;Bali;;;www.baliprov.go.id
HAPUS\t <nama>\t\tMenghapus data warisan budaya, contoh: HAPUS Tari Saman
LIHATREF <nama>\t\tMembuka referensi berdasarkan nama budaya, contoh: LIHATREF Rendang
LIHATDATA \t\tmelihat data yang disimpan
STAT\t\t\tMenghitung banyaknya warisan budaya di Database
STATTIPE\t\tMenampilkan data di Database berdasarkan tipe
STATPROV\t\tMenampilkan data di Database berdasarkan provinsi
PANDUAN\t\t\tMelihat panduan daftar perintah
BERSIHKAN \t\tMembersihkan terminal
KELUAR\t\t\tKeluar BudayaKB Lite
"""
banner = f"{'':=<68}"+u"""\u001b[31m
  ____            _                   _  ______    _     _ _       
 | __ ) _   _  __| | __ _ _   _  __ _| |/ / __ )  | |   (_) |_ ___ 
 |  _ \\| | | |/ _` |/ _` | | | |/ _` | ' /|  _ \\  | |   | | __/ _ \\ \u001b[0m"""+"""
 | |_) | |_| | (_| | (_| | |_| | (_| | . \\| |_) | | |___| | ||  __/ 
 |____/ \\__,_|\\__,_|\\__,_|\\__, |\\__,_|_|\\_\\____/  |_____|_|\\__\\___| 
                          |___/v0.0.2 - Dennis Al Baihaqi Walangadi\n"""+f"{'':=<68}"+"\n{:^68s}\n".format(
    '~Kalau bukan kita yang melestarikan budaya, siapa lagi?~')+"{:^68s}\n".format(
    random.choice(salam))+"{:^68s}".format(
    "Ketik 'PANDUAN' untuk melihat daftar perintah.")+f"\n{'':=<68s}"

def kosong():
    """
    Mengosongkan terminal
    """

    if platform.system() == "Windows":          # Cek apakah program berjalan di Windows
        os.system('cls')                        # Jika ya, eksekusi perintah 'cls'
    else:                                       # Jika bukan, asumsi Linux
        os.system('clear')                      # Eksekusi perintah 'clear'

def parse(perintah):
    """
    Parse argumen dari input yang sudah di split
    :Param perintah: berupa list dari hasil split perintah
    """
    return ' '.join(perintah[1:])

def cekdata():
    if len(database) != 0:
        return True
    else:
        return False

def impordata(perintah):
    """
    Membaca isi file csv dan memasukkannya ke dalam dictionary database
    """
    try:
        if "csv" not in perintah[1].split("."):
            print("Tipe file tidak dikenal, mohon impor file dengan ekstensi CSV\n")
        else:
            warn = False
            with open(parse(perintah), "r") as file:                                    #Buka file yang ada di argument
                bukaFile = csv.reader(file)                                             #Baca menggunakan csv.reader
                counter = 0                                                             #Hitung jumlah baris
                for baris in bukaFile:
                    if len(baris) != 0:                                                 #Cek apakah baris kosong
                        if (baris[0].upper() in database) and (warn == False):          #Beri peringatan jika terdapat duplikat
                            warn = True
                        database[baris[0].upper()] = {}                                 #Buat Dictionary baru
                        counter += 1                                                    #Tambah jumlah baris
                        for data, tipe in zip(baris, kategori):                         #Isi database dengan data sesuai dengan kategori
                            database[baris[0].upper()][tipe] = data
            if counter == 0:
                print("File yang anda buka tidak memiliki data")
            if warn:
                print("BudayaKB mendeteksi adanya duplikat dalam database atau file yang anda impor\n"\
                      "Baris terbawah atau data terbaru dianggap data paling relevan.")
            print("Terimpor {} baris\n".format(counter))

    except FileNotFoundError:
        print("Error: File tidak dapat ditemukan.\n")


def ekspordata(perintah):
    """
    Menulis sebuah file csv berdasarkan dictionary database
    """
    try:
        judulEkspor = perintah[1]
        baris = []
        counter = 0
        if ".csv" not in judulEkspor:                               #Cek apakah file beformat csv
            judulEkspor = judulEkspor+".csv"
        for i in database:                                          #Siapkan semua isi data setiap key di database ke sebuah list
            baris.append(database[i])
        with open(judulEkspor, "w") as fileEkspor:                  #Buka file
            ekspor = csv.DictWriter(fileEkspor, delimiter=",", fieldnames=kategori) #Menggunakan library CSV agar nggak susah memformat
            for data in baris:
                counter += 1
                ekspor.writerow(data)                               #Print setiap data di dalam list baris
        print("Terekspor {} baris\n".format(counter))               #Print jumlah baris
    except IOError:
        print("Terjadi IOError, mohon cek kembali\n")               #Jaga-jaga kalau ada masalah di harddisk/ssd

def carinama(perintah):
    """
    Mencari isi database berdasarkan value nama budaya
    """
    if cekdata():
        namaBudaya = parse(perintah)                                #Masukan nama budaya yang ingin dicari ke variabel
        try:
            if namaBudaya != '*':
                print(','.join([i for i in database[namaBudaya.upper()].values()]), "\n")   #Ambil data berdasarkan key nama
            else:
                for keys in database:
                    print(','.join([i for i in database[keys].values()]), "\n")             #Print semua jika data jika *

        except KeyError:
            print("{} tidak ditemukan\n".format(namaBudaya))        #Kalau gaada, beritahu user
    else:
        print("Database masih kosong, mohon import terlebih dahulu!\n") #Beritahu user jika fatabase masih kosong

def caritipe(perintah):
    """
    Mencari isi database berdasarkan value tipe budaya
    """
    if cekdata():
        namaTipe = ' '.join(perintah[1:])
        counter = 0
        for data in database:
            if database[data]['tipe'].upper() == namaTipe.upper():
                counter += 1
                print(','.join([i for i in database[data].values()]))
                continue
        print('*Ditemukan {} {}*\n'.format(counter, namaTipe))
    else:
        print("Database masih kosong, mohon import terlebih dahulu!\n")

def cariprov(perintah):
    if cekdata():
        namaTipe = ' '.join(perintah[1:])
        counter = 0
        for data in database:
            if database[data]['provinsi'].upper() == namaTipe.upper():
                counter += 1
                print(','.join([i for i in database[data].values()]))
                continue
        print("*Ditemukan {} warisan budaya*\n".format(counter))
    else:
        print("Database masih kosong, mohon import terlebih dahulu!\n")

def tambah(perintah):
    dataTambah = parse(perintah).split(";;;")
    database[dataTambah[0].upper()] = {}
    for data, tipe in zip(dataTambah, kategori):
        database[dataTambah[0].upper()][tipe] = data
    print("{} ditambahkan\n".format(dataTambah[0]))

def perbarui(perintah):
    dataBaru = parse(perintah).split(";;;")
    index = 0
    for data in database:
        if database[data]['namawarisanbudaya'].upper() == dataBaru[0].upper():
            for tipe in kategori:
                database[data][tipe] = dataBaru[index]
                index += 1
                continue
    print("{} diupdate\n".format(dataBaru[0]))

def hapus(perintah):
    dataHapus = parse(perintah)
    for data in database:
        if dataHapus.upper() == data:
            database.pop(data)
            print("{} dihapus\n".format(dataHapus))
            break
        else:
            print("Tidak dapat menemukan {}\n".format(dataHapus))

def bukalink(perintah):
    link = ''.join([i for i in database[parse(perintah).upper()]['referenceurl']])
    webbrowser.open_new_tab(link)

def statistik():
    print("Terdapat {} warisan budaya\n".format(len(database)))

def statistiktipe():
    listTipe = []
    listJumlah = []
    for data in database:
        if database[data]['tipe'] not in listTipe:
            listTipe.append(database[data]['tipe'])
            continue

    for tipe in listTipe:
        count = 0
        for data in database:
            if database[data]['tipe'].upper() == tipe.upper():
                count += 1
        listJumlah.append(count)
    print([x for x in zip(listTipe, listJumlah)],end="\n")

def statistikprov():
    listProv = []
    listJumlah = []
    for data in database:
        if database[data]['provinsi'] not in listProv:
            listProv.append(database[data]['provinsi'])
            continue
    for prov in listProv:
        count = 0
        for data in database:
            if database[data]['provinsi'].upper() == prov.upper():
                count += 1
        listJumlah.append(count)
    print([x for x in zip(listProv, listJumlah)], end="\n")

def keluar():
    kosong()
    print("="*68+"\n{:^68s}\n".format("~Sampai jumpa, jangan lupa mencintai warisan budaya Indonesia!~")+"="*69)
    exit()

def lihatdata():
    if len(database) != 0:
        pretty = pprint.PrettyPrinter()
        pretty.pprint(database)
    else:
        print("Database masih kosong")

def main():
    kosong()
    print(banner)
    while True:
        try:
            perintah = input("> Masukkan perintah: ").split()

            if perintah[0].upper() == "IMPOR":
                impordata(perintah)

            elif perintah[0].upper() == "EKSPOR":
                ekspordata(perintah)

            elif perintah[0].upper() == "CARINAMA":
                carinama(perintah)

            elif perintah[0].upper() == "CARITIPE":
                caritipe(perintah)

            elif perintah[0].upper() == "CARIPROV":
                cariprov(perintah)

            elif perintah[0].upper() == "LIHATREF":
                bukalink(perintah)

            elif perintah[0].upper() == "TAMBAH":
                tambah(perintah)

            elif perintah[0].upper() == "UPDATE":
                perbarui(perintah)

            elif perintah[0].upper() == "HAPUS":
                hapus(perintah)

            elif perintah[0].upper() == "STAT":
                statistik()

            elif perintah[0].upper() == "STATTIPE":
                statistiktipe()

            elif perintah[0].upper() == "STATPROV":
                statistikprov()

            elif perintah[0].upper() == "KELUAR":
                keluar()

            elif perintah[0].upper() == "PANDUAN":
                print(guide)

            elif perintah[0].upper() == "LIHATDATA":
                lihatdata()

            elif perintah[0].upper() == "BERSIHKAN":
                kosong()
                print(banner)

            else:
                print("Terjadi kesalahan: Perintah tidak dikenal\n")
        except IndexError:
            pass
        except KeyboardInterrupt:
            keluar()

if __name__ == "__main__":
    main()
