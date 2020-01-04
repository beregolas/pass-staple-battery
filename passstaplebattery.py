import argparse
import secrets
import math


number_pool = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

special_pool = ['#', '+', '*', '~', '.', ':', ',', ';', '-', '_',
                '!', '?', '\\', '$', '%', '&', '/', '(', ')', '[',
                ']', '=', '<', '>', '@', '{', '}']

any_pool = number_pool + special_pool


def generate(args, wordlist):

    words = args.words

    special = args.special

    number = args.number

    any = args.any

    capitalize = args.capitalize

    password = ""
    choice = math.log(1)

    # words
    for _ in range(words[0]):
        password += secrets.choice(wordlist)
        choice += math.log(wordlist.__len__())

    password = list(password)

    # special

    for _ in range(special[2]):
        special[secrets.randbelow(2)] += 1
        choice += math.log(2)

    for _ in range(special[0]):
        password.insert(secrets.randbelow(password.__len__()), secrets.choice(special_pool))
        choice += math.log(password.__len__() * special_pool.__len__())

    for _ in range(special[1]):
        password[secrets.randbelow(password.__len__())] = secrets.choice(special_pool)
        choice += math.log(password.__len__() * special_pool.__len__())

    # numbers

    for _ in range(number[2]):
        number[secrets.randbelow(2)] += 1
        choice += math.log(2)

    for _ in range(number[0]):
        password.insert(secrets.randbelow(password.__len__()), secrets.choice(number_pool))
        choice += math.log(password.__len__() * number_pool.__len__())

    for _ in range(number[1]):
        password[secrets.randbelow(password.__len__())] = secrets.choice(number_pool)
        choice += math.log(password.__len__() * number_pool.__len__())

    # any

    for _ in range(any[2]):
        any[secrets.randbelow(2)] += 1
        choice += math.log(2)

    for _ in range(any[0]):
        password.insert(secrets.randbelow(password.__len__()), secrets.choice(any_pool))
        choice += math.log(password.__len__() * any_pool.__len__())

    for _ in range(any[1]):
        password[secrets.randbelow(password.__len__())] = secrets.choice(any_pool)
        choice += math.log(password.__len__() * any_pool.__len__())

    # capitalize

    i = 0
    lower = 0
    for c in password:
        if c.islower():
            lower += 1

    while i < capitalize[0]:
        char = secrets.randbelow(password.__len__())
        if password[char].islower():
            password[char] = password[char].upper()
            i += 1
            choice += math.log(lower)
            lower -= 1

    password = ''.join(password)

    return choice, password


def handle_small():
    print("please only specify positive numbers")
    exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='PROG',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-w', '--words', nargs=1, default=[5], type=int,
                        help='how many words to choose')
    parser.add_argument('-l', '--length', nargs=1, default=[16], type=int,
                        help='the minimum length of the password, after word choice and character insertions')
    parser.add_argument('-s', '--special', nargs=3, default=[0, 0, 1], type=int,
                        help='how many special characters to insert, replace, or either')
    parser.add_argument('-n', '--number', nargs=3, default=[0, 0, 1], type=int,
                        help='how many numbers to insert, replace, or either')
    parser.add_argument('-a', '--any', nargs=3, default=[0, 0, 5], type=int,
                        help='how many special characters or numbers to insert, replace, or either')
    parser.add_argument('-c', '--capitalize', nargs=1, default=[5], type=int,
                        help='how many characters to capitalize')
    parser.add_argument('-r', '--random',  action='store_true',
                        help='randomize all other setting by multiplying with +/- 0.5 (except minimum length)')
    parser.add_argument('-p', '--passwords', type=int, default=1, nargs=1, help='generate multiple passwords')
    parser.add_argument('filesin', type=str, nargs='+',
                        help='input files with word lists')

    args = None

    # noinspection PyBroadException
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        exit()

    n = 0

    wordlist = []

    for filename in args.filesin:
        try:
            with open(filename, 'r') as file:
                for line in file:
                    n += 1
                    wordlist.append(line.rstrip())
        except FileNotFoundError:
            print("the specified file (" + filename + ") was not found")

    if wordlist.__len__() is 0:
        print("No words were found, please try again")
        exit()

    print(str(n) + " words were found")

    for e in args.any:
        if e < 0:
            handle_small()

    for e in args.number:
        if e < 0:
            handle_small()

    for e in args.special:
        if e < 0:
            handle_small()

    if args.capitalize[0] < 0:
        handle_small()
    if args.length[0] < 0:
        handle_small()
    if args.words[0] < 1:
        handle_small()

    if args.random:
        # words
        low = int(args.words[0] * 0.5)
        high = int(args.words[0] * 1.5)
        args.words[0] = secrets.choice(range(low, high))
        # special
        for i in range(3):
            low = int(args.special[i] * 0.5)
            high = int(args.special[i] * 1.5) + 1
            if high > low:
                args.special[i] = secrets.choice(range(low, high))
        # numbers
        for i in range(3):
            low = int(args.number[i] * 0.5)
            high = int(args.number[i] * 1.5) + 1
            if high > low:
                args.number[i] = secrets.choice(range(low, high))
        # any
        for i in range(3):
            low = int(args.any[i] * 0.5)
            high = int(args.any[i] * 1.5) + 1
            if high > low:
                args.any[i] = secrets.choice(range(low, high))
        # capitalize
        low = int(args.capitalize[0] * 0.5)
        high = int(args.capitalize[0] * 1.5) + 1
        if high > low:
            args.capitalize[0] = secrets.choice(range(low, high))

    print("value selection confirmed. In order of operations: ")
    print("          word-pool: " + str(n))
    print("              words: " + str(args.words[0]))
    print("            special: " + str(args.special[0]) + ", " + str(args.special[1]) + ", " + str(args.special[2]))
    print("            numbers: " + str(args.number[0]) + ", " + str(args.number[1]) + ", " + str(args.number[2]))
    print("                any: " + str(args.any[0]) + ", " + str(args.any[1]) + ", " + str(args.any[2]))
    print("         capitalize: " + str(args.capitalize[0]))
    print("       length-check: " + str(args.length[0]))

    print("----------------------------------------------------")
    print("entropy: | length: | password: ")

    for _ in range(args.passwords[0]):
        cp = generate(args, wordlist)
        print("   " + str(int(cp[0])) + "        " + str(cp[1].__len__()) + "         " + cp[1])
