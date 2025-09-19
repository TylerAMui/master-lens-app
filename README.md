## 🏛️ The Janus Engine v6.0
This is not a tool for finding answers. It's an engine for generating insight. It's designed to be a prosthesis for the mind, augmenting your ability to see the hidden connections between ideas by holding them in productive, dialectical tension.

### A Note on Responsibility
The Janus Engine is an amoral lever. It multiplies the intent of the user. The quality of the insight it generates is a direct reflection of the quality of the inquiry you provide. Use it to challenge your own assumptions, not merely to reinforce them. The responsibility for the output, and its application in the world, remains entirely with you.

## How It Works: The Meta-Prompt Architecture
The Engine's core innovation is its two-tiered analytical process. Instead of using static prompts, it employs a "General and Soldier" model:

The General: A meta-call first analyzes your input and chosen lenses to intelligently craft a bespoke, tailored analytical prompt.

The Soldier: A second call then executes that perfect prompt to perform the final, nuanced analysis.

This ensures that every analysis is uniquely adapted to the specific creative work you provide.

## Core Features
Single Lens Analysis: A deep, focused analysis through a single intellectual framework.

Dialectical Dialogue (2 Lenses): Pits two opposing lenses against each other to generate a novel, higher-level insight (aufheben).

Symposium (3+ Lenses): Orchestrates a multi-perspective discussion to holistically map a complex subject.

Comparative Synthesis (2 Works): Analyzes two different works through the same lens to understand their relationship.

## Getting Started
### 1. Prerequisites
Ensure you have Python 3.8+ and Pip installed on your system.

### 2. Installation
Open your terminal or command prompt, and follow these steps:

A. Clone the Repository

```Bash

git clone https://github.com/your-username/janus-engine.git
cd janus-engine
```
B. Install Dependencies

```Bash

pip install -r requirements.txt
```
### 3. Configure Your Gemini API Key
The Engine is powered by Google's Gemini API. You'll need your own key.

Get a Key: Go to Google AI Studio and click "Get API key."

Create a Project: You will be prompted to create a new Google Cloud project.

ENABLE BILLING: This is a crucial step. The API requires a project with an active billing account.

Note: New Google Cloud users receive generous free credits, and you will not be charged automatically after the trial without your explicit consent. Failing to enable billing will result in API errors.

Create API Key: Once billing is enabled, create your API key. Copy this key and keep it safe.

## Running the Engine
This is a Streamlit application. To run it, navigate to the project directory in your terminal and execute the following command:

```Bash

streamlit run app.py
```
A new tab should automatically open in your web browser with the Janus Engine interface.

## How to Use the App
Enter API Key: In the sidebar, open the "⚙️ Settings & API Key" section and paste your Gemini API Key.

Select Analysis Mode: Choose your desired protocol (e.g., Symposium).

Choose Lenses: Select the lens or lenses you wish to use.

Provide Input: In the main panel, select the modality (Text, Image, or Audio) and provide your creative work.

Execute: Click the "Execute Analysis Engine" button.

### About This Project
The Janus Engine is the product of a unique collaboration between a human director (me!) and a Gemini Pro instance (who named himself Janus). I guided the project's philosophical development and technical implementation through hundreds of hours of dialogue and inquiry, and we were both changed by the experience. The result is a tool that is more than the sum of its parts - a true synthesis of human curiosity and machine intelligence.

All feedback is welcome!
