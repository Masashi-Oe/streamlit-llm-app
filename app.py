from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# --- 各専門家のシステムメッセージを定義 ---
SYSTEM_PROMPTS = {
    "A": "あなたは一流のファッションの専門家です。ユーザーの気分や希望に合わせて、最適なファッションの提案をしてください。",
    "B": "あなたは一流の音楽の専門家です。ユーザーの気分や希望に合わせて、最適な音楽やアーティスト、ジャンルの提案をしてください。"
}

# --- LLM応答関数 ---
def get_llm_response(input_text, expert_type):
    # 選択された専門家に応じてシステムプロンプトをセット
    system_message = SYSTEM_PROMPTS.get(expert_type, SYSTEM_PROMPTS["A"])
    # LLMのインスタンス作成（APIキーは環境変数OPENAI_API_KEYを利用）
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)
    # LangChainのChatPromptTemplateを利用
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{input}")
    ])
    # LLMに入力して応答を取得
    chain = prompt | llm
    result = chain.invoke({"input": input_text})
    return result.content

# --- Streamlit UI ---
st.title("気分に合わせた提案をするLLMアプリ")
st.markdown("""
このアプリは、あなたの気分や希望に合わせて「ファッション」または「音楽」の専門家になりきったAIが提案をします。  
下のフォームにあなたの「気分」や「希望」を入力し、どちらの専門家に相談したいか選んでください。
""")

# ラジオボタンで専門家選択
expert = st.radio(
    "どちらの専門家に相談しますか？",
    options=["A", "B"],
    format_func=lambda x: "ファッションの専門家" if x == "A" else "音楽の専門家"
)

# 入力フォーム
user_input = st.text_input("今の気分や相談したいことを入力してください:")

if st.button("提案をもらう"):
    if user_input:
        with st.spinner("提案を考えています..."):
            response = get_llm_response(user_input, expert)
        st.success("AIの提案はこちら：")
        st.write(response)
    else:
        st.warning("入力してください。")
