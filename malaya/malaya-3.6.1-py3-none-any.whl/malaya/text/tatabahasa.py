# this file to store possible shortform, normalized, prefix, postfix, tatabahasa, titles and stopwords
# 1. mix laughing words, laughing
# 2. mix negate words, negate_words
# 3. partial noisy words, partial_noisy
# 4. kata tanya, tanya_list
# 5. kata perintah, perintah_list
# 6. kata pangkal, pangkal_list
# 7. kata bantu, bantu_list
# 8. kata penguat, penguat_list
# 9. kata penegas, penegas_list
# 10. kata nafi, nafi_list
# 11. kata pemeri, pemeri_list
# 12. kata sendi, sendi_list
# 13. kata pembenar, pembenar_list
# 14. number, nombor_list
# 15. suku bilangan, suku_bilangan_list
# 16. kata penerangan, keterangan_list
# 17. kata arah, arah_list
# 18. kata hubung, hubung_list
# 19. ganti nama, gantinama_list
# 20. prefix, permulaan
# 21. postfix, hujung
# 22. postfix malaysian slang, hujung_malaysian
# 23. sound to word, sounds
# 24. word replacement for date string, date_replace
# 25. calon dictionary, calon_dictionary
# 26. stopwords, stopwords
# 27. bi_vowels, bivowels, example, `aa`
# 28. group_compound, group for biconsonant, example, `ng`

GO = 0
PAD = 1
EOS = 2
UNK = 3

alphabet = 'qwertyuiopasdfghjklzxcvbnm'
consonants = 'bcdfghjklmnpqrstvwxyz'
vowels = 'aeiou'

laughing = {
    'huhu',
    'haha',
    'gagaga',
    'hihi',
    'wkawka',
    'wkwk',
    'kiki',
    'keke',
    'huehue',
    'hshs',
    'hoho',
    'hewhew',
    'uwu',
    'sksk',
    'ksks',
    'gituu',
    'gitu',
    'mmeeooww',
    'meow',
    'alhamdulillah',
    'muah',
    'mmuahh',
    'hehe',
    'jahagaha',
    'ahakss',
    'ahksk',
}

partial_noisy = {
    'uwuu',
    'dahl',
    'ergh',
    'herm',
    'huwaa',
    'kooo',
    'gais',
    'siaa',
    'hhmm',
    'hmmm',
    'punyala',
    'lhaa',
    'oiii',
    'ooii',
    'oooi',
    'laaa',
    'uuuh',
    'haaa',
    'adee',
    'dahh',
    'errr',
    'hanaa',
    'hais',
    'leww',
    'yumm',
    'jsis',
    'hsis',
    'yahh',
    'fuhh',
    'haih',
    'meow',
    'aiii',
}

negate_words = {
    'tak',
    'jangan',
    'tidak',
    'enggak',
    'tiada',
    'bukan',
    'usah',
    'tidaklah',
    'jgn',
    'tk',
    'bkn',
    "shouldn't",
    "don't",
    "doesn't",
}

tanya_list = [
    'kenapa',
    'bila',
    'siapa',
    'mengapa',
    'apa',
    'bagaimana',
    'berapa',
    'mana',
]
perintah_list = ['jangan', 'sila', 'tolong', 'harap', 'usah', 'jemput', 'minta']
pangkal_list = [
    'maka',
    'alkisah',
    'arakian',
    'syahdah',
    'adapun',
    'bermula',
    'kalakian',
]
bantu_list = [
    'akan',
    'telah',
    'boleh',
    'mesti',
    'belum',
    'sudah',
    'dapat',
    'masih',
    'harus',
    'hendak',
]
penguat_list = [
    'paling',
    'agak',
    'sungguh',
    'amat',
    'terlalu',
    'nian',
    'benar',
    'paling',
]
penegas_list = ['jua', 'juga', 'sahaja', 'hanya', 'memang', 'lagi', 'pun']
nafi_list = ['bukan', 'tidak', 'tak', 'tiada', 'tidaklah', 'tidakkah']
pemeri_list = ['ialah', 'adalah']
sendi_list = [
    'akan',
    'kepada',
    'terhadap',
    'bagi',
    'untuk',
    'dari',
    'daripada',
    'di',
    'dengan',
    'hingga',
    'sampai',
    'ke',
    'kepada',
    'oleh',
    'pada',
    'sejak',
    'seperti',
    'umpama',
    'bak',
    'tentang',
    'laksanabagai',
    'semenjak',
    'dalam',
    'antara',
]
pembenar_list = ['ya', 'benar', 'betul']
nombor_list = [
    'satu',
    'dua',
    'tiga',
    'empat',
    'lima',
    'enam',
    'tujuh',
    'lapan',
    'sembilan',
    'kosong',
]
suku_bilangan_list = ['per', 'suku', 'setengah', 'separuh', 'tiga suku']
pisahan_list = ['setiap', 'tiap']
keterangan_list = [
    'begitu',
    'begini',
    'demikian',
    'perlahan',
    'cepat',
    'lena',
    'akan',
    'sedang',
    'belum',
    'telah',
    'sekarang',
    'sebentar',
    'semalam',
    'mungkin',
    'agak',
    'barangkali',
    'pasti',
    'tentu',
    'sudah',
    'selalu',
    'kadang',
    'acapkali',
    'sesekali',
    'yang',
]
arah_list = [
    'atas',
    'bawah',
    'tepi',
    'antara',
    'hadapan',
    'utara',
    'sisi',
    'luar',
]
hubung_list = [
    'agar',
    'apabila',
    'atau',
    'bahawa',
    'dan',
    'hingga',
    'jika',
    'jikalau',
    'kecuali',
    'kerana',
    'lalu',
    'manakala',
    'sambil',
    'serta',
    'semenjak',
    'sementara',
    'sungguhpun',
    'supaya',
    'walaupun',
    'tetapi',
    'berkenan',
    'berkenaan',
]
gantinama_list = [
    'aku',
    'saya',
    'hamba',
    'patik',
    'beta',
    'kami',
    'kita',
    'anda',
    'awak',
    'engkau',
    'tuanku',
    'kalian',
    'kamu',
    'baginda',
    'beliau',
    'mereka',
    'ini',
    'itu',
    'sini',
    'situ',
    'sana',
    'kini',
    'dia',
    'rm',
]

permulaan = {
    'bel': 'bel',
    'se': 'se',
    'see': 'se',
    'ter': 'ter',
    'terr': 'ter',
    'men': 'men',
    'menn': 'men',
    'meng': 'meng',
    'mengg': 'meng',
    'mem': 'mem',
    'mm': 'mem',
    'memper': 'memper',
    'di': 'di',
    'ddi': 'di',
    'pe': 'pe',
    'ppe': 'pe',
    'ppee': 'pe',
    'me': 'me',
    'mme': 'mme',
    'ke': 'ke',
    'kee': 'ke',
    'ber': 'ber',
    'berr': 'ber',
    'pen': 'pen',
    'penn': 'pen',
    'per': 'per',
    'perr': 'perr',
}

hujung = {
    'kan': 'kan',
    'kann': 'kan',
    'kah': 'kah',
    'kahh': 'kah',
    'lah': 'lah',
    'lahh': 'lah',
    'tah': 'tah',
    'tahh': 'tah',
    'nya': 'nya',
    'nyaa': 'nya',
    'an': 'an',
    'ann': 'an',
    'wan': 'wan',
    'wann': 'wan',
    'wati': 'wati',
    'watii': 'wati',
    'ita': 'ita',
    'itaa': 'ita',
    'nye': 'nya',
    'nyee': 'nya',
    'nyo': 'nya',
    'nyoo': 'nya',
    'loh': 'lah',
    'lohh': 'lah',
}

hujung_malaysian = ['lah', 'la', 'ler']

sounds = {
    'x': 'tidak',
    'y': 'kenapa',
    'n': 'dan',
    'g': 'pergi',
    's': 'seperti',
    'd': 'di',
    'k': 'ok',
    'u': 'awak',
    't': 'nanti',
    'p': 'pergi',
    'wai': 'kenapa',
    'i': 'saya',
}

tatabahasa_dict = {
    'KT': tanya_list,
    'KP': perintah_list,
    'KPA': pangkal_list,
    'KB': bantu_list,
    'KPENGUAT': penguat_list,
    'KPENEGAS': penegas_list,
    'NAFI': nafi_list,
    'KPEMERI': pemeri_list,
    'KS': sendi_list,
    'KPEMBENAR': pembenar_list,
    'NO': nombor_list,
    'SUKU': suku_bilangan_list,
    'PISAHAN': pisahan_list,
    'KETERANGAN': keterangan_list,
    'ARAH': arah_list,
    'KH': hubung_list,
    'GN': gantinama_list,
}

stopword_tatabahasa = list(
    set(
        tanya_list
        + perintah_list
        + pangkal_list
        + bantu_list
        + penguat_list
        + penegas_list
        + nafi_list
        + pemeri_list
        + sendi_list
        + pembenar_list
        + nombor_list
        + suku_bilangan_list
        + pisahan_list
        + keterangan_list
        + arah_list
        + hubung_list
        + gantinama_list
    )
)

date_replace = {
    'awk': 'awak',
    'ngkau': 'engkau',
    'lps': 'lalu',
    'lepas': 'lalu',
    'mnggu': 'minggu',
    'bln': 'bulan',
    'skrg': 'sekarang',
    'thun': 'tahun',
    'hri': 'hari',
    'minute': 'minit',
    'mnit': 'minit',
    'sec': 'saat',
    'second': 'saat',
    'yesterday': 'semalam',
    'kelmarin': 'kelmarin',
    'smalam': 'semalam',
    'dpan': 'depan',
    'dpn': 'depan',
    'esk': 'esok',
    'pagi': 'AM',
    'pgi': 'AM',
    'morning': 'AM',
    'tengahari': 'PM',
    'tngahari': 'PM',
    'petang': 'PM',
    'ptg': 'PM',
    'malam': 'PM',
    'semalam': 'semalam',
    'pkul': 'pukul',
}

stopwords_calon = [
    'datuk',
    'bin',
    'hj',
    'haji',
    'bn',
    'bnt',
    'prof',
    'binti',
    'dr',
    'ustaz',
    'mejar',
    'ir',
    'md',
    'tuan',
    'puan',
    'yb',
    'ustazah',
    'cikgu',
    'dato',
    'dsp',
]

calon_dictionary = {
    'dr': 'Doktor',
    'yb': 'Yang Berhormat',
    'hj': 'Haji',
    'ybm': 'Yang Berhormat Mulia',
    'tyt': 'Tuan Yang Terutama',
    'yab': 'Yang Berhormat',
    'ybm': 'Yang Berhormat Mulia',
    'yabhg': 'Yang Amat Berbahagia',
    'ybhg': 'Yang Berbahagia',
    'miss': 'Cik',
}
stopwords = [
    'not',
    'ada',
    'inikah',
    'sampai',
    'adakah',
    'inilah',
    'sana',
    'adakan',
    'itu',
    'sangat',
    'adalah',
    'itukah',
    'sangatlah',
    'adanya',
    'itulah',
    'saya',
    'adapun',
    'jadi',
    'se',
    'agak',
    'jangan',
    'seandainya',
    'agar',
    'namun',
    'janganlah',
    'sebab',
    'akan',
    'cer',
    'jika',
    'sebagai',
    'aku',
    'usahlah',
    'begitu',
    'cuba',
    'jikalau',
    'sebagaimana',
    'akulah',
    'jua',
    'sebanyak',
    'akupun',
    'juapun',
    'dpt',
    'sebelum',
    'al',
    'juga',
    'sebelummu',
    'alangkah',
    'kalau',
    'sebelumnya',
    'allah',
    'kami',
    'sebenarnya',
    'amat',
    'tengku',
    'kamikah',
    'ckp',
    'mmg',
    'secara',
    'antara',
    'justeru',
    'kamipun',
    'sedang',
    'antaramu',
    'bin',
    'binti',
    'datuk',
    'dato',
    'jumlah',
    'kamu',
    'sedangkan',
    'antaranya',
    'kamukah',
    'sedikit',
    'apa',
    'kamupun',
    'sedikitpun',
    'apa-apa',
    'katakan',
    'segala',
    'dgn',
    'apabila',
    'ke',
    'takde',
    'kat',
    'takda',
    'sehingga',
    'apakah',
    'kecuali',
    'sejak',
    'apapun',
    'kelak',
    'sekalian',
    'atas',
    'tadi',
    'cer',
    'kembali',
    'sekalipun',
    'atasmu',
    'kemudian',
    'sekarang',
    'atasnya',
    'kepada',
    'sekitar',
    'atau',
    'kepadaku',
    'selain',
    'ataukah',
    'kepadakulah',
    'selalu',
    'ataupun',
    'kepadamu',
    'selama',
    'bagaimana',
    'kepadanya',
    'selama-lamanya',
    'bagaimanakah',
    'kepadanyalah',
    'seluruh',
    'bagi',
    'kerana',
    'seluruhnya',
    'bagimu',
    'kerananya',
    'sementara',
    'baginya',
    'kesan',
    'byk',
    'semua',
    'bahawa',
    'ketika',
    'semuanya',
    'bahawasanya',
    'wdir',
    'met',
    'dew',
    'kini',
    'haram',
    'haramm',
    'harem',
    'haremm',
    'semula',
    'bahkan',
    'manakala',
    'selepas',
    'kita',
    'senantiasa',
    'bahwa',
    'ku',
    'sendiri',
    'banyak',
    'kurang',
    'sentiasa',
    'banyaknya',
    'lagi',
    'seolah',
    'barangsiapa',
    'lain',
    'seolah-olah',
    'bawah',
    'lalu',
    'seorangpun',
    'beberapa',
    'ever',
    'got',
    'sane',
    'let',
    'eng',
    'dont',
    "'ve",
    'even',
    'lamanya',
    'separuh',
    'begitu',
    'langsung',
    'sepatutnya',
    'begitupun',
    'lebih',
    'seperti',
    'belaka',
    'maha',
    'seraya',
    'belum',
    'mahu',
    'sering',
    'belumkah',
    'mahukah',
    'pagi',
    'malam',
    'petang',
    'siang',
    'lepas',
    'awak',
    'serta',
    'berada',
    'mahupun',
    'seseorang',
    'berapa',
    'maka',
    'sesiapa',
    'berikan',
    'malah',
    'sesuatu',
    'beriman',
    'wasalam',
    'wsalam',
    'assalamualaikum',
    'salam',
    'assalam',
    'asalam',
    'waalaikumussalam',
    'mana',
    'sesudah',
    'berkenaan',
    'manakah',
    'satu',
    'dua',
    'tiga',
    'empat',
    'lima',
    'enam',
    'tujuh',
    'lapan',
    'sebilan',
    'sepuluh',
    'sebelas',
    'belas',
    'puluh',
    'ratus',
    'seratus',
    'seribu',
    'sejuta',
    'juta',
    'masa',
    'sesudahnya',
    'berupa',
    'manapun',
    'sesungguhnya',
    'beserta',
    'masih',
    'sesungguhnyakah',
    'biarpun',
    'masing',
    'guna',
    'setelah',
    'bila',
    'masing-masing',
    'setiap',
    'bilakah',
    'melainkan',
    'nk',
    'siapa',
    'meh',
    'bilamana',
    'memang',
    'siapakah',
    'lol',
    'macam',
    'tgh',
    'tengah',
    'atas',
    'bawah',
    'perghh',
    'pergh',
    'kiri',
    'buat',
    'leh',
    'kanan',
    'mcm',
    'bisa',
    'mempunyai',
    'sini',
    'boleh',
    'mendapat',
    'situ',
    'bukan',
    'mendapati',
    'situlah',
    'bukankah',
    'mendapatkan',
    'suatu',
    'as',
    'yg',
    'kpd',
    'bukanlah',
    'mengadakan',
    'sudah',
    'dahulu',
    'mengapa',
    'sudahkah',
    'dalam',
    'dlm',
    'mengapakah',
    'sungguh',
    'dalamnya',
    'mengenai',
    'sungguhpun',
    'dan',
    'menjadi',
    'supaya',
    'bole',
    'blum',
    'dapat',
    'menyebabkan',
    'tadinya',
    'dapati',
    'menyebabkannya',
    'tahukah',
    'dapatkah',
    'mereka',
    'jgn',
    'tak',
    'dapatlah',
    'kau',
    'merekalah',
    'tahun',
    'tanpa',
    'dari',
    'merekapun',
    'tanya',
    'daripada',
    'meskipun',
    'tanyakanlah',
    'daripadaku',
    'mu',
    'tapi',
    'daripadamu',
    'nescaya',
    'telah',
    'daripadanya',
    'niscaya',
    'tentang',
    'demi',
    'nya',
    'tentu',
    'demikian',
    'olah',
    'terdapat',
    'demikianlah',
    'oleh',
    'terhadap',
    'dengan',
    'orang',
    'terhadapmu',
    'dengannya',
    'pada',
    'dah',
    'den',
    'hoi',
    'huih',
    'jom',
    'joom',
    'tok',
    'bang',
    'abang',
    'kak',
    'kakak',
    'int',
    'jd',
    'atuk',
    'nenek',
    'ayah',
    'mak',
    'mama',
    'baba',
    'gg',
    'termasuk',
    'di',
    'padahal',
    'terpaksa',
    'dia',
    'padamu',
    'tertentu',
    'dialah',
    'padanya',
    'tetapi',
    'didapat',
    'paling',
    'tiada',
    'xkan',
    'xleh',
    'xtahu',
    'tahu',
    'helai',
    'ketul',
    'biar',
    'keb',
    'ust',
    'dorang',
    'ehh',
    'tetap',
    'tryna',
    'shit',
    'xda',
    'xde',
    'didapati',
    'para',
    'tiadakah',
    'dimanakah',
    'xkira',
    'bul',
    'pasti',
    'tiadalah',
    'engkau',
    'patut',
    'tiap',
    'engkaukah',
    'nak',
    'sahaja',
    'saje',
    'keje',
    'pastu',
    'pon',
    'pun',
    'keja',
    'patutkah',
    'tiap-tiap',
    'engkaulah',
    'per',
    'tidak',
    'disebabkan',
    'sebab',
    'engkaupun',
    'pergilah',
    'tidakkah',
    'hai',
    'perkara',
    'tidaklah',
    'hampir',
    'perkaranya',
    'turut',
    'hampir-hampir',
    'perlu',
    'bt',
    'bn',
    'tun',
    'haji',
    'untuk',
    'hanya',
    'pernah',
    "'s",
    'org',
    'untukmu',
    'hanyalah',
    'pertama',
    'wahai',
    'hendak',
    'woi',
    'wui',
    'pula',
    'hj',
    'photo',
    'video',
    'ir',
    'tuan',
    'yb',
    'puan',
    'walau',
    'prof',
    'hendaklah',
    'pun',
    'walaupun',
    'hingga',
    'sahaja',
    'keb',
    'bir',
    'tetap',
    'utk',
    'nah',
    'bar',
    'last',
    'ya',
    'tan',
    'wan',
    'sri',
    'dr',
    'ia',
    'sebaliknya',
    'adalah',
    'sahaja',
    'yaini',
    'iaitu',
    'saling',
    'yaitu',
    'ialah',
    'sama',
    'yakni',
    'ianya',
    'sama-sama',
    'yang',
    'inginkah',
    'samakah',
    'ini',
    'sambil',
    'beliau',
    'ada',
    'adalah',
    'adanya',
    'adapun',
    'agak',
    'agaknya',
    'agar',
    'akan',
    'akankah',
    'akhir',
    'akhiri',
    'akhirnya',
    'aku',
    'akulah',
    'amat',
    'amatlah',
    'anda',
    'andalah',
    'antar',
    'antara',
    'antaranya',
    'apa',
    'apaan',
    'apabila',
    'apakah',
    'apalagi',
    'apatah',
    'artinya',
    'asal',
    'asalkan',
    'atas',
    'atau',
    'ataukah',
    'ataupun',
    'awal',
    'awalnya',
    'bagai',
    'bagaikan',
    'bagaimana',
    'bagaimanakah',
    'bagaimanapun',
    'bagi',
    'bagian',
    'bahkan',
    'bahwa',
    'bahwasanya',
    'baik',
    'bakal',
    'bakalan',
    'balik',
    'banyak',
    'bapak',
    'baru',
    'bawah',
    'beberapa',
    'begini',
    'beginian',
    'beginikah',
    'beginilah',
    'begitu',
    'begitukah',
    'begitulah',
    'begitupun',
    'bekerja',
    'belakang',
    'belakangan',
    'belum',
    'belumlah',
    'benar',
    'benarkah',
    'benarlah',
    'berada',
    'berakhir',
    'berakhirlah',
    'berakhirnya',
    'berapa',
    'berapakah',
    'berapalah',
    'berapapun',
    'berarti',
    'berawal',
    'berbagai',
    'berdatangan',
    'beri',
    'berikan',
    'berikut',
    'berikutnya',
    'berjumlah',
    'berkali-kali',
    'berkata',
    'berkehendak',
    'berkeinginan',
    'berkenaan',
    'berlainan',
    'berlalu',
    'berlangsung',
    'berlebihan',
    'bermacam',
    'bermacam-macam',
    'bermaksud',
    'bermula',
    'bersama',
    'bersama-sama',
    'bersiap',
    'bersiap-siap',
    'bertanya',
    'bertanya-tanya',
    'berturut',
    'berturut-turut',
    'bertutur',
    'berujar',
    'berupa',
    'besar',
    'betul',
    'betulkah',
    'biasa',
    'biasanya',
    'bila',
    'bilakah',
    'bisa',
    'bisakah',
    'boleh',
    'bolehkah',
    'bolehlah',
    'buat',
    'bukan',
    'bukankah',
    'bukanlah',
    'bukannya',
    'bulan',
    'bung',
    'cara',
    'caranya',
    'cukup',
    'cukupkah',
    'cukuplah',
    'cuma',
    'dahulu',
    'dalam',
    'dan',
    'dapat',
    'dari',
    'daripada',
    'datang',
    'dekat',
    'demi',
    'demikian',
    'demikianlah',
    'dengan',
    'depan',
    'di',
    'dia',
    'diakhiri',
    'diakhirinya',
    'dialah',
    'diantara',
    'diantaranya',
    'diberi',
    'diberikan',
    'diberikannya',
    'dibuat',
    'dibuatnya',
    'didapat',
    'didatangkan',
    'digunakan',
    'diibaratkan',
    'diibaratkannya',
    'diingat',
    'diingatkan',
    'diinginkan',
    'dijawab',
    'dijelaskan',
    'dijelaskannya',
    'dikarenakan',
    'dikatakan',
    'dikatakannya',
    'dikerjakan',
    'diketahui',
    'diketahuinya',
    'dikira',
    'dilakukan',
    'dilalui',
    'dilihat',
    'dimaksud',
    'dimaksudkan',
    'dimaksudkannya',
    'dimaksudnya',
    'diminta',
    'dimintai',
    'dimisalkan',
    'dimulai',
    'dimulailah',
    'dimulainya',
    'dimungkinkan',
    'dini',
    'dipastikan',
    'diperbuat',
    'diperbuatnya',
    'dipergunakan',
    'diperkirakan',
    'diperlihatkan',
    'diperlukan',
    'diperlukannya',
    'dipersoalkan',
    'dipertanyakan',
    'dipunyai',
    'diri',
    'dirinya',
    'disampaikan',
    'disebut',
    'disebutkan',
    'disebutkannya',
    'disini',
    'disinilah',
    'ditambahkan',
    'ditandaskan',
    'ditanya',
    'ditanyai',
    'ditanyakan',
    'ditegaskan',
    'ditujukan',
    'ditunjuk',
    'ditunjuki',
    'ditunjukkan',
    'ditunjukkannya',
    'ditunjuknya',
    'dituturkan',
    'dituturkannya',
    'diucapkan',
    'diucapkannya',
    'diungkapkan',
    'dong',
    'dua',
    'dulu',
    'empat',
    'enggak',
    'enggaknya',
    'entah',
    'entahlah',
    'guna',
    'gunakan',
    'hal',
    'hampir',
    'hanya',
    'hanyalah',
    'hari',
    'harus',
    'haruslah',
    'harusnya',
    'hendak',
    'hendaklah',
    'hendaknya',
    'hingga',
    'ia',
    'ialah',
    'ibarat',
    'ibaratkan',
    'ibaratnya',
    'ibu',
    'ikut',
    'ingat',
    'ingat-ingat',
    'ingin',
    'inginkah',
    'inginkan',
    'ini',
    'inikah',
    'inilah',
    'itu',
    'itukah',
    'itulah',
    'jadi',
    'jadilah',
    'jadinya',
    'jangan',
    'jangankan',
    'janganlah',
    'jauh',
    'jawab',
    'jawaban',
    'jawabnya',
    'jelas',
    'jelaskan',
    'jelaslah',
    'jelasnya',
    'jika',
    'jikalau',
    'juga',
    'jumlah',
    'jumlahnya',
    'justru',
    'kala',
    'kalau',
    'kalaulah',
    'kalaupun',
    'kalian',
    'kami',
    'kamilah',
    'kamu',
    'kamulah',
    'kan',
    'kapan',
    'kapankah',
    'kapanpun',
    'karena',
    'karenanya',
    'kasus',
    'kata',
    'katakan',
    'katakanlah',
    'katanya',
    'ke',
    'keadaan',
    'kebetulan',
    'kecil',
    'kedua',
    'keduanya',
    'keinginan',
    'kelamaan',
    'kelihatan',
    'kelihatannya',
    'kelima',
    'keluar',
    'kembali',
    'kemudian',
    'kemungkinan',
    'kemungkinannya',
    'kenapa',
    'kepada',
    'kepadanya',
    'kesampaian',
    'keseluruhan',
    'keseluruhannya',
    'keterlaluan',
    'ketika',
    'khususnya',
    'kini',
    'kinilah',
    'kira',
    'kira-kira',
    'kiranya',
    'kita',
    'kitalah',
    'kok',
    'kurang',
    'lagi',
    'lagian',
    'lah',
    'lain',
    'lainnya',
    'lalu',
    'lama',
    'lamanya',
    'lanjut',
    'lanjutnya',
    'lebih',
    'lewat',
    'lima',
    'luar',
    'macam',
    'maka',
    'makanya',
    'makin',
    'malah',
    'malahan',
    'mampu',
    'mampukah',
    'mana',
    'manakala',
    'manalagi',
    'masa',
    'masalah',
    'masalahnya',
    'masih',
    'masihkah',
    'masing',
    'masing-masing',
    'mau',
    'maupun',
    'melainkan',
    'melakukan',
    'melalui',
    'melihat',
    'melihatnya',
    'memang',
    'memastikan',
    'memberi',
    'memberikan',
    'membuat',
    'memerlukan',
    'memihak',
    'meminta',
    'memintakan',
    'memisalkan',
    'memperbuat',
    'mempergunakan',
    'memperkirakan',
    'memperlihatkan',
    'mempersiapkan',
    'mempersoalkan',
    'mempertanyakan',
    'mempunyai',
    'memulai',
    'memungkinkan',
    'menaiki',
    'menambahkan',
    'menandaskan',
    'menanti',
    'menanti-nanti',
    'menantikan',
    'menanya',
    'menanyai',
    'menanyakan',
    'mendapat',
    'mendapatkan',
    'mendatang',
    'mendatangi',
    'mendatangkan',
    'menegaskan',
    'mengakhiri',
    'mengapa',
    'mengatakan',
    'mengatakannya',
    'mengenai',
    'mengerjakan',
    'mengetahui',
    'menggunakan',
    'menghendaki',
    'mengibaratkan',
    'mengibaratkannya',
    'mengingat',
    'mengingatkan',
    'menginginkan',
    'mengira',
    'mengucapkan',
    'mengucapkannya',
    'mengungkapkan',
    'menjadi',
    'menjawab',
    'menjelaskan',
    'menuju',
    'menunjuk',
    'menunjuki',
    'menunjukkan',
    'menunjuknya',
    'menurut',
    'menuturkan',
    'menyampaikan',
    'menyangkut',
    'menyatakan',
    'menyebutkan',
    'menyeluruh',
    'menyiapkan',
    'merasa',
    'mereka',
    'merekalah',
    'merupakan',
    'meski',
    'meskipun',
    'meyakini',
    'meyakinkan',
    'minta',
    'mirip',
    'misal',
    'misalkan',
    'misalnya',
    'mula',
    'mulai',
    'mulailah',
    'mulanya',
    'mungkin',
    'mungkinkah',
    'nah',
    'naik',
    'namun',
    'nanti',
    'nantinya',
    'nyaris',
    'nyatanya',
    'oleh',
    'olehnya',
    'pada',
    'padahal',
    'padanya',
    'pak',
    'paling',
    'panjang',
    'pantas',
    'para',
    'pasti',
    'pastilah',
    'penting',
    'pentingnya',
    'per',
    'percuma',
    'perlu',
    'perlukah',
    'perlunya',
    'pernah',
    'persoalan',
    'pertama',
    'pertama-tama',
    'pertanyaan',
    'pertanyakan',
    'pihak',
    'pihaknya',
    'pukul',
    'pula',
    'pun',
    'punya',
    'rasa',
    'rasanya',
    'rata',
    'rupanya',
    'saat',
    'saatnya',
    'sahaja',
    'sajalah',
    'saling',
    'sama',
    'sama-sama',
    'sambil',
    'sampai',
    'sampai-sampai',
    'sampaikan',
    'sana',
    'sangat',
    'sangatlah',
    'satu',
    'saya',
    'sayalah',
    'se',
    'sebab',
    'sebabnya',
    'sebagai',
    'sebagaimana',
    'sebagainya',
    'sebagian',
    'sebaik',
    'sebaik-baiknya',
    'sebaiknya',
    'sebaliknya',
    'sebanyak',
    'sebegini',
    'sebegitu',
    'sebelum',
    'sebelumnya',
    'sebenarnya',
    'seberapa',
    'sebesar',
    'sebetulnya',
    'sebisanya',
    'sebuah',
    'sebut',
    'sebutlah',
    'sebutnya',
    'secara',
    'secukupnya',
    'sedang',
    'sedangkan',
    'sedemikian',
    'sedikit',
    'sedikitnya',
    'seenaknya',
    'segala',
    'segalanya',
    'segera',
    'seharusnya',
    'sehingga',
    'seingat',
    'sejak',
    'sejauh',
    'sejenak',
    'sejumlah',
    'sekadar',
    'sekadarnya',
    'sekali',
    'sekali-kali',
    'sekalian',
    'sekaligus',
    'sekalipun',
    'sekarang',
    'sekarang',
    'sekecil',
    'seketika',
    'sekiranya',
    'sekitar',
    'sekitarnya',
    'sekurang-kurangnya',
    'sekurangnya',
    'sela',
    'selain',
    'selaku',
    'selalu',
    'selama',
    'selama-lamanya',
    'selamanya',
    'selanjutnya',
    'seluruh',
    'seluruhnya',
    'semacam',
    'semakin',
    'semampu',
    'semampunya',
    'semasa',
    'semasih',
    'semata',
    'semata-mata',
    'semaunya',
    'sementara',
    'semisal',
    'semisalnya',
    'sempat',
    'semua',
    'semuanya',
    'semula',
    'sendiri',
    'sendirian',
    'sendirinya',
    'seolah',
    'seolah-olah',
    'seorang',
    'sepanjang',
    'sepantasnya',
    'sepantasnyalah',
    'seperlunya',
    'seperti',
    'sepertinya',
    'sepihak',
    'sering',
    'seringnya',
    'serta',
    'serupa',
    'sesaat',
    'sesama',
    'sesampai',
    'sesegera',
    'sesekali',
    'seseorang',
    'sesuatu',
    'sesuatunya',
    'sesudah',
    'sesudahnya',
    'setelah',
    'setempat',
    'setengah',
    'seterusnya',
    'setiap',
    'setiba',
    'setibanya',
    'setidak-tidaknya',
    'setidaknya',
    'setinggi',
    'seusai',
    'sewaktu',
    'siap',
    'siapa',
    'siapakah',
    'siapapun',
    'sini',
    'sinilah',
    'soal',
    'soalnya',
    'suatu',
    'sudah',
    'sudahkah',
    'sudahlah',
    'supaya',
    'tadi',
    'tadinya',
    'tahu',
    'tahun',
    'tak',
    'tambah',
    'tambahnya',
    'tampak',
    'tampaknya',
    'tandas',
    'tandasnya',
    'tanpa',
    'tanya',
    'tanyakan',
    'tanyanya',
    'tapi',
    'tegas',
    'tegasnya',
    'telah',
    'tempat',
    'tengah',
    'tentang',
    'tentu',
    'tentulah',
    'tentunya',
    'tepat',
    'terakhir',
    'terasa',
    'terbanyak',
    'terdahulu',
    'terdapat',
    'terdiri',
    'terhadap',
    'terhadapnya',
    'teringat',
    'teringat-ingat',
    'terjadi',
    'terjadilah',
    'terjadinya',
    'terkira',
    'terlalu',
    'terlebih',
    'terlihat',
    'termasuk',
    'ternyata',
    'tersampaikan',
    'tersebut',
    'tersebutlah',
    'tertentu',
    'tertuju',
    'terus',
    'terutama',
    'tetap',
    'tetapi',
    'tiap',
    'tiba',
    'tiba-tiba',
    'tidak',
    'tidakkah',
    'tidaklah',
    'tiga',
    'tinggi',
    'toh',
    'tunjuk',
    'turut',
    'tutur',
    'tuturnya',
    'ucap',
    'ucapnya',
    'ujar',
    'ujarnya',
    'umum',
    'umumnya',
    'ungkap',
    'ungkapnya',
    'untuk',
    'usah',
    'usai',
    'waduh',
    'wah',
    'wahai',
    'waktu',
    'waktunya',
    'walau',
    'walaupun',
    'wong',
    'yaitu',
    'yakin',
    'yakni',
    'yang',
]

group_compound = [
    'ng',
    'nt',
    'mp',
    'gs',
    'rb',
    'th',
    'st',
    'mb',
    'ny',
    'gk',
    'ky',
    'km',
    'gd',
    'nd',
]

"""
mw = []
for w in malaya.texts._malay_words._malay_words:
    mw.append(''.join([v for v in w if v in vowels]))
subwords = []
for w in mw:
    for i in range(0, len(w), 4):
        subwords.append(w[i: i + 4])
subwords = [w for w in subwords if len(w) == 4]
u, c = np.unique(subwords, return_counts = True)
quad_vowels = u
"""

quad_vowels = [
    'aaaa',
    'aaai',
    'aaao',
    'aaau',
    'aaea',
    'aaee',
    'aaei',
    'aaeo',
    'aaeu',
    'aaia',
    'aaie',
    'aaii',
    'aaio',
    'aaiu',
    'aaoa',
    'aaoe',
    'aaoi',
    'aaoo',
    'aaou',
    'aaua',
    'aaue',
    'aaui',
    'aauu',
    'aeaa',
    'aeae',
    'aeai',
    'aeei',
    'aeia',
    'aeie',
    'aeii',
    'aeio',
    'aeiu',
    'aeoa',
    'aeoe',
    'aeoi',
    'aeoo',
    'aeua',
    'aeui',
    'aiaa',
    'aiae',
    'aiai',
    'aiao',
    'aiau',
    'aiea',
    'aiee',
    'aiei',
    'aieo',
    'aieu',
    'aiia',
    'aiie',
    'aiii',
    'aiio',
    'aiiu',
    'aioa',
    'aioe',
    'aioi',
    'aioo',
    'aiou',
    'aiua',
    'aiui',
    'aiuu',
    'aoaa',
    'aoai',
    'aoao',
    'aoau',
    'aoea',
    'aoee',
    'aoei',
    'aoeo',
    'aoeu',
    'aoia',
    'aoie',
    'aoii',
    'aoio',
    'aoiu',
    'aooa',
    'aooe',
    'aooi',
    'aooo',
    'aoou',
    'aoui',
    'auaa',
    'auae',
    'auai',
    'auau',
    'auea',
    'auei',
    'aueo',
    'aueu',
    'auia',
    'auie',
    'auii',
    'auio',
    'auiu',
    'auoa',
    'auoe',
    'auoi',
    'auoo',
    'auua',
    'auui',
    'auuu',
    'eaaa',
    'eaae',
    'eaai',
    'eaao',
    'eaau',
    'eaea',
    'eaee',
    'eaei',
    'eaeo',
    'eaeu',
    'eaia',
    'eaie',
    'eaii',
    'eaio',
    'eaiu',
    'eaoa',
    'eaoi',
    'eaoo',
    'eaua',
    'eaue',
    'eaui',
    'eauu',
    'eeaa',
    'eeae',
    'eeai',
    'eeao',
    'eeau',
    'eeea',
    'eeee',
    'eeei',
    'eeeo',
    'eeeu',
    'eeia',
    'eeie',
    'eeii',
    'eeiu',
    'eeoa',
    'eeoe',
    'eeoi',
    'eeoo',
    'eeou',
    'eeua',
    'eeui',
    'eeuu',
    'eiaa',
    'eiae',
    'eiai',
    'eiao',
    'eiau',
    'eiea',
    'eiee',
    'eiei',
    'eiia',
    'eiie',
    'eiii',
    'eiio',
    'eiiu',
    'eioa',
    'eioe',
    'eioi',
    'eioo',
    'eiou',
    'eiua',
    'eiui',
    'eiuu',
    'eoaa',
    'eoae',
    'eoai',
    'eoau',
    'eoea',
    'eoee',
    'eoei',
    'eoeo',
    'eoeu',
    'eoia',
    'eoie',
    'eoii',
    'eoio',
    'eoiu',
    'eooa',
    'eooe',
    'eooi',
    'eooo',
    'eoua',
    'eoue',
    'eoui',
    'euaa',
    'euae',
    'euai',
    'euau',
    'euea',
    'euei',
    'eueo',
    'euia',
    'euii',
    'euio',
    'euoa',
    'euoi',
    'euoo',
    'euua',
    'euue',
    'euui',
    'euuu',
    'iaaa',
    'iaai',
    'iaau',
    'iaea',
    'iaee',
    'iaei',
    'iaia',
    'iaie',
    'iaii',
    'iaiu',
    'iaoa',
    'iaoi',
    'iaoo',
    'iaua',
    'iaue',
    'iaui',
    'iauu',
    'ieaa',
    'ieai',
    'ieao',
    'ieau',
    'ieea',
    'ieee',
    'ieei',
    'ieeo',
    'ieeu',
    'ieia',
    'ieie',
    'ieii',
    'ieio',
    'ieiu',
    'ieoa',
    'ieoe',
    'ieoi',
    'ieoo',
    'ieua',
    'ieui',
    'ieuu',
    'iiaa',
    'iiai',
    'iiao',
    'iiau',
    'iiea',
    'iiee',
    'iieu',
    'iiia',
    'iiie',
    'iiii',
    'iiiu',
    'iioa',
    'iioe',
    'iioo',
    'iiua',
    'iiui',
    'ioaa',
    'ioai',
    'ioao',
    'ioau',
    'ioea',
    'ioee',
    'ioei',
    'ioeo',
    'ioeu',
    'ioia',
    'ioie',
    'ioii',
    'ioio',
    'ioiu',
    'iooa',
    'iooe',
    'iooi',
    'ioua',
    'ioue',
    'iuaa',
    'iuae',
    'iuai',
    'iuao',
    'iuau',
    'iuea',
    'iuia',
    'iuii',
    'iuiu',
    'iuoa',
    'iuua',
    'iuui',
    'oaaa',
    'oaai',
    'oaea',
    'oaee',
    'oaei',
    'oaia',
    'oaie',
    'oaii',
    'oaio',
    'oaiu',
    'oaoa',
    'oaoe',
    'oaoi',
    'oaua',
    'oeae',
    'oeai',
    'oeao',
    'oeea',
    'oeei',
    'oeeo',
    'oeia',
    'oeii',
    'oeio',
    'oeiu',
    'oeoa',
    'oeoe',
    'oeua',
    'oiaa',
    'oiai',
    'oiao',
    'oiau',
    'oiea',
    'oiei',
    'oieo',
    'oiia',
    'oiie',
    'oiii',
    'oiiu',
    'oioe',
    'oioi',
    'oioo',
    'oiou',
    'oiua',
    'oiue',
    'oiui',
    'oiuu',
    'ooaa',
    'ooai',
    'ooau',
    'ooea',
    'ooee',
    'ooei',
    'ooeu',
    'ooia',
    'ooie',
    'ooii',
    'ooio',
    'ooiu',
    'oooa',
    'oooi',
    'oooo',
    'ooui',
    'oouu',
    'ouaa',
    'ouai',
    'ouea',
    'ouia',
    'ouie',
    'ouii',
    'ouiu',
    'uaaa',
    'uaai',
    'uaau',
    'uaea',
    'uaei',
    'uaeu',
    'uaia',
    'uaie',
    'uaii',
    'uaiu',
    'uaoa',
    'uaoe',
    'uaoi',
    'uaua',
    'uaui',
    'ueaa',
    'ueai',
    'ueee',
    'ueeo',
    'ueia',
    'ueie',
    'ueoi',
    'uiaa',
    'uiae',
    'uiai',
    'uiau',
    'uiea',
    'uiei',
    'uiia',
    'uiii',
    'uioa',
    'uioe',
    'uiue',
    'uiui',
    'uiuu',
    'uoao',
    'uoia',
    'uoiu',
    'uooa',
    'uuaa',
    'uuae',
    'uuai',
    'uuau',
    'uuea',
    'uuei',
    'uueo',
    'uueu',
    'uuia',
    'uuie',
    'uuii',
    'uuio',
    'uuoa',
    'uuoe',
    'uuua',
    'uuui',
    'uuuu',
]
