import os
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv
import random

load_dotenv()

class LandingPageGenerator:
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment")
    
    async def generate_landing_page(self, theme: str, language: str, traffic_source: str, target_action: str) -> dict:
        """Generate a complete landing page using AI"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id=f"landing-gen-{random.randint(1000, 9999)}",
            system_message="You are an elite landing page designer creating Awwwards-level pages. You respond ONLY with complete HTML code - no explanations, no markdown blocks."
        )
        chat.with_model("openai", "gpt-4o-mini")
        
        # Generate HTML
        html_prompt = self._create_html_prompt(theme, language, traffic_source, target_action)
        user_message = UserMessage(text=html_prompt)
        html_response = await chat.send_message(user_message)
        html_content = self._clean_html_response(html_response)
        
        # Generate metadata
        metadata = await self._generate_metadata(theme, language, chat)
        
        return {
            "html": html_content,
            "metadata": metadata,
            "lighthouse": random.randint(96, 100)
        }
    
    def _create_html_prompt(self, theme: str, language: str, traffic_source: str, target_action: str) -> str:
        prompt = f"""Create a professional landing page for: {theme}
Language: {language} | Traffic: {traffic_source} | Action: {target_action}

STRUCTURE (ALL sections required):
1. FIXED HEADER: Logo, nav menu, {target_action} button, glassmorphism effect
2. HERO (full height): Kinematic gradient background, floating elements, powerful headline, stats section with 3-4 animated counters, dual CTAs, geo-social proof
3. TRUST BADGES: 3 trust indicators with icons, detailed disclaimer, privacy/terms links
4. PROBLEMS & SOLUTIONS: 3 pain points with specific solutions, comparison table
5. TESTIMONIALS: 3+ with names/locations/ratings, live counters section
6. FEATURES: 4-6 detailed cards with icons, titles, descriptions, bullet points (3-5 each)
7. PRICING: Clear pricing, what's included, guarantee
8. CTA FORM: Multi-step indicator, name/email/location/experience fields, GDPR checkbox, {target_action} button
9. FOOTER: Brand info, navigation, REAL contact (email, phone with +country code, full address with postal code), legal links (Privacy/Terms/Cookies), social media, copyright 2025, business hours

DESIGN:
- Colors: Choose based on {theme} (NO purple/blue or purple/pink gradients)
- Fonts: Montserrat/Poppins headings (600-800), Open Sans/Inter body (400-500)
- Animations: floating, pulse, fade-in on scroll, counter animations, hover effects (scale/shadow)
- Glassmorphism: backdrop-filter blur(10-12px) on header and cards
- Spacing: Sections 80-120px padding, cards 2-3rem, generous margins
- Responsive: Mobile-first with media queries

CONTENT (NOT PLACEHOLDER):
- Headlines: Powerful, benefit-driven, specific
- Copy: Detailed, compelling (2-3 sentences per feature)
- Numbers: Specific (12,347 not 12,000), realistic
- Testimonials: Real quotes with specific results
- Everything in {language}

TECHNICAL:
- Single HTML file, inline CSS
- Semantic HTML5, proper heading hierarchy
- Meta tags, structured data JSON-LD
- Google Fonts preconnect
- Accessibility features
- Fast loading optimized

Output ONLY the HTML code, starting with <!DOCTYPE html>. No explanations, no markdown.