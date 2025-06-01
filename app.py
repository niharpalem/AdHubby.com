import streamlit as st
import os
from openai import OpenAI
import requests
from typing import Optional
import time
from PIL import Image
from pathlib import Path

# --- API Keys Configuration ---
OPENAI_API_KEY = "fake"  # Using fake key as per your example
CUSTOM_BASE_URL = "https://reduced-ginnifer-nihar-cca6cebf.koyeb.app/v1"
HF_TOKEN = ""

def initialize_openai_client() -> Optional[OpenAI]:
    """Initializes and returns an OpenAI client with custom base URL."""
    api_key = os.environ.get("OPENAI_API_KEY") or OPENAI_API_KEY
    base_url = os.environ.get("CUSTOM_BASE_URL") or CUSTOM_BASE_URL
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        return client
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        return None

def call_custom_llm(client: OpenAI, prompt: str, model: str = "meta-llama/Llama-3.1-8B-Instruct", max_tokens: int = 1000) -> Optional[str]:
    """Makes a call to the custom LLM API."""
    if not client:
        return None
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error calling Custom LLM API: {str(e)}")
        return None

# --- Core Functions ---

def generate_marketing_briefing(client: OpenAI, business_name: str, business_type: str, location: str, selected_deliverables: list) -> Optional[str]:
    """Generate comprehensive marketing briefing based on business details and selected deliverables."""
    deliverables_text = ", ".join(selected_deliverables)
    
    prompt = f"""
    Create a comprehensive marketing briefing for this business. Structure your response with these specific sections:

    Business Details:
    - Business Name: {business_name}
    - Business Type: {business_type}
    - Location: {location}
    - Selected Marketing Deliverables: {deliverables_text}

    THE PROBLEM:
    [Identify the core market problem this business solves]

    THE FACTS:
    [Present key market data, demographics, and business facts for {location}]

    THE BIG PICTURE:
    [Describe the broader market opportunity and business vision]

    THE OBJECTIVE:
    [Define clear, measurable marketing goals for the selected deliverables: {deliverables_text}]

    THE TARGET AUDIENCE:
    [Detailed description of ideal customers, including demographics, psychographics, and behaviors]

    AI-RECOMMENDED TONE:
    [Based on the business type, location, and target audience, recommend ONE of these tones with justification:
    - Anime Style
    - Cartoon Style
    - Minimalist Illustration
    - Watercolor Art
    - Vintage Poster]

    Keep each section focused and actionable (total 400-600 words).
    """
    
    return call_custom_llm(client, prompt, max_tokens=800)

def reason_and_enhance_briefing(client: OpenAI, briefing: str, user_tone: str, location: str) -> Optional[str]:
    """Enhanced reasoning model that works with the briefing and identifies local hotspots."""
    prompt = f"""
    You are a strategic marketing consultant. Take this marketing briefing and enhance it with deeper strategic analysis.

    Apply both the user-selected tone ({user_tone}) and incorporate insights from the AI-recommended tone mentioned in the briefing.

    IMPORTANT: Identify exactly 5 famous landmarks, hotspots, or iconic locations in {location} that could be relevant to this business or appealing to the target audience. List them clearly.

    Consider:
    - Competitive landscape analysis in {location}
    - Cultural and demographic insights
    - Brand positioning strategy
    - Marketing channel optimization for selected deliverables
    - Local market opportunities
    - Visual style integration ({user_tone} + AI tone)

    Original Marketing Briefing: {briefing}
    User-Selected Visual Style: {user_tone}
    Location: {location}

    ENHANCED STRATEGIC ANALYSIS:
    [Your detailed analysis here]

    TONE SYNTHESIS:
    [How to blend user-selected {user_tone} with AI-recommended tone from briefing]

    LOCAL HOTSPOTS/LANDMARKS FOR {location.upper()}:
    1. [Landmark 1]
    2. [Landmark 2] 
    3. [Landmark 3]
    4. [Landmark 4]
    5. [Landmark 5]

    (aim for 500-700 words total)
    """
    
    return call_custom_llm(client, prompt, max_tokens=800)

def generate_deliverable_specific_prompt(client: OpenAI, enhanced_analysis: str, user_tone: str, location: str, selected_deliverables: list) -> Optional[str]:
    """Generate image prompts tailored to specific marketing deliverables."""
    deliverables_text = ", ".join(selected_deliverables)
    
    prompt = f"""
    Based on this enhanced marketing analysis, create a detailed 600-word image generation prompt optimized for these specific deliverables: {deliverables_text}

    CRITICAL REQUIREMENTS:
    1. Extract the 5 local landmarks/hotspots from the analysis
    2. Incorporate them as minimalistic background elements
    3. Tailor the visual composition for the selected deliverables: {deliverables_text}
    4. Blend user-selected tone ({user_tone}) with AI-recommended tone from the analysis

    DELIVERABLE-SPECIFIC CONSIDERATIONS:
    - Social Media Carousels: Multi-slide ready, consistent branding
    - Static Social Ads: Platform-optimized dimensions, clear CTAs
    - Billboard/Poster: High-impact, readable from distance
    - Email Newsletter: Header-friendly, brand integration
    - Print Brochure: Print-quality, professional layout
    - Website Banner: Web-optimized, hero image ready
    - Copy Deck: Text-supporting visuals
    - Press Kit: Professional, media-ready aesthetics
    - Point-of-Sale: Retail environment integration

    Enhanced Marketing Analysis: {enhanced_analysis}
    User Visual Style: {user_tone}
    Location: {location}
    Target Deliverables: {deliverables_text}

    Format your response as:
    LANDMARKS IDENTIFIED: [list the 5 landmarks]

    TONE BLEND STRATEGY: [how user tone + AI tone work together]

    DELIVERABLE OPTIMIZATION: [specific adjustments for selected deliverables]

    DETAILED IMAGE GENERATION PROMPT (exactly 600 words):
    [Your comprehensive prompt here, ensuring landmarks and deliverable-specific elements are incorporated]
    """
    
    return call_custom_llm(client, prompt, max_tokens=900)

def generate_image(prompt: str) -> Optional[bytes]:
    """Generate image using Hugging Face API."""
    token = os.environ.get('HF_TOKEN') or HF_TOKEN
    
    if not token or token == "your_hugging_face_token_here":
        st.error("Please set your Hugging Face token for image generation.")
        return None
    
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    
    try:
        with st.spinner("Generating marketing visual..."):
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
        page_title="AdHubby.com - Enhanced Marketing Assistant",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 AdHubby.com - Enhanced Marketing Assistant")
    st.markdown("Create comprehensive marketing campaigns with AI-powered briefings and location-based visuals!")
    
    # Load logo if it exists
    logo_path = "/Users/nihar/Desktop/Desktop - Nihar’s Mac mini/codes/hackathon/newtt/AdHubby_logo_2.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=600, output_format="PNG")
    
    # Initialize client
    openai_client = initialize_openai_client()
    if not openai_client:
        st.error("Failed to initialize OpenAI client. Please check your configuration.")
        st.stop()
    
    # Initialize session state
    if 'marketing_briefing' not in st.session_state:
        st.session_state.marketing_briefing = None
    if 'enhanced_analysis' not in st.session_state:
        st.session_state.enhanced_analysis = None
    if 'image_prompt' not in st.session_state:
        st.session_state.image_prompt = None
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None
    if 'current_location' not in st.session_state:
        st.session_state.current_location = None
    if 'selected_deliverables' not in st.session_state:
        st.session_state.selected_deliverables = []
    
    # Step 1: Business Details Input
    st.header("📝 Step 1: Business Details")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        business_name = st.text_input(
            "Business Name:",
            placeholder="e.g., Brew & Code Coffee",
            help="Enter your business name"
        )
    
    with col2:
        business_type = st.selectbox(
            "Business Type:",
            [
                "Restaurant",
                "Cafe",
                "Retail Store",
                "Service Business",
                "Tech Company",
                "Healthcare",
                "Fitness/Wellness",
                "Education",
                "Real Estate",
                "Entertainment",
                "Professional Services",
                "E-commerce",
                "Other"
            ],
            help="Select your business category"
        )
    
    with col3:
        location = st.text_input(
            "Location:",
            placeholder="e.g., San Francisco, CA",
            help="Be specific about city/region"
        )
    
    # Step 2: Marketing Deliverables Selection
    st.header("🎯 Step 2: Select Marketing Deliverables (Choose 2)")
    st.markdown("*Select exactly 2 marketing deliverables you want to create:*")
    
    deliverables_options = [
        "Social Media Carousels",
        "Static Social Ads", 
        "Billboard or Poster Design",
        "Email Newsletter Design",
        "Print Brochure or One-Pager",
        "Website Banner or Hero Image",
        "Copy Deck",
        "Press Kit (Media Kit)",
        "Point-of-Sale Display Mockups"
    ]
    
    # Create 3x3 grid of checkboxes
    cols = st.columns(3)
    selected_deliverables = []
    
    for i, deliverable in enumerate(deliverables_options):
        with cols[i % 3]:
            if st.checkbox(deliverable, key=f"deliverable_{i}"):
                selected_deliverables.append(deliverable)
    
    # Limit to 2 selections
    if len(selected_deliverables) > 2:
        st.warning("⚠️ Please select only 2 deliverables. Uncheck some options.")
        selected_deliverables = selected_deliverables[:2]
    elif len(selected_deliverables) == 2:
        st.success(f"✅ Selected: {', '.join(selected_deliverables)}")
    
    st.session_state.selected_deliverables = selected_deliverables
    
    # Generate Briefing Button
    if st.button("📋 Generate Marketing Briefing", type="primary") and business_name and business_type and location and len(selected_deliverables) == 2:
        with st.spinner("Generating comprehensive marketing briefing..."):
            st.session_state.marketing_briefing = generate_marketing_briefing(
                openai_client, business_name, business_type, location, selected_deliverables
            )
            st.session_state.current_location = location
            # Reset subsequent steps
            st.session_state.enhanced_analysis = None
            st.session_state.image_prompt = None
            st.session_state.generated_image = None
    
    # Step 3: Show Marketing Briefing
    if st.session_state.marketing_briefing:
        st.header("📋 Step 3: Marketing Briefing")
        st.write(st.session_state.marketing_briefing)
        
        # Step 4: User Visual Style Selection
        st.header("🎨 Step 4: Choose Your Visual Style")
        st.markdown("*This will be combined with the AI-recommended tone from your briefing:*")
        
        tone_options = [
            "Anime Style - Vibrant colors, stylized characters, dynamic compositions",
            "Cartoon Style - Playful, colorful, family-friendly with bold outlines", 
            "Minimalist Illustration - Clean lines, simple shapes, modern aesthetic",
            "Watercolor Art - Soft, flowing colors with organic, artistic feel",
            "Vintage Poster - Retro design elements, classic typography, nostalgic appeal"
        ]
        
        selected_tone_full = st.selectbox(
            "Select your preferred visual style:",
            tone_options,
            help="This will be blended with the AI-recommended tone for optimal results"
        )
        
        # Extract just the main tone name
        selected_tone = selected_tone_full.split(" - ")[0]
        
        if st.button("🧠 Enhanced Strategic Analysis", type="primary") and st.session_state.current_location:
            with st.spinner("Performing deep strategic analysis and identifying local hotspots..."):
                st.session_state.enhanced_analysis = reason_and_enhance_briefing(
                    openai_client, st.session_state.marketing_briefing, selected_tone, st.session_state.current_location
                )
                # Reset subsequent steps
                st.session_state.image_prompt = None
                st.session_state.generated_image = None
    
    # Step 5: Show Enhanced Analysis
    if st.session_state.enhanced_analysis:
        st.header("🧠 Step 5: Enhanced Strategic Analysis & Local Integration")
        st.write(st.session_state.enhanced_analysis)
        
        if st.button("🖼️ Generate Deliverable-Specific Prompt", type="primary"):
            with st.spinner("Creating tailored image prompts for your selected deliverables..."):
                st.session_state.image_prompt = generate_deliverable_specific_prompt(
                    openai_client, st.session_state.enhanced_analysis, selected_tone, 
                    st.session_state.current_location, st.session_state.selected_deliverables
                )
                st.session_state.generated_image = None
    
    # Step 6: Show Image Prompt
    if st.session_state.image_prompt:
        st.header("🎨 Step 6: Deliverable-Optimized Visual Prompt")
        
        # Display the prompt in an editable text area
        edited_prompt = st.text_area(
            "Image Generation Prompt (you can edit this):",
            value=st.session_state.image_prompt,
            height=600,
            help="This prompt is optimized for your selected deliverables and includes local landmarks"
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
                with st.spinner("Regenerating deliverable-specific prompt..."):
                    st.session_state.image_prompt = generate_deliverable_specific_prompt(
                        openai_client, st.session_state.enhanced_analysis, selected_tone,
                        st.session_state.current_location, st.session_state.selected_deliverables
                    )
                    st.rerun()
    
    # Step 7: Show Generated Image
    if st.session_state.generated_image:
        st.header("🖼️ Step 7: Your Campaign Visual")
        deliverables_text = ", ".join(st.session_state.selected_deliverables)
        st.image(
            st.session_state.generated_image, 
            caption=f"Generated Marketing Visual for: {deliverables_text}", 
            use_column_width=True
        )
        
        # Download button
        st.download_button(
            label="📥 Download Campaign Visual",
            data=st.session_state.generated_image,
            file_name="campaign_marketing_visual.png",
            mime="image/png"
        )
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Enhanced Workflow")
        st.markdown("""
        **AI-Powered Marketing Process:**
        
        1. **Business Profiling**: Name, type, and location input
        
        2. **Deliverable Selection**: Choose 2 specific marketing assets
        
        3. **AI Briefing Generation**: Creates problem, facts, objectives, audience analysis
        
        4. **Tone Intelligence**: AI recommends optimal visual style + user preference
        
        5. **Strategic Enhancement**: Deep analysis with local hotspot integration
        
        6. **Deliverable Optimization**: Tailored prompts for selected marketing assets
        """)
        
        st.header("🎯 Marketing Deliverables")
        st.markdown("""
        **Available Options:**
        • Social Media Carousels
        • Static Social Ads
        • Billboard/Poster Design
        • Email Newsletter Design
        • Print Brochure/One-Pager
        • Website Banner/Hero Image
        • Copy Deck
        • Press Kit (Media Kit)
        • Point-of-Sale Display Mockups
        """)
        
        st.header("🤖 AI Features")
        st.markdown("""
        • **Smart Tone Recommendation**: AI analyzes your business and suggests optimal visual style
        • **Briefing Intelligence**: Structured marketing analysis with problem-solution framework
        • **Local Integration**: Identifies and incorporates 5 relevant landmarks
        • **Deliverable Optimization**: Tailors visuals for specific marketing formats
        """)
        
        st.header("📊 API Status")
        if openai_client:
            st.success("✅ Custom LLM API: Connected")
            st.info(f"🔗 Base URL: {CUSTOM_BASE_URL}")
        else:
            st.error("❌ Custom LLM API: Not Connected")
        
        token = os.environ.get('HF_TOKEN') or HF_TOKEN
        if token and token != "your_hugging_face_token_here":
            st.success("✅ Image Generation: Available")
        else:
            st.warning("⚠️ Image Generation: Set HF_TOKEN")
        
        st.header("🔧 Configuration")
        st.code(f"""
# Environment Variables:
OPENAI_API_KEY={os.environ.get("OPENAI_API_KEY", "Not set")}
CUSTOM_BASE_URL={os.environ.get("CUSTOM_BASE_URL", "Not set")}
HF_TOKEN={"Set" if (os.environ.get('HF_TOKEN') or HF_TOKEN) else "Not set"}
        """)

if __name__ == "__main__":
    main()
