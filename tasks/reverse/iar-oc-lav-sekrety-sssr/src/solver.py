for num in range(100000, 100000000):
    if num > 0:
        num_str = str(num)
        if len(num_str) >= 6 and len(num_str) <= 9:
            sum_of_digits = sum(map(int, num_str))
            if num % sum_of_digits == 0:
                if num % 7 == 0:
                    if num % 3 != 0:
                        if num % 5 == 0 or num % 11 == 0:
                            if (num % 17 == 0 and num % 19 == 0) or (num % 23 == 0 or num % 29 == 0):
                                if num % 89 == 0:
                                    if num % 8 != 0:
                                        print(num)
                                        break
