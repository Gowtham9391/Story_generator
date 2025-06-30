import streamlit as st
import requests
from prompts import build_story_prompt

# Hugging Face API Key
HUGGINGFACE_API_KEY = "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"  # Keep secure

# Query Function
def query_huggingface_model(prompt, model="tiiuae/falcon-7b-instruct"):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }
    payload = {
        "inputs": prompt
    }

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model}",
        headers=headers,
        json=payload
    )

    print("STATUS:", response.status_code)
    print("RAW RESPONSE:", repr(response.text))

    try:
        output = response.json()

        if isinstance(output, list) and len(output) > 0:
            if "generated_text" in output[0]:
                return output[0]["generated_text"]
            elif "text" in output[0]:
                return output[0]["text"]
        elif isinstance(output, dict):
            if "generated_text" in output:
                return output["generated_text"]
            elif "error" in output:
                return f"🛑 API Error: {output['error']}"

        return "⚠️ No valid output returned from the model."
    except Exception as e:
        return f"❌ Error decoding response: {e}"

# Streamlit App Config
st.set_page_config(page_title="AI Story Generator for Kids")
st.title("📚 AI Story Generator for Kids")

# Inputs
age = st.selectbox("Select age group", ["3-5", "6-8", "9-12"])
character = st.text_input("Main Character", "a brave bunny")
setting = st.selectbox("Choose the setting", ["magical forest", "space station", "underwater world", "desert", "castle"])
genre = st.selectbox("Story Genre", ["Adventure", "Fantasy", "Fairy Tale", "Moral Story"])
moral = st.text_input("Moral of the Story", "kindness")

# Generate Button
if st.button("Generate Story"):
    with st.spinner("Crafting your story..."):
        prompt = build_story_prompt(age, character, setting, genre, moral)
        story = query_huggingface_model(prompt).strip()

        st.subheader("🧚 Your Story")
        st.write(story)

        if not story.lower().startswith(("error", "api error", "❌", "🛑")):
            st.download_button("📥 Download Story", story, file_name="ai_story.txt")
