# 🚀 AdHubby.com - Enhanced Marketing Assistant

![AdHubby Logo](AdHubby_logo.png)

> **AI-Powered Marketing Campaign Generator with Location-Based Visual Intelligence**

AdHubby is a comprehensive marketing assistant that creates tailored marketing campaigns by combining AI-driven strategic analysis with location-specific visual generation. Perfect for businesses looking to create professional marketing materials with local relevance.

## 🎬 Demo & Examples

### 📹 **Demo Video**
<!-- Replace with your actual demo video -->
[![AdHubby Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

*Click to watch the full demo video showing the complete workflow from business input to final marketing visual generation.*

### 🖼️ **Sample Output**
<!-- Replace with actual generated marketing visuals -->
<table>
  <tr>
    <td align="center">
      <img src="demo_images/sample_billboard.png" width="300" alt="Billboard Design Sample"/>
      <br><b>Billboard Design</b>
      <br><i>Coffee Shop - San Francisco</i>
    </td>
    <td align="center">
      <img src="demo_images/sample_social_media.png" width="300" alt="Social Media Carousel Sample"/>
      <br><b>Social Media Carousel</b>
      <br><i>Tech Startup - Austin</i>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="demo_images/sample_email_banner.png" width="300" alt="Email Newsletter Banner Sample"/>
      <br><b>Email Newsletter Banner</b>
      <br><i>Fitness Studio - Miami</i>
    </td>
    <td align="center">
      <img src="demo_images/sample_poster.png" width="300" alt="Poster Design Sample"/>
      <br><b>Vintage Poster</b>
      <br><i>Restaurant - New York</i>
    </td>
  </tr>
</table>

### 📊 **Before vs After Comparison**

| Traditional Approach | AdHubby Approach |
|---------------------|------------------|
| Generic stock photos | Location-specific landmarks integrated |
| Manual market research | AI-powered strategic analysis |
| Single format creation | Multi-deliverable optimization |
| Hours of design work | Minutes to professional results |

### 🎯 **Sample Marketing Briefing Output**
```
THE PROBLEM:
Local coffee shops struggle to differentiate themselves in saturated markets while conveying their unique community connection and artisanal quality to busy urban professionals.

THE FACTS:
San Francisco has over 400 coffee shops with 68% of residents consuming coffee daily. The target demographic (ages 25-45) values authenticity, local sourcing, and Instagram-worthy experiences.

THE BIG PICTURE:
Position as the go-to community hub for tech professionals seeking authentic, locally-roasted coffee experiences that fuel both productivity and social connection.

AI-RECOMMENDED TONE: Minimalist Illustration
[Clean lines and modern aesthetic align with tech-savvy demographic while highlighting artisanal quality]
```

## ✨ Features

### 🎯 **Smart Marketing Intelligence**
- **AI-Powered Briefing Generation**: Creates structured marketing analysis including problem identification, market facts, objectives, and target audience profiling
- **Dual-Tone Intelligence**: Combines AI-recommended visual styles with user preferences for optimal brand positioning
- **Local Integration**: Automatically identifies and incorporates 5 relevant local landmarks/hotspots into marketing visuals
- **Strategic Enhancement**: Deep competitive landscape and demographic analysis

### 📊 **Deliverable-Specific Optimization**
Choose from 9 professional marketing formats:
- Social Media Carousels
- Static Social Ads
- Billboard/Poster Design
- Email Newsletter Design
- Print Brochure/One-Pager
- Website Banner/Hero Image
- Copy Deck
- Press Kit (Media Kit)
- Point-of-Sale Display Mockups

### 🎨 **Visual Style Engine**
- **Anime Style**: Vibrant colors, stylized characters, dynamic compositions
- **Cartoon Style**: Playful, colorful, family-friendly with bold outlines
- **Minimalist Illustration**: Clean lines, simple shapes, modern aesthetic
- **Watercolor Art**: Soft, flowing colors with organic, artistic feel
- **Vintage Poster**: Retro design elements, classic typography, nostalgic appeal

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Streamlit
- OpenAI Python client
- PIL (Pillow)
- Requests

### Environment Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/adhubby.git
cd adhubby
```

2. **Install dependencies**
```bash
pip install streamlit openai pillow requests pathlib
```

3. **Configure API Keys**
```bash
# Set environment variables
export OPENAI_API_KEY="your_openai_key"
export CUSTOM_BASE_URL="https://your-custom-llm-endpoint.com/v1"
export HF_TOKEN="your_hugging_face_token"
```

Or modify the constants in the code:
```python
OPENAI_API_KEY = "your_actual_key"
CUSTOM_BASE_URL = "https://your-custom-endpoint.com/v1"
HF_TOKEN = "your_hugging_face_token"
```

### 🚀 **Quick Start**

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

## 📋 Usage Workflow

### Step 1: Business Profiling
- Enter your business name, type, and location
- Be specific about location for better local integration

### Step 2: Marketing Deliverable Selection
- Choose exactly 2 marketing deliverables from 9 available options
- Each deliverable is optimized for specific use cases

### Step 3: AI Briefing Generation
- Generates comprehensive marketing analysis
- Includes problem identification, market facts, objectives, and target audience
- Provides AI-recommended visual tone

### Step 4: Visual Style Selection
- Choose your preferred visual style
- System combines your choice with AI recommendation

### Step 5: Strategic Enhancement
- Deep market analysis with local hotspot identification
- Competitive landscape insights
- Brand positioning strategy

### Step 6: Deliverable-Specific Optimization
- Generates tailored image prompts
- Optimized for your selected marketing formats
- Incorporates local landmarks as background elements

### Step 7: Visual Generation
- Creates professional marketing visuals
- Download high-quality images for immediate use

---

## 🖼️ **Live Demo Screenshots**

### Application Interface
<!-- Replace with actual screenshots of your Streamlit app -->
<table>
  <tr>
    <td align="center">
      <img src="screenshots/step1_business_input.png" width="400" alt="Business Input Screen"/>
      <br><b>Step 1: Business Input</b>
    </td>
    <td align="center">
      <img src="screenshots/step2_deliverables.png" width="400" alt="Deliverable Selection"/>
      <br><b>Step 2: Deliverable Selection</b>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/step3_briefing.png" width="400" alt="AI Briefing Generation"/>
      <br><b>Step 3: AI Briefing Output</b>
    </td>
    <td align="center">
      <img src="screenshots/step7_final_visual.png" width="400" alt="Final Generated Visual"/>
      <br><b>Step 7: Generated Marketing Visual</b>
    </td>
  </tr>
</table>

### Generated Content Examples
<!-- Add actual examples of your AI-generated briefings and prompts -->
```markdown
ENHANCED STRATEGIC ANALYSIS:
The San Francisco coffee market presents unique opportunities for community-focused establishments. 
With the proximity to iconic landmarks like Golden Gate Bridge, Lombard Street, and Union Square, 
this business can leverage location-based marketing to attract both locals and tourists.

LOCAL HOTSPOTS FOR SAN FRANCISCO:
1. Golden Gate Bridge
2. Lombard Street  
3. Union Square
4. Fisherman's Wharf
5. Alcatraz Island

DETAILED IMAGE GENERATION PROMPT:
Create a minimalist illustration for billboard and social media featuring a modern coffee shop 
storefront with subtle Golden Gate Bridge silhouette in background, clean typography, 
warm earth tones, professional urban aesthetic targeting tech professionals aged 25-45...
```

## 🔧 Configuration

### API Endpoints

**Custom LLM API**
- Model: `meta-llama/Llama-3.1-8B-Instruct`
- Temperature: 0.7
- Max Tokens: 800-900 (depending on function)

**Image Generation**
- Service: Hugging Face Inference API
- Model: `stabilityai/stable-diffusion-xl-base-1.0`
- Timeout: 60 seconds

### File Structure
```
adhubby/
├── app.py                 # Main Streamlit application
├── AdHubby_logo_2.png    # Application logo
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## 🎨 Business Types Supported

- Restaurant
- Cafe
- Retail Store
- Service Business
- Tech Company
- Healthcare
- Fitness/Wellness
- Education
- Real Estate
- Entertainment
- Professional Services
- E-commerce
- Other

## 🔍 Key Functions

### Core AI Functions
- `generate_marketing_briefing()`: Creates structured marketing analysis
- `reason_and_enhance_briefing()`: Performs strategic enhancement with local insights
- `generate_deliverable_specific_prompt()`: Creates optimized image generation prompts
- `generate_image()`: Handles visual creation via Hugging Face API

### Technical Functions
- `initialize_openai_client()`: Sets up custom LLM connection
- `call_custom_llm()`: Handles API calls with error management

## 🚨 Error Handling

- **API Connection Issues**: Automatic retry logic with user feedback
- **Image Generation Failures**: Model loading detection and status updates
- **Token Validation**: Environment variable validation with setup guidance
- **Input Validation**: Business details and deliverable selection validation

## 🔐 Security & Privacy

- API keys stored as environment variables
- No data persistence between sessions
- Local image processing and download
- Secure API endpoint communication

## 📊 Performance Optimization

- **Session State Management**: Efficient step-by-step processing
- **Lazy Loading**: Components load only when needed
- **Error Recovery**: Graceful handling of API timeouts
- **Memory Management**: Optimized image handling

## 🎯 Use Cases

### Small Businesses
- Quick professional marketing materials
- Location-specific campaign development
- Multi-format asset creation

### Marketing Agencies
- Client campaign development
- Rapid prototyping
- Location-based marketing strategies

### Entrepreneurs
- Brand development
- Market entry strategies
- Cost-effective marketing solutions

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@adhubby.com or create an issue in this repository.

## 🔮 Roadmap

- [ ] Additional visual style options
- [ ] Multi-language support
- [ ] Advanced analytics integration
- [ ] Batch processing capabilities
- [ ] API rate limiting optimization
- [ ] Custom brand template uploads

## 👥 Team

Built with ❤️ by the AdHubby team

---

**Made with Streamlit and powered by AI** 🤖✨
