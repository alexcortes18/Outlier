def sieve(limit):
    primes = []
    # 2 and 3 are known to be prime
    if limit > 2:
        primes.append(2)
    if limit > 3:
        primes.append(3)

    # Initialise the sieve array with False values
    sieve = [False] * (limit + 1)

    x = 1
    while x * x <= limit:
        y = 1
        while y * y <= limit:
            # Main part of Sieve of Atkin
            n = (4 * x * x) + (y * y)
            if (n <= limit and (n % 12 == 1 or n % 12 == 5)):
                sieve[n] ^= True

            n = (3 * x * x) + (y * y)
            if n <= limit and n % 12 == 7:
                sieve[n] ^= True

            n = (3 * x * x) - (y * y)
            if (x > y and n <= limit and n % 12 == 11):
                sieve[n] ^= True
            y += 1
        x += 1

    # Mark all multiples of squares as non-prime
    r = 5
    while r * r <= limit:
        if sieve[r]:
            for i in range(r * r, limit+1, r * r):
                sieve[i] = False
        r += 1

    # Collect primes using sieve[]
    for a in range(5, limit + 1):
        if sieve[a]:
            primes.append(a)

    return primes

def pick_prime(primes, min_size=1000):
    """returns a suitable prime to use as modulus"""
    for prime in primes:
        if prime >= min_size:
            return prime
    # if no prime large enough exists, use last one on list
    return primes[-1]

def hash(string, modulus):
    """implements polynomial rolling of string keys"""
    hash_value = 5381
    for char in string:
        # hash = 33 XOR ord(c)
        hash_value = ((hash_value << 5) + hash_value) + ord(char)  # Change: ^ to +
    return hash_value % modulus

if __name__ == '__main__':
    # generate primes list to use as modulus
    primes = sieve(10000) # modify limit based on your needs
    modulus = pick_prime(primes, 1000)
    test_array = ["alpha","beta","gamma","delta","epsilon"]

    for string in test_array:
        hash_value = hash(string, modulus)
        print(f"Hash of {string} is {hash_value}")