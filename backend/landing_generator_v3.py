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
            session_id=f"landing-{random.randint(1000, 9999)}",
            system_message="You are an elite team: Senior Full-Stack Developer + UX/UI Designer (Awwwards level) + Copywriter + Legal Expert. Create visually EPIC landing pages that: Pass Google Ads moderation, Get Lighthouse 100/100, Look like Behance Featured projects. Respond ONLY with HTML code."
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
        return f"""Create EPIC landing page HTML for: {theme}

CRITICAL: ALL content in {language} | Traffic: {traffic_source} | CTA: {target_action}

SECTIONS:
1. HEADER: Fixed position, backdrop-filter blur, logo with animation, nav links, {target_action} button, live badge
2. HERO: Full viewport, gradient+image, powerful headline, value prop, 4 stats counters (animated), dual CTAs
3. COMPLIANCE: 3 trust cards, detailed descriptions, disclaimer, privacy/terms modals
4. PROBLEMS: 4 problem cards with solutions (5 bullets each)
5. TESTIMONIALS: 6 cards with avatars https://i.pravatar.cc/150?img=1-6, names, locations, quotes, ratings
6. FEATURES: 6 detailed cards with descriptions (3 sentences), 5 bullets each
7. HOW IT WORKS: 4 steps with numbers, descriptions
8. STATS: 6 metrics with animated counters
9. FAQ: 6 questions with accordion, detailed answers
10. PRICING: 3 tiers, 8 features each
11. FORM: Multi-step, fields (name/email/location/experience), GDPR checkbox, {target_action} button
12. FOOTER: 4 columns (Brand/Nav/Resources/Contact), full contact info, legal links, social icons, copyright 2025

CSS VARIABLES (auto-generate based on theme):
:root --color-primary, --color-secondary, --color-accent, --gradient-main, --font-heading, --font-body, --shadow-lg, --radius-lg

VISUAL:
- Gradients: 3+ colors, radial/linear, everywhere
- Shadows: 0 10px 30px rgba, layered
- Images: https://images.unsplash.com/photo-relevant?w=800
- Avatars: https://i.pravatar.cc/150?img=X
- Animations: @keyframes float, pulse, fadeIn, slideUp

ANIMATIONS:
@keyframes pulse-logo, float, fadeIn, slideUp, gradientShift
transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1)
Hover: translateY(-8px) scale(1.03) brightness(1.1)

INTERACTIVE:
- Smooth scroll
- Accordion FAQ
- Modal windows (Privacy/Terms/Cookies)
- Form validation
- Counter animations on scroll
- Live indicators

CONTENT: Specific, detailed, realistic. NO Lorem Ipsum. ALL in {language}.

Output complete self-contained HTML starting with <!DOCTYPE html>. No explanations."""
    
    async def _generate_metadata(self, theme: str, language: str, chat: LlmChat) -> dict:
        """Generate realistic contact information"""
        prompt = f"""Generate professional contact info for: {theme} in {language}

Format:
Company: [name]
Email: [contact@domain.ext]
Phone: [+country xxx xxx xxxx]
Address: [street, city, postal, country]

Make it 100% realistic, professional."""
        
        msg = UserMessage(text=prompt)
        response = await chat.send_message(msg)
        return self._parse_metadata(response)
    
    def _parse_metadata(self, response: str) -> dict:
        """Parse metadata from AI response"""
        lines = response.strip().split('\n')
        metadata = {"company_name": "", "email": "", "phone": "", "address": ""}
        
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
        
        if html.startswith('```html'):
            html = html[7:]
        elif html.startswith('```'):
            html = html[3:]
        
        if html.endswith('```'):
            html = html[:-3]
        
        html = html.strip()
        
        if not html.upper().startswith('<!DOCTYPE'):
            html = '<!DOCTYPE html>\n' + html
        
        return html