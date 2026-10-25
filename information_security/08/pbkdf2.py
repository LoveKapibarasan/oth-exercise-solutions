import hashlib
import time

seq1 = bytes.fromhex(
    "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f895"
    "5ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8"
    "823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99"
    "f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70"
)

salt_a = b"salt_example_A"
salt_b = b"salt_example_B"


def run_pbkdf2(password, hash_name, salt, iterations):
    start_time = time.time()
    dk = hashlib.pbkdf2_hmac(
        hash_name=hash_name,
        password=password,
        salt=salt,
        iterations=iterations,
        dklen=32,
    )
    elapsed = time.time() - start_time
    print(f"[{hash_name}] Iterations: {iterations:,} | Salt: {salt.decode()}")
    print(f"  Result (hex): {dk.hex()}")
    print(f"  Time taken  : {elapsed:.5f} seconds\n")



run_pbkdf2(seq1, "sha256", salt_a, 10000)

run_pbkdf2(seq1, "md5", salt_a, 10000)

run_pbkdf2(seq1, "sha256", salt_b, 10000)

run_pbkdf2(seq1, "sha256", salt_a, 500000)