import streamlit as st
import hashlib
import itertools

st.set_page_config(page_title="Token Analyzer", layout="wide")

st.title("🧠 Token Pattern Analyzer (Teamobi style)")

# ===== INPUT =====
st.subheader("Input Data")

emails = st.text_area("Emails", "sieuxe10x@gmail.com\ningame296@gmail.com")
passwords = st.text_area("Passwords", "975311\n591709")
tokens = st.text_area("Tokens (MD5)", 
"""60a47be3a6729b56cf505a303e5820e5
2051ebf35acdebbd0bda79e427956b2e""")

emails = [x.strip() for x in emails.split("\n") if x.strip()]
passwords = [x.strip() for x in passwords.split("\n") if x.strip()]
tokens = [x.strip() for x in tokens.split("\n") if x.strip()]

# ===== HASH =====
def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

# ===== COMMON PATTERNS =====
def generate_patterns(email, pw):
    patterns = []

    # basic
    patterns += [
        email + pw,
        pw + email,
        email + ":" + pw,
        pw + ":" + email,
    ]

    # separators
    seps = ["", "_", "-", ".", "@", "|"]
    for s in seps:
        patterns.append(email + s + pw)
        patterns.append(pw + s + email)

    # double hash
    patterns += [
        md5(email + pw),
        md5(pw + email),
    ]

    # reverse
    patterns += [
        (email + pw)[::-1],
        (pw + email)[::-1],
    ]

    # uppercase/lowercase
    patterns += [
        (email + pw).upper(),
        (email + pw).lower(),
    ]

    # trim / weird
    patterns += [
        email.strip() + pw.strip(),
        email + pw + "\n",
        email + pw + "\r\n",
    ]

    return set(patterns)

# ===== RUN =====
if st.button("🚀 Analyze Pattern"):
    found = []

    for i in range(min(len(emails), len(passwords), len(tokens))):
        email = emails[i]
        pw = passwords[i]
        target = tokens[i]

        for p in generate_patterns(email, pw):
            if md5(p) == target:
                found.append((email, pw, p))

    if found:
        st.success("🔥 FOUND PATTERN!")
        for f in found:
            st.write(f"Email: {f[0]}")
            st.write(f"Password: {f[1]}")
            st.write(f"Match string: {f[2]}")
            st.write("---")
    else:
        st.warning("❌ Không tìm thấy pattern")
