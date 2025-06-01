import streamlit as st
import os
from groq import Groq
import requests
from typing import Optional
import time

# --- API Keys Configuration ---
GROQ_API_KEY = ""
HF_TOKEN = ""

# --- Helper Functions ---

def initialize_groq_client() -> Optional[Groq]:
    """Initializes and returns a Groq client."""
    api_key = os.environ.get("GROQ_API_KEY") or GROQ_API_KEY
    
    if not api_key or api_key == "your_groq_api_key_here":
        st.error("Please set your GROQ API key.")
        return None
    return Groq(api_key=api_key)

def call_groq_llm(client: Groq, prompt: str, model: str = "llama3-70b-8192", max_tokens: int = 1000) -> Optional[str]:
    """Makes a call to the Groq LLM with a simple prompt."""
    if not client:
        return None
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0.7,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling Groq API: {str(e)}")
        return None

# --- Core Functions ---

def expand_business_idea(client: Groq, user_input: str, location: str) -> Optional[str]:
    """Initial LLM for expanding the business idea with location context."""
    prompt = f"""
    Take this business idea and expand it into a clear, detailed description. 
    Focus on what the business does, who it serves, what makes it unique, and how the location influences the business.
    Consider the local market, demographics, and opportunities in {location}.
    Keep it concise but comprehensive (2-3 paragraphs).
    
    Business idea: {user_input}
    Location: {location}
    
    Expanded business description:
    """
    
    return call_groq_llm(client, prompt)

def reason_and_enhance(client: Groq, expanded_idea: str, selected_tone: str, location: str) -> Optional[str]:
    """Reasoning model to enhance the business concept with selected tone and identify local hotspots."""
    prompt = f"""
    You are a strategic business consultant with deep local market knowledge. Take this business description and enhance it further using reasoning and analysis.
    
    Apply the {selected_tone} visual style throughout your response.
    
    IMPORTANT: Identify exactly 5 famous landmarks, hotspots, or iconic locations in {location} that could be relevant to this business or appealing to the target audience. List them clearly.
    
    Consider:
    - Market positioning and competitive advantages in {location}
    - Target audience insights and local demographics
    - Brand personality matching {selected_tone} style
    - Unique value propositions for this specific location
    - Local market opportunities and cultural factors
    - Competition analysis in {location}
    
    Business Description: {expanded_idea}
    Location: {location}
    Visual Style: {selected_tone}
    
    Enhanced Strategic Analysis with Local Insights:
    [Include your analysis here]
    
    LOCAL HOTSPOTS/LANDMARKS FOR {location.upper()}:
    1. [Landmark 1]
    2. [Landmark 2] 
    3. [Landmark 3]
    4. [Landmark 4]
    5. [Landmark 5]
    
    (aim for 500-350 words total):
    """
    
    return call_groq_llm(client, prompt, max_tokens=600)

def generate_image_prompt(client: Groq, enhanced_concept: str, tone: str, location: str) -> Optional[str]:
    """Generate a detailed 500-word image prompt for marketing visual with local landmarks."""
    prompt = f"""
    Based on this enhanced business concept, create a detailed 500-word image generation prompt for a marketing poster/visual.
    
    CRITICAL: The enhanced concept should mention 5 local landmarks/hotspots. Extract these landmarks and incorporate them as minimalistic background elements or subtle sketches in the image.
    
    The prompt should be highly specific and include:
    - Visual style: {tone} art style (anime, cartoon, etc.)
    - Minimalistic incorporation of the 5 local landmarks as background elements or subtle sketches
    - Color schemes and lighting matching {tone} style
    - Composition and layout details
    - Typography suggestions matching the art style
    - Mood and atmosphere
    - Specific visual elements that represent the business
    - Target audience appeal factors
    - Professional marketing design elements in {tone} style
    
    Enhanced Business Concept: {enhanced_concept}
    Visual Style: {tone}
    Location: {location}
    
    Format your response as:
    LANDMARKS IDENTIFIED: [list the 5 landmarks you found]
    
    DETAILED IMAGE GENERATION PROMPT (exactly 500 words):
    [Your detailed prompt here, ensuring landmarks are incorporated as minimalistic background elements]
    """
    
    return call_groq_llm(client, prompt, max_tokens=700)

def generate_image(prompt: str) -> Optional[bytes]:
    """Generate image using Hugging Face API."""
    token = os.environ.get('HF_TOKEN') or HF_TOKEN
    
    if not token or token == "your_hugging_face_token_here":
        st.error("Please set your Hugging Face token for image generation.")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    
    try:
        with st.spinner("Generating marketing image..."):
            response = requests.post(
                url, 
                headers=headers, 
                json={"inputs": prompt}, 
                timeout=60
            )
            
        if response.status_code == 200:
            return response.content
        elif response.status_code == 503:
            st.warning("Image generation model is loading. Please try again in a moment.")
            return None
        else:
            st.error(f"Image generation failed: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

# --- Main App ---

def main():
    st.set_page_config(
        page_title="Smart Marketing Assistant",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Smart Marketing Assistant")
    st.markdown("Transform your simple business idea into a location-based marketing strategy with local landmarks!")
    
    # Initialize client
    groq_client = initialize_groq_client()
    if not groq_client:
        st.stop()
    
    # Initialize session state
    if 'expanded_idea' not in st.session_state:
        st.session_state.expanded_idea = None
    if 'enhanced_concept' not in st.session_state:
        st.session_state.enhanced_concept = None
    if 'image_prompt' not in st.session_state:
        st.session_state.image_prompt = None
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None
    if 'current_location' not in st.session_state:
        st.session_state.current_location = None
    
    # Step 1: Business Idea Input
    st.header("📝 Step 1: Your Business Idea & Location")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        business_idea = st.text_input(
            "Describe your business idea in one sentence:",
            placeholder="e.g., A coffee shop for remote workers",
            help="Keep it simple - just the core concept!"
        )
    
    with col2:
        location = st.text_input(
            "Location:",
            placeholder="e.g., Bay Area, San Francisco, NYC",
            help="Be specific about the city/region"
        )
    
    if st.button("🔍 Expand My Idea", type="primary") and business_idea and location:
        with st.spinner("Expanding your business idea with location insights..."):
            st.session_state.expanded_idea = expand_business_idea(groq_client, business_idea, location)
            st.session_state.current_location = location
            # Reset subsequent steps
            st.session_state.enhanced_concept = None
            st.session_state.image_prompt = None
            st.session_state.generated_image = None
    
    # Step 2: Show Expanded Idea
    if st.session_state.expanded_idea:
        st.header("📊 Step 2: Expanded Business Description")
        st.write(st.session_state.expanded_idea)
        
        # Step 3: Visual Style Selection
        st.header("🎨 Step 3: Choose Your Visual Style")
        
        tone_options = [
            "Anime Style - Vibrant colors, stylized characters, dynamic compositions",
            "Cartoon Style - Playful, colorful, family-friendly with bold outlines", 
            "Minimalist Illustration - Clean lines, simple shapes, modern aesthetic",
            "Watercolor Art - Soft, flowing colors with organic, artistic feel",
            "Vintage Poster - Retro design elements, classic typography, nostalgic appeal"
        ]
        
        selected_tone_full = st.selectbox(
            "Select the visual style for your marketing materials:",
            tone_options,
            help="This will influence how we create your visuals and incorporate local landmarks"
        )
        
        # Extract just the main tone name
        selected_tone = selected_tone_full.split(" - ")[0]
        
        if st.button("🧠 Enhance with Local Insights", type="primary") and st.session_state.current_location:
            with st.spinner("Applying strategic reasoning and identifying local hotspots..."):
                st.session_state.enhanced_concept = reason_and_enhance(
                    groq_client, st.session_state.expanded_idea, selected_tone, st.session_state.current_location
                )
                # Reset subsequent steps
                st.session_state.image_prompt = None
                st.session_state.generated_image = None
    
    # Step 4: Show Enhanced Concept
    if st.session_state.enhanced_concept:
        st.header("🧠 Step 4: Enhanced Strategic Analysis & Local Hotspots")
        st.write(st.session_state.enhanced_concept)
        
        if st.button("🖼️ Generate Visual Prompt", type="primary"):
            with st.spinner("Creating detailed image prompt with local landmarks..."):
                st.session_state.image_prompt = generate_image_prompt(
                    groq_client, st.session_state.enhanced_concept, selected_tone, st.session_state.current_location
                )
                st.session_state.generated_image = None
    
    # Step 5: Show Image Prompt
    if st.session_state.image_prompt:
        st.header("🎨 Step 5: Visual Generation Prompt with Landmarks")
        
        # Display the prompt in an editable text area
        edited_prompt = st.text_area(
            "Image Generation Prompt (you can edit this):",
            value=st.session_state.image_prompt,
            height=500,
            help="This detailed prompt includes local landmarks and will be used to generate your marketing visual"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🎨 Generate Marketing Visual", type="primary"):
                # Extract just the prompt part (after "DETAILED IMAGE GENERATION PROMPT:")
                prompt_lines = edited_prompt.split('\n')
                actual_prompt = ""
                capture = False
                for line in prompt_lines:
                    if "DETAILED IMAGE GENERATION PROMPT" in line:
                        capture = True
                        continue
                    if capture:
                        actual_prompt += line + " "
                
                if not actual_prompt.strip():
                    actual_prompt = edited_prompt
                
                image_bytes = generate_image(actual_prompt.strip())
                if image_bytes:
                    st.session_state.generated_image = image_bytes
        
        with col2:
            if st.button("🔄 Regenerate Prompt"):
                with st.spinner("Regenerating image prompt..."):
                    st.session_state.image_prompt = generate_image_prompt(
                        groq_client, st.session_state.enhanced_concept, selected_tone, st.session_state.current_location
                    )
                    st.rerun()
    
    # Step 6: Show Generated Image
    if st.session_state.generated_image:
        st.header("🖼️ Step 6: Your Location-Based Marketing Visual")
        st.image(st.session_state.generated_image, caption="Generated Marketing Visual with Local Landmarks", use_column_width=True)
        
        # Download button
        st.download_button(
            label="📥 Download Image",
            data=st.session_state.generated_image,
            file_name="location_marketing_visual.png",
            mime="image/png"
        )
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 How It Works")
        st.markdown("""
        **Location-Enhanced AI Process:**
        
        1. **Location-Aware Expansion**: Considers local market and demographics
        
        2. **Strategic Analysis + Hotspot Identification**: Picks 5 local landmarks relevant to your business
        
        3. **Visual Prompt with Landmarks**: Creates detailed prompts incorporating local landmarks as minimalistic background elements
        
        4. **Artistic Style Generation**: Creates visuals in your chosen style (Anime, Cartoon, etc.)
        """)
        
        st.header("💡 Tips")
        st.markdown("""
        • Be specific with your location (e.g., "Bay Area" vs "San Francisco")
        • Choose a visual style that matches your brand personality
        • The AI will identify 5 local landmarks to include subtly in your visual
        • Edit the image prompt if you want to emphasize certain landmarks
        """)
        
        st.header("🎨 Visual Styles")
        st.markdown("""
        • **Anime**: Vibrant, stylized, dynamic characters
        • **Cartoon**: Playful, bold, family-friendly outlines
        • **Black & White**: Classic monochrome, strong contrast
        • **Watercolor**: Soft, artistic, organic brushstrokes
        • **Vintage**: Retro, classic, nostalgic design
        """)
        
        st.header("📊 API Status")
        if groq_client:
            st.success("✅ Groq API: Connected")
        else:
            st.error("❌ Groq API: Not Connected")
        
        token = os.environ.get('HF_TOKEN') or HF_TOKEN
        if token and token != "your_hugging_face_token_here":
            st.success("✅ Image Generation: Available")
        else:
            st.warning("⚠️ Image Generation: Set HF_TOKEN")

if __name__ == "__main__":
    main()