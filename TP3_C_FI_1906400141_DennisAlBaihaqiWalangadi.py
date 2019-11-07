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
TAMBAH\t <data>\t\tMenambahkan warisan budaya ke Database,\n\t\t\tcontoh: \
TAMBAH Tari Legong;;;Tarian;;;Bali;;;www.baliprov.go.id
UPDATE\t <data>\t\tMemperbarui data warisan budaya,\n\t\t\tcontoh: \
UPDATE Tari Legong;;;Tarian;;;Bali;;;www.baliprov.go.id
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
            return "Tipe file tidak dikenal, mohon impor file dengan ekstensi CSV\n"
        else:
            warn = False
            with open(parse(perintah), "r") as file:                                    # Buka file yang ada di argument
                bukaFile = csv.reader(file)                                             # Baca menggunakan csv.reader
                counter = 0                                                             # Hitung jumlah baris
                for baris in bukaFile:
                    if len(baris) != 0:                                                 # Cek apakah baris kosong
                        if (baris[0].upper() in database) and (warn == False):          # Beri peringatan jika terdapat duplikat
                            warn = True
                        database[baris[0].upper()] = {}                                 # Buat Dictionary baru
                        counter += 1                                                    # Tambah jumlah baris
                        for data, tipe in zip(baris, kategori):                         # Isi database dengan data sesuai dengan kategori
                            database[baris[0].upper()][tipe] = data
            if counter == 0:
                return "File yang anda buka tidak memiliki data"
            if warn:
                return "BudayaKB mendeteksi adanya duplikat dalam database atau file yang anda impor\n"\
                       "Baris terbawah atau data terbaru dianggap data paling relevan.\n"\
                       "Terimpor {} baris\n".format(counter)
            return "Terimpor {} baris\n".format(counter)

    except FileNotFoundError:
        return "Error: File tidak dapat ditemukan.\n"


def ekspordata(perintah):
    """
    Menulis sebuah file csv berdasarkan dictionary database
    """
    try:
        judulEkspor = perintah[1]
        baris = []
        counter = 0
        if ".csv" not in judulEkspor:                               # Cek apakah file beformat csv
            judulEkspor = judulEkspor+".csv"
        for i in database:                                          # Siapkan semua isi data setiap key di database ke sebuah list
            baris.append(database[i])
        with open(judulEkspor, "w") as fileEkspor:                  # Buka file
            ekspor = csv.DictWriter(fileEkspor, delimiter=",", fieldnames=kategori) # Menggunakan library CSV agar nggak susah memformat
            for data in baris:
                counter += 1
                ekspor.writerow(data)                               # Print setiap data di dalam list baris
        return "Terekspor {} baris\n".format(counter)               # Print jumlah baris
    except IOError:
        return "Terjadi IOError, mohon cek kembali\n"               # Jaga-jaga kalau ada masalah di harddisk/ssd


def carinama(nama,database):
    """
    Mencari isi database berdasarkan value nama budaya
    return sebuah list
    """
    terpilih = []
    if nama != '*':
        terpilih.append(','.join(
            [i for i in database[nama.upper()].values()]))  # Ambil data berdasarkan key nama
    else:
        for keys in database:
            terpilih.append(
                ','.join([i for i in database[keys].values()]))  # Print semua jika data jika *
    return terpilih


def caritipe(tipe, database):
    """
    Mencari isi database berdasarkan value tipe budaya
    return list semua data yang sesuai
    """
    terpilih = []
    for data in database:
        if database[data]['tipe'].upper() == tipe.upper():
            terpilih.append(','.join([i for i in database[data].values()]))
            continue
    return terpilih


def cariprov(tipe, database):
    terpilih = []
    for data in database:
        if database[data]['provinsi'].upper() == tipe.upper():
            print(','.join([i for i in database[data].values()]))
            continue
    return terpilih


def tambah(input, database, kategori):
    """
    Menambahkan data kedalan database, sesuai dengan kategori
    input = berupa list
    databse = dictionary dalam dictionary, bertindak sebagai database
    kategori = kategori sesuai urutan csv
    """
    database[input[0].upper()] = {}
    for data, tipe in zip(input, kategori):
        database[input[0].upper()][tipe] = data


def perbarui(newData, database):
    """
    Mengecek apakah ada data tersebut di atabase, jika ada maka perbarui
    newData = data yang akan baru
    database = dictionary dalam dictionary, bertindak sebagai database
    return True/False
    """
    index = 0
    for data in database:
        if database[data]['namawarisanbudaya'].upper() == newData[0].upper():
            for tipe in kategori:
                database[data][tipe] = newData[index]
                index += 1
                continue
            return True
        else:
            return False


def hapus(dataHapus, database):
    """
    Mengahpus data yang ada di databse sesuai dengan nama pada dataHapus
    param dataHapus = nama data yang ingin dihapus
    param database = dictionary dalam dictionary, bertindak sebagai database
    """
    for data in database:
        if dataHapus.upper() == data:
            database.pop(data)
            return True


def bukalink(perintah):
    link = ''.join([i for i in database[parse(perintah).upper()]['referenceurl']])
    webbrowser.open_new_tab(link)


def statistik():
    return "Terdapat {} warisan budaya\n".format(len(database))


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
    return [x for x in zip(listTipe, listJumlah)]


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
    return [x for x in zip(listProv, listJumlah)]


def keluar():
    # TODO: IMPURE
    kosong()
    print("="*68+"\n{:^68s}\n".format("~Sampai jumpa, jangan lupa mencintai warisan budaya Indonesia!~")+"="*69)
    exit()


def lihatdata():
    if len(database) != 0:
        pretty = pprint.PrettyPrinter()
        return pretty.pprint(database)
    else:
        return "Database masih kosong"


def main():
    kosong()
    print(banner)
    while True:
        try:
            perintah = input("> Masukkan perintah: ").split()

            if perintah[0].upper() == "IMPOR":
                print(impordata(perintah))

            elif perintah[0].upper() == "EKSPOR":
                print(ekspordata(perintah))

            elif perintah[0].upper() == "CARINAMA":
                if cekdata():
                    namaBudaya = parse(perintah)  # Masukan nama budaya yang ingin dicari ke variabel
                    try:
                        print(carinama(namaBudaya, database),sep="\n", end="\n")
                    except KeyError:
                        print("{} tidak ditemukan\n".format(namaBudaya))  # Kalau gaada, beritahu user
                else:
                    print("Database masih kosong, mohon import terlebih dahulu!\n")  # Beritahu user jika fatabase masih kosong

            elif perintah[0].upper() == "CARITIPE":

                if cekdata():
                    namaTipe = ' '.join(perintah[1:])
                    data = caritipe(namaTipe, database)
                    print(*data, sep="\n", end="\n")
                    print('*Ditemukan {} {}*\n'.format(len(data), namaTipe))
                else:
                    print("Database masih kosong, mohon import terlebih dahulu!\n")

            elif perintah[0].upper() == "CARIPROV":
                if cekdata():
                    tipe = ' '.join(perintah[1:])
                    data = cariprov(tipe, database)
                    print(*data, sep="\n", end="\n")
                    print("*Ditemukan {} warisan budaya*\n".format(len(data)))
                else:
                    print("Database masih kosong, mohon import terlebih dahulu!\n")

            elif perintah[0].upper() == "LIHATREF":
                bukalink(perintah)

            elif perintah[0].upper() == "TAMBAH":
                masukan = parse(perintah).split(";;;")
                tambah(masukan, database, kategori)
                print("{} ditambahkan\n".format(masukan[0]))

            elif perintah[0].upper() == "UPDATE":
                dataBaru = parse(perintah).split(";;;")
                if perbarui(dataBaru, database):
                    print("{} diupdate\n".format(dataBaru[0]))
                else:
                    print("Nama budaya yang anda cari tidak ditemukan!\n")

            elif perintah[0].upper() == "HAPUS":
                dataHapus = parse(perintah)
                if hapus(dataHapus, database):
                    print("{} dihapus\n".format(dataHapus))
                else:
                    print("Tidak dapat menemukan {}\n".format(dataHapus))

            elif perintah[0].upper() == "STAT":
                print(statistik())

            elif perintah[0].upper() == "STATTIPE":
                pemisah = f"\t{'':=<43s}"
                data = statistiktipe()
                print("\n\tSTATISTIK DATA BERDASARKAN TIPE:")
                print(pemisah)
                print('\t {:<3s}  {:<15s}{:^30s}'.format('No', 'Tipe', 'Banyak Budaya'))
                print(pemisah)
                for i in range(len(data)):  # Memasukkan data tabel
                    print('\t {:>3d}  {:<15s}{:^30d}'.format(i + 1, data[i][0], data[i][1]))
                print(pemisah+"\n")

            elif perintah[0].upper() == "STATPROV":
                pemisah = f"\t{'':=<43s}"
                data = statistikprov()
                print("\n\tSTATISTIK DATA BERDASARKAN PROVINSI:")
                print(pemisah)
                print('\t {:<3s}  {:<15s}{:^30s}'.format('No', 'Provinsi', 'Banyak Budaya'))
                print(pemisah)
                for i in range(len(data)):  # Memasukkan data tabel
                    print('\t {:>3d}  {:<15s}{:^30d}'.format(i + 1, data[i][0], data[i][1]))
                print(pemisah + "\n")

            elif perintah[0].upper() == "KELUAR":
                keluar()

            elif perintah[0].upper() == "PANDUAN":
                print("\n", guide, "\n")

            elif perintah[0].upper() == "LIHATDATA":
                print("\n", lihatdata(), "\n")

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
