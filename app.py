import os
import streamlit as st
from openai import OpenAI

BASE_DIR = r"C:\Users\moeha\Desktop\Lyrico Pro"
DB_DIR = os.path.join(BASE_DIR, "artist_db")
DEFAULT_API_KEY = ""

st.set_page_config(
    page_title="Lyrico Pro - OpenRouter Studio",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "api_key" not in st.query_params:
    initial_api_key = DEFAULT_API_KEY
else:
    initial_api_key = st.query_params["api_key"]

if "lyrics_history" not in st.session_state:
    st.session_state.lyrics_history = []

st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #1a73e8, #4285f4);
        color: white;
        font-weight: 700;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        border: none;
        box-shadow: 0 4px 14px rgba(26, 115, 232, 0.4);
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1557b0, #3367d6);
        box-shadow: 0 6px 20px rgba(26, 115, 232, 0.6);
        transform: translateY(-2px);
    }
    .stTextArea textarea {
        background-color: #131b2e;
        color: white;
        border-radius: 12px;
        font-size: 15px;
        border: 1px solid rgba(66, 133, 244, 0.3);
    }
    div[data-testid="stSidebar"] {
        background-color: #070a12;
        border-right: 1px solid rgba(66, 133, 244, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("**🎛️ Lyrico Pro - OpenRouter Steuerung**")
    
    entered_key = st.text_input(
        "🔑 OpenRouter API-Key", 
        type="password", 
        value=initial_api_key,
        placeholder="sk-or-v1-..."
    )
    
    if entered_key != initial_api_key:
        st.query_params["api_key"] = entered_key
        
    active_key = entered_key if entered_key else initial_api_key
    
    artist_style = st.selectbox(
        "🎤 Künstler & Stil-Profil",
        [
            "Immortal Technique", "Big L", "Kendrick Lamar", "J. Cole", "2Pac", 
            "Eminem", "Kanye West", "Mac Miller", "Drake", "Travis Scott", 
            "Nas", "Haftbefehl", "Bushido (Classic 2000er)", "Bonez MC", 
            "Apache 207", "Luciano", "Sido", "Haze", "Lucio101"
        ]
    )
    
    genre = st.selectbox(
        "🎵 Sub-Genre / Vibe",
        ["Boom Bap / Klassik", "Modern Trap", "Drill", "Melodic Rap / Cloud", "Gangsta Rap / Hardcore", "Storytelling"]
    )
    
    song_structure = st.selectbox(
        "🧱 Song-Struktur",
        ["Standard (Intro -> Verse -> Hook -> Verse -> Hook -> Outro)", "Extended (2 Verses + Bridge + Hook)", "Agressiv (Intro -> Double Verse -> Hook)"]
    )
    
    rhyme_complexity = st.select_slider(
        "🧬 Reimdichte & Reimtechnik",
        options=["Einfach & Direkt", "Komplex & Mehrsilbig", "High-End Lyrik & Punchlines"],
        value="Komplex & Mehrsilbig"
    )
    
    length_words = st.slider(
        "📝 Textlänge (Wörter)",
        min_value=300,
        max_value=1200,
        value=600,
        step=50
    )
    
    creativity = st.slider(
        "✨ Kreativität (Temperatur)",
        min_value=0.0,
        max_value=1.0,
        value=0.75,
        step=0.05
    )

st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px; padding: 25px 30px; background: linear-gradient(135deg, rgba(19, 27, 46, 0.9), rgba(11, 15, 25, 0.95)); border-radius: 18px; border: 1px solid rgba(66, 133, 244, 0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 25px;">
        <div style="background: linear-gradient(135deg, #1a73e8, #4285f4); padding: 16px; border-radius: 14px; display: flex; align-items: center; justify-content: center; box-shadow: 0 6px 20px rgba(26, 115, 232, 0.5);">
            <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle></svg>
        </div>
        <div>
            <h1 style="margin: 0; font-size: 30px; font-weight: 900; background: linear-gradient(90deg, #4285f4, #8ab4f8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">LYRICO PRO - OPENROUTER EDITION</h1>
            <p style="margin: 4px 0 0 0; color: #9ca3af; font-size: 14px;">Hochstabil über OpenRouter angebunden</p>
        </div>
    </div>
""", unsafe_allow_html=True)

prompt_text = st.text_area(
    "💡 Dein Prompt / Thema / Konzept",
    placeholder="z.B. 'Ein harter Track über das Überleben auf der Straße, ehrliche Loyalität und den Druck des Erfolgs...'",
    height=130
)

with st.expander("🛠️ Zusätzliche Feinabstimmung (Optional)"):
    adlibs = st.text_input("Ad-libs / Soundeffekte (z.B. Skrt, Brrr, Yeah)", placeholder="z.B. (Skrt, Skrt), [Ad-lib: Eh]")
    language_style = st.selectbox("Sprachstil / Dialekt", ["Standard Deutsch", "Straßenslang / Authentisch", "Hochdeutsch & Metaphorisch", "Englisch / US-Rap"])

def get_artist_filename(artist_name):
    return artist_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("101", "101")

def load_artist_db(artist_name):
    safe_filename = get_artist_filename(artist_name)
    os.makedirs(DB_DIR, exist_ok=True)
    file_path = os.path.join(DB_DIR, f"{safe_filename}.txt")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return f"[TRAINIERTE LOKALE DATENBANK FÜR {artist_name.upper()}]:\n{content[:15000]}"
        except Exception:
            pass
    return f"[HINWEIS]: Keine lokale Trainingsdatei für {artist_name} gefunden. Nutze Standard-Stil."

def save_to_artist_db(artist_name, text_to_save):
    safe_filename = get_artist_filename(artist_name)
    os.makedirs(DB_DIR, exist_ok=True)
    file_path = os.path.join(DB_DIR, f"{safe_filename}.txt")
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n--- TRAINIERTER TAKE ({artist_name}) ---\n{text_to_save}")
        return True
    except Exception:
        return False

def generate_lyrics():
    if not active_key:
        st.error("⚠️ Bitte gib deinen OpenRouter API-Key in der Seitenleiste ein!")
        return
    elif not prompt_text.strip():
        st.warning("⚠️ Bitte gib ein Thema oder Prompt ein!")
        return
        
    with st.spinner(f"🎧 Gemini generiert über OpenRouter den kompletten Song im Stil von {artist_style}..."):
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=active_key,
            )
            db_content = load_artist_db(artist_style)
            
            system_instruction = (
                f"Du bist ein Elite-Ghostwriter für den Künstler **{artist_style}**.\n"
                f"LOKALE KÜNSTLER-DATENBANK & TRAININGS-DATEN:\n{db_content}\n\n"
                f"PARAMETRIERUNG:\n"
                f"- Sub-Genre: {genre}\n"
                f"- Song-Struktur: {song_structure}\n"
                f"- Reimtechnik: {rhyme_complexity}\n"
                f"- Sprachstil: {language_style}\n"
                f"- Ad-libs Einbindung: {adlibs if adlibs else 'Standard'}\n\n"
                "WICHTIGE REGELN:\n"
                "1. Schreibe den SONG KOMPLETT von Anfang bis Ende aus (Intro, Verses, Hooks, Bridge, Outro). Breche NIEMALS mitten im Text ab.\n"
                "2. Keine KI-Floskeln oder Moralpredigten. Nutze den rohen Vibe, Slang und Wortschatz des Künstlers.\n"
                "3. Achte auf harte Reime und authentischen Sprachgebrauch."
            )
            
            user_content = f"Schreibe einen vollständigen Track zum Konzept: '{prompt_text}'. Ziel-Länge: ca. {length_words} Wörter."

            response = client.chat.completions.create(
                model="~google/gemini-flash-latest",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_content}
                ],
                temperature=creativity,
                max_tokens=4096
            )
            
            result_text = response.choices[0].message.content
            if result_text and len(result_text.strip()) > 50:
                st.session_state.lyrics_history = [result_text]
                st.success("✅ Song vollständig über OpenRouter generiert!")
            else:
                st.error("⚠️ Die Antwort war leer oder unvollständig.")
            
        except Exception as e:
            st.error(f"❌ Fehler: {str(e)}")

if st.button("🚀 Vollständigen Song über OpenRouter generieren"):
    generate_lyrics()

if st.session_state.lyrics_history:
    st.markdown("---")
    st.markdown("**📜 Generierter Text, Training & Feedback**")
    
    st.code(st.session_state.lyrics_history[-1], language="markdown")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Thumbs Up (In lokale DB speichern & trainieren)"):
            success = save_to_artist_db(artist_style, st.session_state.lyrics_history[-1])
            if success:
                st.success(f"✅ Erfolgreich in **{DB_DIR}** gespeichert & für {artist_style} trainiert!")
            else:
                st.error("Fehler beim Speichern der Datei.")
    with col2:
        if st.button("👎 Thumbs Down (Feedback erfassen)"):
            st.warning("⚠️ Feedback registriert. Passe die Parameter oder den Prompt für den nächsten Take an.")

    st.download_button(
        label="💾 Als .txt herunterladen",
        data=st.session_state.lyrics_history[-1],
        file_name=f"Lyrico_Pro_OpenRouter_{artist_style.replace(' ', '_')}.txt",
        mime="text/plain"
    )
