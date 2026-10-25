import hashlib

seq1str = (
    "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f895"
    "5ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8"
    "823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99"
    "f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70"
)

seq2str = (
    "d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f895"
    "5ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8"
    "823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99"
    "f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70"
)

seq1 = bytes.fromhex(seq1str)
seq2 = bytes.fromhex(seq2str)
print(f"Inputs are equal?  : {seq1 == seq2}")


md5_seq1 = hashlib.md5(seq1).hexdigest()
md5_seq2 = hashlib.md5(seq2).hexdigest()

print(f"seq1 (MD5): {md5_seq1}")
print(f"seq2 (MD5): {md5_seq2}")

print(f"Hashes are equal?  : {md5_seq1 == md5_seq2}")


sha256_seq1 = hashlib.sha256(seq1).hexdigest()
sha256_seq2 = hashlib.sha256(seq2).hexdigest()

print(f"seq1 (SHA-256): {sha256_seq1}")
print(f"seq2 (SHA-256): {sha256_seq2}")
print(f"SHA-256 Equal? : {sha256_seq1 == sha256_seq2}")