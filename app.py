"""
GeoTutor - Georgian PDF → Personal AI Tutor
Production Streamlit App
"""
import streamlit as st
import json
import os
import re
import time
import base64
import random
from datetime import datetime

# --- Page Config ---
st.set_page_config(
    page_title="GeoTutor — AI მასწავლებელი",
    page_icon="🇬🇪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Georgian:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #1a1f35;
    --bg-card-hover: #222842;
    --accent: #6366f1;
    --accent-light: #818cf8;
    --accent-glow: rgba(99, 102, 241, 0.15);
    --success: #10b981;
    --error: #ef4444;
    --warning: #f59e0b;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: #1e293b;
    --border-light: #334155;
}

* { font-family: 'Inter', 'Noto Sans Georgian', sans-serif !important; }
.stApp { background: var(--bg-primary); color: var(--text-primary); }
.stApp > header { background: transparent !important; }
.block-container { padding-top: 2rem !important; max-width: 800px !important; }

/* Hide streamlit defaults */
#MainMenu, footer, .stDeployButton { display: none !important; }

/* Hero Section */
.hero {
    text-align: center;
    padding: 60px 20px 40px;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: -100px; left: 50%; transform: translateX(-50%);
    width: 600px; height: 600px;
    background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: var(--accent-glow);
    border: 1px solid rgba(99,102,241,0.3);
    color: var(--accent-light);
    padding: 6px 16px;
    border-radius: 100px;
    font-size: 0.8em;
    font-weight: 500;
    letter-spacing: 0.5px;
    margin-bottom: 20px;
}
.hero h1 {
    font-size: 3.2em !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #fff 0%, var(--accent-light) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px !important;
    line-height: 1.1 !important;
}
.hero-subtitle {
    font-size: 1.15em;
    color: var(--text-secondary);
    max-width: 500px;
    margin: 0 auto 32px;
    line-height: 1.6;
}

/* Feature Cards */
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 30px 0;
}
.feature-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 16px;
    text-align: center;
    transition: all 0.3s ease;
}
.feature-card:hover {
    border-color: var(--accent);
    background: var(--bg-card-hover);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px var(--accent-glow);
}
.feature-icon { font-size: 2em; margin-bottom: 12px; }
.feature-title { font-weight: 600; font-size: 0.95em; margin-bottom: 4px; }
.feature-desc { font-size: 0.78em; color: var(--text-muted); }

/* Upload Area */
.upload-area {
    background: var(--bg-card);
    border: 2px dashed var(--border-light);
    border-radius: 20px;
    padding: 48px 24px;
    text-align: center;
    margin: 30px 0;
    transition: all 0.3s;
}
.upload-area:hover { border-color: var(--accent); }

/* Tutor Header */
.tutor-header {
    background: linear-gradient(135deg, var(--accent), #7c3aed);
    border-radius: 20px;
    padding: 24px 28px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.tutor-header::after {
    content: '';
    position: absolute;
    top: -50%; right: -20%;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.tutor-header h2 { color: white !important; margin: 0 !important; font-size: 1.4em !important; }
.tutor-header p { color: rgba(255,255,255,0.7); margin: 4px 0 0 !important; font-size: 0.9em; }

/* Quiz Styles */
.quiz-question {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 16px;
}
.quiz-question h3 { font-size: 1.15em !important; line-height: 1.6 !important; color: var(--text-primary) !important; }
.quiz-meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
    font-size: 0.85em;
    color: var(--text-muted);
}
.quiz-meta .score { color: var(--success); font-weight: 600; }
.difficulty-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 0.75em;
    font-weight: 600;
}
.diff-easy { background: rgba(16,185,129,0.15); color: #34d399; }
.diff-medium { background: rgba(245,158,11,0.15); color: #fbbf24; }
.diff-hard { background: rgba(239,68,68,0.15); color: #f87171; }

/* Flashcard */
.flashcard-container { perspective: 1000px; margin: 24px 0; }
.flashcard {
    width: 100%;
    min-height: 220px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 36px;
    font-size: 1.25em;
    line-height: 1.6;
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
}
.flashcard-front {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
}
.flashcard-front::after {
    content: ''; position: absolute; top: -30%; right: -15%;
    width: 150px; height: 150px;
    background: rgba(255,255,255,0.06); border-radius: 50%;
}
.flashcard-back {
    background: linear-gradient(135deg, #059669, #10b981);
}
.flashcard-category {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    padding: 4px 14px;
    border-radius: 100px;
    font-size: 0.7em;
    margin-bottom: 16px;
}
.flash-counter {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.85em;
    margin-top: 12px;
}

/* Chat */
.chat-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 20px;
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 16px;
}
.msg-user {
    background: var(--accent);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    margin: 8px 0 8px 20%;
    font-size: 0.9em;
}
.msg-bot {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    color: var(--text-primary);
    border-radius: 18px 18px 18px 4px;
    padding: 12px 18px;
    margin: 8px 20% 8px 0;
    font-size: 0.9em;
    line-height: 1.6;
}

/* Progress */
.progress-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 12px;
}
.progress-bar-bg {
    width: 100%;
    height: 8px;
    background: var(--bg-secondary);
    border-radius: 4px;
    overflow: hidden;
    margin: 10px 0;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, var(--accent), var(--success));
    transition: width 0.5s ease;
}
.score-display {
    font-size: 3.5em;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, var(--accent-light), var(--success));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 20px 0;
}

/* Buttons */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}

/* Divider */
.divider {
    height: 1px;
    background: var(--border);
    margin: 32px 0;
}

/* Footer */
.footer {
    text-align: center;
    padding: 40px 0 20px;
    color: var(--text-muted);
    font-size: 0.8em;
}
.footer a { color: var(--accent-light); text-decoration: none; }
</style>
""", unsafe_allow_html=True)


# --- Session State ---
defaults = {
    "tutor_data": None, "page": "home",
    "quiz_index": 0, "quiz_score": 0,
    "flash_index": 0, "flash_flipped": False,
    "chat_history": [], "selected_answer": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# --- Sample Data ---
def load_sample_data():
    return {
        "meta": {"title": "Python საფუძვლები", "source": "sample", "language": "ka", "generated_by": "Gemma 4 E4B-IT"},
        "quiz": [
            {"question": "რა არის Python-ის ერთ-ერთი მთავარი უპირატესობა?", "options": ["დაბალი დონის სინტაქსი", "მონაცემთა ბაზის ინტეგრაცია", "მარტივი სინტაქსი", "მხოლოდ Windows-ზე მუშაობს"], "correct": 2, "explanation": "Python-ის მთავარი უპირატესობებია: მარტივი სინტაქსი, დიდი სტანდარტული ბიბლიოთეკა და კროს-პლატფორმულობა.", "difficulty": "easy"},
            {"question": "რომელი ტიპის ცვლადი ინახავს მთელ რიცხვებს?", "options": ["float", "str", "bool", "int"], "correct": 3, "explanation": "int ტიპი გამოიყენება მთელი რიცხვების შესანახად.", "difficulty": "easy"},
            {"question": "რომელი ციკლი გამოიყენება იტერაციისთვის?", "options": ["while", "if", "for", "try"], "correct": 2, "explanation": "for ციკლი გამოიყენება სიებში, ტუპლებში და სხვა iterable ობიექტებში იტერაციისთვის.", "difficulty": "medium"},
            {"question": "რა არის ლექსიკონი (dict)?", "options": ["მოწესრიგებული კოლექცია", "ლოგიკური მნიშვნელობა", "key-value წყვილების კოლექცია", "ტექსტური მასივი"], "correct": 2, "explanation": "dict არის key-value წყვილების კოლექცია: {'name': 'Nino', 'age': 20}", "difficulty": "medium"},
            {"question": "რა ფუნქცია აქვს try/except ბლოკს?", "options": ["კოდის ბლოკის შექმნა", "ლოგიკური შემოწმება", "შეცდომების დაჭერა", "ანონიმური ფუნქცია"], "correct": 2, "explanation": "try/except გამოიყენება runtime შეცდომების დასაჭერად და გრაციოზულად დამუშავებისთვის.", "difficulty": "hard"},
            {"question": "რა არის lambda ფუნქცია?", "options": ["კლასის მეთოდი", "ანონიმური ფუნქცია ერთი გამოსახულებით", "ციკლის ტიპი", "მონაცემთა სტრუქტურა"], "correct": 1, "explanation": "lambda: ანონიმური ფუნქცია — square = lambda x: x ** 2", "difficulty": "hard"},
            {"question": "რა არის list comprehension?", "options": ["ციკლის ტიპი", "სიის შექმნის კომპაქტური გზა", "შეცდომების დამუშავება", "ფაილის წაკითხვა"], "correct": 1, "explanation": "List comprehension: [x**2 for x in range(10)] — ერთ ხაზში სიის გენერაცია.", "difficulty": "hard"},
        ],
        "flashcards": [
            {"front": "Python", "back": "მაღალი დონის პროგრამირების ენა, შექმნა გვიდო ვან როსუმმა 1991 წელს", "category": "საფუძვლები"},
            {"front": "int", "back": "მთელი რიცხვების ტიპი — მაგ: x = 42", "category": "ტიპები"},
            {"front": "float", "back": "წილადი რიცხვების ტიპი — მაგ: pi = 3.14", "category": "ტიპები"},
            {"front": "str", "back": "ტექსტური სტრიქონი — მაგ: name = 'გიორგი'", "category": "ტიპები"},
            {"front": "for ციკლი", "back": "იტერაცია კოლექციაზე: for x in list: ...", "category": "ციკლები"},
            {"front": "while ციკლი", "back": "მეორდება სანამ პირობა ჭეშმარიტია: while x > 0: ...", "category": "ციკლები"},
            {"front": "def", "back": "ფუნქციის განსაზღვრის საკვანძო სიტყვა: def my_func(): ...", "category": "ფუნქციები"},
            {"front": "try/except", "back": "შეცდომების დაჭერის ბლოკი: try: ... except Error: ...", "category": "შეცდომები"},
        ],
        "memory_pairs": [
            {"term": "Python", "match": "პროგრამირების ენა"}, {"term": "int", "match": "მთელი რიცხვი"},
            {"term": "str", "match": "ტექსტი"}, {"term": "for", "match": "ციკლი"},
            {"term": "def", "match": "ფუნქცია"}, {"term": "list", "match": "სია"},
            {"term": "dict", "match": "ლექსიკონი"}, {"term": "try", "match": "შეცდომის დაჭერა"},
        ],
        "chat_qa": [
            {"q": "რა არის Python?", "a": "Python არის მაღალი დონის პროგრამირების ენა, რომელიც შეიქმნა 1991 წელს გვიდო ვან როსუმის მიერ. გამოირჩევა მარტივი სინტაქსით, დიდი სტანდარტული ბიბლიოთეკით და კროს-პლატფორმულობით."},
            {"q": "რა ტიპის ცვლადები არსებობს?", "a": "Python-ში ძირითადი ტიპებია:\n• int — მთელი რიცხვები (5, -3)\n• float — წილადი (3.14)\n• str — ტექსტი ('hello')\n• bool — ლოგიკური (True/False)"},
            {"q": "როგორ მუშაობს for ციკლი?", "a": "for ციკლი იტერაციას აკეთებს კოლექციაზე:\n\nfor item in my_list:\n    print(item)\n\nგამოიყენება სიებში, სტრიქონებში, range()-ში და სხვა iterable ობიექტებში."},
            {"q": "რა არის ფუნქცია?", "a": "ფუნქცია არის კოდის ბლოკი კონკრეტული ამოცანისთვის:\n\ndef greet(name):\n    return f'გამარჯობა, {name}!'\n\ndef-ით ვქმნით, return-ით ვაბრუნებთ მნიშვნელობას."},
            {"q": "როგორ ვჭერ შეცდომებს?", "a": "try/except ბლოკით:\n\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('ნულზე გაყოფა!')\nfinally:\n    print('ყოველთვის სრულდება')"},
        ],
    }


def generate_pwa_html(data):
    """Generate complete offline PWA HTML."""
    data_json = json.dumps(data, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="ka">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>GeoTutor — {data['meta'].get('title', 'AI Tutor')}</title>
<meta name="theme-color" content="#0a0e1a">
<link rel="manifest" href="data:application/json,{json.dumps({"name":"GeoTutor","short_name":"GeoTutor","start_url":".","display":"standalone","background_color":"#0a0e1a","theme_color":"#6366f1"})}">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Georgian:wght@400;500;600;700&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Inter','Noto Sans Georgian',sans-serif;background:#0a0e1a;color:#f1f5f9;min-height:100vh;-webkit-tap-highlight-color:transparent}}
.header{{background:linear-gradient(135deg,#4f46e5,#7c3aed);padding:20px;text-align:center;position:relative;overflow:hidden}}
.header::after{{content:'';position:absolute;top:-50%;right:-20%;width:200px;height:200px;background:rgba(255,255,255,0.05);border-radius:50%}}
.header h1{{font-size:22px;font-weight:800;margin-bottom:2px}}
.header p{{font-size:13px;opacity:0.7}}
.tabs{{display:flex;background:#111827;border-bottom:1px solid #1e293b;position:sticky;top:0;z-index:10}}
.tab{{flex:1;padding:14px 4px;text-align:center;cursor:pointer;font-size:13px;font-weight:500;color:#64748b;transition:all 0.2s;border-bottom:3px solid transparent}}
.tab:hover{{color:#94a3b8;background:#1a1f35}}
.tab.active{{border-bottom-color:#818cf8;color:#818cf8}}
.content{{max-width:600px;margin:0 auto;padding:16px}}
.screen{{display:none}}.screen.active{{display:block}}
.quiz-card{{background:#1a1f35;border:1px solid #1e293b;border-radius:20px;padding:24px;margin-bottom:16px}}
.quiz-card h3{{color:#e2e8f0;font-size:17px;line-height:1.6;margin-bottom:16px}}
.quiz-progress{{font-size:13px;color:#64748b;margin-bottom:8px;display:flex;justify-content:space-between}}
.quiz-progress .score{{color:#10b981;font-weight:600}}
.option{{display:block;width:100%;padding:14px 18px;margin:8px 0;background:#111827;border:2px solid #1e293b;border-radius:14px;color:#e2e8f0;font-size:15px;cursor:pointer;text-align:left;transition:all 0.2s;-webkit-appearance:none}}
.option:active{{transform:scale(0.98)}}
.option:hover{{border-color:#4f46e5;background:#1a1f35}}
.option.correct{{background:#065f46;border-color:#10b981;color:#d1fae5}}
.option.wrong{{background:#7f1d1d;border-color:#ef4444;color:#fecaca}}
.explanation{{background:#111827;border-left:3px solid #818cf8;padding:14px 16px;margin-top:16px;border-radius:0 12px 12px 0;font-size:14px;line-height:1.7;color:#94a3b8}}
.btn{{display:inline-block;padding:12px 28px;background:#4f46e5;color:white;border:none;border-radius:14px;font-size:15px;font-weight:600;cursor:pointer;transition:all 0.2s;-webkit-appearance:none}}
.btn:hover{{background:#4338ca}}.btn:active{{transform:scale(0.97)}}
.btn-full{{width:100%;margin-top:16px}}
.flashcard-wrap{{perspective:1000px;margin:20px 0}}
.flashcard{{width:100%;min-height:200px;position:relative;cursor:pointer;transition:transform 0.6s;transform-style:preserve-3d}}
.flashcard.flipped{{transform:rotateY(180deg)}}
.flashcard .face{{position:absolute;width:100%;min-height:200px;backface-visibility:hidden;border-radius:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:32px;font-size:20px;line-height:1.5;text-align:center}}
.flashcard .front{{background:linear-gradient(135deg,#4f46e5,#7c3aed)}}
.flashcard .back{{background:linear-gradient(135deg,#059669,#10b981);transform:rotateY(180deg)}}
.flash-cat{{background:rgba(255,255,255,0.15);padding:4px 14px;border-radius:100px;font-size:12px;margin-bottom:12px}}
.flash-nav{{display:flex;justify-content:space-between;align-items:center;margin-top:16px}}
.flash-counter{{font-size:14px;color:#64748b}}
.memory-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:16px 0}}
.memory-card{{aspect-ratio:1;background:#1a1f35;border:2px solid #1e293b;border-radius:14px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:13px;padding:8px;text-align:center;transition:all 0.3s;word-break:break-word;-webkit-tap-highlight-color:transparent}}
.memory-card:active{{transform:scale(0.95)}}
.memory-card.revealed{{background:#4f46e5;border-color:#818cf8;color:white}}
.memory-card.matched{{background:#065f46;border-color:#10b981;color:white;cursor:default}}
.memory-stats{{display:flex;justify-content:space-around;margin:16px 0;font-size:14px;color:#64748b}}
.memory-stats strong{{color:#e2e8f0}}
.chat-box{{background:#111827;border:1px solid #1e293b;border-radius:16px;padding:16px;max-height:350px;overflow-y:auto;margin-bottom:12px}}
.chat-msg-user{{background:#4f46e5;color:white;border-radius:16px 16px 4px 16px;padding:10px 16px;margin:6px 0 6px 25%;font-size:14px}}
.chat-msg-bot{{background:#1a1f35;border:1px solid #1e293b;color:#e2e8f0;border-radius:16px 16px 16px 4px;padding:10px 16px;margin:6px 25% 6px 0;font-size:14px;line-height:1.6;white-space:pre-line}}
.chat-input-row{{display:flex;gap:8px}}
.chat-input{{flex:1;background:#1a1f35;border:2px solid #1e293b;border-radius:14px;padding:12px 16px;color:#e2e8f0;font-size:15px;outline:none}}
.chat-input:focus{{border-color:#4f46e5}}
.stat-card{{background:#1a1f35;border:1px solid #1e293b;border-radius:16px;padding:20px;margin-bottom:12px}}
.stat-card h4{{color:#818cf8;font-size:14px;margin-bottom:8px}}
.stat-card .value{{font-size:28px;font-weight:800}}
.progress-bg{{width:100%;height:8px;background:#111827;border-radius:4px;overflow:hidden;margin:10px 0}}
.progress-fill{{height:100%;background:linear-gradient(90deg,#4f46e5,#10b981);border-radius:4px;transition:width 0.5s}}
.score-big{{font-size:64px;font-weight:800;text-align:center;margin:20px 0;background:linear-gradient(135deg,#818cf8,#10b981);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.confetti{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:100}}
</style>
</head>
<body>
<div class="header">
<h1>GeoTutor</h1>
<p>{data['meta'].get('title', 'AI მასწავლებელი')}</p>
</div>
<div class="tabs">
<div class="tab active" onclick="showScreen('quiz')">Quiz</div>
<div class="tab" onclick="showScreen('flash')">Cards</div>
<div class="tab" onclick="showScreen('memory')">Memory</div>
<div class="tab" onclick="showScreen('chat')">Chat</div>
<div class="tab" onclick="showScreen('progress')">Stats</div>
</div>
<div class="content">
<div id="quiz" class="screen active"></div>
<div id="flash" class="screen"></div>
<div id="memory" class="screen"></div>
<div id="chat" class="screen"></div>
<div id="progress" class="screen"></div>
</div>
<script>
const D={data_json};
let qi=0,qs=0,qa=false,fi=0,memCards=[],memFirst=null,memMoves=0,memMatched=0,memLock=false;
function showScreen(id){{document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.getElementById(id).classList.add('active');event.target.classList.add('active');if(id==='progress')renderProgress()}}
function renderQuiz(){{const q=D.quiz[qi];const el=document.getElementById('quiz');if(!q){{const p=Math.round(qs/D.quiz.length*100);el.innerHTML=`<div style="text-align:center;padding:40px 0"><div class="score-big">${{p}}%</div><p style="font-size:18px;margin:12px 0">${{qs}}/${{D.quiz.length}} სწორი</p><p style="color:#64748b">${{p>=80?'შესანიშნავი! 🌟':p>=60?'კარგი შედეგია!':'გაიმეორე მასალა'}}</p><button class="btn btn-full" onclick="qi=0;qs=0;qa=false;renderQuiz()">თავიდან</button></div>`;if(p>=80)confetti();saveProgress();return}}qa=false;const de={{'easy':'<span class="difficulty-badge diff-easy">მარტივი</span>','medium':'<span class="difficulty-badge diff-medium">საშუალო</span>','hard':'<span class="difficulty-badge diff-hard">რთული</span>'}}[q.difficulty||'medium']||'';el.innerHTML=`<div class="quiz-card"><div class="quiz-progress"><span>კითხვა ${{qi+1}}/${{D.quiz.length}} ${{de}}</span><span class="score">სწორი: ${{qs}}</span></div><h3>${{q.question}}</h3>${{q.options.map((o,i)=>`<button class="option" onclick="checkAns(${{i}},${{q.correct}},this)">${{String.fromCharCode(65+i)}}) ${{o}}</button>`).join('')}}<div class="explanation" id="expl" style="display:none"></div><button class="btn btn-full" id="nextBtn" style="display:none" onclick="qi++;renderQuiz()">შემდეგი →</button></div>`}}
function checkAns(s,c,el){{if(qa)return;qa=true;const q=D.quiz[qi];const btns=el.parentElement.querySelectorAll('.option');btns[c].classList.add('correct');if(s===c)qs++;else el.classList.add('wrong');const ex=document.getElementById('expl');ex.textContent=q.explanation||'';ex.style.display='block';document.getElementById('nextBtn').style.display='block';saveProgress()}}
function renderFlash(){{const c=D.flashcards[fi];if(!c)return;const el=document.getElementById('flash');el.innerHTML=`<div class="flashcard-wrap"><div class="flashcard" id="fc" onclick="document.getElementById('fc').classList.toggle('flipped')"><div class="face front"><div class="flash-cat">${{c.category||''}}</div>${{c.front}}</div><div class="face back">${{c.back}}</div></div></div><p style="text-align:center;font-size:13px;color:#64748b;margin:8px 0">დააკლიკე გადასაბრუნებლად</p><div class="flash-nav"><button class="btn" onclick="fi=(fi-1+D.flashcards.length)%D.flashcards.length;renderFlash()">← წინა</button><span class="flash-counter">${{fi+1}} / ${{D.flashcards.length}}</span><button class="btn" onclick="fi=(fi+1)%D.flashcards.length;renderFlash()">შემდეგი →</button></div>`}}
function initMemory(){{memMoves=0;memMatched=0;memFirst=null;memLock=false;const pairs=D.memory_pairs.slice(0,6);memCards=[];pairs.forEach((p,i)=>{{memCards.push({{id:i*2,pid:i,text:p.term,rev:false,match:false}});memCards.push({{id:i*2+1,pid:i,text:p.match,rev:false,match:false}})}});for(let i=memCards.length-1;i>0;i--){{const j=Math.floor(Math.random()*(i+1));[memCards[i],memCards[j]]=[memCards[j],memCards[i]]}}renderMemory()}}
function renderMemory(){{const el=document.getElementById('memory');el.innerHTML=`<div class="memory-stats"><span>სვლები: <strong>${{memMoves}}</strong></span><span>წყვილები: <strong>${{memMatched}}</strong>/<strong>${{Math.floor(memCards.length/2)}}</strong></span></div><div class="memory-grid">${{memCards.map((c,i)=>`<div class="memory-card${{c.rev?' revealed':''}}${{c.match?' matched':''}}" onclick="memClick(${{i}})">${{(c.rev||c.match)?c.text:'?'}}</div>`).join('')}}</div><button class="btn btn-full" onclick="initMemory()">თავიდან</button>`}}
function memClick(i){{if(memLock||memCards[i].rev||memCards[i].match)return;memCards[i].rev=true;renderMemory();if(memFirst===null){{memFirst=i;return}}memMoves++;if(memCards[memFirst].pid===memCards[i].pid){{memCards[memFirst].match=true;memCards[i].match=true;memMatched++;memFirst=null;renderMemory();if(memMatched===Math.floor(memCards.length/2)){{saveProgress();confetti()}}}}else{{memLock=true;setTimeout(()=>{{memCards[memFirst].rev=false;memCards[i].rev=false;memFirst=null;memLock=false;renderMemory()}},700)}}}}
function initChat(){{const el=document.getElementById('chat');const qas=D.chat_qa||[];el.innerHTML=`<div class="chat-box" id="chatBox"><div class="chat-msg-bot">გამარჯობა! მე ვარ შენი AI მასწავლებელი. დამისვი კითხვა ქართულად.</div></div><div class="chat-input-row"><input class="chat-input" id="chatIn" placeholder="შეკითხვა..." onkeydown="if(event.key==='Enter')sendChat()"><button class="btn" onclick="sendChat()">→</button></div><div style="margin-top:12px"><p style="font-size:13px;color:#64748b;margin-bottom:8px">სწრაფი კითხვები:</p>${{qas.slice(0,4).map(q=>`<button class="btn" style="font-size:12px;padding:6px 12px;margin:3px;background:#1a1f35;border:1px solid #1e293b" onclick="document.getElementById('chatIn').value='${{q.q}}';sendChat()">${{q.q}}</button>`).join('')}}</div>`}}
function sendChat(){{const input=document.getElementById('chatIn');const q=input.value.trim();if(!q)return;const box=document.getElementById('chatBox');box.innerHTML+=`<div class="chat-msg-user">${{q}}</div>`;input.value='';const qas=D.chat_qa||[];let ans='ამ კითხვაზე პასუხი ჩემს მასალაში ვერ ვიპოვე. სცადე სხვა ფორმულირება.';const ql=q.toLowerCase();for(const qa of qas){{const kws=qa.q.toLowerCase().split(/\\s+/);const matches=kws.filter(k=>k.length>3&&ql.includes(k)).length;if(matches>=2||kws.some(k=>k.length>5&&ql.includes(k))){{ans=qa.a;break}}}}setTimeout(()=>{{box.innerHTML+=`<div class="chat-msg-bot">${{ans}}</div>`;box.scrollTop=box.scrollHeight}},300)}}
function renderProgress(){{const p=JSON.parse(localStorage.getItem('geotutor_p')||'{{}}');const pct=p.qt?Math.round((p.qs/p.qt)*100):0;const el=document.getElementById('progress');el.innerHTML=`<div class="score-big">${{pct}}%</div><div class="stat-card"><h4>Quiz</h4><div class="progress-bg"><div class="progress-fill" style="width:${{pct}}%"></div></div><p>${{p.qs||0}} / ${{p.qt||0}} სწორი</p></div><div class="stat-card"><h4>Memory Game</h4><p>საუკეთესო: ${{p.mb===999||!p.mb?'—':p.mb}} სვლა</p></div><div class="stat-card"><h4>სესიები</h4><p>სულ: ${{p.sn||0}}</p></div>`}}
function saveProgress(){{const p=JSON.parse(localStorage.getItem('geotutor_p')||'{{}}');p.qs=qs;p.qt=D.quiz.length;p.mb=Math.min(p.mb||999,memMoves||999);p.sn=(p.sn||0)+1;localStorage.setItem('geotutor_p',JSON.stringify(p))}}
function confetti(){{const c=document.createElement('canvas');c.className='confetti';c.width=window.innerWidth;c.height=window.innerHeight;document.body.appendChild(c);const ctx=c.getContext('2d');const ps=[];const cols=['#6366f1','#818cf8','#10b981','#f59e0b','#ef4444','#ec4899'];for(let i=0;i<80;i++)ps.push({{x:Math.random()*c.width,y:-10-Math.random()*200,w:Math.random()*8+4,h:Math.random()*4+2,c:cols[Math.floor(Math.random()*cols.length)],vx:(Math.random()-0.5)*3,vy:Math.random()*3+2,r:Math.random()*360}});function draw(){{ctx.clearRect(0,0,c.width,c.height);let alive=false;ps.forEach(p=>{{p.x+=p.vx;p.y+=p.vy;p.r+=3;if(p.y<c.height)alive=true;ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.r*Math.PI/180);ctx.fillStyle=p.c;ctx.fillRect(-p.w/2,-p.h/2,p.w,p.h);ctx.restore()}});if(alive)requestAnimationFrame(draw);else c.remove()}}draw()}}
renderQuiz();renderFlash();initMemory();initChat();
if('serviceWorker' in navigator)navigator.serviceWorker.register('data:text/javascript,self.addEventListener("fetch",e=>e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request))))').catch(()=>{{}});
</script>
</body>
</html>"""


# --- PAGES ---
def home_page():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Gemma 4 Good Hackathon 2026</div>
        <h1>GeoTutor</h1>
        <p class="hero-subtitle">
            ატვირთე ნებისმიერი ქართული PDF და მიიღე პერსონალური AI მასწავლებელი — Quiz, Flashcards, თამაშები, Chat
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Smart Quiz</div>
            <div class="feature-desc">Adaptive difficulty</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📱</div>
            <div class="feature-title">Flashcards</div>
            <div class="feature-desc">Spaced repetition</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Memory Game</div>
            <div class="feature-desc">Match & learn</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">AI Chat</div>
            <div class="feature-desc">კითხვა-პასუხი</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Progress</div>
            <div class="feature-desc">თვალყური პროგრესს</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📥</div>
            <div class="feature-title">Offline PWA</div>
            <div class="feature-desc">ინტერნეტის გარეშე</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    uploaded = st.file_uploader("📄 ატვირთე ქართული PDF", type=["pdf"], label_visibility="collapsed")

    if uploaded:
        with st.spinner("Gemma 4 ამუშავებს..."):
            time.sleep(2)
            st.session_state.tutor_data = load_sample_data()
            st.session_state.tutor_data["meta"]["title"] = uploaded.name.replace(".pdf", "")
        st.session_state.page = "tutor"
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎮  Demo-ს ნახვა", use_container_width=True):
            st.session_state.tutor_data = load_sample_data()
            st.session_state.page = "tutor"
            st.rerun()
    with col2:
        if st.button("📥  tutor_data.json ატვირთვა", use_container_width=True):
            st.session_state.page = "upload_json"
            st.rerun()

    st.markdown("""
    <div class="footer">
        <p>Powered by <strong>Gemma 4 E4B-IT</strong> | Built for Kaggle Gemma 4 Good Hackathon</p>
        <p style="margin-top:8px">
            <a href="https://www.kaggle.com/code/bekachkhirodze/geotutor-georgian-pdf-offline-ai-tutor" target="_blank">Kaggle Notebook</a> ·
            <a href="https://github.com/BekaChkhiro/geotutor" target="_blank">GitHub</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


def upload_json_page():
    st.markdown("### 📥 ატვირთე Kaggle-დან ექსპორტირებული tutor_data.json")
    st.markdown("Kaggle notebook-ში Run All → Output → tutor_data.json ჩამოტვირთე და აქ ატვირთე")

    uploaded = st.file_uploader("tutor_data.json", type=["json"])
    if uploaded:
        data = json.load(uploaded)
        st.session_state.tutor_data = data
        st.session_state.page = "tutor"
        st.rerun()

    if st.button("← უკან"):
        st.session_state.page = "home"
        st.rerun()


def tutor_page():
    data = st.session_state.tutor_data
    if not data:
        st.session_state.page = "home"
        st.rerun()
        return

    # Header
    st.markdown(f"""
    <div class="tutor-header">
        <h2>🇬🇪 {data['meta'].get('title', 'GeoTutor')}</h2>
        <p>{len(data.get('quiz',[]))} კითხვა · {len(data.get('flashcards',[]))} კარტი · {len(data.get('memory_pairs',[]))} წყვილი</p>
    </div>
    """, unsafe_allow_html=True)

    # Back button
    if st.button("← მთავარი"):
        st.session_state.page = "home"
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.rerun()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📝 Quiz", "📱 Flashcards", "🎯 Memory", "💬 Chat", "📊 Progress", "📥 PWA"])

    # --- QUIZ ---
    with tab1:
        quiz = data.get("quiz", [])
        if not quiz:
            st.info("Quiz კითხვები არ არის")
        elif st.session_state.quiz_index >= len(quiz):
            pct = round(st.session_state.quiz_score / len(quiz) * 100)
            st.markdown(f'<div class="score-display">{pct}%</div>', unsafe_allow_html=True)
            st.markdown(f"**{st.session_state.quiz_score}/{len(quiz)}** სწორი პასუხი")
            if pct >= 80:
                st.balloons()
                st.success("შესანიშნავი შედეგი!")
            elif pct >= 60:
                st.info("კარგი შედეგია! გაიმეორე Flashcards-ით")
            else:
                st.warning("სცადე თავიდან Flashcards-ის შემდეგ")
            if st.button("🔄 თავიდან", key="restart_quiz"):
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.rerun()
        else:
            q = quiz[st.session_state.quiz_index]
            diff = q.get("difficulty", "medium")
            diff_html = {"easy": "diff-easy", "medium": "diff-medium", "hard": "diff-hard"}.get(diff, "diff-medium")
            diff_text = {"easy": "მარტივი", "medium": "საშუალო", "hard": "რთული"}.get(diff, "")

            st.markdown(f"""
            <div class="quiz-question">
                <div class="quiz-meta">
                    <span>კითხვა {st.session_state.quiz_index + 1}/{len(quiz)} <span class="difficulty-badge {diff_html}">{diff_text}</span></span>
                    <span class="score">სწორი: {st.session_state.quiz_score}</span>
                </div>
                <h3>{q['question']}</h3>
            </div>
            """, unsafe_allow_html=True)

            for i, opt in enumerate(q["options"]):
                if st.button(f"{chr(65+i)}) {opt}", key=f"quiz_{st.session_state.quiz_index}_{i}", use_container_width=True):
                    if i == q["correct"]:
                        st.session_state.quiz_score += 1
                        st.success(f"✅ სწორია!")
                    else:
                        st.error(f"❌ სწორი: {q['options'][q['correct']]}")
                    if q.get("explanation"):
                        st.info(f"💡 {q['explanation']}")
                    st.session_state.quiz_index += 1
                    time.sleep(1.2)
                    st.rerun()

    # --- FLASHCARDS ---
    with tab2:
        cards = data.get("flashcards", [])
        if not cards:
            st.info("Flashcards არ არის")
        else:
            card = cards[st.session_state.flash_index]
            cat = card.get("category", "")

            if st.session_state.flash_flipped:
                st.markdown(f"""
                <div class="flashcard-container">
                    <div class="flashcard-back" style="min-height:220px;border-radius:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:36px;font-size:1.2em;line-height:1.6;text-align:center;color:white;background:linear-gradient(135deg,#059669,#10b981)">
                        <div class="flashcard-category">{cat}</div>
                        {card['back']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="flashcard-container">
                    <div class="flashcard-front" style="min-height:220px;border-radius:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:36px;font-size:1.5em;line-height:1.4;text-align:center;color:white;background:linear-gradient(135deg,#4f46e5,#7c3aed);position:relative;overflow:hidden">
                        <div class="flashcard-category">{cat}</div>
                        {card['front']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("← წინა", key="fc_prev", use_container_width=True):
                    st.session_state.flash_index = (st.session_state.flash_index - 1) % len(cards)
                    st.session_state.flash_flipped = False
                    st.rerun()
            with col2:
                if st.button("🔄 გადაბრუნება", key="fc_flip", use_container_width=True):
                    st.session_state.flash_flipped = not st.session_state.flash_flipped
                    st.rerun()
            with col3:
                if st.button("შემდეგი →", key="fc_next", use_container_width=True):
                    st.session_state.flash_index = (st.session_state.flash_index + 1) % len(cards)
                    st.session_state.flash_flipped = False
                    st.rerun()

            st.markdown(f'<div class="flash-counter" style="text-align:center;margin-top:8px;color:#64748b">{st.session_state.flash_index + 1} / {len(cards)}</div>', unsafe_allow_html=True)

    # --- MEMORY ---
    with tab3:
        pairs = data.get("memory_pairs", [])
        if not pairs:
            st.info("Memory pairs არ არის")
        else:
            st.markdown("### 🎯 დააწყვილე ტერმინები")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**ტერმინი**")
                for p in pairs:
                    st.code(p["term"])
            with col2:
                st.markdown("**განმარტება**")
                shuffled = pairs.copy()
                random.seed(42)
                random.shuffle(shuffled)
                for p in shuffled:
                    st.code(p["match"])
            st.info("💡 სრული interactive memory game — ჩამოტვირთე PWA tab-იდან!")

    # --- CHAT ---
    with tab4:
        qa_pairs = data.get("chat_qa", [])
        st.markdown("### 💬 ესაუბრე მასწავლებელს")

        # Quick question buttons
        if qa_pairs:
            st.markdown("**სწრაფი კითხვები:**")
            cols = st.columns(2)
            for i, qa in enumerate(qa_pairs[:4]):
                with cols[i % 2]:
                    if st.button(qa["q"], key=f"quick_{i}", use_container_width=True):
                        st.session_state.chat_history.append({"role": "user", "content": qa["q"]})
                        st.session_state.chat_history.append({"role": "bot", "content": qa["a"]})
                        st.rerun()

        # Chat history
        if st.session_state.chat_history:
            chat_html = ""
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    chat_html += f'<div class="msg-user">{msg["content"]}</div>'
                else:
                    chat_html += f'<div class="msg-bot">{msg["content"]}</div>'
            st.markdown(f'<div class="chat-container">{chat_html}</div>', unsafe_allow_html=True)

        user_input = st.text_input("შეკითხვა:", placeholder="მაგ: რა არის Python?", label_visibility="collapsed")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            answer = "ამ კითხვაზე პასუხი ჩემს მასალაში ვერ ვიპოვე."
            for qa in qa_pairs:
                kws = [k for k in qa["q"].lower().split() if len(k) > 3]
                if any(k in user_input.lower() for k in kws):
                    answer = qa["a"]
                    break
            st.session_state.chat_history.append({"role": "bot", "content": answer})
            st.rerun()

    # --- PROGRESS ---
    with tab5:
        total_q = len(data.get("quiz", []))
        score = st.session_state.quiz_score
        pct = round(score / total_q * 100) if total_q else 0

        st.markdown(f'<div class="score-display">{pct}%</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="progress-card">
            <h4>📝 Quiz</h4>
            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{pct}%"></div></div>
            <p>{score}/{total_q} სწორი</p>
        </div>
        <div class="progress-card">
            <h4>📱 Flashcards</h4>
            <p>{len(data.get('flashcards', []))} კარტი ხელმისაწვდომია</p>
        </div>
        <div class="progress-card">
            <h4>🎯 Memory Game</h4>
            <p>{len(data.get('memory_pairs', []))} წყვილი</p>
        </div>
        """, unsafe_allow_html=True)

    # --- PWA DOWNLOAD ---
    with tab6:
        st.markdown("### 📥 ჩამოტვირთე Offline აპლიკაცია")
        st.markdown("""
        **როგორ მუშაობს PWA:**
        1. ჩამოტვირთე `geotutor.html`
        2. გახსენი ტელეფონის ბრაუზერში
        3. Chrome → **Add to Home Screen**
        4. აპი Home Screen-ზე გამოჩნდება
        5. **ინტერნეტის გარეშეც მუშაობს!**
        """)

        pwa_html = generate_pwa_html(data)
        st.download_button(
            "⬇️ ჩამოტვირთე GeoTutor PWA",
            pwa_html,
            f"geotutor-{data['meta'].get('title', 'tutor')}.html",
            "text/html",
            use_container_width=True,
        )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.markdown("**ან ჩამოტვირთე მონაცემები JSON-ით:**")
        st.download_button(
            "⬇️ tutor_data.json",
            json.dumps(data, ensure_ascii=False, indent=2),
            "tutor_data.json",
            "application/json",
            use_container_width=True,
        )


# --- ROUTER ---
page = st.session_state.page
if page == "home":
    home_page()
elif page == "upload_json":
    upload_json_page()
elif page == "tutor":
    tutor_page()
