import streamlit as st
import hashlib
import base64
import urllib.parse
import itertools
import time

st.set_page_config(page_title="Super Token Auditor", layout="wide")
st.title("🧠 Super Hash / Token Auditor (for audit & learning)")

# ===== INPUT =====
col1, col2 = st.columns(2)
with col1:
    email = st.text_input("Email", "user@example.com")
    password = st.text_input("Password", "mypassword")
    extra = st.text_input("Extra (optional: id/nonce/timestamp)", "")
with col2:
    target = st.text_input("Target MD5 (optional)", "")
    max_patterns = st.slider("Max patterns", 1000, 50000, 10000)

# ===== UTILS =====
def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()

def b64(s: str) -> str:
    return base64.b64encode(s.encode()).decode()

def urlenc(s: str) -> str:
    return urllib.parse.quote(s)

def rev(s: str) -> str:
    return s[::-1]

def lower(s: str) -> str:
    return s.lower()

def upper(s: str) -> str:
    return s.upper()

def trims(s: str) -> list[str]:
    return [s, s.strip(), s + "\n", s + "\r\n"]

# ===== GENERATORS =====
SEPS = ["", ":", "|", "_", "-", ".", "@"]

def base_atoms(email, pw, extra):
    atoms = [email, pw]
    if extra:
        atoms.append(extra)
    return atoms

def concat_variants(parts):
    out = set()
    for order in itertools.permutations(parts, len(parts)):
        for sep in SEPS:
            s = sep.join(order)
            out.add(s)
    return out

def encode_layers(s):
    out = set()
    out.add(s)
    out.add(lower(s))
    out.add(upper(s))
    out.add(rev(s))
    out.add(b64(s))
    out.add(urlenc(s))
    # double encodes
    out.add(b64(urlenc(s)))
    out.add(urlenc(b64(s)))
    return out

def hash_layers(s):
    out = set()
    out.add(md5(s))
    out.add(md5(md5(s)))
    # hash after encode
    out.add(md5(b64(s)))
    out.add(md5(urlenc(s)))
    # encode after hash
    out.add(b64(md5(s)))
    return out

def generate_candidates(email, pw, extra, cap):
    atoms = base_atoms(email, pw, extra)

    # 1) concat
    concat = concat_variants(atoms)

    # 2) expand encodings
    expanded = set()
    for c in list(concat)[:cap]:
        for t in trims(c):
            expanded |= encode_layers(t)

    # 3) hash layers
    finals = set()
    for e in list(expanded)[:cap]:
        finals |= hash_layers(e)

    return list(finals)[:cap]

# ===== RUN =====
if st.button("🚀 Analyze (Audit)"):
    t0 = time.time()
    candidates = generate_candidates(email, password, extra, max_patterns)

    st.info(f"Generated ~{len(candidates)} candidates")

    found = []
    if target:
        for c in candidates:
            if c == target:
                found.append(c)

    if target:
        if found:
            st.success("🔥 Match found in tested patterns (weak/guessable construction)")
            for f in found[:5]:
                st.code(f)
        else:
            st.warning("❌ No match in common/weak patterns (good sign if this is your system).")

    # show some samples
    with st.expander("Preview candidates"):
        for c in candidates[:50]:
            st.write(c)

    st.info(f"⏱ {round(time.time()-t0,2)}s")

# ===== GUIDANCE =====
st.subheader("🔐 What good looks like")
st.markdown("""
- Use **HMAC (SHA-256)** with a server-side secret: `HMAC(secret, data)`
- Include **nonce + expiry** (timestamp) → token dùng 1 lần, có hạn
- Store **only hashed passwords** (bcrypt/Argon2), **không gửi password qua email**
- Invalidate token sau khi dùng / sau khi hết hạn
""")
