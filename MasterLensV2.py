# Master Lens Web App - v2.0 (Multi-Prompt)
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
# A dictionary holding our different analytical lenses.
PROMPTS = {
    "Select a Lens...": "",
    "Structural & Formalist Lens": """
Analyze the following creative work from a strictly formalist perspective. Disregard external context such as the author's biography or historical events. Your analysis should focus entirely on the internal structure and aesthetic components of the piece.

- For visual art: Analyze the composition, use of color, line, shape, texture, and medium.
- For writing: Analyze the structure, meter, rhyme scheme, word choice, sentence structure, and use of literary devices.

Explain how these formal elements work together to create the piece's overall effect.
The work is as follows:
""",
    "Psychological & Archetypal Lens": """
Analyze the following creative work using a lens of depth psychology. Your goal is to uncover the underlying emotional and archetypal currents.

- Identify any Jungian archetypes present (e.g., the Shadow, the Persona, Anima/Animus).
- Explore the emotional journey of the characters or the implied narrator.
- Discuss the psychological state that the work seems to express or evoke in the viewer/reader.
- Interpret the work as a "stained glass" self-portrait. What facet of the human condition is being examined?

The work is as follows:
""",
    "Philosophical & Mythological Lens": """
Analyze the following creative work for its deeper philosophical themes and mythological resonances.

- Identify the core philosophical questions the work is asking (e.g., about existence, meaning, morality, reality).
- If the work presents a duality, analyze how it is treated (e.g., as a conflict, a harmony, or something to be transcended).
- Connect the work's narrative or imagery to any relevant universal myths, fables, or spiritual concepts.

The work is as follows:
""",
    "Socio-Political Lens": """
Analyze the following creative work as a product of its social and historical context.

- How does the work reflect or critique the societal norms, power structures, or political events of its time?
- Explore themes of class, gender, race, or ideology present in the work.
- Discuss the political or social statement the work appears to be making.

The work is as follows:
"""
}


# --- SIDEBAR FOR SETUP ---
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    
    st.header("Analytical Protocol")
    # Step 1: User selects a lens
    selected_lens = st.selectbox(
        "Choose your analytical lens:",
        options=list(PROMPTS.keys())
    )
    
    # We store the selected lens in the session state to remember it.
    st.session_state.selected_lens = selected_lens


# --- MAIN PAGE ---
if st.session_state.selected_lens != "Select a Lens...":
    st.header(f"Using: {st.session_state.selected_lens}")
    
    poem_title = st.text_input("Enter the title of the work:")
    poem_text = st.text_area("Paste your text or describe your artwork here:", height=250)

    if st.button("Analyze"):
        if not api_key:
            st.warning("Please enter your Gemini API Key in the sidebar to begin.")
        elif not poem_text:
            st.warning("Please provide the creative work to be analyzed.")
        else:
            with st.spinner("Janus is thinking..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
                    
                    # Get the base prompt from our dictionary
                    base_prompt = PROMPTS[st.session_state.selected_lens]
                    
                    # Combine the prompt, title, and the work
                    final_prompt = f"{base_prompt}\nTitle: {poem_title}\n\n{poem_text}"
                    
                    response = model.generate_content(final_prompt)
                    
                    st.header("Analysis")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
else:
    st.info("⬅️ Please select an analytical lens from the sidebar to begin.")
