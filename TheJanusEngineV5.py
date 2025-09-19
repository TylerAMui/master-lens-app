# The Janus Engine v5.0 (The Comparative Synthesis)
import streamlit as st
import google.generativeai as genai
import textwrap
import PIL.Image
import io
import mimetypes
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="The Janus Engine v5.0",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ The Janus Engine v5.0")
st.write("A multi-modal (Text, Image, Audio), AI-powered analytical platform for deep comparison, dialectical dialogue, and isolated analysis across diverse frameworks.")

# --- CONSTANTS ---

# Constants for Modalities
M_TEXT = "Text Analysis"
M_IMAGE = "Image Analysis"
M_AUDIO = "Audio Analysis"
MODALITIES = (M_TEXT, M_IMAGE, M_AUDIO)

# Constants for Analysis Modes
A_SINGLE = "Single Lens"
A_DIALECTICAL = "Dialectical Dialogue"
A_COMPARATIVE = "Comparative Synthesis"
ANALYSIS_MODES = (A_SINGLE, A_DIALECTICAL, A_COMPARATIVE)

# --- PROMPT DEFINITIONS (LENSES v5) ---

# Directive 1: Expanded Analytical Dial
LENSES_HIERARCHY = {
    "Structural & Formalist": {
        "description": "A formalist analysis focusing purely on craft, composition, technique, and structure.",
        "prompt": """
Analyze the following creative work from a strictly formalist perspective. Disregard external context, biography, or social implications. Your analysis should focus entirely on the internal structure and aesthetic components.

- Analyze elements such as composition, color, line, medium, structure, meter, rhyme scheme, word choice, sound structure, instrumentation, or editing techniques.
- Explain how these formal elements work together to create the piece's overall aesthetic effect.
"""
    },
    "Psychological": {
        "description": "An inquiry into the work's emotional, symbolic, and behavioral currents.",
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
""",
            "Behaviorism": """
Analyze the following creative work through the lens of Behaviorism.
- Focus strictly on observable behaviors, actions, and interactions depicted or elicited by the work.
- Discuss potential conditioning (classical or operant), reinforcement schedules, and environmental determinants of behavior.
- Analyze how the work itself acts as a stimulus. Explicitly avoid speculation on internal mental states.
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
""",
            "Stoicism": """
Analyze the following creative work through a Stoic lens.
- Examine the themes of virtue, reason, and the dichotomy of control (what is and is not within our power).
- Discuss how the work addresses fate, adversity, and the pursuit of emotional tranquility (apatheia).
- Explore any representations of living in accordance with nature.
""",
            "Platonism": """
Analyze the following creative work through a Platonic lens.
- Explore the distinction between appearance (the physical/sensory world) and reality (the realm of Forms or Ideals).
- Discuss how the work might be interpreted in relation to the Allegory of the Cave.
- Examine the role of beauty, truth, and the good, and the ascent of the soul towards higher understanding.
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
    "Ethical Frameworks": {
        "description": "An evaluation of the moral implications and ethical questions raised by the work.",
        "sub_lenses": {
            "Utilitarianism": """
Analyze the following creative work using a Utilitarian ethical framework.
- Evaluate the actions, decisions, or themes within the work based on their consequences.
- Apply the principle of the 'greatest good for the greatest number'.
- Discuss the calculation of pleasure vs. pain (hedonic calculus) and whether the work promotes overall utility or happiness.
""",
            "Virtue Ethics": """
Analyze the following creative work through the lens of Virtue Ethics (primarily Aristotelian).
- Focus on the character, virtues, and vices depicted or embodied in the work.
- Discuss how the work explores the concept of 'eudaimonia' (human flourishing) and the development of moral character.
- Evaluate whether the work provides moral exemplars or cautionary tales regarding the cultivation of virtue.
"""
        }
    },
    "Scientific Perspectives": {
        "description": "Applying concepts from natural and social sciences to interpret the work.",
        "sub_lenses": {
            "Cognitive Science": """
Analyze the following creative work through the lens of Cognitive Science.
- Explore how the work engages human mental processes, including perception, attention, memory, and decision-making.
- Discuss the use of conceptual metaphors, cognitive biases, or narrative structures that resonate with how the mind processes information.
- Analyze the work's impact on the audience's cognitive and emotional state.
""",
            "Systems Theory": """
Analyze the following creative work using Systems Theory (Complexity Theory).
- Examine the work as a complex system of interconnected parts.
- Identify feedback loops, emergent properties, boundaries, and the interaction between the system and its environment.
- Discuss how elements within the narrative, visual composition, or sound design interact to create complexity and meaning that is greater than the sum of its parts.
""",
            "Ecocriticism": """
Analyze the following creative work through the lens of Ecocriticism.
- Examine the relationship between the work and the natural environment.
- Discuss how nature/the environment is represented (e.g., as background, antagonist, sanctuary).
- Explore themes of environmental ethics, sustainability, the human impact on the planet, and the portrayal of non-human life.
"""
        }
    },
    "Spiritual & Esoteric Beliefs": {
        "description": "Interpreting the work through the lens of specific spiritual traditions or hidden knowledge.",
        "sub_lenses": {
            "Buddhist": """
Analyze the following creative work through a Buddhist philosophical lens.
- Explore themes related to the Four Noble Truths and the nature of suffering (dukkha).
- Discuss concepts of impermanence (anicca), non-self (anatta), dependent origination, and karma.
- Analyze how the work might relate to the path towards enlightenment or liberation.
""",
            "Western Esotericism": """
Analyze the following creative work through the lens of Western Esotericism.
- Look for influences or symbolism derived from traditions such as Hermeticism, Alchemy, Kabbalah, Gnosticism, or Neoplatonism.
- Discuss the concept of correspondences ('as above, so below'), the search for hidden knowledge (gnosis), and themes of initiation or transformation.
- Interpret symbolic language and imagery that may have esoteric meaning.
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
    "Comparative (General)": {
        "description": "Places the work in conversation with other similar artists and movements. (To compare two specific works, use 'Comparative Synthesis' mode).",
        "prompt": """
Analyze the following creative work using a comparative lens.
- Identify the key themes, styles, and aesthetic choices in the piece.
- Compare and contrast this work with other similar artists, movements, or genres.
- Discuss where this work fits within its broader artistic or literary tradition.
"""
    }
}

# --- DATA STRUCTURES ---

# Directive 2 & 3: Input Handling Structure
class WorkInput:
    """A class to hold the data and metadata for a creative work."""
    def __init__(self, title="", modality=M_TEXT, data=None, uploaded_file_obj=None):
        self.title = title
        self.modality = modality
        self.data = data # Holds text string or raw bytes (for preview/fallback)
        self.uploaded_file_obj = uploaded_file_obj # Holds the Streamlit UploadedFile object

    def is_ready(self):
        # Check if we have data (for text) or a file object ready to process (for media)
        if self.modality == M_TEXT:
            return self.data is not None and len(self.data) > 0
        else:
            return self.uploaded_file_obj is not None

    def get_display_title(self):
        return self.title if self.title else "(Untitled)"

# --- HELPER FUNCTIONS ---

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

# A flattened dictionary used for prompt lookup and the selection UIs.
FLATTENED_LENSES = flatten_lenses(LENSES_HIERARCHY)
SORTED_LENS_NAMES = sorted(list(FLATTENED_LENSES.keys()))

def create_persona_name(lens_name):
    """Creates a suitable persona title from a lens name."""
    # Extract the core term
    if "(" in lens_name:
        name = lens_name.split("(")[1].replace(")", "")
    else:
        name = lens_name

    # Specific formatting tweaks for natural sounding titles
    if name == "Structural & Formalist": return "The Formalist"
    if name == "Historical & Biographical": return "The Historian"
    if name == "Comparative" or name == "General": return "The Comparativist"
    if name in ["Jungian", "Freudian"]: return f"The {name} Analyst"
    if name == "Evolutionary Psychology": return "The Evolutionary Psychologist"
    if name == "Behaviorism": return "The Behaviorist"
    if name in ["Marxist", "Feminist"]: return f"The {name} Critic"
    
    if name in ["Existentialist", "Taoist", "Phenomenological"]:
        return f"The {name} Philosopher"
    if name == "Stoicism": return "The Stoic Philosopher"
    if name == "Platonism": return "The Platonic Philosopher"

    if name in ["Utilitarianism", "Virtue Ethics"]:
        return f"The {name.replace('ism', '')} Ethicist"
        
    if name == "Cognitive Science": return "The Cognitive Scientist"
    if name == "Systems Theory": return "The Systems Theorist"
    if name == "Ecocriticism": return "The Ecocritic"
    if name == "Buddhist": return "The Buddhist Scholar"
    if name == "Western Esotericism": return "The Esotericist"
    
    if "Theory" in name or name == "Post-Colonial":
        return f"The {name.replace(' Theory', '')} Theorist"
    
    # Fallback
    return f"The {name} Scholar"

def get_model(api_key):
    """Configures and returns the Gemini model."""
    try:
        genai.configure(api_key=api_key)
        # Using Gemini 1.5 Pro for complex reasoning, multi-modal input, and audio capabilities
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        return model
    except Exception as e:
        st.error(f"Failed to initialize Gemini API. Please ensure your API Key is correct. Error: {e}")
        return None

# --- CORE GENERATION FUNCTIONS ---

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
        # 2. Prepare File Object
        # Get bytes from the Streamlit UploadedFile object
        file_bytes = work_input.uploaded_file_obj.getvalue()
        # Create a file-like object for the SDK
        file_like_object = io.BytesIO(file_bytes)

        # 3. Upload the file
        display_name = work_input.get_display_title()[:128]
        status_container.write(f"Uploading '{display_name}' to Gemini...")
        
        uploaded_file = genai.upload_file(
            path=file_like_object,
            display_name=display_name,
            mime_type=mime_type
        )

        # 4. Poll for Processing (Crucial for Audio/Video)
        status_container.write(f"File uploaded. Waiting for processing (URI: {uploaded_file.uri})...")
        
        start_time = time.time()
        POLL_INTERVAL = 3
        TIMEOUT = 300 # 5 minutes

        while uploaded_file.state.name == "PROCESSING":
            if time.time() - start_time > TIMEOUT:
                raise TimeoutError("File processing timed out.")
            
            time.sleep(POLL_INTERVAL)
            # Refresh the file object to get the new state
            uploaded_file = genai.get_file(uploaded_file.name)
            status_container.write(f"Current state: {uploaded_file.state.name}...")

        # 5. Final State Check
        if uploaded_file.state.name == "FAILED":
            st.error(f"File processing failed: {uploaded_file.state}")
            return None
        
        if uploaded_file.state.name == "ACTIVE":
            status_container.write("File processed successfully.")
            return uploaded_file

        st.error(f"File upload resulted in unexpected state: {uploaded_file.state.name}")
        return None

    except TimeoutError:
        st.error("File upload timed out. The file may be too large or the servers are busy.")
        return None
    except Exception as e:
        st.error(f"An error occurred during file upload to Gemini: {e}")
        return None


def generate_analysis(model, prompt_key, work_input: WorkInput):
    """Handles a single API call for analysis (Text, Image, or Audio)."""
    base_prompt = FLATTENED_LENSES[prompt_key]
    content_input = []
    gemini_file = None
    final_prompt = ""

    # Use st.status for managing uploads and generation feedback
    status_text = f"Analyzing '{work_input.get_display_title()}'..."
    with st.status(status_text, expanded=True) as status:
        try:
            if work_input.modality == M_TEXT:
                # Standard text prompt format
                final_prompt = f"{base_prompt}\n\nThe work is as follows:\n---\nTitle: {work_input.get_display_title()}\n\nWork:\n{work_input.data}"
                content_input = [final_prompt]

            elif work_input.modality == M_IMAGE:
                # Multi-modal image prompt format
                image_instruction = """
Important: You are analyzing a visual artwork (the attached image).
1. First, provide a detailed, objective description of the image (composition, colors, subjects, textures).
2. Then, apply the requested analytical lens to the visual evidence. Ensure your analysis refers directly to what is visible in the image.
"""
                final_prompt = f"{image_instruction}\n\n{base_prompt}\n\nTitle: {work_input.get_display_title()}"

                # Use the File API for robustness
                gemini_file = upload_to_gemini(work_input, status)
                if gemini_file:
                    content_input = [final_prompt, gemini_file]
                else:
                    status.update(label="Analysis failed due to upload error.", state="error")
                    return None

            elif work_input.modality == M_AUDIO:
                # Directive 2: Multi-modal audio prompt format
                audio_instruction = """
Important: You are analyzing an audio work (the attached file).
1. First, provide a detailed, objective description of the audio.
   - If music: Analyze instrumentation, tempo, dynamics, structure, mood, and lyrics (if present).
   - If speech: Provide a summary or analysis of the content, and analyze tone, pacing, and rhetorical devices.
   - If soundscape: Describe the sonic environment, sound sources, and atmosphere.
2. Then, apply the requested analytical lens to the audio evidence. Ensure your analysis refers directly to what is audible in the file.
"""
                final_prompt = f"{audio_instruction}\n\n{base_prompt}\n\nTitle: {work_input.get_display_title()}"

                # Upload the audio file using File API
                gemini_file = upload_to_gemini(work_input, status)
                if gemini_file:
                    content_input = [final_prompt, gemini_file]
                else:
                    status.update(label="Analysis failed due to upload error.", state="error")
                    return None

            # Execute the generation request
            status.write("Generating analysis...")
            # Set a reasonable timeout for generation
            response = model.generate_content(content_input, request_options={"timeout": 600})
            status.update(label="Analysis complete!", state="complete")
            return response.text

        except Exception as e:
            st.error(f"An error occurred during analysis generation: {e}")
            status.update(label="Analysis failed.", state="error")
            # Attempt to retrieve feedback if generation failed (e.g., safety block)
            try:
                if hasattr(e, 'response') and e.response.prompt_feedback:
                    st.warning(f"Generation blocked. Feedback: {e.response.prompt_feedback}")
            except:
                pass
            return None
        finally:
            # Clean up the uploaded file from Gemini servers
            if gemini_file:
                try:
                    genai.delete_file(gemini_file.name)
                    print(f"Cleaned up Gemini file: {gemini_file.name}")
                except Exception as e:
                    print(f"Failed to delete Gemini file: {e}")


def generate_dialectical_synthesis(model, lens_a_name, analysis_a, lens_b_name, analysis_b, work_title):
    """Synthesizes two analyses of the SAME work into a dialectical dialogue."""

    # Generate personas programmatically
    persona_a = create_persona_name(lens_a_name)
    persona_b = create_persona_name(lens_b_name)

    # The Synthesis Prompt
    synthesis_prompt = textwrap.dedent(f"""
    You are tasked with creating a "Dialectical Dialogue" regarding the creative work titled "{work_title}". This dialogue must synthesize two distinct analytical perspectives that have already been generated on this single work.

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
        response = model.generate_content(synthesis_prompt, request_options={"timeout": 600})
        return response.text
    except Exception as e:
        st.error(f"An error occurred during dialectical synthesis: {e}")
        return None

# Directive 3: New Comparative Synthesis Function
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

# --- SIDEBAR FOR SETUP & PROTOCOL SELECTION ---

with st.sidebar:
    st.header("🔑 Setup")
    api_key = st.text_input("Enter your Gemini API Key", type="password")

    st.header("🔄 Analytical Protocol")
    # Directive 3: Include Comparative Synthesis Mode
    analysis_mode = st.radio("Select Analysis Mode:", ANALYSIS_MODES)
    st.session_state.analysis_mode = analysis_mode

    # Directive 4: Context-Dependent Information
    if analysis_mode in [A_SINGLE, A_DIALECTICAL]:
        st.info("Analyze ONE creative work. Modality is selected in the main area.")
    elif analysis_mode == A_COMPARATIVE:
        st.info("Analyze TWO different creative works. Modalities are selected in the main area.")

    st.markdown("---")
    st.subheader("🔬 Lens Selection")

    # Directive 4: Refined UI for lens selection across modes
    if analysis_mode == A_SINGLE or analysis_mode == A_COMPARATIVE:
        # Hierarchical selection for modes requiring a single lens

        if analysis_mode == A_COMPARATIVE:
            st.caption("Select the common lens for comparison.")

        main_lens = st.selectbox(
            "1. Category:",
            options=sorted(list(LENSES_HIERARCHY.keys())),
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

    elif analysis_mode == A_DIALECTICAL:
        # Multi-select for dialectical dialogue (using the pre-flattened list)
        st.caption("Select two lenses to synthesize.")
        
        selected_lenses = st.multiselect(
            "Select exactly two lenses:",
            options=SORTED_LENS_NAMES,
            max_selections=2,
            placeholder="Choose lenses..."
        )
        # Store the list of selections
        st.session_state.selection = selected_lenses


# --- MAIN PAGE LOGIC & DISPLAY ---

# Determine if we are ready to display the analysis form
display_analysis_form = False
header_text = ""
# Initialize WorkInput objects
work_a = WorkInput()
work_b = WorkInput() # Only used in Comparative mode

# --- MODE-SPECIFIC LOGIC & UI SETUP ---

if st.session_state.analysis_mode == A_SINGLE:
    selection = st.session_state.selection
    header_text = f"{A_SINGLE}"

    if selection:
        display_analysis_form = True
        header_text += f" | {selection}"

        # Display description if available
        if "(" in selection:
            main_lens = selection.split(" (")[0]
        else:
            main_lens = selection

        description = LENSES_HIERARCHY.get(main_lens, {}).get("description", "")
        st.info(f"**{main_lens}**: {description}")

    else:
        st.info("⬅️ Please select an analytical category and specific lens (if applicable) from the sidebar to begin.")

elif st.session_state.analysis_mode == A_DIALECTICAL:
    selection = st.session_state.selection
    header_text = f"{A_DIALECTICAL}"

    if selection and len(selection) == 2:
        display_analysis_form = True
        header_text += f" | {selection[0]} vs. {selection[1]}"
        st.info("Ready to synthesize these two distinct viewpoints on a single work.")
    elif selection and len(selection) != 2:
         st.warning("⬅️ Please select exactly two lenses in the sidebar.")
    else:
        st.info("⬅️ Please select two lenses from the sidebar.")

elif st.session_state.analysis_mode == A_COMPARATIVE:
    selection = st.session_state.selection
    header_text = f"{A_COMPARATIVE}"

    if selection:
        display_analysis_form = True
        header_text += f" | Lens: {selection}"
        st.info(f"Ready to compare two different works through the {selection} lens.")
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
            uploaded_file = st.file_uploader("Upload Image (JPG, PNG, WEBP):", type=["jpg", "jpeg", "png", "webp"], key=f"{ui_key_prefix}_image")
            if uploaded_file is not None:
                try:
                    # Store the UploadedFile object (needed for File API)
                    work_input.uploaded_file_obj = uploaded_file
                    
                    # Read bytes for preview
                    image_bytes = uploaded_file.getvalue()
                    work_input.data = image_bytes # Store bytes for preview source

                    # Display the image preview
                    image = PIL.Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption="Preview", use_column_width=True)

                except Exception as e:
                    st.error(f"Error processing image: {e}")
                    work_input.uploaded_file_obj = None

        elif work_input.modality == M_AUDIO:
            # Directive 2: Audio Input Handling
            uploaded_file = st.file_uploader("Upload Audio (MP3, WAV, FLAC, M4A, OGG):", type=["mp3", "wav", "flac", "m4a", "ogg"], key=f"{ui_key_prefix}_audio")
            if uploaded_file is not None:
                # Store the UploadedFile object (needed for File API)
                work_input.uploaded_file_obj = uploaded_file

                # Read bytes for the audio player
                audio_bytes = uploaded_file.getvalue()
                work_input.data = audio_bytes
                
                # Display audio player
                st.audio(audio_bytes)


if display_analysis_form:
    st.header(header_text)

    if st.session_state.analysis_mode in [A_SINGLE, A_DIALECTICAL]:
        # Single Input UI
        st.subheader("Input Work")
        handle_input_ui(work_a, st.container(border=True), "work_single")

    elif st.session_state.analysis_mode == A_COMPARATIVE:
        # Directive 3: Dual Input UI
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
    if st.button("Execute Analysis Engine", type="primary", use_container_width=True):
        # Validation
        is_valid = True
        if not api_key:
            st.warning("Please enter your Gemini API Key in the sidebar.")
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

                # --- Mode 1: Single Lens Execution ---
                if st.session_state.analysis_mode == A_SINGLE:
                    # The selection is the prompt key
                    prompt_key = st.session_state.selection
                    
                    # Analysis generation function handles its own status/spinner
                    analysis_text = generate_analysis(
                        model,
                        prompt_key,
                        work_a
                    )

                    if analysis_text:
                        st.header("Analysis Result")
                        st.markdown(analysis_text)

                # --- Mode 2: Dialectical Dialogue Execution ---
                elif st.session_state.analysis_mode == A_DIALECTICAL:
                    # Selections are stored as a list of 2
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

                # --- Mode 3: Comparative Synthesis Execution ---
                elif st.session_state.analysis_mode == A_COMPARATIVE:
                     # Selection is the single lens name
                    lens_name = st.session_state.selection

                    # Call 1: Analyze Work A
                    st.subheader(f"Step 1/3: Analyzing Work A")
                    analysis_a = generate_analysis(
                        model,
                        lens_name,
                        work_a
                    )

                    # Call 2: Analyze Work B
                    analysis_b = None
                    if analysis_a:
                        st.subheader(f"Step 2/3: Analyzing Work B")
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
