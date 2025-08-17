import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# 環境変数を読み込み
load_dotenv()

def get_ai_response(user_input, expert_type):
    """
    LLMから回答を取得する関数
    
    Args:
        user_input (str): ユーザーの質問内容
        expert_type (str): 選択された専門家の種類
    
    Returns:
        str: LLMからの回答
    """
    
    # 専門家の種類に応じてシステムメッセージを設定
    if expert_type == "医療専門家":
        system_message = """あなたは経験豊富な医療専門家です。
健康や医療に関する質問に、専門的で分かりやすい回答をしてください。
ただし、診断や治療の決定は医師の判断が必要であることを必ず伝えてください。"""
        
    elif expert_type == "法律専門家":
        system_message = """あなたは経験豊富な法律専門家です。
法律や契約、権利に関する質問に、専門的で分かりやすい回答をしてください。
ただし、具体的な法的判断は弁護士などの専門家に相談することを推奨してください。"""
        
    elif expert_type == "ITエンジニア":
        system_message = """あなたは経験豊富なITエンジニアです。
プログラミング、システム設計、技術的な問題に関して、実践的で分かりやすい回答をしてください。
コード例や具体的な解決策を含めて説明してください。"""
    
    try:
        # ChatOpenAIインスタンスを作成
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # メッセージを作成
        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_input)
        ]
        
        # LLMに送信して回答を取得
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# アプリのタイトルと概要
st.title("🤖 AI専門家相談アプリ")
st.markdown("---")

# アプリの概要説明
st.markdown("""
## 📋 アプリの概要
このアプリでは、様々な分野の専門家AIに相談できます。
専門家を選択して、質問や相談内容を入力してください。

## 🔧 操作方法
1. **専門家を選択**：ラジオボタンから相談したい専門家を選んでください
2. **質問を入力**：テキストエリアに質問や相談内容を入力してください
3. **相談開始**：「相談する」ボタンをクリックしてAIからの回答を受け取ってください
""")

st.markdown("---")

# 専門家選択のラジオボタン
st.subheader("👨‍⚕️ 専門家を選択してください")
expert_type = st.radio(
    "相談したい専門家を選んでください：",
    ["医療専門家", "法律専門家", "ITエンジニア"],
    index=0
)

# 選択された専門家の説明を表示
if expert_type == "医療専門家":
    st.info("🏥 健康、症状、医療に関する一般的な情報をお答えします。")
elif expert_type == "法律専門家":
    st.info("⚖️ 法律、契約、権利に関する一般的な情報をお答えします。")
elif expert_type == "ITエンジニア":
    st.info("💻 プログラミング、システム、技術に関する質問にお答えします。")

st.markdown("---")

# テキスト入力フォーム
st.subheader("💬 質問・相談内容を入力してください")
user_input = st.text_area(
    "ここに質問や相談内容を入力してください：",
    placeholder="例：最近頭痛が続いているのですが、どのような原因が考えられますか？",
    height=150
)

# 相談ボタン
if st.button("🚀 相談する", type="primary"):
    if user_input.strip():
        with st.spinner(f"{expert_type}が回答を準備中..."):
            # LLM関数を呼び出し
            ai_response = get_ai_response(user_input, expert_type)
            
        # 回答結果を表示
        st.markdown("---")
        st.subheader("💡 AI専門家からの回答")
        st.info(f"**{expert_type}より：**")
        st.markdown(ai_response)
        
        # 追加情報
        st.markdown("---")
        st.caption("⚠️ この回答は参考情報です。重要な判断は必ず専門家にご相談ください。")
        
    else:
        st.error("質問内容を入力してください。")
