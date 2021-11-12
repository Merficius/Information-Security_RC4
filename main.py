import time

N = 256
plaintext = "MEET ME AFTER THE TOGA PARTY."


def ksa_rc4(key):
    s = list(range(N))
    key = [ord(c) for c in key]

    j = 0
    for i in range(N):
        j = (j + s[i] + key[i % len(key)]) % N
        #print("j:", j)
        s[i], s[j] = s[j], s[i]

    #print("rc4:", s)
    # print(s)
    return s


def PRGA_rc4(s):
    i = 0
    j = 0
    ciphertext = ""

    for iterator in range(len(plaintext)):
        i = (i + 1) % N
        j = (j + s[i]) % N

        s[i], s[j] = s[j], s[i]

        key = s[(s[i] + s[j]) % N]
        #print("key:", key)

        #print(hex(ord(plaintext[iterator]) ^ key))
        pre_cipher = str(hex(ord(plaintext[iterator]) ^ key))
        ciphertext += pre_cipher[2:]
    #print("ciphertext:", ciphertext)
    return ciphertext


def ksa_proposed(key):
    s1 = []
    s2 = []
    key = [ord(c) for c in key]
    t = []
    for i in range(N):
        if i <= N//2 - 1:
            s1.append(i)
        else:
            s2.append(i)

    key1 = key[:len(key)//2]
    key2 = key[len(key)//2:]
    #print(key1, key2)
    j = 0

    for i in range(N//2):
        j = (j + s1[i] + key1[i % len(key1)]) % (N//2)
        #print("j:", j)
        s1[i], s1[j] = s1[j], s1[i]

        j = (j + s2[i] + key2[i % len(key2)]) % (N//2)
        #print("j:", j)
        s2[i], s2[j] = s2[j], s2[i]

    return s1, s2


def PRGA_proposed(s1, s2):
    i = 0
    j1 = 0
    j2 = 0
    ciphertext = ""

    for iterator in range(len(plaintext)):
        i = (i+1) % (N//2)
        j1 = (j1 + s1[i]) % (N//2)
        s1[i], s2[j1] = s2[j1], s1[i]

        t1 = (s1[i] + s1[j1]) % (N//2)
        key1 = s1[t1]
        #print("keey1:", key1)

        j2 = (j2 + s2[i]) % (N//2)
        s2[i], s1[j2] = s1[j2], s2[i]

        t2 = (s2[i] + s2[j2]) % (N//2)
        key2 = s2[t2]
        #print("keey2:", key2)

        key = key1 + key2
        # print(key)
        #print("keey:", key)
        pre_cipher = str(hex(ord(plaintext[iterator]) ^ key))
        ciphertext += pre_cipher[2:]
    #print("ciphertext:", ciphertext)
    return ciphertext


start = time.time()
result = ksa_rc4("alice")
print(PRGA_rc4(result))
end = time.time()
print(f"Runtime of normal rc4 is   {end - start}")


start = time.time()
s1, s2 = ksa_proposed("alice")
print(PRGA_proposed(s1, s2))
end = time.time()
print(f"Runtime of proposed rc4 is {end - start}")
