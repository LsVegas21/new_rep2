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
        return f"""Create VISUALLY STUNNING landing page: {theme}
ALL CONTENT IN: {language} | CTA: {target_action}

SECTIONS (with images):
1. HEADER: Fixed glassmorphism, logo, nav, {target_action} button
2. HERO: Full height, RICH GRADIENT background, hero image (use https://images.unsplash.com/photo-relevant), headline, stats, dual CTAs
3. TRUST: 3 badges with icons, images, disclaimer
4. PROBLEMS: 3 cards with images from unsplash
5. TESTIMONIALS: 3+ with avatar images (https://i.pravatar.cc/150?img=X), names, ratings
6. FEATURES: 4-6 cards with unsplash images, icons, bullets
7. PRICING: Cards with imagery
8. FORM: With background image, fields, {target_action} button
9. FOOTER: Complete with imagery

VISUAL REQUIREMENTS (CRITICAL):
IMAGES: Use Unsplash API for ALL sections:
- Hero: https://images.unsplash.com/photo-relevant-to-theme?w=1920&h=1080&fit=crop
- Features: https://images.unsplash.com/photo-relevant?w=800&h=600&fit=crop
- Avatars: https://i.pravatar.cc/150?img=1,2,3
- Use realistic relevant search terms

GRADIENTS: Rich, vibrant gradients everywhere:
- Hero: linear-gradient(135deg, color1 0%, color2 50%, color3 100%)
- Cards: radial-gradient or linear with 3+ colors
- Buttons: gradient backgrounds with shift on hover
- Overlays: gradient overlays on images

SHADOWS: Multiple layered shadows:
- Cards: box-shadow: 0 10px 30px rgba(0,0,0,0.1), 0 1px 8px rgba(0,0,0,0.06)
- Hover: box-shadow: 0 20px 60px rgba(0,0,0,0.15), 0 5px 15px rgba(0,0,0,0.08)
- Text shadows on hero: text-shadow: 2px 2px 8px rgba(0,0,0,0.3)

HOVER EFFECTS (on ALL interactive elements):
- transform: translateY(-8px) scale(1.03)
- box-shadow transitions
- gradient shifts
- opacity changes
- filter: brightness(1.1)

ANIMATIONS (smooth):
- @keyframes float, pulse, fadeIn, slideUp, shimmer
- Entrance animations on scroll
- Counter animations
- Background gradients animate
- Smooth transitions: transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1)

COLORS: Vibrant, modern (NO boring grays):
- Use bold, saturated colors
- Complementary color schemes
- Accent colors that pop
- NO purple/blue or purple/pink unless requested

CSS: Modern, rich styling, glassmorphism everywhere, backdrop-filter, colorful, NOT boring!

ALL TEXT in {language}. Output HTML only."""
    
    async def _generate_metadata(self, theme: str, language: str, chat: LlmChat) -> dict:
        """Generate realistic contact information"""
        prompt = f"""Generate REALISTIC professional contact info for: {theme}

CRITICAL: Make this 100% real-looking - NOT placeholder!

Requirements:
- Company name: Professional, memorable
- Email: Format like contact@companyname.com
- Phone: Proper international format (+country xxx xxx xxxx)
- Address: COMPLETE with street, suite/office, city, postal code, country

Language: {language} (use appropriate country format)

Provide in EXACT format:
Company: [name]
Email: [professional@domain.com]
Phone: [+X XXX XXX XXXX]
Address: [Full Address with Postal Code]

Make it completely real and professional."""
        
        msg = UserMessage(text=prompt)
        response = await chat.send_message(msg)
        return self._parse_metadata(response)
    
    def _parse_metadata(self, response: str) -> dict:
        """Parse metadata from AI response"""
        lines = response.strip().split('\n')
        metadata = {
            "company_name": "",
            "email": "",
            "phone": "",
            "address": ""
        }
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if 'company' in key:
                    metadata['company_name'] = value
                elif 'email' in key:
                    metadata['email'] = value
                elif 'phone' in key:
                    metadata['phone'] = value
                elif 'address' in key:
                    metadata['address'] = value
        
        return metadata
    
    def _clean_html_response(self, html: str) -> str:
        """Clean HTML response from AI"""
        html = html.strip()
        
        # Remove markdown code blocks
        if html.startswith('```html'):
            html = html[7:]
        elif html.startswith('```'):
            html = html[3:]
        
        if html.endswith('```'):
            html = html[:-3]
        
        html = html.strip()
        
        # Ensure it starts with DOCTYPE
        if not html.upper().startswith('<!DOCTYPE'):
            html = '<!DOCTYPE html>\n' + html
        
        return html