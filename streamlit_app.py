import streamlit as st
import google.generativeai as genai

st.title("💬 Chatbot (Gemini Flash 2.5)")
st.write(
    "このチャットボットは Google Gemini Flash 2.5 を使って応答を生成します。"
    "APIキーは .streamlit/secrets.toml で管理できます（`[gemini] api_key = \"...\"` を追加）。"
)

# secrets.tomlからAPIキーを取得
gemini_api_key = st.secrets.get("gemini", {}).get("api_key", "")

if not gemini_api_key:
    st.info("Gemini APIキーがsecrets.tomlに設定されていません。", icon="🗝️")
else:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("メッセージを入力してください"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        history = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                history.append({"role": "user", "parts": [m["content"]]})
            else:
                history.append({"role": "model", "parts": [m["content"]]})

        response = ""
        with st.chat_message("assistant"):
            stream = model.generate_content(history, stream=True)
            for chunk in stream:
                if chunk.candidates:
                    delta = chunk.candidates[0].content.parts[0].text
                    response += delta
                    st.write(delta, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
