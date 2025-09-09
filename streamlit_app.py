import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("💬 Chatbot (Gemini Flash 2.5)")
st.write(
    "このチャットボットは Google Gemini Flash 2.5 を使って応答を生成します。"
    "ご利用には Gemini API キーが必要です。API キーは [Google AI Studio](https://makersuite.google.com/app/apikey) で取得できます。"
)

# Ask user for their Gemini API key.
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Gemini APIキーを入力してください。", icon="🗝️")
else:
    # Configure Gemini
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # セッションステートでチャット履歴を保持
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 既存メッセージの表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # チャット入力
    if prompt := st.chat_input("メッセージを入力してください"):
        # ユーザーの発言を保存・表示
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gemini API へリクエスト
        history = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                history.append({"role": "user", "parts": [m["content"]]})
            else:
                history.append({"role": "model", "parts": [m["content"]]})

        # Gemini の generate_content はストリーミング対応
        response = ""
        with st.chat_message("assistant"):
            stream = model.generate_content(history, stream=True)
            for chunk in stream:
                if chunk.candidates:
                    delta = chunk.candidates[0].content.parts[0].text
                    response += delta
                    st.write(delta, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
