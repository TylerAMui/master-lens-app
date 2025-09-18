# Master Lens Web App - v3.0 (The Dialectical Dialogue Upgrade)
import streamlit as st
import google.generativeai as genai
import textwrap

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="The Master Lens v3.0",
    page_icon="🎭",
    layout="wide"
)

st.title("🎭 The Master Lens v3.0")
st.write("An AI-powered analytical partner for creative works, now featuring Dialectical Dialogue.")

# --- PROMPT DEFINITIONS (LENSES v3) ---
# Directive 1: Expand the Analytical Lenses

# The hierarchical structure defines the organization and prompts.
LENSES_HIERARCHY = {
    "Structural & Formalist": {
        "description": "A formalist analysis focusing purely on craft, composition, technique, and structure.",
        "prompt": """
Analyze the following creative work from a strictly formalist perspective. Disregard external context, biography, or social implications. Your analysis should focus entirely on the internal structure and aesthetic components.

- Analyze elements such as composition, color, line, medium, structure, meter, rhyme scheme, word choice, and literary devices.
- Explain how these formal elements work together to create the piece's overall aesthetic effect.
The work is as follows:
"""
    },
    "Psychological": {
        "description": "An inquiry into the work's emotional, symbolic, and archetypal currents.",
        "sub_lenses": {
            "Jungian": """
Analyze the following creative work using a Jungian psychological lens.
- Explore the role of archetypes (e.g., the Shadow, Persona, Anima/Animus), the process of individuation, and connections to the collective unconscious.
- Interpret the work's symbols and imagery as manifestations of the psyche.
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
            "Existentialist": """
Analyze the following creative work through an Existentialist lens.
- Discuss themes of freedom, responsibility, authenticity, and the search for meaning in a meaningless world (the Absurd).
- Explore how the characters or narrator confront anxiety, dread, and the burden of choice.
The work is as follows:
""",
            "Taoist": """
Analyze the following creative work through a Taoist lens.
- Explore the concepts of Yin and Yang, the harmony of opposites, and the idea of 'wu wei' (effortless action).
- Discuss how the work reflects the natural flow of the Tao, simplicity, and the virtue of accepting reality.
The work is as follows:
"""
        }
    },
    "Socio-Political": {
        "description": "A critical analysis of the work's relationship to society, power, and ideology.",
        "sub_lenses": {
            "Marxist": """
Analyze the following creative work through a Marxist critical lens.
- Focus on the representation of class struggle, economic structures, and the means of production.
- Discuss how the work either reinforces or subverts the dominant ideology (hegemony).
- Explore themes of alienation and commodification.
The work is as follows:
""",
            "Feminist": """
Analyze the following creative work using a Feminist critical lens.
- Examine the representation of gender roles, power dynamics between sexes, and the presence of patriarchal structures.
- Discuss how the work challenges or reinforces societal expectations regarding gender and explores the intersectionality of identity.
The work is as follows:
""",
            "Post-Colonial": """
Analyze the following creative work using Post-Colonial theory.
- Examine the representation of the colonizer and the colonized, and the lasting impact of imperialism on cultural identity.
- Discuss themes of hybridity, resistance, agency, and the representation of the "Other".
The work is as follows:
""",
            "Queer Theory": """
Analyze the following creative work through the lens of Queer Theory.
- Examine how the work constructs, deconstructs, or challenges norms of gender and sexuality.
- Challenge heteronormative assumptions and explore marginalized identities and desires.
- Discuss the performance of identity and the subversion of stable categories.
The work is as follows:
"""
        }
    },
    "Historical & Biographical": {
        "description": "Examines the work in the context of the artist's life and the historical period.",
        "prompt": """
Analyze the following creative work through a Historical and Biographical lens.
- How does the artist's personal life, experiences, and known beliefs influence the creation and content of the work?
- Place the work within the specific historical, cultural, and political context of its time.
- Discuss how understanding the biography and the historical milieu enriches the interpretation.
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

# --- HELPER FUNCTIONS & DATA STRUCTURES ---

def flatten_lenses(lenses):
    """Flattens the hierarchical LENSES dictionary into a single dictionary for easy lookup."""
    flat_lenses = {}
    for main_lens, details in lenses.items():
        if "sub_lenses" in details:
            for sub_lens, prompt in details["sub_lenses"].items():
                # Create a unique name: "Main Lens (Sub Lens)"
                lens_name = f"{main_lens} ({sub_lens})"
                flat_lenses[lens_name] = textwrap.dedent(prompt).strip()
        elif "prompt" in details:
            flat_lenses[main_lens] = textwrap.dedent(details["prompt"]).strip()
    return flat_lenses

# A flattened dictionary used for prompt lookup and the Dialectical Dialogue selection UI.
FLATTENED_LENSES = flatten_lenses(LENSES_HIERARCHY)
SORTED_LENS_NAMES = sorted(list(FLATTENED_LENSES.keys()))

def create_persona_name(lens_name):
    """Creates a suitable persona title from a lens name (Directive 2)."""
    # Extract the core term (the most specific part of the lens name)
    if "(" in lens_name:
        # e.g., "Psychological (Jungian)" -> "Jungian"
        name = lens_name.split("(")[1].replace(")", "")
    else:
        # e.g., "Comparative"
        name = lens_name

    # Specific formatting tweaks for natural sounding titles
    if name == "Structural & Formalist":
        return "The Formalist"
    if name == "Historical & Biographical":
        return "The Historian"
    if name == "Comparative":
        return "The Comparativist"
    if name in ["Jungian", "Freudian"]:
         return f"The {name} Analyst"
    if name in ["Marxist", "Feminist"]:
        return f"The {name} Critic"
    if name in ["Existentialist", "Taoist"]:
        return f"The {name} Philosopher"
    elif "Theory" in name or name == "Post-Colonial":
        # e.g., Queer Theory, Post-Colonial
        return f"The {name.replace(' Theory', '')} Theorist"
    else:
        # Fallback
        return f"The {name} Scholar"

def get_model(api_key):
    """Configures and returns the Gemini model."""
    try:
        genai.configure(api_key=api_key)
        # Using Gemini 1.5 Pro for complex reasoning required by synthesis
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        return model
    except Exception as e:
        st.error(f"Failed to initialize Gemini API. Please check your API Key. Error: {e}")
        return None

def generate_analysis(model, prompt_key, work_title, work_text):
    """Handles a single API call for analysis."""
    base_prompt = FLATTENED_LENSES[prompt_key]
    final_prompt = f"{base_prompt}\n\n---\nTitle: {work_title}\n\nWork:\n{work_text}"
    
    try:
        response = model.generate_content(final_prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred during analysis generation: {e}")
        return None

def generate_synthesis(model, lens_a_name, analysis_a, lens_b_name, analysis_b, work_title):
    """Synthesizes two analyses into a dialectical dialogue using a second API call."""
    
    # Generate personas programmatically
    persona_a = create_persona_name(lens_a_name)
    persona_b = create_persona_name(lens_b_name)

    # The Synthesis Prompt (Directive 2)
    synthesis_prompt = textwrap.dedent(f"""
    You are tasked with creating a "Dialectical Dialogue" regarding the creative work titled "{work_title}". This dialogue must synthesize two distinct analytical perspectives that have already been generated.

    Perspective A: {lens_a_name}
    <analysis_a>
    {analysis_a}
    </analysis_a>

    Perspective B: {lens_b_name}
    <analysis_b>
    {analysis_b}
    </analysis_b>

    Instructions:
    1. **Format as Dialogue:** Create a structured conversation between two personas. Persona A must be titled "**{persona_a}**" and Persona B must be titled "**{persona_b}**".
    2. **Interaction:** The dialogue should explore the tensions, agreements, and gaps between the two analyses. Each persona must argue from their specific viewpoint, referencing evidence from their respective analyses. The conversation should flow naturally, involving rebuttals and concessions.
    3. **Aufheben / Synthesis:** After the dialogue, provide a concluding section titled "## Aufheben / Synthesis". This section must resolve the tensions discussed (thesis and antithesis) and offer a higher-level interpretation that incorporates the most salient points from both perspectives, demonstrating a richer understanding of the work.

    Begin the dialogue immediately.
    """)
    
    try:
        response = model.generate_content(synthesis_prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred during dialogue synthesis: {e}")
        return None

# --- SIDEBAR FOR SETUP & PROTOCOL SELECTION (Directive 3: Refine UI) ---
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("Enter your Gemini API Key", type="password")

    st.header("🔄 Protocol")

    # Analysis Mode Selection
    analysis_mode = st.radio(
        "Select Analysis Mode:",
        ("Single Lens Analysis", "Dialectical Dialogue")
    )
    # Store the mode in session state for access in the main area
    st.session_state.analysis_mode = analysis_mode

    st.markdown("---")
    st.subheader("Lens Selection")

    # Initialize session state keys if they don't exist (for safety)
    if 'main_lens_name' not in st.session_state: st.session_state.main_lens_name = None
    if 'sub_lens_name' not in st.session_state: st.session_state.sub_lens_name = None
    if 'lens_a_name' not in st.session_state: st.session_state.lens_a_name = None
    if 'lens_b_name' not in st.session_state: st.session_state.lens_b_name = None

    if analysis_mode == "Single Lens Analysis":
        # Step 1: User selects a main lens from the hierarchy
        # Using index=None for a true placeholder if supported by the user's Streamlit version
        main_lens_name = st.selectbox(
            "1. Choose primary category:",
            options=list(LENSES_HIERARCHY.keys()),
            index=None,
            placeholder="Select a category..."
        )
        st.session_state.main_lens_name = main_lens_name

        # Step 2: If the selected lens has sub-lenses, show them
        if main_lens_name and "sub_lenses" in LENSES_HIERARCHY[main_lens_name]:
            # Sort the sub-lenses for better presentation
            sub_lens_options = sorted(list(LENSES_HIERARCHY[main_lens_name]["sub_lenses"].keys()))
            sub_lens_name = st.selectbox(
                "2. Choose specific lens/school:",
                options=sub_lens_options,
                index=None,
                placeholder="Select a specific lens..."
            )
            st.session_state.sub_lens_name = sub_lens_name
        else:
            # Clear sub_lens_name if not applicable
            st.session_state.sub_lens_name = None

    elif analysis_mode == "Dialectical Dialogue":
        st.write("Select two different lenses for synthesis.")

        # Lens A Selection (using the flattened list)
        lens_a_name = st.selectbox(
            "1. Lens A (Thesis):",
            options=SORTED_LENS_NAMES,
            index=None,
            placeholder="Select Lens A..."
        )
        st.session_state.lens_a_name = lens_a_name

        # Lens B Selection
        # Dynamically filter options to ensure Lens B is different from Lens A
        if lens_a_name:
            available_for_b = [lens for lens in SORTED_LENS_NAMES if lens != lens_a_name]
        else:
            available_for_b = SORTED_LENS_NAMES

        lens_b_name = st.selectbox(
            "2. Lens B (Antithesis):",
            options=available_for_b,
            index=None,
            placeholder="Select Lens B..."
        )
        st.session_state.lens_b_name = lens_b_name


# --- MAIN PAGE LOGIC & DISPLAY ---

# Determine if we are ready to display the analysis form
display_analysis_form = False
header_text = ""

# Logic for Single Lens Mode readiness
if st.session_state.analysis_mode == "Single Lens Analysis":
    main_lens = st.session_state.main_lens_name
    sub_lens = st.session_state.sub_lens_name
    header_text = "Single Lens Analysis"

    if main_lens:
        # Display description of the selected category
        description = LENSES_HIERARCHY[main_lens].get("description", "")
        st.info(f"**{main_lens}**: {description}")

        if "sub_lenses" in LENSES_HIERARCHY[main_lens]:
            if sub_lens:
                display_analysis_form = True
                # Store the key needed for prompt lookup later
                st.session_state.current_prompt_key = f"{main_lens} ({sub_lens})"
                header_text += f": {st.session_state.current_prompt_key}"
            else:
                st.warning("⬅️ Please select a specific lens/school (Step 2) in the sidebar.")
        else:
            display_analysis_form = True
            st.session_state.current_prompt_key = main_lens
            header_text += f": {main_lens}"
    else:
        st.info("⬅️ Welcome! Please select a primary analytical category (Step 1) from the sidebar to begin.")

# Logic for Dialectical Dialogue Mode readiness
elif st.session_state.analysis_mode == "Dialectical Dialogue":
    lens_a = st.session_state.lens_a_name
    lens_b = st.session_state.lens_b_name
    header_text = "Dialectical Dialogue"

    if lens_a and lens_b:
        # The sidebar logic prevents them from being the same, but we check again for robustness
        if lens_a == lens_b:
             st.error("Error: Lens A and Lens B must be different.")
        else:
            display_analysis_form = True
            header_text += f": {lens_a} vs. {lens_b}"
            st.info("Ready to synthesize these two distinct viewpoints.")
    else:
        st.info("⬅️ Please select both Lens A and Lens B from the sidebar.")

# --- ANALYSIS FORM & EXECUTION ---
if display_analysis_form:
    st.header(header_text)

    work_title = st.text_input("Enter the title of the work (Optional):")
    work_text = st.text_area("Paste your text or describe your artwork here:", height=300)

    if st.button("Analyze", type="primary"):
        if not api_key:
            st.warning("Please enter your Gemini API Key in the sidebar to begin.")
        elif not work_text:
            st.warning("Please provide the creative work to be analyzed.")
        else:
            # --- Execution Block ---
            model = get_model(api_key)
            if model:
                st.markdown("---")
                
                if st.session_state.analysis_mode == "Single Lens Analysis":
                    # --- Single Lens Execution ---
                    with st.spinner("Analyzing through the selected lens..."):
                        prompt_key = st.session_state.current_prompt_key
                        analysis_text = generate_analysis(model, prompt_key, work_title, work_text)

                        if analysis_text:
                            st.header("Analysis Result")
                            st.markdown(analysis_text)

                elif st.session_state.analysis_mode == "Dialectical Dialogue":
                    # --- Dialectical Dialogue Execution (Two-Call Process) ---
                    lens_a_name = st.session_state.lens_a_name
                    lens_b_name = st.session_state.lens_b_name

                    # Call 1 (Part A): Generate Thesis
                    analysis_a = None
                    with st.spinner(f"Step 1/3: Generating Analysis A (Thesis: {lens_a_name})..."):
                         analysis_a = generate_analysis(model, lens_a_name, work_title, work_text)
                    
                    # Call 1 (Part B): Generate Antithesis
                    analysis_b = None
                    if analysis_a:
                        with st.spinner(f"Step 2/3: Generating Analysis B (Antithesis: {lens_b_name})..."):
                            analysis_b = generate_analysis(model, lens_b_name, work_title, work_text)

                    # Call 2: Synthesis
                    if analysis_a and analysis_b:
                        with st.spinner("Step 3/3: Synthesizing the dialogue (Aufheben)..."):
                            dialogue_text = generate_synthesis(model, lens_a_name, analysis_a, lens_b_name, analysis_b, work_title)
                        
                        if dialogue_text:
                            st.header("Dialectical Dialogue Result")
                            st.markdown(dialogue_text)

                            # Display the raw analyses for reference
                            st.markdown("---")
                            st.subheader("Source Analyses (Reference)")
                            with st.expander(f"View Raw Analysis A: {lens_a_name}"):
                                st.markdown(analysis_a)
                            with st.expander(f"View Raw Analysis B: {lens_b_name}"):
                                st.markdown(analysis_b)
                    else:
                        st.error("Could not generate the initial analyses. Cannot proceed to synthesis.")
