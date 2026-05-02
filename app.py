import streamlit as st
import hashlib
import base64
import urllib.parse

st.set_page_config(page_title="Hash Formula Analyzer", layout="wide")
st.title("🧠 Hash Formula Analyzer")

sample_input = st.text_input("Input string", "mypassword123")
target_hash = st.text_input("Target MD5", "")


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def generate_patterns(x):
    patterns = {}

    patterns["plain"] = x
    patterns["upper"] = x.upper()
    patterns["lower"] = x.lower()
    patterns["reverse"] = x[::-1]

    patterns["md5(x)"] = md5(x)
    patterns["md5(md5(x))"] = md5(md5(x))

    patterns["base64(x)"] = base64.b64encode(x.encode()).decode()
    patterns["urlencode(x)"] = urllib.parse.quote(x)

    patterns["md5(base64(x))"] = md5(patterns["base64(x)"])
    patterns["md5(urlencode(x))"] = md5(patterns["urlencode(x)"])

    patterns["x + 123"] = x + "123"
    patterns["123 + x"] = "123" + x
    patterns["md5(x+123)"] = md5(x + "123")
    patterns["md5(123+x)"] = md5("123" + x)

    return patterns


if st.button("Analyze"):
    patterns = generate_patterns(sample_input)

    found = False

    for name, value in patterns.items():
        result = md5(value) if name not in ["md5(x)", "md5(md5(x))", "md5(base64(x))", "md5(urlencode(x))", "md5(x+123)", "md5(123+x)"] else value

        if target_hash and result == target_hash:
            st.success(f"🔥 Match found: {name}")
            st.code(value)
            found = True

    if not found and target_hash:
        st.warning("No known pattern matched.")

    with st.expander("Show all tested patterns"):
        for name, value in patterns.items():
            result = md5(value) if not name.startswith("md5") else value
            st.write(f"{name}: {result}")
