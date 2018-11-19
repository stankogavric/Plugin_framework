def prvi_zadatak(neki_tekst):
    if len(neki_tekst) > 10:
        print("Uneti string je dug.")

prvi_zadatak("Provera dugog stringa.")
prvi_zadatak("Kratak")

def drugi_zadatak(neki_tekst):
    if neki_tekst[0] == "a" or neki_tekst[1] == "A":
        print("String pocinje sa a.")
    else:
        print("String nema a na pocetku.")

def treci_zadatak_a(n):
    for i in range(1, n+1):
        print(i**2)

treci_zadatak_a(10)

def treci_zadatak_b(n):
    i = 1
    while i <= n:
        print(i*i)
        i += 1

treci_zadatak_b(10)

