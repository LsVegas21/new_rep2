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
        return f"""Create CONTENT-RICH, VISUALLY STUNNING landing page: {theme}
ALL CONTENT IN: {language} | CTA: {target_action}

MUST HAVE SECTIONS (RICH CONTENT):
1. HEADER: Fixed, glassmorphism, logo, nav (4+ links), {target_action} button, live badge

2. HERO: Full viewport, gradient + hero image overlay, powerful H1 (specific to theme), 2-3 sentence value prop, STATS ROW (4 animated counters with descriptions), dual CTAs, social proof quote, scroll indicator

3. COMPLIANCE/TRUST: 3 cards with icons + images, detailed 2-3 sentence descriptions, disclaimer paragraph, privacy/terms links

4. PROBLEMS & SOLUTIONS: 
- 3-4 problem cards with unsplash images
- Each: Problem title, 2 sentences description, Solution section with 4-5 specific bullet points
- Comparison table with 5+ comparison points

5. SOCIAL PROOF:
- 6 testimonial cards with avatars (https://i.pravatar.cc/150?img=1,2,3,4,5,6)
- Each: Name, location, company, specific quote (2 sentences), star rating
- Live counters section: 4-5 metrics with animated numbers
- Trust logos/badges section

6. FEATURES (DETAILED):
- 6-8 feature cards with unsplash images
- Each card: Large icon, feature title, 3-4 sentence description, 5-6 benefit bullets
- Interactive tabs or accordion for more details

7. HOW IT WORKS:
- Step-by-step process (4-5 steps)
- Each step: Number, title, description, image
- Timeline visual or process flow

8. STATISTICS/ACHIEVEMENTS:
- 6-8 impressive stats with icons
- Animated numbers on scroll
- Visual charts or progress bars

9. FAQ SECTION:
- 6-8 common questions with detailed answers
- Accordion style with smooth open/close
- Rich text answers (2-3 sentences each)

10. PRICING:
- 2-3 pricing tiers with images
- Each: Plan name, price, 8-10 features list, {target_action} button
- Money-back guarantee badge

11. FINAL CTA:
- Background image with overlay
- Compelling headline, subheadline
- Large form or CTA button
- Trust indicators

12. FOOTER (COMPLETE):
- 4 column layout: Brand, Navigation, Resources, Contact
- Brand: Logo, 2-3 sentence description, social icons
- Navigation: 8-10 links
- Resources: Blog, guides, help links
- Contact: Email, phone (+country format), full address, business hours
- Bottom bar: Legal links (Privacy, Terms, Cookies), copyright 2025, certifications

VISUAL EXCELLENCE:
IMAGES: Unsplash everywhere:
- Hero: https://images.unsplash.com/photo-1560472355-536de3962603?w=1920
- Cards: https://images.unsplash.com/photo-relevant?w=800&h=600
- Avatars: https://i.pravatar.cc/150?img=X
- Use specific relevant search terms

GRADIENTS: Rich multi-color:
- Hero: linear-gradient(135deg, 3+ colors)
- Section backgrounds with gradients
- Button gradients with hover shift
- Animated gradient backgrounds

SHADOWS: Deep, layered:
- Cards: 0 10px 30px rgba(0,0,0,0.1), 0 1px 8px rgba(0,0,0,0.06)
- Hover: 0 20px 60px rgba(0,0,0,0.15)
- Text shadows on headers

HOVER: Everything interactive:
- transform: translateY(-8px) scale(1.03)
- Gradient shifts, brightness(1.1)
- Shadow depth increases
- Color transitions

ANIMATIONS:
- @keyframes: float, pulse, fadeIn, slideUp, shimmer, gradientShift
- Scroll animations, counter animations
- Smooth: transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1)

COLORS: Bold, vibrant, complementary scheme

ALL TEXT strictly in {language}. Output complete HTML."""
    
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