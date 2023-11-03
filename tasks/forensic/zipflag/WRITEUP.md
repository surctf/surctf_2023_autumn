# zipflag

По заданию мы узнаем, что нам нужно каким-то способом вытащить файл `flag.txt` и второй файл `gnu.org_licenses_gpl-3.0.txt` является каким-то знакомым. 

Давайте погуглим про возможные способы разархивировать zip архив без пароля. Мы узнаем несколько способов, например:
1. Брутфорс пароля от архива
2. Устаревшее шифрование ZipCrypto

Брутфорс может быть очень долгим, если пароля нет в популярных словарях паролей или если он состоит из большого колличества символов.
А вот использование ZipCrypto будет не сложно проверить. Ещё немного погуглив мы находим интересный [репозиторий](https://github.com/kimci86/bkcrack), который реализовывает атаку на ZipCrypto. Там есть флаг, который показывает каким шифрованием зашифровывались файлы в архиве.

```bash
$ bkcrack -L zipflag.zip
bkcrack 1.5.0 - 2023-11-03
Archive: zipflag.zip
Index Encryption Compression CRC32    Uncompressed  Packed size Name
----- ---------- ----------- -------- ------------ ------------ ----------------
    0 ZipCrypto  Store       97673d00        35149        35161 gnu.org_licenses_gpl-3.0.txt
    1 ZipCrypto  Deflate     03c7b694           48           63 flag.txt
```

Из этих данных мы понимаем, что всё-таки использывался ZipCrypto, а также файл `flag.txt` был сжат (`Deflate`), а `gnu.org_licenses_gpl-3.0.txt` хранится несжатым (`Store`).

Осталось только отыскать этот самый файл в интернете. Попробуем загуглить название файла и по первой [ссылке](https://gnu.org/licenses/gpl-3.0.txt) мы находим полный текст лицензии. 

Интересный факт: если посмотреть на url ссылки (`https://gnu.org/licenses/gpl-3.0.txt`) и на название нашего файла (`gnu.org_licenses_gpl-3.0.txt`), то становится очевидно, что он был скачан с этого сайта.

Теперь попробуем реализовать атаку и узнать ключ шифрования

```bash
$ bkcrack -C zipflag.zip -c gnu.org_licenses_gpl-3.0.txt -p gpl-3.0.txt
bkcrack 1.5.0 - 2023-11-03
[09:02:01] Z reduction using 35142 bytes of known plaintext
16.8 % (5891 / 35142)
[09:02:02] Attack on 35 Z values at index 29396
Keys: 3bbe9612 1c9a221e fb7791fa
97.1 % (34 / 35)
[09:02:02] Keys
3bbe9612 1c9a221e fb7791fa
```

Ключ нашелся, здорово. У нас есть два пути, по полученному ключу попробовать забрутфорсить пароль от архива или с помощью этого ключа создать новый архив с новым паролем. Нам нужно вытащить файл, поэтому давайте просто создадим новый архив со своим паролем.

```bash
$ bkcrack -C zipflag.zip -k 3bbe9612 1c9a221e fb7791fa -U newzipflag.zip lol
bkcrack 1.5.0 - 2023-11-03
[09:05:16] Writing unlocked archive newzipflag.zip with password "lol"
100.0 % (2 / 2)
Wrote unlocked archive.
```

А теперь попробуем прочитать что же написано в `flag.txt`

```bash
$ unzip -P lol -c newzipflag.zip flag.txt
Archive:  newzipflag.zip
  inflating: flag.txt
флаг: surctf_n3vER_S4Ve_fi1Es_w1tH_Z1pCrypt0
```


`flag: surctf_n3vER_S4Ve_fi1Es_w1tH_Z1pCrypt0`
