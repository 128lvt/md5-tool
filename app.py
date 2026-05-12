import streamlit as st
import hashlib
import itertools

# =====================================================
# CONFIG
# =====================================================

TARGET = "d47a6297d582b52a88992a32da81c3f2"

DEFAULT_PARTS = [
    "dragon ball",
    "teamobi",
    "418462",
    "1d712c355980d92ebf8816edad70bb5f",
    "Tue, 12 May 2026 01:16:31 GMT",
    "ingame902@gmail.com"
]

SEPARATORS = [
    "",
    " ",
    "|",
    ":",
    "_",
    "-",
    ".",
    ",",
    "/"
]

# =====================================================
# UI
# =====================================================

st.set_page_config(
    page_title="MD5 AI Finder",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 MD5 AI Combination Finder")

st.write("Generate all possible combinations and compare MD5 hashes.")

target = st.text_input(
    "Target MD5",
    TARGET
)

required = st.text_input(
    "Required value",
    "418462"
)

parts_input = st.text_area(
    "Input data (1 line = 1 value)",
    "\n".join(DEFAULT_PARTS),
    height=200
)

parts = [
    p.strip()
    for p in parts_input.split("\n")
    if p.strip()
]

# =====================================================
# START BUTTON
# =====================================================

if st.button("🚀 Start Search"):

    matches = []
    checked = 0

    progress = st.progress(0)
    status = st.empty()

    estimated_total = 0

    for r in range(1, len(parts) + 1):

        estimated_total += (
            len(list(itertools.combinations(parts, r)))
            * len(SEPARATORS)
        )

    current = 0

    # =================================================
    # GENERATE COMBINATIONS
    # =================================================

    for r in range(1, len(parts) + 1):

        combinations = itertools.combinations(parts, r)

        for combo in combinations:

            # REQUIRED VALUE MUST EXIST
            if required not in combo:
                continue

            permutations = itertools.permutations(combo)

            for perm in permutations:

                for sep in SEPARATORS:

                    current += 1

                    text = sep.join(perm)

                    variants = [

                        text,
                        text.lower(),
                        text.upper(),
                        text.strip()
                    ]

                    for candidate in variants:

                        checked += 1

                        md5 = hashlib.md5(
                            candidate.encode()
                        ).hexdigest()

                        if md5 == target:

                            matches.append({
                                "input": candidate,
                                "md5": md5
                            })

                    progress.progress(
                        min(current / estimated_total, 1.0)
                    )

                    status.text(
                        f"Checked: {checked:,}"
                    )

    # =================================================
    # RESULTS
    # =================================================

    st.success("Done!")

    st.write(f"### Total Checked: {checked:,}")

    if matches:

        st.success(f"Found {len(matches)} match(es)!")

        for m in matches:

            st.code(
                f"INPUT : {m['input']}\n"
                f"MD5   : {m['md5']}"
            )

    else:

        st.warning("No matches found.")
