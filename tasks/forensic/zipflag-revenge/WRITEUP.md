# zipflag_revenge

Этот таск был продолжением таска [zipflag](https://github.com/surctf/surctf_2023_autumn/tree/main/tasks/forensic/zipflag), поэтому чтобы понять про что я пишу в этом райтапе, нужно знать [решение того таска](https://github.com/surctf/surctf_2023_autumn/blob/main/tasks/forensic/zipflag/WRITEUP.md).

В таске нам говорят, что нужно вытащить пароль от архива.
Мы видим другой архив в котором находятся `pass.txt` и `gnu.org_licenses_gpl-3.0.txt`. Давайте попробуем снова совершить эти же действия и узнать что находится в `pass.txt`

```bash
$ bkcrack -C zipflag_revenge.zip -c gnu.org_licenses_gpl-3.0.txt -p gpl-3.0.txt
bkcrack 1.5.0 - 2023-11-03
[09:56:05] Z reduction using 35142 bytes of known plaintext
100.0 % (35142 / 35142)
[09:56:08] Attack on 416 Z values at index 28838
Keys: a0e534c6 a60e8723 c3ae4278
31.5 % (131 / 416)
[09:56:08] Keys
a0e534c6 a60e8723 c3ae4278

$ bkcrack -C zipflag_revenge.zip -k a0e534c6 a60e8723 c3ae4278 -U newzipflag_revenge.zip lol
bkcrack 1.5.0 - 2023-11-03
[09:57:08] Writing unlocked archive newzipflag_revenge.zip with password "lol"
100.0 % (2 / 2)
Wrote unlocked archive.

$ unzip -P lol -c newzipflag_revenge.zip pass.txt
Archive:  newzipflag_revenge.zip
  inflating: pass.txt
Пароль начинается с: surctf_can_u_brute_me_

Попробуйте узнать вторую часть пароля!
```

Интересно, получается теперь мы знаем начало пароля и оно уже очень длинное. 

В `bkcrack` есть флаг с помощью которого можно забрутфорсить пароль, но проблема в том, что первые 6 символов находятся моментально, а вот остальные символы находятся от n<sup>i-6</sup>, где i - длина пароля. Получается чтобы найти весь пароль, нам нужно научиться брутфорсить не весь пароль, а только его часть.

Если полазить по репозиторию bkcrack, то можно найти несколько интересных обсуждений, например [это](https://github.com/kimci86/bkcrack/issues/55). Оказывается в этом репозитории есть другой бранч ([prefix](https://github.com/kimci86/bkcrack/tree/prefix)), в котором реализована такая функция. Скачиваем, компилируем и пробуем.

```bash
$ bkcrack -C zipflag_revenge.zip -k a0e534c6 a60e8723 c3ae4278 -r 12 ?p -m "surctf_can_u_brute_me_"
bkcrack 1.5.0 - 2023-11-03
[10:47:10] Recovering password
length 0-6...
length 7...
length 8...
length 9...
length 10...
length 11...
length 12...
18.2 % (1640 / 9025)
[10:50:31] Password
as bytes: 73 75 72 63 74 66 5f 63 61 6e 5f 75 5f 62 72 75 74 65 5f 6d 65 5f 31 38 68 31 66 4e 6f 62 74 36 58 34
as text: surctf_can_u_brute_me_18h1fNobt6X4
```


`flag: surctf_can_u_brute_me_18h1fNobt6X4`
