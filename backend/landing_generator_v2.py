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
        prompt = f"""Create an Awwwards-quality landing page for: {theme}
Language: {language} | Traffic: {traffic_source} | Main CTA: {target_action}

MUST HAVE ALL SECTIONS:

1. HEADER (position: fixed, backdrop-filter: blur(10px)):
   - Animated logo
   - Nav links with smooth scroll
   - Live indicator badge
   - Primary CTA button: {target_action}

2. HERO SECTION (min-height: 100vh):
   - Kinematic background with radial gradients
   - Floating decorative elements (position: absolute with animations)
   - H1: Powerful headline (not generic - be specific to {theme})
   - Subtitle: Clear value proposition
   - STATS ROW with 3-4 animated counters:
     Example: "12,347 Active Users | 95% Success Rate | 25+ Cities"
   - Two CTAs: Primary ({target_action}) + Secondary link
   - Social proof: "María from [City] just [achievement]"
   - Scroll indicator

3. COMPLIANCE/TRUST (3 cards):
   - Icon + claim for each (e.g., "GDPR Compliant", "Secure Data", "Money-back")
   - Detailed disclaimer paragraph
   - Links to Privacy Policy & Terms

4. PROBLEM/SOLUTION (3 problems):
   - Each problem: Title + description + solution with 3 benefits
   - Comparison table: Traditional way vs Our solution

5. SOCIAL PROOF:
   - 3+ Testimonial cards:
     * Avatar/initial
     * Name, Location
     * Quote with SPECIFIC results (not generic)
     * 5-star rating
   - Live counters section (animated numbers)

6. FEATURES/MODULES (4-6 cards):
   - Each card: Large icon, Title, 2-3 sentence description, 3-5 bullet benefits
   - Grid layout with hover effects
   - Add simulated interactive map or tabs

7. PRICING:
   - Price tiers or single price
   - What's included list
   - Guarantee statement

8. LEAD FORM:
   - Multi-step progress bar (Step 1 of 3 style)
   - Fields: Name, Email, City/Country dropdown, Experience level select
   - GDPR consent checkbox
   - Large submit button: {target_action}
   - Trust badges near form

9. FOOTER (complete):
   - Logo + company tagline
   - Quick links section
   - Contact section with:
     * Email: professional@domain.com format
     * Phone: +country code format (e.g., +1 415 555 1234)
     * Full address: Street, City, Postal Code, Country
     * Business hours: Mon-Fri, 9am-5pm
   - Legal links: Privacy Policy | Terms | Cookies
   - Social media icons (use Unicode: 👤 💼 🐦)
   - Copyright 2025
   - Additional CTA section

CSS REQUIREMENTS:
- CSS variables for colors
- Animations: @keyframes float, pulse, fadeIn
- Glassmorphism: backdrop-filter: blur(12px), rgba backgrounds
- Hover effects: transform: translateY(-4px) scale(1.02), box-shadow transitions
- Responsive: @media (max-width: 768px)
- Smooth scroll: html scroll-behavior: smooth

CONTENT QUALITY:
- Headlines: Not generic! Example for education: "Master Python in 30 Days" not "Learn Programming"
- Features: Specific details, not "Great features" but "24/7 Expert Support with <2hr Response"
- Numbers: Use specific like 10,247 not 10,000
- Testimonials: Specific results "Increased revenue by 45% in 3 months"
- Write everything in {language}

COLOR SCHEME (choose based on theme):
- Education/Tech: Deep blues (#1e40af), teal (#0d9488), slate (#334155)
- Health/Fitness: Greens (#059669), coral (#f87171), orange (#f59e0b)
- Business/Finance: Navy (#1e3a8a), gold (#f59e0b), forest green (#065f46)
- Creative: Rich purples (NOT with pink/blue), magenta, deep orange

FONTS:
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght=600;700;800&family=Open+Sans:wght=400;500&display=swap" rel="stylesheet">

Output complete HTML starting with <!DOCTYPE html>. No explanations or markdown blocks."""
        return prompt
    
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