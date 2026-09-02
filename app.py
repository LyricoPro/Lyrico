import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Lyrico Pro - Database Connected Ghostwriter",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        border-radius: 10px;
        padding: 0.75rem 1rem;
        border: none;
        box-shadow: 0 4px 14px rgba(255, 75, 75, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff3333, #ff7300);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.6);
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎤 **LYRICO PRO**")
    st.markdown("Database-Connected Ghostwriting Engine")
    st.markdown("---")
    
    api_key_input = st.text_input(
        "🔑 Groq API-Key", 
        type="password", 
        value="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"
    )
    
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
    
    st.markdown("---")
    st.markdown("🚀 **Engine:** `openai/gpt-oss-120b`")

st.title("🎤 Lyrico Pro — Database Connected Ghostwriter")
st.markdown("Schreibt Texte unter direkter Einbindung deiner lokalen Künstler-Datenbanken und harten Reim-Mustern.")

prompt_text = st.text_area(
    "💡 Thema / Kerngedanke / Story-Konzept",
    placeholder="z.B. 'Der schmale Grat zwischen Erfolg und Paranoia, falsche Freunde im Dunstkreis...'",
    height=130
)

# Funktion zum Laden der echten lokalen Künstler-Datenbank aus einem Ordner namens "artist_db"
def load_local_artist_database(artist_name):
    safe_filename = artist_name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("101", "101")
    file_path = os.path.join("artist_db", f"{safe_filename}.txt")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                return f"[GEFUNDENE LOKALE DATENBANK FÜR {artist_name.upper()}]:\n{content[:5000]}"
        except Exception as e:
            return f"Fehler beim Lesen der Datenbankdatei: {str(e)}"
    return f"[HINWEIS]: Keine lokale Textdatei unter '{file_path}' gefunden. Nutze internes Fallback-Profil."

# Fallback-Profile (inkl. Lucio101)
FALLBACK_PROFILES = {
    "Big L": "Harlem 90s East Coast Battle Rap. Komplexe Multisilbenreime, dunkler Humor, Harlem-Slang.",
    "Kendrick Lamar": "Compton Lyrical Visionary. Innere Zerrissenheit, non-lineare Jazz-Rhythmik, survivor's guilt.",
    "Haftbefehl": "Offenbach Real Street Rap. Harte Konsonanten, offenbacher Straßenslang, Paranoia, Luxus, Kriminalität.",
    "Bushido (Classic 2000er)": "Legendäre Berliner Gangsta-Rap-Ära. Eiskalte Berliner Straße, minimalistische Härte.",
    "Sido": "Berliner Schule. Rotzig, selbstironisch, zynischer Humor, genial erzählte Geschichten.",
    "Lucio101": "Berlin-Moabit Trap. Melodisch, cooler Vibe, Designer-Klamotten, Nachtleben, unaufgeregter aber treibender Flow."
}

if st.button("🚀 Trainierte Master-Lyrics aus DB generieren"):
    if not api_key_input:
        st.error("⚠️ Bitte gib deinen API-Key ein!")
    elif not prompt_text.strip():
        st.warning("⚠️ Bitte gib ein Thema oder Konzept ein!")
    else:
        with st.spinner("🎧 Lyrico scannt deine Künstler-Datenbank und schmiedet authentische Bars..."):
            try:
                client = Groq(api_key=api_key_input)
                
                db_content = load_local_artist_database(artist_style)
                fallback_info = FALLBACK_PROFILES.get(artist_style, "Professioneller Rap-Interpret mit markantem Flow.")
                
                system_instruction = (
                    f"Du bist ein professioneller Ghostwriter, spezialisiert auf den Stil von: **{artist_style}**.\n"
                    f"HIER IST DIE ECHTE LOKALE DATENBANK / TEXTBASIS DES KÜNSTLERS:\n{db_content}\n\n"
                    f"FALLBACK-PROFIL / STIL: {fallback_info}\n\n"
                    f"SPRACHE: Der Song muss zu 100% auf **{language}** geschrieben sein.\n"
                    f"GENRE / VIBE: '{genre}'.\n\n"
                    "ABSOLUTE REGELN:\n"
                    "1. ANALYSIERE die obige Datenbank nach Vokabular, Satzbau und Reimtechnik des Künstlers und kopiere diesen Stil exakt.\n"
                    "2. KEINE KI-Floskeln, kein Kitsch. Verwende echte Straßen- oder Tiefgang-Metaphern passend zum Künstler.\n"
                    "3. STRUKTUR: Zwingend sauber unterteilen in [Intro], [Part 1], [Hook / Refrain], [Part 2], [Bridge], [Outro].\n"
                )
                
                max_tokens = int(length_words * 1.4)
                if max_tokens > 8000:
                    max_tokens = 8000
                
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",  # Aktives, funktionierendes Modell auf Groq
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": f"Schreibe basierend auf der Künstler-Datenbank und dem Stil einen rohen, kompromisslos authentischen Rap-Text zu diesem Konzept: '{prompt_text}'. Ziel-Länge: ca. {length_words} Wörter."}
                    ],
                    max_tokens=max_tokens,
                    temperature=creativity
                )
                
                lyrics_result = response.choices[0].message.content
                
                st.success("✅ Master-Lyrics erfolgreich aus Datenbank generiert!")
                st.markdown("### 📜 Deine Lyrics (Klicke oben rechts im Kasten zum Kopieren):")
                
                st.code(lyrics_result, language="markdown")
                
                st.download_button(
                    label="💾 Als Textdatei (.txt) herunterladen",
                    data=lyrics_result,
                    file_name=f"Lyrico_DB_{artist_style.replace(' ', '_')}_{language}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Ein Fehler ist aufgetreten: {str(e)}")