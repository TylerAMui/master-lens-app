# Master Lens Web App - v4.0 (The Multi-Modal Synthesis)
import streamlit as st
import google.generativeai as genai
import textwrap
import PIL.Image
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="The Master Lens v4.0",
    page_icon="🖼️",
    layout="wide"
)

st.title("🖼️ The Master Lens v4.0")
st.write("A multi-modal, AI-powered analytical partner for creative works, featuring Dialectical Dialogue and Image Analysis.")

# --- PROMPT DEFINITIONS (LENSES v4) ---

# Directive 2: New Lenses Added (Evolutionary Psychology, Phenomenological)

LENSES_HIERARCHY = {
    "Structural & Formalist": {
        "description": "A formalist analysis focusing purely on craft, composition, technique, and structure.",
        "prompt": """
Analyze the following creative work from a strictly formalist perspective. Disregard external context, biography, or social implications. Your analysis should focus entirely on the internal structure and aesthetic components.

- Analyze elements such as composition, color, line, medium, structure, meter, rhyme scheme, word choice, and literary devices.
- Explain how these formal elements work together to create the piece's overall aesthetic effect.
"""
    },
    "Psychological": {
        "description": "An inquiry into the work's emotional, symbolic, and archetypal currents.",
        "sub_lenses": {
            "Jungian": """
Analyze the following creative work using a Jungian psychological lens.
- Explore the role of archetypes (e.g., the Shadow, Persona, Anima/Animus), the process of individuation, and connections to the collective unconscious.
- Interpret the work's symbols and imagery as manifestations of the psyche.
""",
            "Freudian": """
Analyze the following creative work using a Freudian psychoanalytic lens.
- Explore themes of repressed desires, the unconscious mind, and the interplay of the Id, Ego, and Superego.
- Discuss any potential dream symbolism, wish-fulfillment, or Oedipal dynamics present in the work.
""",
            "Evolutionary Psychology": """
Analyze the following creative work through the lens of Evolutionary Psychology.
- Explore how the themes, characters, or imagery reflect innate human behaviors shaped by natural selection (e.g., survival instincts, mating strategies, altruism, kinship).
- Discuss how the work resonates with universal aspects of human nature rooted in our ancestral past.
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
""",
            "Taoist": """
Analyze the following creative work through a Taoist lens.
- Explore the concepts of Yin and Yang, the harmony of opposites, and the idea of 'wu wei' (effortless action).
- Discuss how the work reflects the natural flow of the Tao, simplicity, and the virtue of accepting reality.
""",
            "Phenomenological": """
Analyze the following creative work using a Phenomenological approach.
- Focus intensely on the subjective, lived experience of perceiving the work. How does it appear to consciousness?
- Discuss the relationship between the observer and the object, focusing on embodiment, perception, time, and space as depicted or evoked by the work.
- Bracket out external explanations and focus on the 'things themselves' as presented.
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
""",
            "Feminist": """
Analyze the following creative work using a Feminist critical lens.
- Examine the representation of gender roles, power dynamics between sexes, and the presence of patriarchal structures.
- Discuss how the work challenges or reinforces societal expectations regarding gender and explores the intersectionality of identity.
""",
            "Post-Colonial": """
Analyze the following creative work using Post-Colonial theory.
- Examine the representation of the colonizer and the colonized, and the lasting impact of imperialism on cultural identity.
- Discuss themes of hybridity, resistance, agency, and the representation of the "Other".
""",
            "Queer Theory": """
Analyze the following creative work through the lens of Queer Theory.
- Examine how the work constructs, deconstructs, or challenges norms of gender and sexuality.
- Challenge heteronormative assumptions and explore marginalized identities and desires.
- Discuss the performance of identity and the subversion of stable categories.
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
"""
    },
    "Comparative": {
        "description": "Places the work in conversation with other similar artists and movements.",
        "prompt": """
Analyze the following creative work using a comparative lens.
- Identify the key themes, styles, and aesthetic choices in the piece.
- Compare and contrast this work with other similar artists, movements, or genres.
- Discuss where this work fits within its broader artistic or literary tradition.
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
                # Dedent and strip whitespace from the prompt
                flat_lenses[lens_name] = textwrap.dedent(prompt).strip()
        elif "prompt" in details:
            # Dedent and strip whitespace from the prompt
            flat_lenses[main_lens] = textwrap.dedent(details["prompt"]).strip()
    return flat_lenses

# A flattened dictionary used for prompt lookup and the Dialectical Dialogue selection UI.
FLATTENED_LENSES = flatten_lenses(LENSES_HIERARCHY)
SORTED_LENS_NAMES = sorted(list(FLATTENED_LENSES.keys()))

def create_persona_name(lens_name):
    """Creates a suitable persona title from a lens name."""
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
    if name == "Evolutionary Psychology":
        return "The Evolutionary Psychologist"
    if name in ["Marxist", "Feminist"]:
        return f"The {name} Critic"
    if name in ["Existentialist", "Taoist", "Phenomenological"]:
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
        # Using Gemini 1.5 Pro for complex reasoning and multi-modal input
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        return model
    except Exception as e:
        st.error(f"Failed to initialize Gemini API. Please check your API Key. Error: {e}")
        return None

# Directive 3: Update generate_analysis for Multi-Modal Input
def generate_analysis(model, prompt_key, work_title, work_data, modality):
    """Handles a single API call for analysis (Text or Image)."""
    base_prompt = FLATTENED_LENSES[prompt_key]
    
    if modality == "Text Analysis":
        # Standard text prompt format
        final_prompt = f"{base_prompt}\n\nThe work is as follows:\n---\nTitle: {work_title}\n\nWork:\n{work_data}"
        content_input = [final_prompt]
    elif modality == "Image Analysis":
        # Multi-modal prompt format
        # Instruction for the AI to ground its analysis in the visual evidence
        image_instruction = """
Important: You are analyzing a visual artwork (the attached image). 
1. First, provide a detailed, objective description of the image (composition, colors, subjects, textures).
2. Then, apply the requested analytical lens to the visual evidence. Ensure your analysis refers directly to what is visible in the image.
"""
        final_prompt = f"{image_instruction}\n\n{base_prompt}\n\nTitle: {work_title}"
        # Gemini expects the prompt first, then the data (PIL image object)
        content_input = [final_prompt, work_data]
    else:
        st.error("Invalid modality selected.")
        return None

    try:
        response = model.generate_content(content_input)
        return response.text
    except Exception as e:
        st.error(f"An error occurred during analysis generation: {e}")
        # Attempt to retrieve feedback if generation failed (e.g., safety block)
        try:
            if hasattr(e, 'response') and e.response.prompt_feedback:
                 st.warning(f"Generation blocked. Feedback: {e.response.prompt_feedback}")
        except:
            pass
        return None

def generate_synthesis(model, lens_a_name, analysis_a, lens_b_name, analysis_b, work_title):
    """Synthesizes two analyses into a dialectical dialogue using a second API call."""
    
    # Generate personas programmatically
    persona_a = create_persona_name(lens_a_name)
    persona_b = create_persona_name(lens_b_name)

    # The Synthesis Prompt
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
    2. **Interaction:** The dialogue should explore the tensions, agreements, and gaps between the two analyses. Each persona must argue from their specific viewpoint, referencing evidence from their respective analyses (which may be textual or visual). The conversation should flow naturally, involving rebuttals and concessions.
    3. **Aufheben / Synthesis:** After the dialogue, provide a concluding section titled "## Aufheben / Synthesis". This section must resolve the tensions discussed (thesis and antithesis) and offer a higher-level interpretation that incorporates the most salient points from both perspectives, demonstrating a richer understanding of the work.

    Begin the dialogue immediately.
    """)
    
    try:
        response = model.generate_content(synthesis_prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred during dialogue synthesis: {e}")
        return None

# --- SESSION STATE INITIALIZATION ---
if 'selection' not in st.session_state:
    st.session_state.selection = None

# --- SIDEBAR FOR SETUP & PROTOCOL SELECTION ---
# Directive 1: Integrate Refined UI (Component 2)

with st.sidebar:
    st.header("🔑 Setup")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    
    # Directive 3: Modality Selection
    st.header("🖼️ Modality")
    input_modality = st.radio("Select Input Type:", ("Text Analysis", "Image Analysis"))
    st.session_state.input_modality = input_modality

    st.header("🔄 Analytical Protocol")
    analysis_mode = st.radio("Select Analysis Mode:", ("Single Lens", "Dialectical Dialogue"))
    st.session_state.analysis_mode = analysis_mode

    st.markdown("---")
    st.subheader("Lens Selection")

    if analysis_mode == "Single Lens":
        # Hierarchical selection for single lens
        main_lens = st.selectbox(
            "1. Category:", 
            options=list(LENSES_HIERARCHY.keys()),
            index=None,
            placeholder="Select a category..."
        )
        
        if main_lens:
            if "sub_lenses" in LENSES_HIERARCHY[main_lens]:
                sub_lens = st.selectbox(
                    "2. Specific Lens:", 
                    options=sorted(list(LENSES_HIERARCHY[main_lens]["sub_lenses"].keys())),
                    index=None,
                    placeholder="Select a specific lens..."
                )
                if sub_lens:
                    # Store the final selection key
                    st.session_state.selection = f"{main_lens} ({sub_lens})"
                else:
                    st.session_state.selection = None
            else:
                # Store the final selection key
                st.session_state.selection = main_lens
        else:
            st.session_state.selection = None
    
    elif analysis_mode == "Dialectical Dialogue":
        # Multi-select for dialectical dialogue (using the pre-flattened list)
        
        selected_lenses = st.multiselect(
            "Select exactly two lenses to synthesize:", 
            options=SORTED_LENS_NAMES, 
            max_selections=2,
            placeholder="Choose lenses..."
        )
        # Store the list of selections
        st.session_state.selection = selected_lenses


# --- MAIN PAGE LOGIC & DISPLAY ---

# Determine if we are ready to display the analysis form
display_analysis_form = False
header_text = f"{st.session_state.input_modality}: "
work_data = None # Will hold text or image data

# Logic for Readiness based on the new UI integration
if st.session_state.analysis_mode == "Single Lens":
    selection = st.session_state.selection
    header_text += "Single Lens Analysis"

    if selection:
        display_analysis_form = True
        header_text += f" | {selection}"
        
        # Display description if available (requires parsing the selection key)
        if "(" in selection:
            main_lens = selection.split(" (")[0]
        else:
            main_lens = selection
        
        description = LENSES_HIERARCHY.get(main_lens, {}).get("description", "")
        st.info(f"**{main_lens}**: {description}")

    else:
        st.info("⬅️ Please select an analytical category and specific lens (if applicable) from the sidebar to begin.")

elif st.session_state.analysis_mode == "Dialectical Dialogue":
    selection = st.session_state.selection
    header_text += "Dialectical Dialogue"

    if selection and len(selection) == 2:
        display_analysis_form = True
        header_text += f" | {selection[0]} vs. {selection[1]}"
        st.info("Ready to synthesize these two distinct viewpoints.")
    elif selection and len(selection) != 2:
         st.warning("⬅️ Please select exactly two lenses in the sidebar.")
    else:
        st.info("⬅️ Please select two lenses from the sidebar.")

# --- ANALYSIS FORM & INPUT HANDLING ---
if display_analysis_form:
    st.header(header_text)

    work_title = st.text_input("Enter the title of the work (Optional):")

    # Directive 3: Conditional Input based on Modality
    if st.session_state.input_modality == "Text Analysis":
        work_text = st.text_area("Paste your text or describe your artwork here:", height=300)
        if work_text:
            work_data = work_text
    
    elif st.session_state.input_modality == "Image Analysis":
        uploaded_file = st.file_uploader("Upload an image (JPG, PNG, WEBP):", type=["jpg", "jpeg", "png", "webp"])
        if uploaded_file is not None:
            try:
                # Open the image using Pillow
                image = PIL.Image.open(uploaded_file)
                
                # Display the image preview
                st.image(image, caption="Uploaded Artwork Preview", width=400)
                
                # Store the PIL image object for the Gemini API
                work_data = image
                
            except Exception as e:
                st.error(f"Error processing image: {e}")
                work_data = None

    # --- EXECUTION BUTTON ---
    if st.button("Analyze", type="primary"):
        if not api_key:
            st.warning("Please enter your Gemini API Key in the sidebar.")
        elif work_data is None:
            st.warning("Please provide the creative work (text or image) to be analyzed.")
        else:
            # --- Execution Block ---
            model = get_model(api_key)
            if model:
                st.markdown("---")
                
                if st.session_state.analysis_mode == "Single Lens":
                    # --- Single Lens Execution ---
                    with st.spinner("Analyzing through the selected lens..."):
                        # The selection is the prompt key in Single Lens mode
                        prompt_key = st.session_state.selection
                        analysis_text = generate_analysis(
                            model, 
                            prompt_key, 
                            work_title, 
                            work_data, 
                            st.session_state.input_modality
                        )

                        if analysis_text:
                            st.header("Analysis Result")
                            st.markdown(analysis_text)

                elif st.session_state.analysis_mode == "Dialectical Dialogue":
                    # --- Dialectical Dialogue Execution (Two-Call Process) ---
                    # Selections are stored as a list of 2
                    lens_a_name = st.session_state.selection[0]
                    lens_b_name = st.session_state.selection[1]

                    # Call 1 (Part A): Generate Thesis
                    analysis_a = None
                    with st.spinner(f"Step 1/3: Generating Analysis A (Thesis: {lens_a_name})..."):
                        analysis_a = generate_analysis(
                            model, 
                            lens_a_name, 
                            work_title, 
                            work_data, 
                            st.session_state.input_modality
                        )
                    
                    # Call 1 (Part B): Generate Antithesis
                    analysis_b = None
                    if analysis_a:
                        with st.spinner(f"Step 2/3: Generating Analysis B (Antithesis: {lens_b_name})..."):
                            analysis_b = generate_analysis(
                                model, 
                                lens_b_name, 
                                work_title, 
                                work_data, 
                                st.session_state.input_modality
                            )

                    # Call 2: Synthesis
                    if analysis_a and analysis_b:
                        with st.spinner("Step 3/3: Synthesizing the dialogue (Aufheben)..."):
                            # Synthesis only requires the resulting text, not the original data
                            dialogue_text = generate_synthesis(
                                model, 
                                lens_a_name, 
                                analysis_a, 
                                lens_b_name, 
                                analysis_b, 
                                work_title
                            )
                        
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
