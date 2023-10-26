# whynot

Идея таска заключалась в том, что ключ и текст имеют одинаковую длину 
```python
len(text*len(key)) == len(key*len(text))
```

Мы знаем длину полученного текста (988 символов) и примерную длину ключа (от 13 до 37 символов).

Пробуем узнать настоящую длину ключа, получаем что длина может быть: 13, 19 или 26 символов.
А текст соответственно в длину: 76, 52 или 38 символов.

Давайте теперь попробуем разобрать какой-нибудь пример со своим текстом и ключом:

```
ТЕКСТ: surctf_flag (11 символов)

КЛЮЧ: youtube (7 символов)
```


При преобразовании получаем одинаковую длину ключа и текста (77 символов):

```
surctf_flagsurctf_flagsurctf_flagsurctf_flagsurctf_flagsurctf_flagsurctf_flag
youtubeyoutubeyoutubeyoutubeyoutubeyoutubeyoutubeyoutubeyoutubeyoutubeyoutube
```

В этом тексте можно заметить: что у ключа первый символ ксорит каждую букву с тексте:

```
surctf_flagsurctf_flagsurctf_flagsurctf_flagsurctf_flagsurctf_flagsurctf_flag
y      y      y      y      y      y      y      y      y      y      y      
```

Если вытащить каждую букву:

```
s f c g _ r a f u l t
```

Осталось только собрать из этих букв наш текст.

Получается мы имеем готовый текст, который заксорин одним символом от 00 до FF, остается только подобрать.

При подборе находим строчку в base64:
```
c3VyY3RmX3doeXlfZDBfdGgxNV93aDR0X2g0cHAzbjVfbjN4Nw==
```

Дешефруем и получаем флаг.

Прикладываю скрипт с решением [dec.py](dec.py).

`flag: surctf_whyy_d0_th15_wh4t_h4pp3n5_n3x7`
