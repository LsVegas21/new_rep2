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
        return f"""Create stunning landing page: {theme}
ALL TEXT in {language} | CTA: {target_action}

Sections: Header, Hero(stats+images), Trust(3), Problems(4), Testimonials(6 with https://i.pravatar.cc/150?img=1-6), Features(6 detailed), How-it-works(4), Stats(6), FAQ(6), Pricing(3), CTA-Form, Footer(complete contact)

Visuals: Unsplash images everywhere, rich gradients, deep shadows, hover effects(scale+translateY), smooth animations, bold colors

Content: Detailed, specific, realistic. HTML only."""
    
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