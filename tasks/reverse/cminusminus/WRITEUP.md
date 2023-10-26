# cminusminus

## Описание
> Год 199X, эпоха старых персональных компьютеров. Вы - молодой хакер, и однажды, просматривая антикварные магазины, вы обнаружили забытый в пыльном уголке старый ПК.<br><br> Это аппарат, которым пользовались ваши родители или даже бабушка и дедушка. На его мониторе мерцает загадочное приглашение к командной строке, а клавиши скрипят под вашими пальцами.<br><br>Сможете ли вы разгадать тайны старых ПК и вернуться во времена, когда компьютеры были менее мощными, но не менее захватывающими? Погрузитесь в старую компьютерную атмосферу и откройте тайны программы, скрытой в этом аппарате времен и памяти.<br><br>Исходный код:<br><br><a href="cminusminus" download>cminusminus</a>

Автор: [cornael](https://t.me/cornael)

## Анализ файла
Проанализируем файл при помощи [онлайн декомпилятора](https://dogbolt.org/)

GHIDRA:
```c

undefined8 main(void)

{
  int iVar1;
  time_t tVar2;
  char local_81;
  uint local_80;
  uint local_7c;
  char local_77;
  char local_76;
  char local_75;
  char local_74;
  char local_73;
  char local_72;
  char local_71;
  char local_70;
  char local_6f;
  char local_6e;
  char local_6d;
  char local_6c;
  char local_6b;
  undefined local_6a;
  char local_69;
  char local_68;
  char local_67;
  char local_66;
  char local_65;
  char local_64;
  undefined local_63;
  char local_62;
  char local_61;
  char local_60;
  char local_5f;
  char local_5e;
  char local_5d;
  char local_5c;
  char local_5b;
  char local_5a;
  char local_59;
  char local_58;
  char local_57;
  char local_56;
  char local_55;
  char local_54;
  char local_53;
  char local_52;
  char local_51;
  char local_50;
  char local_4f;
  char local_4e;
  char local_4d;
  char local_4c;
  char local_4b;
  char local_4a;
  char local_49;
  char local_48;
  char local_47;
  char local_46;
  undefined local_45;
  char local_44;
  char local_43;
  char local_42;
  char local_41;
  char *local_40;
  undefined1 *local_38;
  char *local_30;
  char *local_28;
  char *local_20;
  char *local_18;
  char *local_10;
  
  do {
    local_10 = "choose_an_action:\n";
    local_18 = "1) current time\n";
    local_20 = "2) say hello to this world\n";
    local_28 = "3) give me a poem\n";
    local_30 = "4) random number\n";
    local_38 = "5) flag\n";
    local_40 = "0) exit\n";
    iVar1 = sprintf(&local_81,"%02x",L's');
    local_81 = (char)iVar1;
    local_41 = local_30[0xb];
    local_42 = local_20[0x17];
    local_43 = local_10[0xb];
    local_44 = local_18[0xb];
    local_45 = local_38[3];
    local_46 = local_10[6];
    local_47 = local_10[0xf];
    local_48 = local_10[3];
    local_49 = local_20[0x15];
    local_4a = local_10[9];
    local_4b = local_18[4];
    local_4c = local_10[6];
    local_4d = local_20[0x11];
    local_4e = *local_30;
    local_4f = local_28[5];
    local_50 = local_10[5];
    local_51 = local_10[6];
    local_52 = local_30[0xd];
    local_53 = *local_28;
    local_54 = local_10[0xb];
    local_55 = local_10[0xe];
    local_56 = local_18[0xd];
    local_57 = local_10[5];
    local_58 = local_10[9];
    local_59 = local_10[10];
    local_5a = local_10[6];
    local_5b = local_28[0x10];
    local_5c = local_10[7];
    local_5d = local_20[3];
    local_5e = local_10[0xc];
    local_5f = *local_28;
    local_60 = local_30[0xf];
    local_61 = local_10[9];
    local_62 = *local_40;
    local_63 = local_38[3];
    local_64 = local_10[9];
    local_65 = local_18[6];
    local_66 = local_18[7];
    local_67 = local_28[5];
    local_68 = local_30[0xe];
    local_69 = local_18[6];
    local_6a = *local_38;
    local_6b = local_10[5];
    local_6c = local_10[9];
    local_6d = local_10[5];
    local_6e = local_10[0xf];
    local_6f = local_28[3];
    local_70 = *local_18;
    local_71 = local_10[0xf];
    local_72 = local_18[0xe];
    local_73 = *local_28;
    local_74 = local_20[0x17];
    local_75 = local_10[0xd];
    local_76 = local_30[5];
    local_77 = local_28[3];
    printf("%s",local_10);
    printf("%s",local_18);
    printf("%s",local_20);
    printf("%s",local_28);
    printf("%s",local_30);
    printf("%s",local_38);
    printf("%s",local_40);
    __isoc99_scanf(&DAT_00402087,&local_80);
    switch(local_80) {
    case 1:
      system("date \'+Current time: %T\'");
      break;
    case 2:
      printf("Hello, world!");
      break;
    case 3:
      printf("In the still of the night, stars shimmer above,");
      printf("Whispering secrets of the universe, filled with love.");
      printf("Moonlight dances on the tranquil sea\'s shore,");
      printf("Nature\'s beauty leaves us wanting more.");
      break;
    case 4:
      tVar2 = time((time_t *)0x0);
      srand((uint)tVar2);
      local_7c = rand();
      printf("Random number: %d\n",(ulong)local_7c);
      break;
    case 5:
      puts("It\'s not that simple");
      break;
    case 0xbad1abe1:
      puts("Incorrect choice. Try again.");
      break;
    default:
      return 0;
    }
  } while( true );
}
```

Здесь мы видим обычную программу, где особо нет нигде флага, выводится обычный текст. И даже по команде флаг выводится сообщение, что не все так просто, как хотелось бы. Но еще мы можем заметить кучу переменных, которые являются каким либо символом из существующих команд. Попробуем написать программу на python, которая соберет за нас флаг и учтем что первый символ у нас записан как `L's'`:

```py
local_10 = "choose_an_action:\n"
local_18 = "1) current time\n"
local_20 = "2) say hello to this world\n"
local_28 = "3) give me a poem\n"
local_30 = "4) random number\n"
local_38 = "5) flag\n"
local_40 = "0) exit\n"

a=["s", 
    local_30[0xb], 
    local_20[0x17], 
    local_10[0xb], 
    local_18[0xb], 
    local_38[3], 
    local_10[6], 
    local_10[0xf], 
    local_10[3], 
    local_20[0x15], 
    local_10[9], 
    local_18[4], 
    local_10[6], 
    local_20[0x11], 
    local_30[0], 
    local_28[5], 
    local_10[5], 
    local_10[6], 
    local_30[0xd], 
    local_28[0], 
    local_10[0xb], 
    local_10[0xe], 
    local_18[0xd], 
    local_10[5], 
    local_10[9], 
    local_10[10], 
    local_10[6], 
    local_28[0x10], 
    local_10[7], 
    local_20[3], 
    local_10[0xc], 
    local_28[0], 
    local_30[0xf], 
    local_10[9], 
    local_40[0], 
    local_38[3], 
    local_10[9], 
    local_18[6], 
    local_18[7], 
    local_28[5], 
    local_30[0xe], 
    local_18[6], 
    local_38[0], 
    local_10[5], 
    local_10[9], 
    local_10[5], 
    local_10[0xf], 
    local_28[3], 
    local_18[0], 
    local_10[0xf], 
    local_18[0xe], 
    local_28[0], 
    local_20[0x17], 
    local_10[0xd], 
    local_30[5],
    local_28[3],
]

print(''.join(a))
```

Вывод программы:

```bash
❯ python3 solver.py
surctf_now_u_h4ve_b3come_a_mast3r_0f_rever5e_eng1ne3ring
```

Отлично, флаг получен.

`flag: surctf_now_u_h4ve_b3come_a_mast3r_0f_rever5e_eng1ne3ring`
