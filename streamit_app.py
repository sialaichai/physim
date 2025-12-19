import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="Physics Simulations Hub", layout="wide")

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
    # If searching, show the filtered results in a radio list
    selected_script = st.sidebar.radio("Search Results:", options=filtered_names)
    
    # Find which topic this belongs to for the display
    selected_topic = next(t for t in ANIMATIONS if selected_script in ANIMATIONS[t])
else:
    # Standard Navigation if not searching
    selected_topic = st.sidebar.selectbox("Choose a Topic:", options=list(ANIMATIONS.keys()))
    available_animations = list(ANIMATIONS[selected_topic].keys())
    selected_script = st.sidebar.radio("Select Animation:", options=available_animations)

# --- MAIN PANEL ---
current_data = ANIMATIONS[selected_topic][selected_script]

st.title(selected_script)
st.caption(f"Category: {selected_topic}")

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("### Guide")
    st.info(current_data["description"])
    st.markdown("---")
    st.write("Tip: Use the search box in the sidebar to find animations across all topics.")

with col2:
    components.iframe(current_data["url"], height=600, scrolling=False)
