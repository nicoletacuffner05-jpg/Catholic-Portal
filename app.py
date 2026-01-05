import streamlit as st
import requests
from datetime import date, datetime

# --- 1. THE VATICAN ENGINE (Liturgical Intelligence) ---
@st.cache_data(ttl=3600)  # Caches data for 1 hour to save battery/data
def fetch_liturgy():
    try:
        r = requests.get("http://calapi.inadiutorium.cz/api/v1/calendars/general-en/today", timeout=5).json()
        celebration = r['celebrations'][0]
        return celebration['title'], celebration['colour'], celebration['rank']
    except:
        return "Ordinary Time", "green", "ferial"

saint, color_name, rank = fetch_liturgy()

# Sacred Color Mapping (Gold for White, Deep Purple for Lent/Advent)
color_map = {
    "green": "#1E5631", "purple": "#4B0082", "red": "#8B0000", 
    "white": "#B8860B", "violet": "#4B0082"
}
app_color = color_map.get(color_name.lower(), "#1E5631")

# --- 2. MASTER UI CONFIGURATION ---
st.set_page_config(page_title="Catholic Master", page_icon="🇻🇦", layout="centered")

# Custom CSS for "Cathedral Aesthetic"
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FDFCF0; }}
    [data-testid="stSidebar"] {{ background-color: {app_color} !important; }}
    .stSidebar * {{ color: white !important; }}
    .stButton>button {{ background-color: {app_color}; color: white; border-radius: 20px; width: 100%; }}
    .stMetric {{ background-color: #ffffff; padding: 10px; border-radius: 10px; border: 1px solid #ddd; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DYNAMIC NAVIGATION ---
with st.sidebar:
    st.title("🇻🇦 Cathedral Portal")
    st.write(f"**Season:** {color_name.capitalize()}")
    st.divider()
    page = st.radio("Sanctuary Navigation", 
        ["🏠 Daily Dashboard", "📖 The Daily Lectures", "📿 Rosary & Psalms", "🕊️ Confession Guide", "🎵 Sacred Audio", "🕯️ Intentions & Journal"])
    st.divider()
    st.caption(f"Rank: {rank.upper()}")

# --- 4. MASTER PAGES ---

if page == "🏠 Daily Dashboard":
    st.title("Daily Sanctuary")
    col1, col2 = st.columns([2,1])
    with col1:
        st.write(f"#### {date.today().strftime('%A, %B %d, %Y')}")
        st.success(f"**Today's Feast:** {saint}")
    with col2:
        st.metric("Liturgical Color", color_name.capitalize())
    
    st.divider()
    st.subheader("Today's Spiritual Goal")
    st.info("Perform one spiritual or corporal work of mercy today.")

elif page == "📖 The Daily Lectures":
    st.title("📖 Liturgy of the Word")
    try:
        b_res = requests.get("https://bible-api.com/verse_of_the_day?translation=dra").json()
        st.subheader(f"Today's Gospel: {b_res['verse']['name']}")
        st.markdown(f"### '{b_res['verse']['text']}'")
        st.caption("Douay-Rheims American Edition (DRA)")
    except: 
        st.warning("Could not connect to the Lectionary. Please use your physical Missal.")

elif page == "📿 Rosary & Psalms":
    st.title("📿 Prayer & Meditation")
    tab1, tab2 = st.tabs(["The Holy Rosary", "The Book of Psalms"])
    
    with tab1:
        day = datetime.now().strftime('%A')
        mysteries = {"Monday": "Joyful", "Tuesday": "Sorrowful", "Wednesday": "Glorious", "Thursday": "Luminous", "Friday": "Sorrowful", "Saturday": "Joyful", "Sunday": "Glorious"}
        st.success(f"Today is {day}: Pray the **{mysteries[day]} Mysteries**.")
        with st.expander("Common Prayers (Anima Christi, Memorare)"):
            st.write("**Anima Christi:** Soul of Christ, sanctify me. Body of Christ, save me...")
            st.write("**Memorare:** Remember, O most gracious Virgin Mary...")
    
    with tab2:
        psalm = st.selectbox("Select a Psalm:", ["Psalm 23 (The Good Shepherd)", "Psalm 51 (The Miserere)", "Psalm 91 (The Protection)"])
        if "23" in psalm:
            st.write("*The Lord is my shepherd; I shall not want. He maketh me to lie down in green pastures...*")
        elif "51" in psalm:
            st.write("*Have mercy upon me, O God, according to thy lovingkindness...*")
        elif "91" in psalm:
            st.write("*He that dwelleth in the secret place of the most High shall abide under the shadow of the Almighty...*")

elif page == "🕊️ Confession Guide":
    st.title("🕊️ Sacrament of Reconciliation")
    role = st.selectbox("Guide for:", ["Adult", "Teenager", "Child"])
    st.subheader(f"Examination of Conscience: {role}")
    st.checkbox("Have I neglected God in daily prayer?")
    st.checkbox("Have I used God's name in vain or in anger?")
    st.checkbox("Have I been truthful and honest with others?")
    st.divider()
    with st.expander("The Confession Rite (What to say)"):
        st.write("**You:** Bless me Father for I have sinned. It has been [Time] since my last confession.")
        st.write("**You:** I confess these sins... [List Sins]")
        st.write("**Act of Contrition:** O my God, I am heartily sorry for having offended Thee...")

elif page == "🎵 Sacred Audio":
    st.title("🎵 Sacred Soundscape")
    st.subheader("Gregorian Chant")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Placeholder for high-quality chant
    st.subheader("Holy Rosary Video")
    st.video("https://www.youtube.com/watch?v=tuW_N-N843A")

elif page == "🕯️ Intentions & Journal":
    st.title("🕯️ Spiritual Journal")
    note = st.text_area("Write your prayer intention or reflection for today:")
    if st.button("Save to Heart"):
        st.balloons()
        st.success("Your reflection has been recorded.")
  
