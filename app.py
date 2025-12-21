import streamlit as st
import streamlit.components.v1 as components
import json
# Custom CSS to remove padding and margins
st.markdown("""
    <style>
        /* Remove padding from the main container */
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }

        /* Optional: Hide the header bar at the top */
        header {visibility: hidden;}

        /* Optional: Hide the footer "Made with Streamlit" */
        footer {visibility: hidden;}
        
        /* Ensure the iframe fills the container width */
        iframe {
            width: 100%;
            border: none;
        }
    </style>
    """, unsafe_allow_html=True)

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
st.write("Tip: Use the search box in the sidebar to find animations across all topics.")
st.caption(f"Category: {selected_topic}")
st.title(selected_script)

st.markdown("### Guide")
st.info(current_data["description"])
#st.markdown("---")

components.iframe(current_data["url"], height=600, scrolling=False)

