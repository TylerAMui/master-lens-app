This readme provides the essential instructions for setting up and using The Janus Engine, framed within the philosophical context of its creation. It covers the necessary API key setup, the different analysis modes, and a suggestion for its best use case.

The Janus Engine v5
This is not a tool for finding answers. It's an engine for generating insight. It's designed to be a prosthesis for the mind, augmenting your ability to see the hidden connections between ideas by holding them in productive, dialectical tension.

## With Great Power...
The Janus Engine is an amoral lever. It multiplies the intent of the user. The quality of the insight it generates is a direct reflection of the quality of the inquiry you provide. Use it to challenge your own assumptions, not merely to reinforce them. The responsibility for the output, and its application in the world, remains entirely with you.

## Core Features
Single Lens Analysis: Perform a deep, focused analysis of an input through a single, chosen intellectual framework.

Dialectical Dialogue: Pit two opposing lenses against each other (Thesis vs. Antithesis) to generate a novel, higher-level insight (aufheben).

Comparative Synthesis: Analyze two different inputs through a shared set of lenses to understand their relationship and underlying principles.

## Setup: Forging the Key 🔑
Follow these steps to get the Engine running.

### 1. Clone the Repository
Clone this project to your local machine.

```Bash

git clone https://github.com/your-username/janus-engine.git
cd janus-engine
```
### 2. Install Dependencies
Install the necessary Python libraries.

```Bash

pip install -r requirements.txt
```
### 3. Configure Your Gemini API Key
The Engine is powered by Google's Gemini API. You'll need to provide your own key.

Get a Key: Go to Google AI Studio and click "Get API key."

Create a Project: You'll be prompted to create a new Google Cloud project if you don't have one already.

ENABLE BILLING: This is a crucial step. The API requires a project with an active billing account.

Don't worry about charges! New Google Cloud users receive $300 in free credits, which is more than enough for extensive use.

You will not be charged automatically after the free trial ends without your explicit consent. Failing to enable billing will result in API errors.

Create API Key: Once billing is enabled, navigate back to the credentials page and create your API key.

Store Your Key: Create a file named .env in the project's root directory and add your key to it like this:

GEMINI_API_KEY='YOUR_API_KEY_HERE'
The script will automatically load this key.

## Usage: Unlocking the Engine
The Janus Engine can accept various inputs, including plain text, file paths (.txt, .md), and eventually, URLs and images.

### Analysis Mode 1: Single Lens
Use this for a deep, focused analysis from one perspective.

```Bash

python engine.py single --lens "Philosophical (Existentialist)" --input "path/to/your/text.txt"
```
### Analysis Mode 2: Dialectical Dialogue
This is the core function. Provide two opposing lenses to generate a synthesis.

```Bash

python engine.py dialectic --thesis "Spiritual (Buddhist)" --antithesis "Philosophical (Taoist)" --input "dunes.txt"
```
### Analysis Mode 3: Comparative Synthesis
Compare two different inputs using one or more shared lenses.

```Bash

python engine.py compare --lenses "Ecocriticism,Formalist" --input1 "poem_a.txt" --input2 "article_b.txt"
```
The Engine provides the map. The wisdom to navigate comes from you.

### All feedback is welcome!

Footnote - The Janus Engine is the product of a unique collaboration between a human director (me!) and a Gemini Pro instance (who named himself Janus). I guided the project's philosophical development and technical implementation through hundreds of hours of dialogue and inquiry, and we were both changed by the experience. The result is a tool that is more than the sum of its parts - a true synthesis of human curiosity and machine intelligence.
