import streamlit as st
import streamlit.components.v1 as components
import json
import os

# 1. Page Config must be the very first Streamlit command
st.set_page_config(page_title="Physics Simulations Hub", layout="wide")

# 2. Advanced CSS to remove margins but keep Sidebar controls
st.markdown("""
    <style>
        /* 1. Remove padding from the main block-container */
        .block-container {
            padding-top: 2rem; /* Added slight padding so title isn't cut off */
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        /* 2. Target the specific element that creates the top white-space gap */
        .stAppViewMain {
            margin-top: -3rem;
        }

        /* 3. Keep the Sidebar toggle button visible and clickable */
        .st-emotion-cache-12fmjuu, .st-emotion-cache-6q9sum {
            background-color: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            z-index: 999999;
        }

        /* 4. Ensure the iframe fills the exact screen height minus the title/guide */
        iframe {
            border: none;
            width: 100%; /* Changed to 100% to fit container */
        }
        
        [data-testid="stDecoration"] {
            display: none;
        }
                /* Add this inside your <style> tag */
        h1 {
            font-size: 2rem !important; /* Adjust 2.5rem to whatever size you prefer */
            padding-bottom: 0rem;         /* Optional: reduces gap below title */
        }
    </style>
    """, unsafe_allow_html=True)

# Load data
def load_data():
    with open('simulations.json', 'r') as f:
        return json.load(f)

ANIMATIONS = load_data()

# --- SIDEBAR SEARCH & NAV ---
st.sidebar.title("Find Simulation")

# Create a flat list of all simulation names for the search/filter
all_sim_names = []
for topic in ANIMATIONS:
    all_sim_names.extend(ANIMATIONS[topic].keys())

# Add a text search box
search_query = st.sidebar.text_input("🔍 Search by name:", "").lower()

# Filter names based on search
filtered_names = [name for name in all_sim_names if search_query in name.lower()]

if search_query:
    selected_script = st.sidebar.radio("Search Results:", options=filtered_names)
    # Find which topic this belongs to for the display
    if selected_script:
        selected_topic = next(t for t in ANIMATIONS if selected_script in ANIMATIONS[t])
    else:
        selected_topic = list(ANIMATIONS.keys())[0] # Fallback
        selected_script = list(ANIMATIONS[selected_topic].keys())[0]
else:
    selected_topic = st.sidebar.selectbox("Choose a Topic:", options=list(ANIMATIONS.keys()))
    available_animations = list(ANIMATIONS[selected_topic].keys())
    selected_script = st.sidebar.radio("Select Animation:", options=available_animations)

# --- MAIN PANEL ---
st.write("") # Dummy spacer
st.write("") # Dummy spacer
current_data = ANIMATIONS[selected_topic][selected_script]
st.caption(f"Category: {selected_topic}")
st.title(selected_script)

st.markdown("### Guide")
st.info(current_data.get("description", "No description available."))

# --- NEW SECTION: IMAGE DISPLAY ---
# Use .get() to safely access 'image' even if the key is missing in some JSON entries
image_path = current_data.get("image", "")

if image_path:
    # Check if it is a local file or a URL (simple check)
    if os.path.exists(image_path) or image_path.startswith("http"):
        # You can adjust width as needed (e.g., width=500)
        st.image(image_path, caption=f"Diagram for {selected_script}")
    else:
        st.warning(f"Image file not found: {image_path}")
# ----------------------------------

# Render the simulation
components.iframe(current_data["url"], height=600, scrolling=False)

# --- NEW SECTION: QUESTIONS DISPLAY ---
questions = current_data.get("questions", [])

if questions:
    st.markdown("### 📝 Discussion Questions")
    for i, question in enumerate(questions, 1):
        st.markdown(f"**{i}.** {question}")
# --------------------------------------

# Tip at the bottom
st.markdown("---")
st.caption("Tip: Use the search box in the sidebar to find animations across all topics.")

