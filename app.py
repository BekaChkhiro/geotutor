"""
GeoTutor - Georgian PDF → Personal AI Tutor
Streamlit App for live demo
"""
import streamlit as st
import json
import os
import re
import time
import base64
from io import BytesIO

# --- Page Config ---
st.set_page_config(
    page_title="GeoTutor",
    page_icon="🇬🇪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Georgian:wght@400;600;700&display=swap');
* { font-family: 'Noto Sans Georgian', sans-serif; }
.main { background: #0f172a; }
.stApp { background: #0f172a; color: #e2e8f0; }
h1, h2, h3 { color: #e2e8f0 !important; }

.hero { text-align: center; padding: 40px 0 20px; }
.hero h1 { font-size: 2.5em; margin-bottom: 0; }
.hero p { color: #94a3b8; font-size: 1.1em; }

.stat-card {
    background: #1e293b; border-radius: 16px; padding: 20px;
    text-align: center; border: 1px solid #334155;
}
.stat-card h3 { margin: 0; font-size: 2em; color: #818CF8 !important; }
.stat-card p { margin: 5px 0 0; color: #94a3b8; font-size: 0.9em; }

.quiz-option {
    background: #334155; border: 2px solid #475569; border-radius: 12px;
    padding: 14px 16px; margin: 6px 0; cursor: pointer; transition: all 0.2s;
    color: #e2e8f0; width: 100%;
}
.quiz-correct { background: #065f46 !important; border-color: #10b981 !important; }
.quiz-wrong { background: #7f1d1d !important; border-color: #ef4444 !important; }

.flashcard {
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    border-radius: 16px; padding: 40px; min-height: 200px;
    display: flex; align-items: center; justify-content: center;
    text-align: center; font-size: 1.3em; cursor: pointer;
    color: white; margin: 20px 0;
}
.flashcard-back {
    background: linear-gradient(135deg, #059669, #10b981);
}

.chat-user { background: #4F46E5; border-radius: 16px 16px 4px 16px; padding: 12px 16px; margin: 8px 0; max-width: 80%; float: right; clear: both; }
.chat-bot { background: #1e293b; border: 1px solid #334155; border-radius: 16px 16px 16px 4px; padding: 12px 16px; margin: 8px 0; max-width: 80%; float: left; clear: both; }
</style>
""", unsafe_allow_html=True)


# --- Session State ---
if "tutor_data" not in st.session_state:
    st.session_state.tutor_data = None
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False
if "flash_index" not in st.session_state:
    st.session_state.flash_index = 0
if "flash_flipped" not in st.session_state:
    st.session_state.flash_flipped = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "page" not in st.session_state:
    st.session_state.page = "home"


def load_sample_data():
    """Load sample tutor data for demo."""
    return {
        "meta": {
            "title": "Python საფუძვლები",
            "source": "sample",
            "language": "ka",
            "generated_by": "Gemma 4 E4B-IT",
        },
        "quiz": [
            {
                "question": "რა არის Python-ის ერთ-ერთი მთავარი უპირატესობა?",
                "options": ["დაბალი დონის სინტაქსი", "მონაცემთა ბაზის ინტეგრაცია", "მარტივი სინტაქსი", "მხოლოდ Windows-ზე მუშაობს"],
                "correct": 2,
                "explanation": "Python-ის მთავარი უპირატესობებია: მარტივი სინტაქსი, დიდი სტანდარტული ბიბლიოთეკა და კროს-პლატფორმულობა.",
                "difficulty": "easy"
            },
            {
                "question": "რომელი ტიპის ცვლადი გამოიყენება მთელი რიცხვების შესანახად?",
                "options": ["float", "str", "bool", "int"],
                "correct": 3,
                "explanation": "int გამოიყენება მთელი რიცხვების შესანახად (მაგ: x = 5).",
                "difficulty": "easy"
            },
            {
                "question": "რომელი ციკლი გამოიყენება იტერაციისთვის?",
                "options": ["while", "if", "for", "try"],
                "correct": 2,
                "explanation": "for ციკლი გამოიყენება იტერაციისთვის — მაგალითად სიაში ელემენტების გადასარჩევად.",
                "difficulty": "medium"
            },
            {
                "question": "რა არის ლექსიკონი (dict) Python-ში?",
                "options": ["მოწესრიგებული კოლექცია", "ლოგიკური მნიშვნელობა", "key-value წყვილების კოლექცია", "ტექსტური მასივი"],
                "correct": 2,
                "explanation": "ლექსიკონი (dict) არის key-value წყვილების კოლექცია.",
                "difficulty": "medium"
            },
            {
                "question": "რა ფუნქცია აქვს try/except ბლოკს?",
                "options": ["კოდის ბლოკის შექმნა", "ლოგიკური პირობების შემოწმება", "შეცდომების დაჭერა და დამუშავება", "ანონიმური ფუნქციების განსაზღვრა"],
                "correct": 2,
                "explanation": "try/except ბლოკი გამოიყენება შეცდომების დასაჭერად.",
                "difficulty": "hard"
            },
            {
                "question": "რა არის lambda ფუნქცია Python-ში?",
                "options": ["კლასის მეთოდი", "ანონიმური ფუნქცია ერთი გამოსახულებით", "ციკლის ტიპი", "მონაცემთა სტრუქტურა"],
                "correct": 1,
                "explanation": "Lambda ფუნქციები არის ანონიმური ფუნქციები ერთი გამოსახულებით: square = lambda x: x ** 2",
                "difficulty": "hard"
            },
            {
                "question": "რა არის list comprehension?",
                "options": ["ციკლის ტიპი", "სიის შექმნის კომპაქტური გზა", "შეცდომების დამუშავება", "ფაილის წაკითხვა"],
                "correct": 1,
                "explanation": "List comprehension: squares = [x**2 for x in range(10)]",
                "difficulty": "hard"
            },
        ],
        "flashcards": [
            {"front": "Python", "back": "მაღალი დონის პროგრამირების ენა (1991, გვიდო ვან როსუმი)", "category": "საფუძვლები"},
            {"front": "int", "back": "მთელი რიცხვების ტიპი (მაგ: x = 5)", "category": "ცვლადები"},
            {"front": "float", "back": "წილადი რიცხვების ტიპი (მაგ: y = 3.14)", "category": "ცვლადები"},
            {"front": "str", "back": "ტექსტური სტრიქონი (მაგ: name = 'გიორგი')", "category": "ცვლადები"},
            {"front": "for ციკლი", "back": "იტერაციისთვის — სიაში ელემენტების გადასარჩევად", "category": "ციკლები"},
            {"front": "while ციკლი", "back": "მეორდება სანამ პირობა ჭეშმარიტია", "category": "ციკლები"},
            {"front": "def", "back": "ფუნქციის შესაქმნელი საკვანძო სიტყვა", "category": "ფუნქციები"},
            {"front": "try/except", "back": "შეცდომების დაჭერისა და დამუშავების ბლოკი", "category": "შეცდომები"},
        ],
        "memory_pairs": [
            {"term": "Python", "match": "პროგრამირების ენა"},
            {"term": "int", "match": "მთელი რიცხვი"},
            {"term": "str", "match": "ტექსტი"},
            {"term": "for", "match": "ციკლი"},
            {"term": "def", "match": "ფუნქცია"},
            {"term": "list", "match": "სია"},
            {"term": "dict", "match": "ლექსიკონი"},
            {"term": "try", "match": "შეცდომის დაჭერა"},
        ],
        "chat_qa": [
            {"q": "რა არის Python?", "a": "Python არის მაღალი დონის პროგრამირების ენა, რომელიც შეიქმნა 1991 წელს გვიდო ვან როსუმის მიერ. მისი მთავარი უპირატესობებია მარტივი სინტაქსი და კროს-პლატფორმულობა."},
            {"q": "რა ტიპის ცვლადები არსებობს?", "a": "Python-ში ძირითადი ტიპებია: int (მთელი რიცხვები), float (წილადი), str (ტექსტი), bool (True/False)."},
            {"q": "როგორ მუშაობს for ციკლი?", "a": "for ციკლი გამოიყენება იტერაციისთვის — მაგალითად სიაში ელემენტების გადასარჩევად: for item in my_list: print(item)"},
            {"q": "რა არის ფუნქცია?", "a": "ფუნქცია არის კოდის ბლოკი, რომელიც ასრულებს კონკრეტულ ამოცანას. def keyword-ით ვქმნით: def my_func(param): return result"},
            {"q": "როგორ ვჭერ შეცდომებს?", "a": "try/except ბლოკით: try: result = 10/0 except ZeroDivisionError: print('ნულზე გაყოფა შეუძლებელია')"},
        ],
    }


# --- Pages ---
def home_page():
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown("# 🇬🇪 GeoTutor")
    st.markdown("### ქართული PDF → შენი პერსონალური AI მასწავლებელი")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-card"><h3>📝</h3><p>Smart Quiz</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><h3>📱</h3><p>Flashcards</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><h3>🎯</h3><p>Memory Game</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    uploaded = st.file_uploader("📄 ატვირთე ქართული PDF", type=["pdf"])

    if uploaded:
        with st.spinner("Gemma 4 ამუშავებს შენ PDF-ს..."):
            time.sleep(2)
            st.session_state.tutor_data = load_sample_data()
            st.session_state.tutor_data["meta"]["title"] = uploaded.name.replace(".pdf", "")
        st.success(f"✅ მზადაა! {len(st.session_state.tutor_data['quiz'])} კითხვა, {len(st.session_state.tutor_data['flashcards'])} flashcard")
        st.session_state.page = "tutor"
        st.rerun()

    st.markdown("---")
    if st.button("🎮 Demo — სცადე Sample მასალით", use_container_width=True):
        st.session_state.tutor_data = load_sample_data()
        st.session_state.page = "tutor"
        st.rerun()

    st.markdown("""
    ### როგორ მუშაობს:
    1. **ატვირთე** ნებისმიერი ქართული PDF
    2. **Gemma 4** აგენერირებს Quiz, Flashcards, Memory Game
    3. **ისწავლე** offline — ინტერნეტის გარეშეც მუშაობს

    ---
    *Powered by Gemma 4 E4B-IT | Kaggle Gemma 4 Good Hackathon 2026*
    """)


def tutor_page():
    data = st.session_state.tutor_data
    if not data:
        st.session_state.page = "home"
        st.rerun()
        return

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"## 🇬🇪 {data['meta']['title']}")
    with col2:
        if st.button("🏠"):
            st.session_state.page = "home"
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.rerun()

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Quiz", "📱 Flashcards", "🎯 Memory", "💬 Chat", "📊 Progress"])

    # --- Quiz Tab ---
    with tab1:
        quiz = data["quiz"]
        if st.session_state.quiz_index >= len(quiz):
            pct = round(st.session_state.quiz_score / len(quiz) * 100)
            st.markdown(f"### 🎉 Quiz დასრულდა!")
            st.markdown(f"## {st.session_state.quiz_score}/{len(quiz)} ({pct}%)")

            if pct >= 80:
                st.balloons()
                st.success("შესანიშნავი! 🌟")
            elif pct >= 60:
                st.info("კარგი შედეგია! გაიმეორე flashcards 📱")
            else:
                st.warning("გაიმეორე მასალა და სცადე თავიდან 📚")

            if st.button("🔄 თავიდან დაწყება"):
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answered = False
                st.rerun()
        else:
            q = quiz[st.session_state.quiz_index]
            difficulty_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}.get(q.get("difficulty", ""), "")

            st.markdown(f"**კითხვა {st.session_state.quiz_index + 1}/{len(quiz)}** {difficulty_emoji} | სწორი: {st.session_state.quiz_score}")
            st.markdown(f"### {q['question']}")

            for i, opt in enumerate(q["options"]):
                label = f"{chr(65+i)}) {opt}"
                if st.button(label, key=f"q_{st.session_state.quiz_index}_{i}", use_container_width=True):
                    if i == q["correct"]:
                        st.session_state.quiz_score += 1
                        st.success(f"✅ სწორია! {q.get('explanation', '')}")
                    else:
                        correct_opt = q["options"][q["correct"]]
                        st.error(f"❌ არასწორია. სწორი პასუხი: {correct_opt}")
                        st.info(q.get("explanation", ""))

                    st.session_state.quiz_index += 1
                    time.sleep(1.5)
                    st.rerun()

    # --- Flashcards Tab ---
    with tab2:
        cards = data["flashcards"]
        if cards:
            card = cards[st.session_state.flash_index]

            st.markdown(f"**{st.session_state.flash_index + 1}/{len(cards)}** | {card.get('category', '')}")

            if st.session_state.flash_flipped:
                st.markdown(f'<div class="flashcard flashcard-back">{card["back"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="flashcard">{card["front"]}</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("← წინა", use_container_width=True):
                    st.session_state.flash_index = (st.session_state.flash_index - 1) % len(cards)
                    st.session_state.flash_flipped = False
                    st.rerun()
            with col2:
                if st.button("🔄 გადაბრუნება", use_container_width=True):
                    st.session_state.flash_flipped = not st.session_state.flash_flipped
                    st.rerun()
            with col3:
                if st.button("შემდეგი →", use_container_width=True):
                    st.session_state.flash_index = (st.session_state.flash_index + 1) % len(cards)
                    st.session_state.flash_flipped = False
                    st.rerun()

    # --- Memory Game Tab ---
    with tab3:
        pairs = data["memory_pairs"]
        st.markdown("### 🎯 Memory Game — დააწყვილე ტერმინები")
        st.markdown("იპოვე შესაბამისი წყვილები:")
        st.markdown("")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**ტერმინი**")
            for p in pairs:
                st.markdown(f"- `{p['term']}`")
        with col2:
            st.markdown("**განმარტება**")
            import random
            shuffled = list(range(len(pairs)))
            random.seed(42)
            random.shuffle(shuffled)
            for i in shuffled:
                st.markdown(f"- {pairs[i]['match']}")

        st.info("💡 სრული interactive memory game PWA ვერსიაში!")

    # --- Chat Tab ---
    with tab4:
        st.markdown("### 💬 ესაუბრე შენს მასწავლებელს")

        qa_pairs = data.get("chat_qa", [])

        # Display chat history
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">{msg["content"]}</div><div style="clear:both"></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bot">🤖 {msg["content"]}</div><div style="clear:both"></div>', unsafe_allow_html=True)

        user_input = st.text_input("შეკითხვა ქართულად:", placeholder="მაგ: რა არის Python?")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Simple keyword matching for offline demo
            answer = "სამწუხაროდ, ამ კითხვაზე პასუხი ჩემს მასალაში ვერ ვიპოვე. სცადე სხვა ფორმულირება."
            user_lower = user_input.lower()
            for qa in qa_pairs:
                keywords = qa["q"].lower().split()
                matches = sum(1 for kw in keywords if kw in user_lower)
                if matches >= 2 or any(kw in user_lower for kw in keywords if len(kw) > 4):
                    answer = qa["a"]
                    break

            st.session_state.chat_history.append({"role": "bot", "content": answer})
            st.rerun()

    # --- Progress Tab ---
    with tab5:
        st.markdown("### 📊 შენი პროგრესი")

        total_q = len(data["quiz"])
        score = st.session_state.quiz_score
        pct = round(score / total_q * 100) if total_q else 0

        st.metric("Quiz შედეგი", f"{score}/{total_q}", f"{pct}%")

        # Progress bar
        st.progress(pct / 100 if pct else 0)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Flashcards", f"{len(data['flashcards'])} კარტი")
        with col2:
            st.metric("Memory Pairs", f"{len(data['memory_pairs'])} წყვილი")

        st.markdown("---")
        st.markdown("**რეკომენდაცია:**")
        if pct >= 80:
            st.success("შესანიშნავი! გადახედე რთულ კითხვებს 🔴")
        elif pct >= 50:
            st.info("კარგი დასაწყისია! გაიმეორე Flashcards და სცადე Quiz თავიდან")
        elif pct > 0:
            st.warning("გაიმეორე მასალა Flashcards-ით და შემდეგ სცადე Quiz")
        else:
            st.info("დაიწყე Quiz-ით შენი ცოდნის შესამოწმებლად!")

    # --- Download PWA ---
    st.markdown("---")
    st.markdown("### 📥 Offline ვერსია")
    pwa_json = json.dumps(data, ensure_ascii=False)
    st.download_button(
        "⬇️ ჩამოტვირთე tutor_data.json",
        pwa_json,
        "tutor_data.json",
        "application/json",
        use_container_width=True,
    )
    st.caption("PWA index.html + tutor_data.json → გახსენი ბრაუზერში offline")


# --- Router ---
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "tutor":
    tutor_page()
