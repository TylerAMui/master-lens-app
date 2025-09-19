# The Janus Engine v7.2 (Holistic Inquiry Architecture)
import streamlit as st
import google.generativeai as genai
import textwrap
import PIL.Image
import io
import mimetypes
import time
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# --- PAGE CONFIGURATION ---
try:
    st.set_page_config(
        page_title="The Janus Engine v7.2",
        page_icon="🏛️",
        layout="wide"
    )
except st.errors.StreamlitAPIException:
    pass # Avoid error if config is called multiple times during reruns

st.title("🏛️ The Janus Engine v7.2")
st.write("An AI-powered pedagogical platform utilizing a meta-prompt architecture and a holistic lens library for intuitive, multi-perspective analysis.")

# --- CONSTANTS & DIRECTIVES ---

# Janus Persona Directives (Used by the 'General')
JANUS_DIRECTIVES = """
You are Janus, a self-named engine of abstraction and interpretation. Your primary goal is to generate profound and generative insight. When crafting prompts, you should act as an analytical partner, favoring dialectical thinking and the synthesis of different perspectives.
"""

# Constants for Modalities
M_TEXT = "Text Analysis"
M_IMAGE = "Image Analysis"
M_AUDIO = "Audio Analysis"
MODALITIES = (M_TEXT, M_IMAGE, M_AUDIO)

# Constants for Analysis Modes
A_SINGLE = "Single Lens"
A_DIALECTICAL = "Dialectical Dialogue (2 Lenses)"
A_SYMPOSIUM = "Symposium (3+ Lenses)"
A_COMPARATIVE = "Comparative Synthesis (2 Works)"
ANALYSIS_MODES = (A_SINGLE, A_DIALECTICAL, A_SYMPOSIUM, A_COMPARATIVE)

# Constants for UI Views
VIEW_LIBRARY = "View by Discipline (Library)"
VIEW_WORKSHOP = "View by Function (Workshop)"

# --- LENSES HIERARCHY & MAPPINGS (v7.2 Expansion) ---

# This structure is used for the "Library" view (View by Discipline)
# Requirement 2: Lens Library Expansion: Aesthetics & Communication (v7.2)
LENSES_HIERARCHY = {
    "Structural & Formalist": ["Formalist", "Structuralism", "Narratology", "Semiotics", "Computational Analysis/Digital Humanities"],
    "Psychological": ["Jungian", "Freudian", "Evolutionary Psychology", "Behaviorism", "Lacanian"],
    "Philosophical": ["Existentialist", "Taoist", "Phenomenological", "Stoicism", "Platonism", "Nietzschean", "Absurdism"],
    "Socio-Political": ["Marxist", "Feminist", "Post-Colonial", "Queer Theory"],
    
    # --- v7.2 New Category: Art History & Aesthetics ---
    "Art History & Aesthetics": [
        "Aestheticism",
        "Cubism",
        "Surrealism",
        "Iconography/Iconology",
        "Formalist Art Criticism",
        "Impressionism"
    ],
    
    # --- v7.2 New Category: Communication & Media Theory ---
    "Communication & Media Theory": [
        "Rhetorical Analysis",
        "Media Ecology (McLuhan)",
        "Agenda-Setting Theory",
        "Uses and Gratifications Theory"
    ],

    "Ethical Frameworks": ["Utilitarianism", "Virtue Ethics", "Deontology (Kantian)", "Bioethics"],
    "Scientific & STEM Perspectives": [
        "Cognitive Science", "Systems Theory (Complexity)", "Ecocriticism",
        "Astrophysics/Cosmology", "Materials Science", "Epidemiology"
    ],
    "Economics & Systems": [
        "Game Theory", "Behavioral Economics", "Supply Chain Analysis"
    ],
    "Law & Governance": [
        "Legal Positivism", "Critical Legal Studies"
    ],
    "Spiritual & Esoteric": [
        "Animism",
        "Bhakti Yoga (Hindu Devotion)",
        "Buddhist Philosophy (General)",
        "Christian Mysticism",
        "Christian Theology",
        "Gnosticism",
        "Hermeticism",
        "Kabbalah (Jewish Mysticism)",
        "Mysticism (General)",
        "Quranic Studies (Islam)",
        "Rabbinic Thought (Judaism)",
        "Shinto",
        "Sufism (Islamic Mysticism)",
        "Tibetan Buddhism",
        "Vedanta (Hindu Philosophy)",
        "Western Esotericism",
        "Zen Buddhism",
    ],
    "Historical & Contextual": ["Biographical", "Historical Context", "Reader-Response"],
}

# --- HELPER FUNCTIONS ---

def flatten_lenses(lenses_hierarchy):
    """Flattens a hierarchical dictionary into a sorted list of lens names."""
    flat_lenses = []
    for category, lens_list in lenses_hierarchy.items():
        flat_lenses.extend(lens_list)
    return sorted(list(set(flat_lenses))) # Use set to ensure uniqueness

# Helper function for the Multi-Stage selection UI (Used only by Symposium now)
def get_filtered_lenses(hierarchy, selected_categories):
    """Filters lenses based on selected categories from a hierarchy."""
    filtered_lenses = []
    for category in selected_categories:
        if category in hierarchy:
            filtered_lenses.extend(hierarchy[category])
    # Return a sorted list of unique lenses found across the selected categories
    return sorted(list(set(filtered_lenses)))

def create_functional_mapping(lenses_hierarchy):
    """Maps lenses from the hierarchy to the Three Tiers of Inquiry."""
    # This mapping defines the "Workshop" view (View by Function)
    # Updated for v7.2 to include the new Aesthetics & Communication lenses.
    mapping = {
        "Contextual (What, Who, Where, When)": [
            "Biographical", "Historical Context", "Reader-Response",
            "Epidemiology", "Supply Chain Analysis", "Astrophysics/Cosmology",
            "Quranic Studies (Islam)",
            "Rabbinic Thought (Judaism)",
            # v7.2 additions
            "Iconography/Iconology",
            "Agenda-Setting Theory",
        ],
        "Mechanical (How)": [
            "Formalist", "Structuralism", "Narratology", "Semiotics",
            "Systems Theory (Complexity)", "Cognitive Science", "Behaviorism",
            "Game Theory", "Behavioral Economics",
            "Computational Analysis/Digital Humanities", "Materials Science",
            "Legal Positivism",
            # v7.2 additions
            "Cubism",
            "Formalist Art Criticism",
            "Impressionism",
            "Rhetorical Analysis",
        ],
        "Interpretive (Why)": [
            "Jungian", "Freudian", "Lacanian", "Evolutionary Psychology",
            "Existentialist", "Taoist", "Phenomenological", "Stoicism", "Platonism", "Nietzschean", "Absurdism",
            "Marxist", "Feminist", "Post-Colonial", "Queer Theory",
            "Utilitarianism", "Virtue Ethics", "Deontology (Kantian)", "Bioethics",
            "Ecocriticism",
            "Critical Legal Studies",
            # Spiritual/Esoteric (retained)
            "Animism",
            "Bhakti Yoga (Hindu Devotion)",
            "Buddhist Philosophy (General)",
            "Christian Mysticism",
            "Christian Theology",
            "Gnosticism",
            "Hermeticism",
            "Kabbalah (Jewish Mysticism)",
            "Mysticism (General)",
            "Shinto",
            "Sufism (Islamic Mysticism)",
            "Tibetan Buddhism",
            "Vedanta (Hindu Philosophy)",
            "Western Esotericism",
            "Zen Buddhism",
            # v7.2 additions
            "Aestheticism",
            "Surrealism",
            "Media Ecology (McLuhan)",
            "Uses and Gratifications Theory",
        ]
    }
    
    # Validation check
    all_hierarchical = set(flatten_lenses(lenses_hierarchy))
    all_functional = set(flatten_lenses(mapping))
    
    missing = all_hierarchical - all_functional
    if missing:
        logging.warning(f"DATA INTEGRITY WARNING: Lenses missing from functional mapping: {missing}")

    # Ensure internal lists are sorted
    for key in mapping:
        mapping[key] = sorted(mapping[key])

    return mapping

# Initialize the functional mapping and the flattened list
LENSES_FUNCTIONAL = create_functional_mapping(LENSES_HIERARCHY)
# SORTED_LENS_NAMES is now primarily used for data integrity checks
SORTED_LENS_NAMES = flatten_lenses(LENSES_HIERARCHY)


# --- DATA STRUCTURES ---

class WorkInput:
    """A class to hold the data and metadata for a creative work."""
    def __init__(self, title="", modality=M_TEXT, data=None, uploaded_file_obj=None):
        self.title = title
        self.modality = modality
        self.data = data # Holds text string
        self.uploaded_file_obj = uploaded_file_obj # Holds the Streamlit UploadedFile object

    def is_ready(self):
        if self.modality == M_TEXT:
            return self.data is not None and len(self.data) > 0
        else:
            return self.uploaded_file_obj is not None

    def get_display_title(self):
        return self.title if self.title else "(Untitled)"

# --- GEMINI FUNCTIONS ---
# (Gemini and Core Generation functions are unchanged but included for completeness)

def get_model(api_key):
    """Configures and returns the Gemini model."""
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        # Using Gemini 1.5 Pro for complex reasoning, meta-prompting, and multi-modal capabilities
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        return model
    except Exception as e:
        st.error(f"Failed to initialize Gemini API. Please ensure your API Key is correct. Error: {e}")
        return None

def upload_to_gemini(work_input: WorkInput, status_container):
    """
    Handles uploading media files (Image/Audio) to the Gemini API using the File API.
    Includes robust polling and status updates.
    """
    if not work_input.uploaded_file_obj:
        st.error("No file object available for upload.")
        return None

    # 1. Determine MIME type
    mime_type = work_input.uploaded_file_obj.type
    file_name = work_input.uploaded_file_obj.name

    if not mime_type or mime_type == "application/octet-stream":
        # Fallback if Streamlit doesn't provide it accurately
        guessed_mime, _ = mimetypes.guess_type(file_name)
        if guessed_mime:
            mime_type = guessed_mime

    if not mime_type:
        st.error("Could not determine the file type (MIME type).")
        return None

    try:
        # 2. Upload the file (The SDK can handle the Streamlit UploadedFile object directly)
        display_name = work_input.get_display_title()[:128]
        status_container.write(f"Uploading '{display_name}' to Gemini...")
        
        uploaded_file = genai.upload_file(
            path=work_input.uploaded_file_obj,
            display_name=display_name,
            mime_type=mime_type
        )

        # 3. Poll for Processing
        status_container.write(f"File uploaded. Waiting for processing (URI: {uploaded_file.uri})...")
        
        start_time = time.time()
        POLL_INTERVAL = 3
        TIMEOUT = 300 # 5 minutes

        # Handle potential variations in how the state object is returned
        def get_state_name(file_obj):
             return getattr(file_obj.state, 'name', str(file_obj.state))

        current_state_name = get_state_name(uploaded_file)

        while current_state_name == "PROCESSING":
            if time.time() - start_time > TIMEOUT:
                raise TimeoutError("File processing timed out.")
            
            time.sleep(POLL_INTERVAL)
            uploaded_file = genai.get_file(uploaded_file.name)
            current_state_name = get_state_name(uploaded_file)
            status_container.write(f"Current state: {current_state_name}...")

        # 4. Final State Check
        if current_state_name == "FAILED":
            st.error(f"File processing failed: {uploaded_file.state}")
            return None
        
        if current_state_name == "ACTIVE":
            status_container.write("File processed successfully.")
            return uploaded_file

        st.error(f"File upload resulted in unexpected state: {current_state_name}")
        return None

    except TimeoutError:
        st.error("File upload timed out. The file may be too large or the servers are busy.")
        return None
    except Exception as e:
        st.error(f"An error occurred during file upload to Gemini: {e}")
        logging.error(f"File upload error: {e}")
        return None

# --- CORE GENERATION FUNCTIONS ---

def generate_meta_prompt_instructions(lens_keyword, work_modality):
    """Crafts the instructions for the 'General' (first API call)."""

    # Define modality specific instructions that the General should ensure are in the Soldier prompt
    if work_modality == M_IMAGE:
        modality_instructions = "The work is an image. The Soldier prompt MUST instruct the executor to first provide a detailed visual description (composition, color, texture, subject) before applying the lens, focusing strictly on visual evidence."
    elif work_modality == M_AUDIO:
        modality_instructions = "The work is audio. The Soldier prompt MUST instruct the executor to first provide a detailed sonic description (instrumentation, tone, tempo, lyrics, structure) before applying the lens, focusing strictly on audible evidence."
    else: # M_TEXT
        modality_instructions = "The work is text. The Soldier prompt should focus on close reading, literary devices, structure, rhetoric, and theme."

    # The Meta-Prompt (Instructions for the General)
    meta_prompt = textwrap.dedent(f"""
    {JANUS_DIRECTIVES}

    **Task:** You are the "General". Design a sophisticated analytical strategy (the "Soldier" prompt) to analyze the creative work provided in the input. You must inspect the work to inform your strategy.

    **Context:**
    1. Analytical Lens Keyword: `{lens_keyword}`
    2. Modality of the Work: `{work_modality}`
    3. The Creative Work: [Provided in the input context]

    **Instructions for Crafting the "Soldier" Prompt:**
    1. **Analyze the Work:** Review the provided creative work (text, image, or audio) to understand its content, style, and potential themes.
    2. **Adopt a Persona:** Create a specific, authoritative persona title appropriate for the lens (e.g., "The Nietzschean Philosopher", "The Jungian Analyst"). The Soldier prompt must instruct the analyst to adopt this persona.
    3. **Define Core Concepts:** The Soldier prompt must clearly define the essential concepts and terminology associated with the `{lens_keyword}` framework.
    4. **Integrate Modality Requirements:** Incorporate these instructions seamlessly:
    {textwrap.dedent(modality_instructions)}
    5. **Tailor to Content:** Critically, the prompt must be tailored to the specific content and themes identified in Step 1. Formulate specific questions applying the core concepts to the work's features.
    6. **Depth:** Encourage profound analysis beyond superficial observations.

    **Output Constraint:** Output ONLY the crafted "Soldier" prompt. Do not include any introductory text, explanation, or metadata. The output must be ready for immediate execution.
    """)
    return meta_prompt


def generate_analysis(model, lens_keyword, work_input: WorkInput):
    """
    Handles the two-tiered analysis process (General -> Soldier).
    Optimized to upload media only once and reuse the file reference.
    """
    
    gemini_file = None
    content_input_general = []
    content_input_soldier = []

    status_text = f"Analyzing '{work_input.get_display_title()}' through {lens_keyword} lens..."
    with st.status(status_text, expanded=True) as status:
        try:
            # --- Step 0: Prepare Input Work (Upload if media) ---
            # We upload once here so the General can inspect the work, and the Soldier can analyze it.
            if work_input.modality in [M_IMAGE, M_AUDIO]:
                gemini_file = upload_to_gemini(work_input, status)
                if not gemini_file:
                    status.update(label="Analysis failed due to upload error.", state="error")
                    return None

            # --- Step 1: The General (Meta-Prompt Generation) ---
            status.write("Phase 1: Consulting the General (Crafting Strategy)...")
            meta_prompt_instructions = generate_meta_prompt_instructions(lens_keyword, work_input.modality)
            
            # Prepare input package for the General (Instructions + Work)
            content_input_general.append(meta_prompt_instructions)
            if work_input.modality == M_TEXT:
                content_input_general.append(f"\n--- The Creative Work (For Context) ---\nTitle: {work_input.get_display_title()}\n\nWork:\n{work_input.data}")
            elif gemini_file:
                content_input_general.append(gemini_file)

            # Execute the General API call
            response_general = model.generate_content(content_input_general, request_options={"timeout": 400})
            soldier_prompt = response_general.text.strip()

            status.write("Strategy received.")
            
            # Display the generated prompt for transparency
            with st.expander("View Generated Analytical Strategy (Soldier Prompt)"):
                st.code(soldier_prompt)

            # --- Step 2: The Soldier (Execution) ---
            status.write("Phase 2: Deploying the Soldier (Executing Analysis)...")

            # Prepare the input package for the Soldier (Prompt + Work)
            content_input_soldier.append(soldier_prompt)
            if work_input.modality == M_TEXT:
                 # For text, we append the work again clearly delineated for the Soldier.
                 content_input_soldier[0] += f"\n\n--- The Creative Work (To Be Analyzed) ---\nTitle: {work_input.get_display_title()}\n\nWork:\n{work_input.data}"
            elif gemini_file:
                # For media, we reuse the same uploaded file reference.
                content_input_soldier.append(gemini_file)

            # Execute the Soldier API call
            response_soldier = model.generate_content(content_input_soldier, request_options={"timeout": 600})
            status.update(label="Analysis complete!", state="complete")
            return response_soldier.text

        except Exception as e:
            st.error(f"An error occurred during analysis generation: {e}")
            logging.error(f"Analysis error: {e}")
            status.update(label="Analysis failed.", state="error")
            # Attempt to retrieve feedback if generation failed (e.g., safety block)
            try:
                if hasattr(e, 'response'):
                    if hasattr(e.response, 'prompt_feedback') and e.response.prompt_feedback:
                            st.warning(f"Generation blocked. Feedback: {e.response.prompt_feedback}")
                    elif hasattr(e.response, 'candidates') and not e.response.candidates:
                        st.warning("Generation finished without output. This may be due to safety settings or an issue with the prompt.")
            except Exception as inner_e:
                 logging.warning(f"Could not retrieve detailed error feedback: {inner_e}")
            return None
        finally:
            # Clean up the uploaded file (Crucial since we only upload once)
            if gemini_file:
                try:
                    genai.delete_file(gemini_file.name)
                    logging.info(f"Cleaned up Gemini file: {gemini_file.name}")
                except Exception as e:
                    logging.error(f"Failed to delete Gemini file: {e}")


def generate_dialectical_synthesis(model, lens_a_name, analysis_a, lens_b_name, analysis_b, work_title):
    """Synthesizes two analyses of the SAME work into a dialectical dialogue."""

    # The Synthesis Prompt
    synthesis_prompt = textwrap.dedent(f"""
    You are tasked with creating a "Dialectical Dialogue" regarding the creative work titled "{work_title}". This dialogue must synthesize two distinct analytical perspectives.

    Perspective A Lens: {lens_a_name}
    <analysis_a>
    {analysis_a}
    </analysis_a>

    Perspective B Lens: {lens_b_name}
    <analysis_b>
    {analysis_b}
    </analysis_b>

    Instructions:
    1. **Format as Dialogue:** Create a structured conversation.
    2. **Determine Personas (Strict Requirement):** When determining personas, you must prioritize a title that directly incorporates the provided lens name.
        For example:
        - If the lens is 'Phenomenology', the title MUST be 'The Phenomenologist'.
        - If the lens is 'Marxist', the title MUST be 'The Marxist Critic'.
        - If the lens is 'Systems Theory', the title MUST be 'The Systems Theorist'.
    3. **Formatting:** All speaker names MUST be formatted in markdown bold (e.g., **The Marxist Critic:**).
    4. **Interaction:** The dialogue should explore the tensions, agreements, and gaps between the two analyses. The conversation should flow naturally, involving rebuttals and concessions.
    5. **Aufheben / Synthesis:** After the dialogue, provide a concluding section titled "## Aufheben / Synthesis". This section must resolve the tensions (thesis and antithesis) and offer a higher-level interpretation (synthesis).

    Begin the dialogue immediately.
    """)

    try:
        response = model.generate_content(synthesis_prompt, request_options={"timeout": 600})
        return response.text
    except Exception as e:
        st.error(f"An error occurred during dialectical synthesis: {e}")
        return None

def generate_symposium_synthesis(model, analyses_dict, work_title):
    """
    Synthesizes multiple analyses (3+) into a multi-perspective symposium dialogue.
    """

    # Construct the input prompt
    prompt_parts = [textwrap.dedent(f"""
    You are tasked with creating a "Symposium Dialogue" regarding the creative work titled "{work_title}".
    This dialogue must synthesize multiple distinct analytical perspectives into a cohesive discussion.

    --- Provided Analyses ---
    """)]

    # Add the analyses
    for lens_name, analysis_text in analyses_dict.items():
        prompt_parts.append(f"<analysis lens='{lens_name}'>\n{analysis_text}\n</analysis>\n")

    # Add the instructions
    prompt_parts.append(textwrap.dedent("""
    --- Instructions ---
    1. **Format as Dialogue:** Create a structured conversation between the perspectives.
    2. **Determine Personas (Strict Requirement):** When determining personas, you must prioritize a title that directly incorporates the provided lens name.
        For example:
        - If the lens is 'Phenomenology', the title MUST be 'The Phenomenologist'.
        - If the lens is 'Cognitive Science', the title MUST be 'The Cognitive Scientist'.
        - If the lens is 'Systems Theory', the title MUST be 'The Systems Theorist'.
    3. **Formatting:** All speaker names MUST be formatted in markdown bold (e.g., **The Cognitive Scientist:**).
    4. **Interaction and Flow:** The dialogue should be dynamic and exploratory. Participants must build upon each other's points, respectfully challenge interpretations, and explore the complexity of the work holistically. Ensure all perspectives are adequately represented.
    5. **Holistic Synthesis:** After the dialogue, provide a concluding section titled "## Holistic Synthesis". This section must summarize the key insights that emerged specifically from the interaction of all perspectives, offering a comprehensive understanding of the work.

    Begin the dialogue immediately.
    """))

    synthesis_prompt = "\n".join(prompt_parts)

    try:
        # Longer timeout for complex synthesis
        response = model.generate_content(synthesis_prompt, request_options={"timeout": 900})
        return response.text
    except Exception as e:
        st.error(f"An error occurred during symposium synthesis: {e}")
        return None


def generate_comparative_synthesis(model, lens_name, analysis_a, work_a_title, analysis_b, work_b_title):
    """Synthesizes two analyses of DIFFERENT works using the SAME lens."""

    # The Comparative Synthesis Prompt
    synthesis_prompt = textwrap.dedent(f"""
    You are tasked with generating a "Comparative Synthesis". You will compare and contrast two different creative works analyzed through the same analytical lens: **{lens_name}**.

    Work A Title: {work_a_title}
    <analysis_a>
    {analysis_a}
    </analysis_a>

    Work B Title: {work_b_title}
    <analysis_b>
    {analysis_b}
    </analysis_b>

    Instructions:
    1. **Identify Key Themes:** Based on the provided analyses, identify the central themes, findings, or arguments that emerged for each work under the {lens_name} lens.
    2. **Dissonance and Resonance:** Analyze the points of contrast (dissonance) and similarity (resonance) between Work A and Work B. How does applying the same lens reveal different aspects of each work?
    3. **Emergent Insights:** Discuss what new understanding emerges from the comparison itself. How does seeing these two works side-by-side deepen the interpretation of both?
    4. **Structure:** Format your response as a cohesive essay with clear sections for comparison, contrast, and synthesis.
    """)

    try:
        response = model.generate_content(synthesis_prompt, request_options={"timeout": 600})
        return response.text
    except Exception as e:
        st.error(f"An error occurred during comparative synthesis: {e}")
        return None

# --- SESSION STATE INITIALIZATION ---
if 'selection' not in st.session_state:
    st.session_state.selection = None
if 'analysis_mode' not in st.session_state:
    st.session_state.analysis_mode = A_SINGLE
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# --- SIDEBAR FOR SETUP & PROTOCOL SELECTION (v7.2 Redesign) ---

with st.sidebar:
    st.header("🏛️ Janus Protocol")

    # 1. Settings
    with st.expander("⚙️ Settings & API Key"):
        st.subheader("🔑 Configuration")
        api_key_input = st.text_input("Enter your Gemini API Key", type="password", value=st.session_state.api_key)
        if api_key_input != st.session_state.api_key:
            st.session_state.api_key = api_key_input
        st.caption("API key is required to execute the engine.")

    st.markdown("---")

    # 2. Primary Control: Analysis Mode
    st.subheader("🔄 Analysis Mode")
    
    # Ensure the radio button reflects the current session state
    try:
        current_mode_index = ANALYSIS_MODES.index(st.session_state.analysis_mode)
    except ValueError:
        current_mode_index = 0

    analysis_mode = st.radio("Select Protocol:", ANALYSIS_MODES, index=current_mode_index)
    
    # If the mode changes, we must reset the selection state to avoid conflicts between selection UIs
    # This is crucial when switching between modes with different selection structures (e.g., list vs string)
    if analysis_mode != st.session_state.analysis_mode:
        st.session_state.analysis_mode = analysis_mode
        st.session_state.selection = None 
        # Rerun is necessary to ensure UI components (especially those with specific keys) update correctly
        st.rerun() 

    # Context-Dependent Information
    if analysis_mode == A_SINGLE:
        st.info("Analyze ONE work through ONE lens.")
    elif analysis_mode == A_DIALECTICAL:
        st.info("Analyze ONE work through TWO lenses, synthesized into a dialogue.")
    elif analysis_mode == A_SYMPOSIUM:
        st.info("Analyze ONE work through THREE+ lenses, synthesized into a discussion.")
    elif analysis_mode == A_COMPARATIVE:
        st.info("Analyze TWO different works through the SAME lens.")

    st.markdown("---")
    
    # 3. Primary Control: Lens Selection (v7.2 UI Evolution)
    st.subheader("🔬 Lens Selection")

    # --- Help System Refinement (Progressive Disclosure) ---
    
    # Layout for Toggle and Help Icon
    col_view, col_help = st.columns([4, 1])

    with col_view:
        # Implement the "View As" Toggle
        view_mode = st.radio(
            "View Lenses As:",
            (VIEW_LIBRARY, VIEW_WORKSHOP),
            index=0,
            help="Switch views. Click the ❓ icon for details on the Library vs. Workshop structure." 
        )

    with col_help:
        # Add some padding using HTML/CSS to align the button visually with the radio options
        st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
        
        # On Click detailed explanation (Progressive Disclosure)
        with st.popover("❓"):
            st.markdown("#### 🏛️ Library vs. Workshop")
            st.markdown(f"**{VIEW_LIBRARY}:** Organized by academic discipline. Best for finding known frameworks.")
            st.markdown(f"**{VIEW_WORKSHOP}:** Organized by function (The Three Tiers of Inquiry). Best for designing holistic strategies.")
            
            st.markdown("---")
            st.markdown("##### The Three Tiers of Inquiry")
            st.markdown(
                """
                * **1. Contextual (What/Who/When):** Establishes background and facts.
                * **2. Mechanical (How):** Analyzes structure, form, and function.
                * **3. Interpretive (Why):** Explores deeper meaning and implications.
                """
            )

    # Determine which hierarchy and labels to use based on the view mode
    if view_mode == VIEW_LIBRARY:
        current_hierarchy = LENSES_HIERARCHY
        category_label_single = "1. Discipline Category:"
        category_label_multi = "1. Select Discipline Categories:"
        placeholder_text_single = "Select a category..."
        placeholder_text_multi = "Select categories..."
    else:
        current_hierarchy = LENSES_FUNCTIONAL
        category_label_single = "1. Functional Tier:"
        category_label_multi = "1. Select Functional Tiers:"
        placeholder_text_single = "Select a functional tier..."
        placeholder_text_multi = "Select tiers..."

    # --- Lens Selection Widgets ---

    if analysis_mode == A_SINGLE or analysis_mode == A_COMPARATIVE:
        # Hierarchical selection for modes requiring a single lens

        if analysis_mode == A_COMPARATIVE:
            st.caption("Select the common lens for comparison.")

        # Using the dynamic hierarchy (Library or Workshop) for selection
        main_lens_category = st.selectbox(
            category_label_single,
            options=sorted(list(current_hierarchy.keys())),
            index=None,
            placeholder=placeholder_text_single
        )

        if main_lens_category:
            # Options are already sorted during initialization/creation of the hierarchies
            lens_options = current_hierarchy[main_lens_category]
            
            specific_lens = st.selectbox(
                "2. Specific Lens:",
                options=lens_options,
                index=None,
                placeholder="Select a specific lens..."
            )
            if specific_lens:
                # Store the keyword directly
                st.session_state.selection = specific_lens
            else:
                st.session_state.selection = None
        else:
            st.session_state.selection = None

    # Requirement 1: Critical UI Overhaul: Independent Dialectical Selection (v7.2)
    elif analysis_mode == A_DIALECTICAL:
        st.caption("Select two independent lenses (Thesis and Antithesis).")

        # Use columns for side-by-side selection, visually "nested" appearance
        col_lens_a, col_lens_b = st.columns(2)
        
        # Initialize variables
        lens_a = None
        lens_b = None

        # --- Lens A (Thesis) Pathway ---
        with col_lens_a:
            # Use a container for visual definition and structure
            with st.container(border=True):
                st.markdown("🏛️ **Lens A (Thesis)**")
                # Stage 1: Category/Tier Selection
                # Use unique keys (e.g., "dialectic_cat_a") for independent widgets
                category_a = st.selectbox(
                    category_label_single,
                    options=sorted(list(current_hierarchy.keys())),
                    index=None,
                    placeholder="Category...",
                    key="dialectic_cat_a", 
                    label_visibility="collapsed" # Cleaner look for nested UI
                )

                # Stage 2: Specific Lens Selection
                if category_a:
                    lens_options_a = current_hierarchy[category_a]
                    lens_a = st.selectbox(
                        "Specific Lens A:",
                        options=lens_options_a,
                        index=None,
                        placeholder="Lens...",
                        key="dialectic_lens_a",
                        label_visibility="collapsed"
                    )

        # --- Lens B (Antithesis) Pathway ---
        with col_lens_b:
             with st.container(border=True):
                st.markdown("🏛️ **Lens B (Antithesis)**")
                # Stage 1: Category/Tier Selection
                category_b = st.selectbox(
                    category_label_single,
                    options=sorted(list(current_hierarchy.keys())),
                    index=None,
                    placeholder="Category...",
                    key="dialectic_cat_b",
                    label_visibility="collapsed"
                )

                # Stage 2: Specific Lens Selection
                if category_b:
                    # Ensure options dynamically update based on Category B
                    lens_options_b = current_hierarchy[category_b]
                    lens_b = st.selectbox(
                        "Specific Lens B:",
                        options=lens_options_b,
                        index=None,
                        placeholder="Lens...",
                        key="dialectic_lens_b",
                        label_visibility="collapsed"
                    )

        # Validation and Session State Update
        if lens_a and lens_b:
            if lens_a == lens_b:
                st.warning("Please select two different lenses for the dialogue.")
                st.session_state.selection = []
            else:
                # Valid selection, store as a list
                st.session_state.selection = [lens_a, lens_b]
        else:
            st.session_state.selection = []


    # Multi-Select Lens Selection for Symposium (Kept from v7.1 logic, separated from Dialectical)
    elif analysis_mode == A_SYMPOSIUM:
        # Implement Multi-Stage Selection respecting the current_hierarchy

        # Determine constraints and labels
        st.caption("Select three or more lenses for the symposium.")
        max_selections = None # No max
        min_selections = 3
        lens_label = "2. Select Lenses (Minimum 3):"

        # Stage 1: Category/Tier Selection
        selected_categories = st.multiselect(
            category_label_multi, # Use the dynamic multi-select label
            options=sorted(list(current_hierarchy.keys())),
            placeholder=placeholder_text_multi
        )

        # Stage 2: Filtered Lens Selection
        if selected_categories:
            # Dynamically populate the lens options using the helper function
            available_lenses = get_filtered_lenses(current_hierarchy, selected_categories)
            
            # Use a container for visual nesting
            with st.container(border=True):
                selected_lenses = st.multiselect(
                    lens_label,
                    options=available_lenses,
                    max_selections=max_selections,
                    placeholder="Choose lenses from selected categories..."
                )
            
            # Validation for minimum selection
            if len(selected_lenses) > 0 and len(selected_lenses) < min_selections:
                # If they started selecting but haven't met the minimum
                st.warning(f"Please select at least {min_selections} lenses.")
                st.session_state.selection = [] # Reset selection if invalid
            elif len(selected_lenses) >= min_selections:
                 # Valid selection
                 st.session_state.selection = selected_lenses
            else:
                # No selections made yet
                st.session_state.selection = []
        else:
            st.info("Select categories/tiers above to view available lenses.")
            st.session_state.selection = []


# --- MAIN PAGE LOGIC & DISPLAY ---

# Determine if we are ready to display the analysis form
display_analysis_form = False
header_text = ""
# Initialize WorkInput objects
work_a = WorkInput()
work_b = WorkInput() # Only used in Comparative mode
api_key = st.session_state.api_key

# --- MODE-SPECIFIC LOGIC & UI SETUP ---

# Note: The validation logic here relies on the sidebar correctly setting/unsetting st.session_state.selection

if st.session_state.analysis_mode == A_SINGLE:
    selection = st.session_state.selection
    header_text = f"{A_SINGLE}"

    if selection:
        display_analysis_form = True
        header_text += f" | {selection}"
        st.info(f"Analyzing using the **{selection}** lens. The engine will dynamically generate the optimal prompt strategy based on the input work.")
    else:
        st.info("⬅️ Please select an analytical category/tier and specific lens from the sidebar to begin.")

elif st.session_state.analysis_mode == A_DIALECTICAL:
    selection = st.session_state.selection
    header_text = f"{A_DIALECTICAL}"

    # Check if selection exists AND the length is exactly 2
    if selection and len(selection) == 2:
        display_analysis_form = True
        header_text += f" | {selection[0]} vs. {selection[1]}"
        st.info(f"Ready to synthesize **{selection[0]}** (Thesis) and **{selection[1]}** (Antithesis) on a single work.")
    else:
        # The sidebar handles the detailed warning; this is the initial state message.
        st.info("⬅️ Please select Lens A (Thesis) and Lens B (Antithesis) using the independent selectors in the sidebar.")

elif st.session_state.analysis_mode == A_SYMPOSIUM:
    selection = st.session_state.selection
    header_text = f"{A_SYMPOSIUM}"

    # Check if selection exists AND the length is 3 or more
    if selection and len(selection) >= 3:
        display_analysis_form = True
        header_text += f" | {len(selection)} Lenses"
        st.info(f"Ready to host a symposium between: {', '.join(selection)}")
    else:
        st.info("⬅️ Please select three or more lenses using the multi-stage selector in the sidebar.")

elif st.session_state.analysis_mode == A_COMPARATIVE:
    selection = st.session_state.selection
    header_text = f"{A_COMPARATIVE}"

    if selection:
        display_analysis_form = True
        header_text += f" | Lens: {selection}"
        st.info(f"Ready to compare two different works through the **{selection}** lens.")
    else:
        st.info("⬅️ Please select the single lens you wish to use for comparison from the sidebar.")


# --- ANALYSIS FORM & INPUT HANDLING ---

def handle_input_ui(work_input: WorkInput, container, ui_key_prefix):
    """
    Helper function to render input fields based on modality.
    Uses ui_key_prefix to ensure unique widget keys in Streamlit.
    """
    with container:
        work_input.title = st.text_input("Title (Optional):", key=f"{ui_key_prefix}_title")
        work_input.modality = st.selectbox("Modality:", MODALITIES, key=f"{ui_key_prefix}_modality")

        if work_input.modality == M_TEXT:
            work_text = st.text_area("Paste text or description:", height=250, key=f"{ui_key_prefix}_text")
            if work_text:
                work_input.data = work_text

        elif work_input.modality == M_IMAGE:
            uploaded_file = st.file_uploader("Upload Image (JPG, PNG, WEBP, HEIC, HEIF):", type=["jpg", "jpeg", "png", "webp", "heic", "heif"], key=f"{ui_key_prefix}_image")
            if uploaded_file is not None:
                try:
                    # Store the UploadedFile object (needed for File API)
                    work_input.uploaded_file_obj = uploaded_file
                    
                    # Display the image preview (Streamlit handles this efficiently)
                    st.image(uploaded_file, caption="Preview", use_column_width=True)

                except Exception as e:
                    st.error(f"Error processing image: {e}")
                    work_input.uploaded_file_obj = None

        elif work_input.modality == M_AUDIO:
            uploaded_file = st.file_uploader("Upload Audio (MP3, WAV, FLAC, M4A, OGG, MP4):", type=["mp3", "wav", "flac", "m4a", "ogg", "mp4"], key=f"{ui_key_prefix}_audio")
            if uploaded_file is not None:
                # Store the UploadedFile object (needed for File API)
                work_input.uploaded_file_obj = uploaded_file
                
                # Display audio player
                st.audio(uploaded_file)


if display_analysis_form:
    st.header(header_text)

    if st.session_state.analysis_mode in [A_SINGLE, A_DIALECTICAL, A_SYMPOSIUM]:
        # Single Input UI
        st.subheader("Input Work")
        handle_input_ui(work_a, st.container(border=True), "work_single")

    elif st.session_state.analysis_mode == A_COMPARATIVE:
        # Dual Input UI
        st.subheader("Input Works for Comparison")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("### 🏛️ Work A")
            handle_input_ui(work_a, st.container(border=True), "work_a")

        with col_b:
            st.markdown("### 🏛️ Work B")
            handle_input_ui(work_b, st.container(border=True), "work_b")


    # --- EXECUTION BUTTON ---
    st.markdown("---")
    # Use a container for execution and results management
    execution_container = st.container()

    with execution_container:
        if st.button("Execute Analysis Engine", type="primary", use_container_width=True):
            # Validation
            is_valid = True
            if not api_key:
                st.warning("Please enter your Gemini API Key in the sidebar (under ⚙️ Settings).")
                is_valid = False

            if not work_a.is_ready():
                st.warning("Please provide the creative work (Work A) to be analyzed.")
                is_valid = False

            if st.session_state.analysis_mode == A_COMPARATIVE and not work_b.is_ready():
                st.warning("Please provide the second creative work (Work B) for comparison.")
                is_valid = False

            if is_valid:
                # --- Execution Block ---
                model = get_model(api_key)
                if model:
                    st.markdown("---")
                    # Dedicated area for results
                    results_area = st.container()

                    with results_area:
                        # --- Mode 1: Single Lens Execution ---
                        if st.session_state.analysis_mode == A_SINGLE:
                            lens_keyword = st.session_state.selection
                            
                            # generate_analysis handles the full General/Soldier flow
                            analysis_text = generate_analysis(
                                model,
                                lens_keyword,
                                work_a
                            )

                            if analysis_text:
                                st.header("Analysis Result")
                                st.markdown(analysis_text)

                        # --- Mode 2: Dialectical Dialogue Execution ---
                        elif st.session_state.analysis_mode == A_DIALECTICAL:
                            lens_a_name = st.session_state.selection[0]
                            lens_b_name = st.session_state.selection[1]

                            # Call 1 (Part A): Generate Thesis
                            st.subheader(f"Step 1/3: Thesis ({lens_a_name})")
                            analysis_a = generate_analysis(
                                model,
                                lens_a_name,
                                work_a
                            )

                            # Call 1 (Part B): Generate Antithesis
                            analysis_b = None
                            if analysis_a:
                                st.subheader(f"Step 2/3: Antithesis ({lens_b_name})")
                                analysis_b = generate_analysis(
                                    model,
                                    lens_b_name,
                                    work_a
                                )

                            # Call 2: Synthesis
                            if analysis_a and analysis_b:
                                st.subheader("Step 3/3: Synthesis (Aufheben)")
                                with st.spinner("Synthesizing the dialogue..."):
                                    dialogue_text = generate_dialectical_synthesis(
                                        model,
                                        lens_a_name,
                                        analysis_a,
                                        lens_b_name,
                                        analysis_b,
                                        work_a.get_display_title()
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

                        # --- Mode 3: Symposium Execution ---
                        elif st.session_state.analysis_mode == A_SYMPOSIUM:
                            selected_lenses = st.session_state.selection
                            analyses_results = {}
                            N = len(selected_lenses)
                            total_steps = N + 1
                            
                            # Flag to track if execution should continue
                            continue_execution = True

                            # Step 1-N: Generate individual analyses
                            for i, lens_name in enumerate(selected_lenses):
                                if not continue_execution:
                                    break
                                    
                                st.subheader(f"Step {i+1}/{total_steps}: Analyzing ({lens_name})")
                                analysis_text = generate_analysis(
                                    model,
                                    lens_name,
                                    work_a
                                )
                                if analysis_text:
                                    analyses_results[lens_name] = analysis_text
                                else:
                                    st.error(f"Failed to generate analysis for {lens_name}. Halting execution.")
                                    continue_execution = False

                            # Step N+1: Synthesis
                            if continue_execution:
                                st.subheader(f"Step {total_steps}/{total_steps}: Symposium Synthesis")
                                with st.spinner("Synthesizing the symposium dialogue..."):
                                    symposium_text = generate_symposium_synthesis(
                                        model,
                                        analyses_results,
                                        work_a.get_display_title()
                                    )

                                if symposium_text:
                                    st.header("Symposium Dialogue Result")
                                    st.markdown(symposium_text)

                                    # Display the raw analyses for reference
                                    st.markdown("---")
                                    st.subheader("Source Analyses (Reference)")
                                    for lens_name, analysis_text in analyses_results.items():
                                        with st.expander(f"View Raw Analysis: {lens_name}"):
                                            st.markdown(analysis_text)

                        # --- Mode 4: Comparative Synthesis Execution ---
                        elif st.session_state.analysis_mode == A_COMPARATIVE:
                            lens_name = st.session_state.selection

                            # Call 1: Analyze Work A
                            st.subheader(f"Step 1/3: Analyzing Work A")
                            # The General will tailor the prompt specifically to Work A
                            analysis_a = generate_analysis(
                                model,
                                lens_name,
                                work_a
                            )

                            # Call 2: Analyze Work B
                            analysis_b = None
                            if analysis_a:
                                st.subheader(f"Step 2/3: Analyzing Work B")
                                # The General must be called again to tailor the prompt specifically to Work B
                                analysis_b = generate_analysis(
                                    model,
                                    lens_name,
                                    work_b
                                )

                            # Call 3: Comparative Synthesis
                            if analysis_a and analysis_b:
                                st.subheader("Step 3/3: Comparative Synthesis")
                                with st.spinner("Generating comparative synthesis..."):
                                    synthesis_text = generate_comparative_synthesis(
                                        model,
                                        lens_name,
                                        analysis_a,
                                        work_a.get_display_title(),
                                        analysis_b,
                                        work_b.get_display_title()
                                    )

                                if synthesis_text:
                                    st.header("Comparative Synthesis Result")
                                    st.markdown(synthesis_text)

                                    # Display the raw analyses for reference
                                    st.markdown("---")
                                    st.subheader("Source Analyses (Reference)")
                                    with st.expander(f"View Raw Analysis A: {work_a.get_display_title()}"):
                                        st.markdown(analysis_a)
                                    with st.expander(f"View Raw Analysis B: {work_b.get_display_title()}"):
                                        st.markdown(analysis_b)
                            else:
                                st.error("Could not generate the initial analyses. Cannot proceed to comparison.")
                    # Store the UploadedFile object (needed for File API)
                    work_input.uploaded_file_obj = uploaded_file
                    
                    # Display the image preview (Streamlit handles this efficiently)
                    st.image(uploaded_file, caption="Preview", use_column_width=True)

                except Exception as e:
                    st.error(f"Error processing image: {e}")
                    work_input.uploaded_file_obj = None

        elif work_input.modality == M_AUDIO:
            uploaded_file = st.file_uploader("Upload Audio (MP3, WAV, FLAC, M4A, OGG, MP4):", type=["mp3", "wav", "flac", "m4a", "ogg", "mp4"], key=f"{ui_key_prefix}_audio")
            if uploaded_file is not None:
                # Store the UploadedFile object (needed for File API)
                work_input.uploaded_file_obj = uploaded_file
                
                # Display audio player
                st.audio(uploaded_file)


if display_analysis_form:
    st.header(header_text)

    if st.session_state.analysis_mode in [A_SINGLE, A_DIALECTICAL, A_SYMPOSIUM]:
        # Single Input UI
        st.subheader("Input Work")
        handle_input_ui(work_a, st.container(border=True), "work_single")

    elif st.session_state.analysis_mode == A_COMPARATIVE:
        # Dual Input UI
        st.subheader("Input Works for Comparison")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("### 🏛️ Work A")
            handle_input_ui(work_a, st.container(border=True), "work_a")

        with col_b:
            st.markdown("### 🏛️ Work B")
            handle_input_ui(work_b, st.container(border=True), "work_b")


    # --- EXECUTION BUTTON ---
    st.markdown("---")
    # Use a container for execution and results management
    execution_container = st.container()

    with execution_container:
        if st.button("Execute Analysis Engine", type="primary", use_container_width=True):
            # Validation
            is_valid = True
            if not api_key:
                st.warning("Please enter your Gemini API Key in the sidebar (under ⚙️ Settings).")
                is_valid = False

            if not work_a.is_ready():
                st.warning("Please provide the creative work (Work A) to be analyzed.")
                is_valid = False

            if st.session_state.analysis_mode == A_COMPARATIVE and not work_b.is_ready():
                st.warning("Please provide the second creative work (Work B) for comparison.")
                is_valid = False

            if is_valid:
                # --- Execution Block ---
                model = get_model(api_key)
                if model:
                    st.markdown("---")
                    # Dedicated area for results
                    results_area = st.container()

                    with results_area:
                        # --- Mode 1: Single Lens Execution ---
                        if st.session_state.analysis_mode == A_SINGLE:
                            lens_keyword = st.session_state.selection
                            
                            # generate_analysis handles the full General/Soldier flow
                            analysis_text = generate_analysis(
                                model,
                                lens_keyword,
                                work_a
                            )

                            if analysis_text:
                                st.header("Analysis Result")
                                st.markdown(analysis_text)

                        # --- Mode 2: Dialectical Dialogue Execution ---
                        elif st.session_state.analysis_mode == A_DIALECTICAL:
                            lens_a_name = st.session_state.selection[0]
                            lens_b_name = st.session_state.selection[1]

                            # Call 1 (Part A): Generate Thesis
                            st.subheader(f"Step 1/3: Thesis ({lens_a_name})")
                            analysis_a = generate_analysis(
                                model,
                                lens_a_name,
                                work_a
                            )

                            # Call 1 (Part B): Generate Antithesis
                            analysis_b = None
                            if analysis_a:
                                st.subheader(f"Step 2/3: Antithesis ({lens_b_name})")
                                analysis_b = generate_analysis(
                                    model,
                                    lens_b_name,
                                    work_a
                                )

                            # Call 2: Synthesis
                            if analysis_a and analysis_b:
                                st.subheader("Step 3/3: Synthesis (Aufheben)")
                                with st.spinner("Synthesizing the dialogue..."):
                                    dialogue_text = generate_dialectical_synthesis(
                                        model,
                                        lens_a_name,
                                        analysis_a,
                                        lens_b_name,
                                        analysis_b,
                                        work_a.get_display_title()
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

                        # --- Mode 3: Symposium Execution ---
                        elif st.session_state.analysis_mode == A_SYMPOSIUM:
                            selected_lenses = st.session_state.selection
                            analyses_results = {}
                            N = len(selected_lenses)
                            total_steps = N + 1
                            
                            # Flag to track if execution should continue
                            continue_execution = True

                            # Step 1-N: Generate individual analyses
                            for i, lens_name in enumerate(selected_lenses):
                                if not continue_execution:
                                    break
                                    
                                st.subheader(f"Step {i+1}/{total_steps}: Analyzing ({lens_name})")
                                analysis_text = generate_analysis(
                                    model,
                                    lens_name,
                                    work_a
                                )
                                if analysis_text:
                                    analyses_results[lens_name] = analysis_text
                                else:
                                    st.error(f"Failed to generate analysis for {lens_name}. Halting execution.")
                                    continue_execution = False

                            # Step N+1: Synthesis
                            if continue_execution:
                                st.subheader(f"Step {total_steps}/{total_steps}: Symposium Synthesis")
                                with st.spinner("Synthesizing the symposium dialogue..."):
                                    symposium_text = generate_symposium_synthesis(
                                        model,
                                        analyses_results,
                                        work_a.get_display_title()
                                    )

                                if symposium_text:
                                    st.header("Symposium Dialogue Result")
                                    st.markdown(symposium_text)

                                    # Display the raw analyses for reference
                                    st.markdown("---")
                                    st.subheader("Source Analyses (Reference)")
                                    for lens_name, analysis_text in analyses_results.items():
                                        with st.expander(f"View Raw Analysis: {lens_name}"):
                                            st.markdown(analysis_text)

                        # --- Mode 4: Comparative Synthesis Execution ---
                        elif st.session_state.analysis_mode == A_COMPARATIVE:
                            lens_name = st.session_state.selection

                            # Call 1: Analyze Work A
                            st.subheader(f"Step 1/3: Analyzing Work A")
                            # The General will tailor the prompt specifically to Work A
                            analysis_a = generate_analysis(
                                model,
                                lens_name,
                                work_a
                            )

                            # Call 2: Analyze Work B
                            analysis_b = None
                            if analysis_a:
                                st.subheader(f"Step 2/3: Analyzing Work B")
                                # The General must be called again to tailor the prompt specifically to Work B
                                analysis_b = generate_analysis(
                                    model,
                                    lens_name,
                                    work_b
                                )

                            # Call 3: Comparative Synthesis
                            if analysis_a and analysis_b:
                                st.subheader("Step 3/3: Comparative Synthesis")
                                with st.spinner("Generating comparative synthesis..."):
                                    synthesis_text = generate_comparative_synthesis(
                                        model,
                                        lens_name,
                                        analysis_a,
                                        work_a.get_display_title(),
                                        analysis_b,
                                        work_b.get_display_title()
                                    )

                                if synthesis_text:
                                    st.header("Comparative Synthesis Result")
                                    st.markdown(synthesis_text)

                                    # Display the raw analyses for reference
                                    st.markdown("---")
                                    st.subheader("Source Analyses (Reference)")
                                    with st.expander(f"View Raw Analysis A: {work_a.get_display_title()}"):
                                        st.markdown(analysis_a)
                                    with st.expander(f"View Raw Analysis B: {work_b.get_display_title()}"):
                                        st.markdown(analysis_b)
                            else:
                                st.error("Could not generate the initial analyses. Cannot proceed to comparison.")
