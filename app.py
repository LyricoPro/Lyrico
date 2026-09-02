import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Lyrico Pro",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "api_key" not in st.query_params:
    initial_api_key = ""
else:
    initial_api_key = st.query_params["api_key"]

if "lyrics_result" not in st.session_state:
    st.session_state.lyrics_result = None

st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff4b4b, #ff8c00);
        color: white;
        font-weight: 700;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        border: none;
        box-shadow: 0 4px 14px rgba(255, 75, 75, 0.4);
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff3333, #ff7300);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.6);
        transform: translateY(-1px);
    }
    .stTextArea textarea {
        background-color: #131b2e;
        color: white;
        border-radius: 10px;
        font-size: 15px;
    }
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎤 **LYRICO PRO**")
    st.markdown("Mobile Ghostwriting Engine")
    st.markdown("---")
    
    entered_key = st.text_input(
        "🔑 Groq API-Key (Wird im Browser gespeichert)", 
        type="password", 
        value=initial_api_key,
        placeholder="gsk_..."
    )
    
    if entered_key != initial_api_key:
        st.query_params["api_key"] = entered_key
        
    active_key = entered_key if entered_key else initial_api_key
    
    st.markdown("### 🎛️ Master Control")
    
    language = st.selectbox(
        "🌐 Sprache",
        ["Deutsch", "Englisch"]
    )
    
    artist_style = st.selectbox(
        "🎤 Interpret & Signatur-Flow",
        [
            "Big L", "Kendrick Lamar", "J. Cole", "2Pac", "Eminem", 
            "Kanye West", "Mac Miller", "Drake", "Travis Scott", "Nas",
            "Haftbefehl", "Bushido (Classic 2000er)", "Bonez MC", "Apache 207", 
            "Luciano", "Sido", "Haze", "Genetikk", "Nate 57", "Lucio101"
        ]
    )
    
    genre = st.selectbox(
        "🎵 Beat-Vibe & Genre",
        [
            "Boom Bap (90s / True School)", "Modern Trap", "Dark Drill", 
            "Conscious Storytelling", "Melancholic / Lo-Fi", "Westcoast Gangsta Rap", 
            "Cloud Rap", "Afro Trap / Melodic", "Aggressive Street Rap (Harte Beats)"
        ]
    )
    
    length_words = st.slider(
        "📝 Textlänge (Wörter)",
        min_value=250,
        max_value=2500,
        value=850,
        step=50
    )
    
    creativity = st.slider(
        "✨ Kreativität (Temperatur)",
        min_value=0.5,
        max_value=1.0,
        value=0.8,
        step=0.05
    )

st.title("🎤 Lyrico Pro")
st.markdown("Mobile-optimierter Database Ghostwriter")

prompt_text = st.text_area(
    "💡 Thema / Kerngedanke / Story-Konzept",
    placeholder="z.B. 'Der schmale Grat zwischen Erfolg und Paranoia, falsche Freunde...'",
    height=120
)

def load_local_artist_database(artist_name):
    safe_filename = artist_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("101", "101")
    file_path = os.path.join("artist_db", f"{safe_filename}.txt")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return f"[GEFUNDENE LOKALE DATENBANK FÜR {artist_name.upper()}]:\n{content[:6000]}"
        except Exception as e:
            return f"Fehler beim Lesen der Datenbankdatei: {str(e)}"
    return f"[HINWEIS]: Keine lokale Textdatei unter '{file_path}' gefunden. Nutze internes Fallback-Profil."

FALLBACK_PROFILES = {
    "Big L": "Harlem 90s East Coast Battle Rap. Komplexe Multisilbenreime, dunkler Humor, Harlem-Slang.",
    "Kendrick Lamar": "Compton Lyrical Visionary. Innere Zerrissenheit, non-lineare Jazz-Rhythmik, survivor's guilt.",
    "Haftbefehl": "Offenbach Real Street Rap. Harte Konsonanten, offenbacher Straßenslang, Paranoia, Luxus, Kriminalität.",
    "Bushido (Classic 2000er)": "Legendäre Berliner Gangsta-Rap-Ära. Eiskalte Berliner Straße, minimalistische Härte.",
    "Sido": "Berliner Schule. Rotzig, selbstironisch, zynischer Humor, genial erzählte Geschichten.",
    "Lucio101": "Berlin-Moabit Trap. Melodisch, cooler Vibe, Designer-Klamotten, Nachtleben, unaufgeregter aber treibender Flow."
}

def generate_lyrics(is_reimagine=False):
    if not active_key:
        st.error("⚠️ Bitte gib deinen API-Key in der Seitenleiste ein!")
        return
    elif not prompt_text.strip():
        st.warning("⚠️ Bitte gib ein Thema oder Konzept ein!")
        return
        
    with st.spinner("🎧 Lyrico scannt deine Künstler-Datenbank und baut authentische Bars..."):
        try:
            client = Groq(api_key=active_key)
            db_content = load_local_artist_database(artist_style)
            fallback_info = FALLBACK_PROFILES.get(artist_style, "Professioneller Rap-Interpret mit markantem Flow.")
            
            system_instruction = (
                f"Du bist ein professioneller Ghostwriter, spezialisiert auf den authentischen Stil von: **{artist_style}**.\n"
                f"HIER IST DIE ECHTE LOKALE TEXTBASIS / DATENBANK DES KÜNSTLERS (Nutze diesen Slang, Vokabular und Stil als strikte Hauptquelle):\n{db_content}\n\n"
                f"FALLBACK-PROFIL / STIL: {fallback_info}\n\n"
                f"SPRACHE: Der Song muss zu 100% auf **{language}** geschrieben sein.\n"
                f"GENRE / VIBE: '{genre}'.\n\n"
                "ABSOLUTE REGELN & STRIKTE VERBOTE:\n"
                "1. DATENBANK-TREUE: Orientiere dich primär an den echten Wörtern, Redewendungen und der Wortwahl aus der obigen Künstler-Datenbank. Erfinde keinen künstlichen, fremden Stil.\n"
                "2. ABSOLUTES WORTVERBOT: Verwende NIEMALS generische KI-Klischees oder Modewörter wie 'Neon', 'Neonlicht', 'Matrix', 'Schatten der Nacht', 'Labyrinth' oder geschmacklosen Kitsch. Wenn es nicht zu 100% authentisch nach dem echten Künstler klingt, ist es verboten.\n"
                "3. STRUKTUR: Zwingend sauber unterteilen in [Intro], [Part 1], [Hook / Refrain], [Part 2], [Bridge], [Outro].\n"
            )
            
            if is_reimagine and st.session_state.get("lyrics_result"):
                user_content = (
                    f"Hier ist der vorherige Song als Referenz:\n\n{st.session_state.lyrics_result}\n\n"
                    f"AUFGABE (REIMAGINE): Erstelle einen komplett neuen, eigenständigen Take zu demselben Konzept ('{prompt_text}'). "
                    f"Schreibe völlig neue Bars, verändere die Reime und den Aufbau innerhalb der Zeilen, aber behalte exakt dieselbe Song-Struktur bei ([Intro], [Part 1], [Hook / Refrain], [Part 2], [Bridge], [Outro])."
                )
            else:
                user_content = f"Schreibe basierend auf der lokalen Datenbank einen absolut rohen, ungeskripteten und authentischen Rap-Text zu diesem Konzept: '{prompt_text}'. Ziel-Länge: ca. {length_words} Wörter."

            max_tokens = int(length_words * 1.4)
            if max_tokens > 8000:
                max_tokens = 8000
            
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_content}
                ],
                max_tokens=max_tokens,
                temperature=creativity
            )
            
            st.session_state.lyrics_result = response.choices[0].message.content
            st.success("✅ Master-Lyrics erfolgreich generiert!")
            
        except Exception as e:
            st.error(f"❌ Ein Fehler ist aufgetreten: {str(e)}")

if st.button("🚀 Master-Lyrics aus DB generieren"):
    generate_lyrics(is_reimagine=False)

if st.session_state.lyrics_result:
    st.markdown("### 📜 Deine Lyrics:")
    st.code(st.session_state.lyrics_result, language="markdown")
    
    if st.button("✨ Reimagine (Komplett neuer Take, selbe Struktur)"):
        generate_lyrics(is_reimagine=True)
        st.rerun()
        
    st.download_button(
        label="💾 Als Textdatei speichern",
        data=st.session_state.lyrics_result,
        file_name=f"Lyrico_DB_{artist_style.replace(' ', '_')}_{language}.txt",
        mime="text/plain"
    )
