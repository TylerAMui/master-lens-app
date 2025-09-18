# Master Lens Web App - v2.1 (With Sub-Lenses)
import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="The Master Lens",
    page_icon="🎭",
    layout="wide"
)

st.title("🎭 The Master Lens")
st.write("An AI-powered analytical partner for creative works.")

# --- PROMPT DEFINITIONS ---
# We now have a more complex structure with sub-lenses.
LENSES = {
    "Structural & Formalist": {
        "description": "A formalist analysis focusing purely on craft, composition, color, line, meter, rhyme, and technique.",
        "prompt": """
Analyze the following creative work from a strictly formalist perspective. Disregard external context. Your analysis should focus entirely on the internal structure and aesthetic components of the piece.

- For visual art: Analyze the composition, use of color, line, shape, texture, and medium.
- For writing: Analyze the structure, meter, rhyme scheme, word choice, and use of literary devices.

Explain how these formal elements work together to create the piece's overall effect.
The work is as follows:
"""
    },
    "Psychological": {
        "description": "An inquiry into the work's emotional and archetypal currents.",
        "sub_lenses": {
            "Select a School...": "",
            "Jungian": """
Analyze the following creative work using a Jungian psychological lens.
- Explore the role of archetypes (e.g., the Shadow, Persona, Anima/Animus), the process of individuation, and any connection to the collective unconscious.
- Interpret the work as a "stained glass" self-portrait of the creator's psyche.
The work is as follows:
""",
            "Freudian": """
Analyze the following creative work using a Freudian psychoanalytic lens.
- Explore themes of repressed desires, the unconscious mind, and the interplay of the Id, Ego, and Superego.
- Discuss any potential dream symbolism, wish-fulfillment, or Oedipal dynamics present in the work.
The work is as follows:
"""
        }
    },
    "Philosophical": {
        "description": "An exploration of the work's deeper, universal themes and ideas.",
        "sub_lenses": {
            "Select a School...": "",
            "Existentialist": """
Analyze the following creative work through an Existentialist lens.
- Discuss themes of freedom, responsibility, authenticity, and the search for meaning in a meaningless world.
- Explore how the characters or narrator confront the absurdity of their existence and create their own values.
The work is as follows:
""",
            "Taoist": """
Analyze the following creative work through a Taoist lens.
- Explore the concepts of Yin and Yang, the harmony of opposites, and the idea of 'wu wei' (effortless action).
- Discuss how the work reflects the natural flow of the Tao and the virtue of accepting the nature of reality.
The work is as follows:
"""
        }
    },
    "Socio-Political": {
        "description": "A critical analysis of the work's relationship to society, history, and power.",
        "prompt": """
Analyze the following creative work as a product of its social and historical context.
- How does the work reflect or critique societal norms, power structures, or political events?
- Explore themes of class, gender, race, or ideology present in the work.
The work is as follows:
"""
    },
    "Comparative": {
        "description": "Places the work in conversation with other similar artists and movements.",
        "prompt": """
Analyze the following creative work using a comparative lens.
- Identify the key themes, styles, and aesthetic choices in the piece.
- Compare and contrast this work with other similar artists, movements, or genres.
- Discuss where this work fits within its broader artistic or literary tradition.
The work is as follows:
"""
    }
}


# --- SIDEBAR FOR SETUP ---
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter your Gemini API Key", type="password")

    st.header("Analytical Protocol")
    # Step 1: User selects a main lens
    main_lens_name = st.selectbox(
        "Step 1: Choose your analytical lens:",
        options=list(LENSES.keys()),
        index=0  # Default to no selection
    )
    
    # Store the selection in the session state
    st.session_state.main_lens_name = main_lens_name
    
    # Step 2: If the selected lens has sub-lenses, show them
    if main_lens_name and "sub_lenses" in LENSES[main_lens_name]:
        sub_lens_name = st.selectbox(
            "Step 2: Choose a school of thought:",
            options=list(LENSES[main_lens_name]["sub_lenses"].keys())
        )
        st.session_state.sub_lens_name = sub_lens_name

# --- MAIN PAGE ---
if st.session_state.get('main_lens_name') and st.session_state.main_lens_name != "Select a Lens...":
    
    # Check if a sub-lens is needed and if it has been selected
    if "sub_lenses" in LENSES[st.session_state.main_lens_name]:
        if st.session_state.get('sub_lens_name') and st.session_state.sub_lens_name != "Select a School...":
            display_analysis_form = True
            st.header(f"Lens: {st.session_state.main_lens_name} ({st.session_state.sub_lens_name})")
        else:
            display_analysis_form = False
            st.info("⬅️ Please select a school of thought from the sidebar to continue.")
    else:
        display_analysis_form = True
        st.header(f"Lens: {st.session_state.main_lens_name}")

    if display_analysis_form:
        work_title = st.text_input("Enter the title of the work:")
        work_text = st.text_area("Paste your text or describe your artwork here:", height=250)

        if st.button("Analyze"):
            if not api_key:
                st.warning("Please enter your Gemini API Key in the sidebar to begin.")
            elif not work_text:
                st.warning("Please provide the creative work to be analyzed.")
            else:
                with st.spinner("Janus is thinking..."):
                    try:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
                        
                        # Determine which prompt to use
                        if "sub_lenses" in LENSES[st.session_state.main_lens_name]:
                            base_prompt = LENSES[st.session_state.main_lens_name]["sub_lenses"][st.session_state.sub_lens_name]
                        else:
                            base_prompt = LENSES[st.session_state.main_lens_name]["prompt"]

                        final_prompt = f"{base_prompt}\nTitle: {work_title}\n\n{work_text}"
                        
                        response = model.generate_content(final_prompt)
                        
                        st.header("Analysis")
                        st.markdown(response.text)

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
else:
    st.info("⬅️ Please select an analytical lens from the sidebar to begin.")
