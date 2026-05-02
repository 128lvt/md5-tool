import streamlit as st
import hashlib
import itertools
import concurrent.futures
import time

st.set_page_config(page_title="MD5 Hardcore Tool", layout="wide")

st.title("🔥 MD5 Hardcore Pattern Tester")

# ===== INPUT =====
col1, col2 = st.columns(2)

with col1:
    passwords_input = st.text_area("Passwords", "975311\n617160\n224403")

with col2:
    hashes_input = st.text_area("Target Hashes",
"""60a47be3a6729b56cf505a303e5820e5
2133d90471982ea1b46c5b70a097f898
a192a951eb99fea4c8ad92deb915493e""")

passwords = [x.strip() for x in passwords_input.split("\n") if x.strip()]
targets = [x.strip() for x in hashes_input.split("\n") if x.strip()]

# ===== CONFIG =====
st.subheader("⚙️ Config")

default_keys = [
    "", "teamobi", "ngocrong", "dragonball",
    "dbo", "nr", "admin", "123", "123456",
    "key", "salt"
]

extra_keys = st.text_input("Thêm key (cách nhau bằng dấu phẩy)")
if extra_keys:
    default_keys += [k.strip() for k in extra_keys.split(",")]

uploaded_file = st.file_uploader("Upload wordlist (.txt)")
if uploaded_file:
    wordlist = uploaded_file.read().decode("utf-8").splitlines()
    default_keys += wordlist

seps = ["", "|", "_", "-", ".", "@"]

use_double_md5 = st.checkbox("Enable double MD5", True)
use_case = st.checkbox("Test UPPERCASE / lowercase", True)

# ===== HASH =====
def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

# ===== SMART KEY =====
def generate_smart_keys():
    base = ["teamobi", "ngocrong", "dragon", "dbz", "nro"]
    smart = []
    for b in base:
        smart += [
            b,
            b + "123",
            b + "2024",
            b + "2025",
            b + "vip",
            b.upper(),
            b.capitalize(),
        ]
    return smart

# ===== NUMERIC KEYS =====
def generate_numeric_keys():
    nums = ["123", "456", "789", "000", "111"]
    combos = []
    for a, b in itertools.product(nums, nums):
        combos.append(a + b)
    return combos

default_keys += generate_smart_keys()
default_keys += generate_numeric_keys()

# ===== VARIANTS =====
def generate_variants(pw, key):
    variants = []

    for sep in seps:
        variants += [
            pw,
            pw + key,
            key + pw,
            pw + sep + key,
            key + sep + pw,
            pw + key + sep,
            key + pw + key,
            pw + key + pw,
            key + "_" + pw + "_" + key,
            pw[::-1],
            pw + pw,
            key + pw + "123",
            "123" + pw + key,
        ]

    if use_double_md5:
        variants += [
            md5(pw),
            md5(md5(pw)),
            md5(pw) + key,
            key + md5(pw),
        ]

    if use_case:
        variants += [v.upper() for v in variants]
        variants += [v.lower() for v in variants]

    return set(variants)

# ===== WORKER =====
def worker(pw, target, key):
    results = []
    variants = generate_variants(pw, key)

    for v in variants:
        if md5(v) == target:
            results.append((pw, v, key))

    return results

# ===== RUN =====
if st.button("🚀 Run Hardcore Test"):
    start = time.time()
    found = []

    total = len(passwords) * len(default_keys)
    progress = st.progress(0)
    count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        for i, pw in enumerate(passwords):
            if i >= len(targets):
                break

            target = targets[i]

            for key in default_keys:
                futures.append(executor.submit(worker, pw, target, key))

        for f in concurrent.futures.as_completed(futures):
            res = f.result()
            if res:
                found.extend(res)

            count += 1
            progress.progress(min(count / total, 1.0))

    end = time.time()

    if found:
        st.success("🔥 FOUND MATCH!")
        for pw, match, key in found:
            st.write(f"Password: `{pw}` → Match: `{match}` (key: `{key}`)")
    else:
        st.warning("❌ Không tìm thấy")

    st.info(f"⏱ Time: {round(end - start, 2)}s")
