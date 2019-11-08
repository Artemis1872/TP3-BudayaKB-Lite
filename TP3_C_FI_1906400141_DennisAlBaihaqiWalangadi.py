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
\t*DAFTAR PERINTAH:*
\tIMPOR\t <file.csv>\tMengimpor data CSV ke Database, contoh: IMPOR file.csv
\tEKSPOR\t <file.csv>\tMengekspor data Database ke CSV, contoh: EKSPOR file.csv
\tCARINAMA <nama>\t\tMencari warisan budaya berdasarkan nama, contoh: CARINAMA Rendang
\tCARITIPE <tipe>\t\tMencari warisan budaya berdasarkan tipe, contoh: CARITIPE Makanan
\tCARIPROV <prov>\t\tMencari warisan budaya berdasarkan provinsi daerah asal, contoh: CARIPROV Bali
\tTAMBAH\t <data>\t\tMenambahkan warisan budaya ke Database,\n\t\t\t\t  contoh: \
TAMBAH Tari Legong;;;Tarian;;;Bali;;;www.baliprov.go.id
\tUPDATE\t <data>\t\tMemperbarui data warisan budaya,\n\t\t\t\t  contoh: \
UPDATE Tari Legong;;;Tarian;;;Bali;;;www.baliprov.go.id
\tHAPUS\t <nama>\t\tMenghapus data warisan budaya, contoh: HAPUS Tari Saman
\tLIHATREF <nama>\t\tMembuka referensi berdasarkan nama budaya, contoh: LIHATREF Rendang
\tLIHATDATA \t\tmelihat data yang disimpan
\tSTAT\t\t\tMenghitung banyaknya warisan budaya di Database
\tSTATTIPE\t\tMenampilkan data di Database berdasarkan tipe
\tSTATPROV\t\tMenampilkan data di Database berdasarkan provinsi
\tPANDUAN\t\t\tMelihat panduan daftar perintah
\tBERSIHKAN \t\tMembersihkan terminal
\tKELUAR\t\t\tKeluar BudayaKB Lite
"""

banner = f"{'':=<68}"+u"""\u001b[31m
  ____            _                   _  ______    _     _ _       
 | __ ) _   _  __| | __ _ _   _  __ _| |/ / __ )  | |   (_) |_ ___ 
 |  _ \\| | | |/ _` |/ _` | | | |/ _` | ' /|  _ \\  | |   | | __/ _ \\ \u001b[0m
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
    param perintah: berupa list dari hasil split perintah
    """
    return ' '.join(perintah[1:])


def cekdata(gudangdata):
    """
    Mengecek apakah database masih kosong
    param gudangdata = dictionary dalam dictionary, bertindak sebagai database
    """
    if len(gudangdata) != 0:
        return True
    else:
        return False


def impordata(perintah, gudangdata):
    """
    Membaca isi file csv dan memasukkannya ke dalam dictionary database
    param perintah = list hasil split perintah asli
    param gudangdata = dictionary dalam dictionary, bertindak sebagai database
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
                        if (baris[0].upper() in gudangdata) and (warn == False):        # Beri peringatan jika terdapat
                            warn = True                                                 # duplikat
                        gudangdata[baris[0].upper()] = {}                               # Buat Dictionary baru
                        counter += 1                                                    # Tambah jumlah baris
                        for data, tipe in zip(baris, kategori):                         # Isi database dengan data
                            gudangdata[baris[0].upper()][tipe] = data                   # sesuai dengan kategori
            if counter == 0:
                return "File yang anda buka tidak memiliki data"
            if warn:
                return "BudayaKB mendeteksi adanya duplikat dalam database atau file yang anda impor\n"\
                       "Baris terbawah atau data terbaru dianggap data paling relevan.\n"\
                       "Terimpor {} baris\n".format(counter)
            return "Terimpor {} baris\n".format(counter)

    except FileNotFoundError:
        return "Error: File tidak dapat ditemukan.\n"


def ekspordata(perintah, gudangdata):
    """
    Menulis sebuah file csv berdasarkan dictionary database
    param perintah = list hasil split perintah asli
    param gudangdata = dictionary dalam dictionary, bertindak sebagai database
    """
    try:
        judulEkspor = perintah[1]
        baris = []
        counter = 0
        if ".csv" not in judulEkspor:                                   # Cek apakah file beformat csv
            judulEkspor = judulEkspor+".csv"
        for i in gudangdata:                                            # Siapkan semua isi data setiap key di database
            baris.append(gudangdata[i])                                 # ke sebuah list
        with open(judulEkspor, "w") as fileEkspor:                      # Buka file
            ekspor = csv.DictWriter(fileEkspor, delimiter=",", fieldnames=kategori)  # Menggunakan library CSV
            for data in baris:
                counter += 1
                ekspor.writerow(data)                               # Print setiap data di dalam list baris
        return "Terekspor {} baris\n".format(counter)               # Print jumlah baris
    except IOError:
        return "Terjadi IOError, mohon cek kembali\n"               # Jaga-jaga kalau ada masalah di harddisk/ssd


def carinama(nama, gudangdata):
    """
    Mencari isi database berdasarkan value nama budaya
    return sebuah list
    param nama = Nama budaya
    param gudangdata = dictionary dalam dictionary, bertindak sebagai database
    """
    terpilih = []
    if nama != '*':
        terpilih.append(','.join(
                [i for i in gudangdata[nama.upper()].values()]))    # Ambil data berdasarkan key nama
    else:
        for keys in gudangdata:
            terpilih.append(','.join(
                [i for i in gudangdata[keys].values()]))   # Ambil semua jika data jika *
    return terpilih


def caritipe(tipe, gudangdata):
    """
    Mencari isi database berdasarkan value tipe budaya
    return list semua data yang sesuai
    param tipe = Nama tipe
    param gudangdata = dictionary dalam dictionary, bertindak sebagai database
    """
    terpilih = []
    for data in gudangdata:
        if gudangdata[data]['tipe'].upper() == tipe.upper():
            terpilih.append(','.join([i for i in gudangdata[data].values()]))
            continue
    return terpilih


def cariprov(tipe, gudangdata):
    """
    Mencari isi database berdasarkan value provinsi asal budaya
    return list semua data yang sesuai
    param tipe = Nama provinsi
    param gudangdata = dictionary dalam dictionary, bertindak sebagai database
    """
    terpilih = []
    for data in gudangdata:
        if gudangdata[data]['provinsi'].upper() == tipe.upper():
            terpilih.append(','.join([i for i in gudangdata[data].values()]))
            continue
    return terpilih


def tambah(datamasuk, gudangdata, kelas):
    """
    Menambahkan data kedalan database, sesuai dengan kategori
    input = berupa list
    gudangdata = dictionary dalam dictionary, bertindak sebagai database
    kategori = kategori sesuai urutan csv
    """
    warn = False
    if datamasuk[0].upper() in gudangdata:
        warn = True
    gudangdata[datamasuk[0].upper()] = {}
    for data, tipe in zip(datamasuk, kelas):
        gudangdata[datamasuk[0].upper()][tipe] = data
    return warn


def perbarui(newdata, gudangdata):
    """
    Mengecek apakah ada data tersebut di atabase, jika ada maka perbarui
    newData = data yang akan baru
    gudangdata = dictionary dalam dictionary, bertindak sebagai database
    return True/False
    """
    index = 0
    for data in gudangdata:
        if gudangdata[data]['namawarisanbudaya'].upper() == newdata[0].upper():
            for tipe in kategori:
                gudangdata[data][tipe] = newdata[index]
                index += 1
                continue
            return True
        continue
    else:
        return False


def hapus(datahapus, gudangdata):
    """
    Mengahpus data yang ada di databse sesuai dengan nama pada dataHapus
    param dataHapus = nama data yang ingin dihapus
    param database = dictionary dalam dictionary, bertindak sebagai database
    """
    for data in gudangdata:
        if datahapus.upper() == data:
            gudangdata.pop(data)
            return True


def bukalink(perintah, gudangdata):
    link = ''.join([i for i in gudangdata[parse(perintah).upper()]['referenceurl']])
    return webbrowser.open_new_tab(link)


def statistik(gudangdata):
    return "Terdapat {} warisan budaya\n".format(len(gudangdata))


def statistiktipe(gudangdata):
    listTipe = []
    listJumlah = []
    for data in gudangdata:
        if gudangdata[data]['tipe'] not in listTipe:
            listTipe.append(gudangdata[data]['tipe'])
            continue

    for tipe in listTipe:
        count = 0
        for data in gudangdata:
            if gudangdata[data]['tipe'].upper() == tipe.upper():
                count += 1
        listJumlah.append(count)
    return sorted([x for x in zip(listTipe, listJumlah)], key=lambda x: x[1])


def statistikprov(gudangdata):
    listProv = []
    listJumlah = []
    for data in gudangdata:
        if gudangdata[data]['provinsi'] not in listProv:
            listProv.append(gudangdata[data]['provinsi'])
            continue
    for prov in listProv:
        count = 0
        for data in gudangdata:
            if gudangdata[data]['provinsi'].upper() == prov.upper():
                count += 1
        listJumlah.append(count)
    return sorted([x for x in zip(listProv, listJumlah)], key=lambda x: x[1])


def lihatdata(gudangdata):
    if cekdata(gudangdata):
        pretty = pprint.PrettyPrinter()
        return pretty.pprint(gudangdata)
    else:
        return "Database masih kosong"


def main():
    kosong()
    print(banner)
    while True:
        try:
            perintah = input("> Masukkan perintah: ").split()

            "DAFTAR PERINTAH"
            if perintah[0].upper() == "IMPOR":
                print(impordata(perintah, database))

            elif perintah[0].upper() == "EKSPOR":
                print(ekspordata(perintah, database))

            elif perintah[0].upper() == "CARINAMA":

                if cekdata(database):
                    namaBudaya = parse(perintah)                                        # Masukan nama budaya yang ingin
                    try:                                                                # dicari ke variabel
                        print(*carinama(namaBudaya, database), sep="\n")
                        print("\n")
                    except KeyError:
                        print("{} tidak ditemukan\n".format(namaBudaya.title()))        # Kalau gaada, beritahu user
                else:
                    print("Database masih kosong, mohon import terlebih dahulu!\n")
            elif perintah[0].upper() == "CARITIPE":

                if cekdata(database):
                    namaTipe = ' '.join(perintah[1:])
                    data = caritipe(namaTipe, database)
                    if len(data) != 0:
                        print(*data, sep="\n")
                        print('*Ditemukan {} {}*\n'.format(len(data), namaTipe.lower()))
                    else:
                        print("Tidak ditemukan tipe budaya {} di dalam database\n".format(namaTipe.upper()))
                else:
                    print("Database masih kosong, mohon import terlebih dahulu!\n")

            elif perintah[0].upper() == "CARIPROV":
                if cekdata(database):
                    prov = ' '.join(perintah[1:])
                    data = cariprov(prov, database)
                    if len(data) != 0:
                        print(*data, sep="\n")
                        print("\n*Ditemukan {} warisan budaya*\n".format(len(data)))
                    else:
                        print("Tidak ditemukan budaya dari provinsi {} di dalam database\n".format(prov.title()))
                else:
                    print("Database masih kosong, mohon import terlebih dahulu!\n")

            elif perintah[0].upper() == "TAMBAH":
                masukan = parse(perintah).split(";;;")
                if tambah(masukan, database, kategori) == True:
                    print("Ditemukan data yang serupa di database sebelumnya.\n"+
                          "BudayaKB Lite akan mengubah seluruh data lama dengan data baru.")
                print("{} ditambahkan\n".format(masukan[0].title()))

            elif perintah[0].upper() == "UPDATE":
                dataBaru = parse(perintah).split(";;;")
                if perbarui(dataBaru, database):
                    print("{} diupdate\n".format(dataBaru[0].title()))
                else:
                    print("Nama budaya yang anda cari tidak ditemukan!\n")

            elif perintah[0].upper() == "HAPUS":
                dataHapus = parse(perintah)
                if hapus(dataHapus, database):
                    print("{} dihapus\n".format(dataHapus.title()))
                else:
                    print("Tidak dapat menemukan {}\n".format(dataHapus))

            elif perintah[0].upper() == "LIHATREF":
                try:
                    bukalink(perintah, database)
                except KeyError:
                    print("Tidak dapat menemukan {}".format(parse(perintah)))

            elif perintah[0].upper() == "LIHATDATA":
                if len(database) != 0:
                    print("\n")
                    lihatdata(database)
                    print("\n")
                else:
                    print("Database masih kosong.")

            elif perintah[0].upper() == "STAT":
                print(statistik(database))

            elif perintah[0].upper() == "STATTIPE":
                pemisah = f"\t{'':=<43s}"
                data = statistiktipe(database)
                print("\n\tSTATISTIK DATA BERDASARKAN TIPE:")
                print(pemisah)
                print('\t {:<3s}  {:<15s}{:^30s}'.format('No', 'Tipe', 'Banyak Budaya'))
                print(pemisah)
                for i in range(len(data)):  # Memasukkan data tabel
                    print('\t {:>3d}  {:<15s}{:^30d}'.format(i + 1, data[i][0], data[i][1]))
                print(pemisah+"\n")

            elif perintah[0].upper() == "STATPROV":
                pemisah = f"\t{'':=<43s}"
                data = statistikprov(database)
                print("\n\tSTATISTIK DATA BERDASARKAN PROVINSI:")
                print(pemisah)
                print('\t {:<3s}  {:<15s}{:^30s}'.format('No', 'Provinsi', 'Banyak Budaya'))
                print(pemisah)
                for i in range(len(data)):  # Memasukkan data tabel
                    print('\t {:>3d}  {:<15s}{:^30d}'.format(i + 1, data[i][0], data[i][1]))
                print(pemisah + "\n")

            elif perintah[0].upper() == "PANDUAN":
                print("\n", guide, "\n")

            elif perintah[0].upper() == "BERSIHKAN":
                kosong()
                print(banner)

            elif perintah[0].upper() == "KELUAR":
                kosong()
                print("=" * 68 + "\n{:^68s}\n".format(
                    "~Sampai jumpa, jangan lupa mencintai warisan budaya Indonesia!~") + "=" * 69)
                exit()

            else:
                print("Terjadi kesalahan: Perintah tidak dikenal\n")

        except IndexError:
            pass
        except KeyboardInterrupt:
            kosong()
            print("=" * 68 + "\n{:^68s}\n".format(
                "~Sampai jumpa, jangan lupa mencintai warisan budaya Indonesia!~") + "=" * 69)
            exit()
        except ModuleNotFoundError:
            print("Matplotlib didatk ditemukan.\
                  Mohon install library matplotlib menggunakan:\n\
                  \tpip -m install matplotlib")


if __name__ == "__main__":
    main()
