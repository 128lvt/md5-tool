import streamlit as st
import hashlib
import itertools
import time

st.set_page_config(page_title="MD5 Cracker Tool", layout="wide")

st.title("🔥 MD5 Pattern Tester (Advanced)")

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

uploaded_file = st.file_uploader("Upload wordlist key (.txt)")

if uploaded_file:
    wordlist = uploaded_file.read().decode("utf-8").splitlines()
    default_keys += wordlist

seps = ["", "|", "_", "-", ".", "@"]

use_double_md5 = st.checkbox("Enable double MD5", True)
use_case = st.checkbox("Test UPPERCASE / lowercase", True)

# ===== HASH =====
def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

# ===== GENERATE VARIANTS =====
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
        ]

    if use_double_md5:
        variants += [
            md5(pw),
            md5(pw) + key,
            key + md5(pw)
        ]

    if use_case:
        variants += [v.upper() for v in variants]
        variants += [v.lower() for v in variants]

    return set(variants)

# ===== RUN =====
if st.button("🚀 Run Test"):
    total = len(passwords) * len(default_keys)
    progress = st.progress(0)
    found = []

    count = 0
    start_time = time.time()

    for i, pw in enumerate(passwords):
        if i >= len(targets):
            break

        target = targets[i]

        for key in default_keys:
            variants = generate_variants(pw, key)

            for v in variants:
                if md5(v) == target:
                    found.append((pw, v, key))

            count += 1
            progress.progress(min(count / total, 1.0))

    end_time = time.time()

    if found:
        st.success("🎯 FOUND MATCH!")
        for f in found:
            st.write(f"Password: `{f[0]}` → Match: `{f[1]}` (key: `{f[2]}`)")
    else:
        st.warning("❌ Không tìm thấy")

    st.info(f"⏱ Time: {round(end_time - start_time, 2)}s")
