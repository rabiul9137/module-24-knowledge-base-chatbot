import streamlit as st

from src.qa import answer_question


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="বিশ্বের উপাদান - AI Chatbot",
    page_icon="📚",
    layout="centered"
)


# ==========================================
# Custom CSS
# ==========================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    .book-info {
        padding: 15px;
        border-radius: 10px;
        background-color: #f5f5f5;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# Header
# ==========================================

st.markdown(
    '<div class="main-title">📚 বিশ্বের উপাদান</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">বাংলা বইভিত্তিক Knowledge Base Chatbot</div>',
    unsafe_allow_html=True
)


# ==========================================
# Book Information
# ==========================================

with st.expander("📖 বই সম্পর্কে তথ্য"):

    st.write("**বই:** বিশ্বের উপাদান")
    st.write("**লেখক:** শ্রীচারুচন্দ্র ভট্টাচার্য")
    st.write("**প্রকাশকাল:** ১৯৫২")
    st.write("**উৎস:** Bengali Wikisource")

    st.caption(
        "এই chatbot শুধুমাত্র নির্বাচিত বইয়ের তথ্য ব্যবহার করে উত্তর দেয়।"
    )


# ==========================================
# Initialize Chat History
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================================
# Display Previous Messages
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# Chat Input
# ==========================================

question = st.chat_input(
    "আপনার প্রশ্ন লিখুন..."
)


# ==========================================
# Process Question
# ==========================================

if question:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner("📚 বই থেকে তথ্য খুঁজে উত্তর তৈরি করা হচ্ছে..."):

            try:

                answer = answer_question(question)

                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                error_message = f"⚠️ একটি সমস্যা হয়েছে: {e}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )


# ==========================================
# Clear Chat Button
# ==========================================

if st.session_state.messages:

    if st.button("🗑️ Chat Clear করুন"):

        st.session_state.messages = []

        st.rerun()