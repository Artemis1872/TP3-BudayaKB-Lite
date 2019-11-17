import csv
import os
import platform
import pprint
import random
import webbrowser

database = {}

kategori = ["namawarisanbudaya", "tipe", "provinsi", "referenceurl"]

sep = ";;;"

salam = ["Peu na haba?", "Hadia Duria?", "Aha do kabar?", "Camano kabo awak?", "Cemane kabe?", "Ba a kabanyo?",
         "Ape kaber?", "Apo kabar?", "Pedio Kabarnyo?", "Dame pangabaran?", "Api kabagh?", "Nyow kabagh?",
         "Maye kabagh?", "Pripun habare?", "Kepriben kabare?", "Kepriwe kabare?", "Rika Kepriben kabare?",
         "Piye kabarmu?", "Karabem pe leh?", "Pripun kabare?", "Kados pundi kabaripun?", "Kelendai riko?",
         "Pimen kabare?", "Napa habar?", "Kayapa habar pian?", "Aga kareba?", "Sapunapi gatrane?", "Punapi gatre?",
         "Brembe kabar?", "Ngumbe kabarne?", "Meluk rungan?", "Bune haba?", "Nara gerotelo?"]

guide = u" \t\33[1m" + "DAFTAR PERINTAH:" + u" \33[0m\n" + \
        "\tIMPOR\t <file.csv>\tMengimpor data CSV ke Database, contoh: IMPOR file.csv atau IMPOR C:\\folder\\file.csv\n" + \
        "\tEKSPOR\t <file.csv>\tMengekspor data Database ke CSV, contoh: EKSPOR file.csv atau IMPOR C:\\folder\\file.csv\n" + \
        "\tCARINAMA <nama>\t\tMencari warisan budaya berdasarkan nama, contoh: CARINAMA Rendang\n" + \
        "\tCARITIPE <tipe>\t\tMencari warisan budaya berdasarkan tipe, contoh: CARITIPE Makanan\n" + \
        "\tCARIPROV <prov>\t\tMencari warisan budaya berdasarkan provinsi daerah asal, contoh: CARIPROV Bali\n" + \
        "\tTAMBAH\t <data>\t\tMenambahkan warisan budaya ke Database,\n\t\t\t\t  contoh: TAMBAH Tari Legong;;;Tarian;;;Bali;;;www.baliprov.go.id\n" + \
        "\tUPDATE\t <data>\t\tMemperbarui data warisan budaya,\n\t\t\t\t  contoh: UPDATE Tari Legong;;;Tarian;;;Bali;;;www.baliprov.go.id\n" + \
        "\tHAPUS\t <nama>\t\tMenghapus data warisan budaya, contoh: HAPUS Tari Saman\n" + \
        "\tLIHATREF <nama>\t\tMembuka referensi berdasarkan nama budaya, contoh: LIHATREF Rendang\n" + \
        "\tLIHATDATA \t\tmelihat data yang disimpan\n" + \
        "\tSTAT\t\t\tMenghitung banyaknya warisan budaya di Database\n" + \
        "\tSTATTIPE\t\tMenampilkan data di Database berdasarkan tipe\n" + \
        "\tSTATPROV\t\tMenampilkan data di Database berdasarkan provinsi\n" + \
        "\tPANDUAN\t\t\tMelihat panduan daftar perintah\n" + \
        "\tLOG\t\t\tMelihat histori perintah\n" + \
        "\tBERSIHKAN \t\tMembersihkan terminal\n" + \
        "\tKELUAR\t\t\tKeluar BudayaKB Lite\n"

separator = f"{'':=<68}"

banner = separator + u"\33[31m" + \
         "\n  ____            _                   _  ______    _     _ _        " + \
         "\n | __ ) _   _  __| | __ _ _   _  __ _| |/ / __ )  | |   (_) |_ ___  " + \
         "\n |  _ \\| | | |/ _` |/ _` | | | |/ _` | ' /|  _ \\  | |   | | __/ _ \\ " + u" \33[37m" + \
         "\n | |_) | |_| | (_| | (_| | |_| | (_| | . \\| |_) | | |___| | ||  __/ " + \
         "\n |____/ \\__,_|\\__,_|\\__,_|\\__, |\\__,_|_|\\_\\____/  |_____|_|\\__\\___| " + \
         "\n                          |___/v0.0.4 - Dennis Al Baihaqi Walangadi " + "\33[0m\n" + \
         separator + \
         "\n{:^68s}\n".format("~Kalau bukan kita yang melestarikan budaya, siapa lagi?~") + u"\33[7m" + \
         "{:^68s}".format(random.choice(salam)) + u"\33[0m" + \
         "\n{:^68s}".format("Ketik 'PANDUAN' untuk melihat daftar perintah.")


def kosong():
    """
    Mengosongkan terminal
    """

    if platform.system() == "Windows":  # Cek apakah program berjalan di Windows
        os.system("cls")  # Jika ya, eksekusi perintah "cls"

    else:  # Jika bukan, asumsi Linux
        os.system("clear")  # Eksekusi perintah "clear"


def parse(perintah):
    """
    Parse argumen dari input yang sudah di split
    :param: perintah: berupa list dari hasil split perintah
    """

    return " ".join(perintah[1:])  # Return seluruh string selain perintah


def cekdata(gudangdata):
    """
    Mengecek apakah database masih kosong
    :param: gudangdata = dictionary dalam dictionary, bertindak sebagai database
    """

    if len(gudangdata) != 0:
        return True
    else:
        return False


def impordata(perintah, gudangdata):
    """
    Membaca isi file csv dan memasukkannya ke dalam dictionary database
    :param: perintah = list hasil split perintah asli
    :param: gudangdata = dictionary dalam dictionary, bertindak sebagai database
    """

    try:
        if "csv" not in perintah[1].split("."):     # Jika file tidak terdapat ekstensi csv, jangan terima
            return u" \33[43m\33[30m (!) Tipe file tidak dikenal, mohon impor file dengan ekstensi CSV \33[0m"
        else:
            warn = False
            with open(parse(perintah), "r") as file:    # Buka file yang ada di argument
                bukaFile = csv.reader(file)             # Baca menggunakan csv.reader
                counter = 0                             # Hitung jumlah baris

                for baris in bukaFile:
                    if len(baris) != 0:  # Cek apakah baris kosong

                        if (baris[0].upper() in gudangdata) and (warn == False):    # Beri peringatan jika terdapat
                            warn = True                                             # duplikat
                        gudangdata[baris[0].upper()] = {}   # Buat Dictionary baru
                        counter += 1                        # Tambah hitungan jumlah baris

                        for data, tipe in zip(baris, kategori):        # Isi database dengan data
                            gudangdata[baris[0].upper()][tipe] = data  # sesuai dengan kategori

            if counter == 0:    # Kalau tidak ada line yang di import
                return u" \33[43m\33[30m (!) File yang anda buka tidak memiliki data \33[0m"

            if warn:            # Peringatan jika tedapat duplikat
                return u" \33[43m\33[30m (!) BudayaKB mendeteksi adanya duplikat dalam database atau file yang anda impor \33[0m" +\
                       u"\n \33[43m\33[30m Baris terbawah atau data terbaru dianggap data paling relevan.\33[0m\n" \
                       + u" \33[42m\33[30m (i) Terimpor {} baris \33[0m\n".format(counter)

            # Return banyak baris yang dibaca
            return u" \33[42m\33[30m (i) Terimpor {} baris \33[0m\n".format(counter)

    except FileNotFoundError:
        return "\33[43m\33[30m (!) Error: File tidak dapat ditemukan. \33[0m\n"


def ekspordata(perintah, gudangdata):
    """
    Menulis sebuah file csv berdasarkan dictionary database
    :param: perintah = list hasil split perintah asli
    :param: gudangdata = dictionary dalam dictionary, bertindak sebagai database
    """

    try:
        judulEkspor = perintah[1]
        baris = []
        counter = 0
        if ".csv" not in judulEkspor:           # Cek apakah file beformat csv
            judulEkspor = judulEkspor + ".csv"  # Jika tidak, beri ekstensi csv

        for i in gudangdata:                # Siapkan semua isi data setiap key di database
            baris.append(gudangdata[i])     # ke sebuah list

        with open(judulEkspor, "w") as fileEkspor:  # Buka file
            ekspor = csv.DictWriter(fileEkspor, delimiter=",", fieldnames=kategori, lineterminator="\n")

            for data in baris:
                counter += 1
                ekspor.writerow(data)  # Print setiap data di dalam list baris

        return u" \33[42m\33[30m (i) Terekspor {} baris di {} \33[0m\n".format(counter, judulEkspor)

    # Kalau terjadi IOError, jaga-jaga
    except IOError:
        return u" \33[41m (!) Terjadi IOError, mohon cek kembali \33[0m\n"


def carinama(nama, gudangdata):
    """
    Mencari isi database berdasarkan value nama budaya
    :param: nama = Nama budaya
    :param: gudangdata = dictionary dalam dictionary, bertindak sebagai database
    :return: list
    """

    terpilih = []
    if nama != "*":
        terpilih.append(",".join(
            [i for i in gudangdata[nama.upper()].values()]))  # Ambil values berdasarkan key nama, lalu append

    else:
        for keys in gudangdata:
            terpilih.append(",".join(
                [i for i in gudangdata[keys].values()]))  # Ambil semua jika data jika argumen berupa "*"

    return terpilih


def caritipe(tipe, gudangdata):
    """
    Mencari isi database berdasarkan value tipe budaya
    :param: tipe = Nama tipe
    :param: gudangdata = dictionary dalam dictionary, bertindak sebagai database
    :return: list
    """

    terpilih = []

    for data in gudangdata:
        if gudangdata[data]["tipe"].upper() == tipe.upper():                    # Kalau tipe budaya sesuai yang diminta
            terpilih.append(",".join([i for i in gudangdata[data].values()]))   # Append ke sebuah list
            continue

    return terpilih


def cariprov(tipe, gudangdata):
    """
    Mencari isi database berdasarkan value provinsi asal budaya
    :param: tipe = Nama provinsi
    :param: gudangdata = dictionary dalam dictionary, bertindak sebagai database
    :return: list
    """

    terpilih = []
    for data in gudangdata:
        if gudangdata[data]["provinsi"].upper() == tipe.upper():                # Kalau provinsi sesuai dengan diminta
            terpilih.append(",".join([i for i in gudangdata[data].values()]))   # Append ke sebuah list
            continue

    return terpilih


def tambah(datamasuk, gudangdata, kelas):
    """
    Menambahkan data kedalan database, sesuai dengan kategori
    :param: datamasuk = berupa list
    :param: gudangdata = dictionary dalam dictionary, bertindak sebagai database
    :param: kategori = kategori sesuai urutan csv
    :return: bool
    """

    warn = False

    if datamasuk[0].upper() in gudangdata:                  # Jika data yang dimasukan sudah ada, beri pringatan
        warn = True

    gudangdata[datamasuk[0].upper()] = {}                   # Buat key baru yang berisi sebuah dictionary baru
    for data, tipe in zip(datamasuk, kelas):
        gudangdata[datamasuk[0].upper()][tipe] = data

    return warn


def perbarui(newdata, gudangdata):
    """
    Mengecek apakah ada data tersebut di atabase, jika ada maka perbarui
    newData = data yang akan baru
    gudangdata = dictionary dalam dictionary, bertindak sebagai database
    return bool
    """

    index = 0
    for data in gudangdata:
        if gudangdata[data]["namawarisanbudaya"].upper() == newdata[0].upper():
            # Jika ditemukan data yang sama, perbarui setiap isinya dengan data baru
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
    Menghapus data yang ada di databse sesuai dengan nama pada dataHapus
    :param: dataHapus = nama data yang ingin dihapus
    :param: database = dictionary dalam dictionary, bertindak sebagai database
    :return: bool
    """

    for data in gudangdata:
        if datahapus.upper() == data:
            # Jika ditemukan data yang sama, pop data tersebut
            gudangdata.pop(data)
            return True


def bukalink(perintah, gudangdata):
    """
    Membuka link yang ada di referensi
    :param: perintah: list yang berisi list hasil split perintah
    :param: gudangdata: dictionary dalam dictionary, bertindak sebagai database
    """

    link = ''.join([i for i in gudangdata[parse(perintah).upper()]["referenceurl"]])
    # Ambil link yang terdapat didalam database sesuai dengan nama budaya, lalu buka di webbrowser
    return webbrowser.open_new_tab(link)


def statistik(gudangdata):
    """
    Menghasilkan jumlah data yang ada di database
    :param: gudangdata = dictionary dalam dictionary, bertindak sebagai database
    :return: int
    """

    return "Terdapat {} warisan budaya".format(len(gudangdata))  # Banyaknya data


def statistiktipe(gudangdata):
    """
    Menampilkan jumlah data berdasarkan tipe budaya
    :param: gudangdata = dictionary dalam dictionary, bertindak sebagai database
    :return: tuples in list
    """

    listTipe = []
    listJumlah = []
    for data in gudangdata:
        # Memasukkan setiap tipe data di database
        if gudangdata[data]["tipe"] not in listTipe:
            listTipe.append(gudangdata[data]["tipe"])
            continue

    for tipe in listTipe:
        # Menghitung setiap tipe data di database
        count = 0
        for data in gudangdata:
            if gudangdata[data]["tipe"].upper() == tipe.upper():
                count += 1
        listJumlah.append(count)

    return sorted([x for x in zip(listTipe, listJumlah)], key=lambda x: x[1], reverse=True)


def statistikprov(gudangdata):
    """
    Menampilkan jumlah data berdasarkan tipe budaya
    :param: gudangdata = dictionary dalam dictionary, bertindak sebagai database
    :return: tuples in list
    """

    listProv = []
    listJumlah = []
    for data in gudangdata:
        # Memasukkan setiap nama provinsi di database
        if gudangdata[data]["provinsi"] not in listProv:
            listProv.append(gudangdata[data]["provinsi"])
            continue

    for prov in listProv:
        # Menghitung banyak frekuansi setiap provinsi di dalam database
        count = 0
        for data in gudangdata:
            if gudangdata[data]["provinsi"].upper() == prov.upper():
                count += 1
        listJumlah.append(count)

    return sorted([x for x in zip(listProv, listJumlah)], key=lambda x: x[1], reverse=True)


def lihatdata(gudangdata):
    """
    Pretty print gudangdata dengan modul pprint agar mudah dilihat dan di inspeksi
    :param: gudangdata = dictionary dalam dictionary, bertindak sebagai database
    :return: string
    """

    if cekdata(gudangdata):
        # Print database dengan formatting rapi
        pretty = pprint.PrettyPrinter()
        return pretty.pprint(gudangdata)

    else:
        return "Database masih kosong"


def main():
    """
    Main process
    """

    log = []    # Berisi log dari perintah yang dijalankan
    kosong()    # Mengosongkan terminal

    print(banner)       # Print banner

    while True:
        print(separator) # Buat separator di setiap perintah

        try:
            perintah = input("> Masukkan perintah: ").split()

            # IMPOR
            if perintah[0].upper() == "IMPOR":
                print(impordata(perintah, database))
                log.append("Terimpor {}".format(perintah[1]))

            # EKSPOR
            elif perintah[0].upper() == "EKSPOR":
                print(ekspordata(perintah, database))
                log.append("Terekspor {}".format(perintah[1]))

            # CARINAMA
            elif perintah[0].upper() == "CARINAMA":
                if cekdata(database):
                    namaBudaya = parse(perintah)  # Masukan nama budaya yang ingin

                    try:  # dicari ke variabel
                        print(*carinama(namaBudaya, database), sep="\n")
                        print(" ")
                        log.append("CARINAMA {} ditemukan".format(namaBudaya.title()))
                    except KeyError:
                        print(u" \33[41m (!) {} tidak ditemukan \33[0m \n".format(namaBudaya.title()))
                        log.append("CARINAMA {} tidak ditemukan".format(namaBudaya.title()))

                else:
                    print(u" \33[41m (!) Database masih kosong, mohon import terlebih dahulu! \33[0m\n")
                    log.append("CARINAMA, Error database kosong")

            # CARITIPE
            elif perintah[0].upper() == "CARITIPE":
                if cekdata(database):
                    namaTipe = parse(perintah)
                    data = caritipe(namaTipe, database)

                    if len(data) != 0:
                        print(*data, sep="\n")
                        print(u" \33[42m\33[30m (i) *Ditemukan {} {}* \33[0m\n".format(len(data), namaTipe.lower()))
                        log.append("CARITIPE ditemukan {}".format(namaTipe.title()))
                    else:
                        print(u" \33[41m (!) Tidak ditemukan tipe budaya {} di dalam database \33[0m\n".format(
                            namaTipe.upper()))
                        log.append("CARITIPE tidak ditemukan {}".format(namaTipe.title()))

                else:
                    print(u" \33[41m (!) " + "Database masih kosong, mohon import terlebih dahulu! \33[0m\n")
                    log.append("CARINAMA {}, Error database kosong".format(perintah[0].title()))

            # CARIPROV
            elif perintah[0].upper() == "CARIPROV":
                if cekdata(database):
                    prov = parse(perintah)
                    data = cariprov(prov, database)

                    if len(data) != 0:
                        print(*data, sep="\n")
                        print(u" \n\33[42m\33[30m (i) *Ditemukan {} warisan budaya* \33[0m\n".format(len(data)))
                        log.append("CARIPROV {} ditemukan".format(prov.title()))
                    else:
                        print(u" \33[41m (!) Tidak ditemukan budaya dari provinsi {} di dalam database \33[0m\n".format(
                            prov.title()))
                        log.append("CARIPROV {} tidak ditemukan".format(prov.title()))

                else:
                    print(u" \33[41m (!) Database masih kosong, mohon import terlebih dahulu! \33[0m\n")
                    log.append("CARINAMA {}, Error database kosong".format(perintah[0].title()))

            # TAMBAH
            elif perintah[0].upper() == "TAMBAH":
                parsed = parse(perintah)
                if sep in parsed:
                    masukan = parsed.split(sep)

                    if tambah(masukan, database, kategori):
                        print(u" \33[43m\33[30m (!) Ditemukan data yang serupa di database sebelumnya. \33[0m\n" +
                              u" \33[43m\33[30m BudayaKB Lite akan mengubah seluruh data lama dengan data baru. \33[0m\n")

                    print(u" \33[42m\33[30m (i) {} ditambahkan \33[0m\n".format(masukan[0].title()))
                    log.append("TAMBAH {}".format(parsed))

                else:
                    print(u" \33[43m\33[30m (!) Gunakan {} sepagai pembatas antar data. \33[0m\n".format(sep))
                    log.append("TAMBAH failed seperator: {}".format(parsed))

            # UPDATE
            elif perintah[0].upper() == "UPDATE":
                parsed = parse(perintah)
                if sep in parsed:
                    dataBaru = parsed.split(sep)

                    if perbarui(dataBaru, database):
                        print(u" \33[42m\33[30m (i) {} diupdate \33[0m\n".format(dataBaru[0].title()))
                        log.append("UPDATE {}: {}".format(dataBaru[0], parsed))
                    else:
                        print(u" \33[41m (!) Nama budaya yang anda cari tidak ditemukan! \33[0m\n")
                        log.append("UPDATE tidak ditemukan: {}".format(parsed))

                else:
                    print(u" \33[43m\33[30m (!) Gunakan {} sepagai pembatas antar data. \33[0m\n".format(sep))
                    log.append("TAMBAH failed seperator: {}".format(parsed))

            # HAPUS
            elif perintah[0].upper() == "HAPUS":
                dataHapus = parse(perintah)
                if hapus(dataHapus, database):
                    print(u" \33[42m\33[30m (i) {} dihapus \33[0m\n".format(dataHapus.title()))
                    log.append("HAPUS {}".format(dataHapus))
                else:
                    print(u" \33[41m (!) Tidak dapat menemukan {} \33[0m\n".format(dataHapus))
                    log.append("HAPUS, data {} tidak ditemukan".format(dataHapus))

            # LIHATREF
            elif perintah[0].upper() == "LIHATREF":
                parsed = parse(perintah)
                try:
                    bukalink(perintah, database)
                    print(" \33[42m\33[30m (i) Membuka browser \33[0m\n")
                    log.append("LIHATREF {}".format(parsed))

                except KeyError:
                    print(" \33[41m (!) Tidak dapat menemukan {} \33[0m\n".format(parsed))
                    log.append("LIHATREF gagal, data {} tidak ditemukan".format(parsed))

            # LIHATDATA
            elif perintah[0].upper() == "LIHATDATA":
                if len(database) != 0:
                    print("\n")
                    lihatdata(database)
                    print("\n")
                    log.append("LIHATDATA")

                else:
                    print(" \33[41m (!) Database masih kosong. \33[0m")
                    log.append("LIHATDATA gagal, data masih kosong")

            # STAT
            elif perintah[0].upper() == "STAT":
                print(" \33[42m\33[30m (i) " + statistik(database) + u" \33[0m\n")
                log.append("STAT")

            # STATTIPE
            elif perintah[0].upper() == "STATTIPE":
                pemisah = f"\t{'':=<43s}"
                data = statistiktipe(database)

                print("\n\tSTATISTIK DATA BERDASARKAN TIPE:")
                print(pemisah)
                print("\t {:<3s}  {:<15s}{:^30s}".format("No", "Tipe", "Banyak Budaya"))
                print(pemisah)

                for i in range(len(data)):  # Memasukkan data tabel
                    print("\t {:>3d}  {:<15s}{:^30d}".format(i + 1, data[i][0], data[i][1]))

                print(pemisah + "\n")
                log.append("STATTIPE")

            # STATPROV
            elif perintah[0].upper() == "STATPROV":
                pemisah = f"\t{'':=<43s}"
                data = statistikprov(database)

                print("\n\tSTATISTIK DATA BERDASARKAN PROVINSI:")
                print(pemisah)
                print("\t {:<3s}  {:<15s}{:^30s}".format("No", "Provinsi", "Banyak Budaya"))
                print(pemisah)

                for i in range(len(data)):  # Memasukkan data tabel
                    print("\t {:>3d}  {:<15s}{:^30d}".format(i + 1, data[i][0], data[i][1]))

                print(pemisah + "\n")
                log.append("STATPROV")

            # PANDUAN
            elif perintah[0].upper() == "PANDUAN":
                # Print sebuah panduan
                print("\n", guide, "\n")
                log.append("PANDUAN")

            # LOG
            elif perintah[0].upper() == "LOG":
                # Print histori perintah
                print(*log, sep="\n")

            # BERSIHKAN
            elif perintah[0].upper() == "BERSIHKAN":
                # Kosongkan terminal
                kosong()
                print(banner)
                log.append("BERSIHKAN")

            # KELUAR
            elif perintah[0].upper() == "KELUAR":
                # Kosongkan terminal dan beri salam
                kosong()
                print("=" * 68 + "\n{:^68s}\n".format(
                    "~Sampai jumpa, jangan lupa mencintai warisan budaya Indonesia!~") + "=" * 69)
                exit()

            # INVALID COMMAND
            else:
                # Kalau perintah belum ada
                print(u" \33[41m (!) Terjadi kesalahan: Perintah tidak dikenal \33[0m\n")
                log.append("Perintah tidak dikenal")

        except IndexError:
            pass

        except (KeyboardInterrupt, EOFError) as e:
            # Kalau ada yang iseng utak atik
            kosong()
            print("=" * 68 + "\n{:^68s}\n".format(
                "~Sampai jumpa, jangan lupa mencintai warisan budaya Indonesia!~") + "=" * 69)
            exit()


if __name__ == "__main__":
    main()
