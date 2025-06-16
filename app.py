import streamlit as st
from minilang import tokenize, parse_tokens, check_semantics, generate_TAC, symbol_table

# ---------------- Streamlit Web App ----------------
st.set_page_config(page_title="MiniLang++ Analyzer", layout="wide")
st.title("🧠 MiniLang++ Code Analyzer")

code_input = st.text_area("Paste your MiniLang++ code here:", height=250)

if st.button("Analyze"):
    try:
        symbol_table.clear()
        tokens = tokenize(code_input)
        ast = parse_tokens(tokens)
        errors = check_semantics(ast)
        tac = generate_TAC(ast)

        st.subheader("🔹 Tokens")
        st.code("\n".join(str(t) for t in tokens), language="text")

        st.subheader("🔹 Abstract Syntax Tree")
        st.code("\n".join(str(t) for t in ast), language="text")

        st.subheader("🔹 Symbol Table")
        st.code("\n".join(f"{k}: {v}" for k, v in symbol_table.items()), language="text")

        st.subheader("🔹 Semantic Errors")
        if errors:
            st.error("\n".join(errors))
        else:
            st.success("No semantic errors found.")

        st.subheader("🔹 Three Address Code (TAC)")
        st.code("\n".join(tac), language="text")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
