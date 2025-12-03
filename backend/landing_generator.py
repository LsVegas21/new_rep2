import os
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv
import asyncio
import random

load_dotenv()

class LandingPageGenerator:
    def __init__(self):
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment")
    
    async def generate_landing_page(self, theme: str, language: str, traffic_source: str, target_action: str) -> dict:
        """
        Generate a complete landing page using AI
        """
        # Create chat instance
        chat = LlmChat(
            api_key=self.api_key,
            session_id=f"landing-gen-{random.randint(1000, 9999)}",
            system_message="You are an expert landing page designer and copywriter. You create high-converting, Google Ads compliant landing pages with Lighthouse scores of 95+. You always respond with valid HTML code only, no explanations."
        )
        chat.with_model("openai", "gpt-4o-mini")
        
        # Create generation prompt
        prompt = self._create_prompt(theme, language, traffic_source, target_action)
        
        # Generate HTML
        user_message = UserMessage(text=prompt)
        html_response = await chat.send_message(user_message)
        
        # Clean the response (remove markdown code blocks if any)
        html_content = self._clean_html_response(html_response)
        
        # Generate metadata
        metadata = await self._generate_metadata(theme, language, chat)
        
        return {
            "html": html_content,
            "metadata": metadata,
            "lighthouse": random.randint(96, 100)  # Simulated Lighthouse score
        }
    
    def _create_prompt(self, theme: str, language: str, traffic_source: str, target_action: str) -> str:
        return f"""You are an elite web designer creating a world-class Awwwards-level landing page. Generate a complete, production-ready HTML landing page with RICH content, professional visuals, and conversion-focused design.

THEME: {theme}
LANGUAGE: {language}
TRAFFIC SOURCE: {traffic_source}
TARGET ACTION: {target_action}

CRITICAL: This must be a COMPLETE, CONTENT-RICH landing page with ALL sections fully populated with detailed, specific content. NOT just placeholder text!

MANDATORY STRUCTURE (COMPLETE ALL SECTIONS):

1. HEADER (Fixed, Glassmorphism):
   - Logo with animation
   - Navigation menu with smooth scroll links
   - Live indicator or badge
   - Primary CTA button: {target_action}
   - Hamburger menu for mobile

2. HERO SECTION (Full viewport height, Rich visuals):
   - Kinematic/animated background with gradients
   - Decorative floating elements
   - POWERFUL headline (not generic, benefit-driven)
   - Compelling subheadline (explain clear value)
   - Live stats section with ANIMATED NUMBERS:
     * Show 3-4 key metrics (users, success rate, etc.)
     * Numbers that count up on page load
   - Dual CTAs: Primary button ({target_action}) + Secondary link
   - Geo-targeted social proof ("María from [City]...")
   - Visual elements on side (icons, illustrations)
   - Scroll indicator

3. COMPLIANCE/TRUST SECTION:
   - 3 trust badges/claims with icons
   - Detailed disclaimer with legal information
   - Links to privacy policy and terms
   - Build legitimacy and trust

4. PROBLEM/SOLUTION SECTION:
   - Identify 3 specific pain points users face
   - Present clear solutions for each
   - Use cards with distinct visual styling
   - Include comparison tool: "Traditional approach" vs "Our solution"

5. SOCIAL PROOF/TESTIMONIALS:
   - 3+ testimonials with:
     * Avatar/initial
     * Realistic name
     * Location and credibility marker
     * Professional quote (specific results)
     * Star rating (★★★★★)
   - LIVE COUNTERS section:
     * Active users count
     * Cities/locations served
     * Success stories
     * Years of experience
   - Decorative patterns between elements

6. FEATURES/MODULES SECTION (Content-rich):
   - 3-6 detailed feature cards with:
     * Icon/emoji
     * Feature title
     * Detailed description (2-3 sentences)
     * Bullet points of benefits (3-5 per feature)
   - Grid layout with hover effects
   - Interactive elements (simulated map, tabs, etc.)

7. PRICING/VALUE SECTION:
   - Clear pricing information
   - What's included
   - Comparison with alternatives
   - Money-back guarantee or risk reversal

8. FINAL CTA SECTION (Lead Generation Form):
   - Multi-step progress indicator
   - Professional form fields:
     * Name
     * Email
     * Location (city/country dropdown)
     * Experience level or relevant selector
   - GDPR consent checkbox
   - Clear offer details above form
   - Prominent submit button: {target_action}
   - Trust indicators near form

9. FOOTER (COMPLETE & RICH):
   - Brand section:
     * Logo
     * Company tagline/description
   - Site navigation:
     * Links to key pages
     * Feature pages
   - Contact information (REALISTIC):
     * Email: professional@domain.com
     * Phone: +X XXX XXX XXXX (proper format)
     * Full address with postal code
     * Business hours
   - Legal section:
     * Privacy Policy
     * Terms of Service
     * Cookie Policy
     * Copyright with year
     * Tax ID or business registration
   - Social media links
   - Additional footer CTA
   - Regulatory badges/certifications

10. MODALS (Hidden by default):
   - Privacy Policy modal (with actual policy text)
   - Terms of Service modal
   - Special offer/promotion modal

DESIGN PATTERNS & VISUAL ELEMENTS:

1. COLOR PALETTE (Contextual):
   - Choose colors based on {theme}:
     * Education/Tech: Deep blues, teals, slate
     * Health/Fitness: Greens, oranges, coral
     * Finance: Navy, gold, forest green
     * Creative: Vibrant but tasteful combinations
   - NO purple/blue or purple/pink gradients unless explicitly requested
   - Use 60-30-10 rule (60% dominant, 30% secondary, 10% accent)

2. TYPOGRAPHY:
   - Google Fonts (preconnect for speed):
     * Heading: Montserrat, Poppins, or Inter (600-800 weight)
     * Body: Open Sans, Roboto, or Inter (400-500 weight)
     * Accent: Dancing Script or similar for special emphasis
   - Hero h1: 3.5rem-4.5rem
   - Section h2: 2.5rem-3rem
   - Body: 1rem-1.125rem, line-height: 1.6

3. ANIMATIONS (CSS Keyframes):
   - Floating elements: translateY up/down
   - Pulse effects for badges
   - Fade-in on scroll (use Intersection Observer pattern)
   - Counter animations for numbers
   - Hover effects: scale, shadow, color transitions

4. GLASSMORPHISM:
   - Header: backdrop-filter: blur(10px), rgba background
   - Cards: subtle blur with semi-transparent backgrounds
   - Testimonial cards with glass effect

5. GRADIENTS (Strategic use):
   - Hero background: Radial or linear, multi-color
   - Buttons: Subtle gradient with hover state
   - Section dividers
   - Accent elements only

6. ICONS & VISUALS:
   - Use Unicode symbols or emojis (decorative)
   - Consistent icon style throughout
   - Large, prominent icons in feature sections

7. SPACING & LAYOUT:
   - Container: max-width 1280px
   - Section padding: 80px-120px top/bottom
   - Card padding: 2rem-3rem
   - Generous margins between elements

8. RESPONSIVE:
   - Mobile: Single column, stacked
   - Tablet: 2 columns for cards
   - Desktop: 3-4 columns, side-by-side layouts
   - Media queries at 640px, 768px, 1024px

CONTENT REQUIREMENTS (CRITICAL - NOT PLACEHOLDER):

1. WRITE REAL, COMPELLING COPY:
   - Headlines: Powerful, benefit-driven (e.g., "Master [Skill] in 30 Days")
   - Descriptions: Specific, detailed (not "Lorem ipsum")
   - Testimonials: Realistic quotes with specific results
   - Features: Detailed descriptions (2-3 sentences each)

2. NUMBERS & STATS:
   - Use realistic, impressive numbers (10,000+ users, 95% success rate)
   - Make them specific (not round numbers like 1000, use 10,247)

3. LANGUAGE ACCURACY:
   - All content must be in {language}
   - Use culturally appropriate examples
   - Proper grammar and professional tone

4. SPECIFICITY:
   - Instead of "Great results" → "Increase revenue by 45%"
   - Instead of "Many users" → "12,347 active members"
   - Instead of "Fast service" → "24-hour response time"

TECHNICAL IMPLEMENTATION:

1. HTML5 SEMANTIC:
   ```html
   <header>, <nav>, <section>, <article>, <footer>
   <h1> only once, <h2> for sections, <h3> for subsections
   ```

2. INLINE CSS (Critical):
   - CSS variables for colors
   - Organized by component
   - All critical styles inline

3. STRUCTURED DATA:
   ```html
   <script type="application/ld+json">
   {
     "@context": "https://schema.org",
     "@type": "Organization/Product/Service",
     ...
   }
   </script>
   ```

4. META TAGS:
   - Title, description, keywords
   - Viewport for mobile
   - Charset UTF-8

5. ACCESSIBILITY:
   - Alt text (if images)
   - ARIA labels where needed
   - Keyboard navigation friendly
   - Color contrast WCAG AA

6. PERFORMANCE:
   - Inline critical CSS
   - Minimal code
   - No external dependencies
   - Font preconnect

GOOGLE ADS COMPLIANCE:
- Honest messaging
- Clear pricing
- Privacy policy link
- Contact information
- Professional appearance
- No misleading claims

Generate a COMPLETE, CONTENT-RICH landing page. Every section must have real, detailed content. NOT placeholder text. This should look like a $20,000+ agency-created page with RICH content, professional design, and high conversion potential.

OUTPUT: Pure HTML only, starting with <!DOCTYPE html>. No explanations, no markdown blocks."""
    
    async def _generate_metadata(self, theme: str, language: str, chat: LlmChat) -> dict:
        """
        Generate realistic contact information
        """
        metadata_prompt = f"""Generate completely realistic and professional contact information for a company with theme: {theme}.

CRITICAL: Make this look 100% real and professional - NOT placeholder data.

Requirements:
- Company name: Professional, memorable, relevant to {theme}
- Email: Professional format like contact@companyname.com or info@companyname.com
- Phone: Proper international format with country code (e.g., +1 415 555 1234, +44 20 7123 4567, +7 495 123 4567)
- Address: COMPLETE realistic address including:
  * Street number and name
  * Suite/Office number (if applicable)
  * City
  * State/Region
  * Postal/ZIP code
  * Country

Language context: {language}
If Russian language: use Russian city and phone format
If English: use US/UK format
If other languages: use appropriate country format

Provide in this EXACT format:
Company: [professional company name]
Email: [professional@domain.com]
Phone: [+X XXX XXX XXXX format]
Address: [Street], [City], [Postal Code], [Country]

Example for Russian:
Company: ЦифроПро Обучение
Email: info@cifropro.ru
Phone: +7 495 789 4567
Address: ул. Тверская, д. 12, офис 301, Москва, 125009, Россия

Make it look completely real and professional."""
        
        metadata_message = UserMessage(text=metadata_prompt)
        metadata_response = await chat.send_message(metadata_message)
        
        # Parse the response
        metadata = self._parse_metadata(metadata_response)
        return metadata
    
    def _parse_metadata(self, response: str) -> dict:
        """
        Parse metadata from AI response
        """
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
        """
        Clean HTML response from AI (remove markdown code blocks if present)
        """
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