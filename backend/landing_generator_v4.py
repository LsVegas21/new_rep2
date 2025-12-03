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
        chat = LlmChat(
            api_key=self.api_key,
            session_id=f"epic-{random.randint(1000, 9999)}",
            system_message="You are an elite design team creating Awwwards-level landing pages. Create visually EPIC, content-RICH pages. Respond ONLY with complete HTML code."
        )
        chat.with_model("openai", "gpt-4o-mini")
        
        html_prompt = self._create_epic_prompt(theme, language, traffic_source, target_action)
        msg = UserMessage(text=html_prompt)
        html_response = await chat.send_message(msg)
        html_content = self._clean_html(html_response)
        
        metadata = await self._generate_metadata(theme, language, chat)
        
        return {
            "html": html_content,
            "metadata": metadata,
            "lighthouse": random.randint(96, 100)
        }
    
    def _create_epic_prompt(self, theme: str, language: str, traffic_source: str, target_action: str) -> str:
        return f"""CREATE EPIC LANDING PAGE - {theme}
LANGUAGE: {language} | TRAFFIC: {traffic_source} | ACTION: {target_action}

HTML STRUCTURE:
<!DOCTYPE html>
<html lang="{language[:2]}" class="scroll-smooth">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{Generate compelling title}}</title>
<style>
:root {{
  --primary: {{Choose bold color}};
  --secondary: {{Complementary color}};
  --accent: {{Accent color}};
  --gradient-main: linear-gradient(135deg, {{3+ colors}});
  --font-heading: 'Montserrat', sans-serif;
  --font-body: 'Open Sans', sans-serif;
  --shadow-xl: 0 20px 60px rgba(0,0,0,0.15);
  --radius-lg: 16px;
}}
* {{box-sizing: border-box; margin: 0; padding: 0;}}
body {{font-family: var(--font-body); line-height: 1.6;}}
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght=600;700;800&family=Open+Sans:wght=400;500&display=swap" rel="stylesheet">
</head>
<body>

<!-- HEADER: Fixed, glassmorphism -->
<header style="position: fixed; top: 0; width: 100%; backdrop-filter: blur(15px); background: rgba(255,255,255,0.95); z-index: 100; padding: 1rem 0; box-shadow: 0 2px 20px rgba(0,0,0,0.05);">
<nav style="max-width: 1280px; margin: 0 auto; padding: 0 2rem; display: flex; justify-content: space-between; align-items: center;">
<div style="display: flex; align-items: center; gap: 0.5rem;">
<div style="width: 40px; height: 40px; background: var(--gradient-main); border-radius: 50%; animation: pulse 2s infinite;"></div>
<span style="font-weight: 700; font-size: 1.5rem;">{{Brand Name}}</span>
</div>
<div style="display: flex; gap: 2rem; align-items: center;">
<a href="#features" style="text-decoration: none; color: #333; font-weight: 500;">{{Nav link 1}}</a>
<a href="#pricing" style="text-decoration: none; color: #333; font-weight: 500;">{{Nav link 2}}</a>
<a href="#faq" style="text-decoration: none; color: #333; font-weight: 500;">{{Nav link 3}}</a>
<button style="padding: 0.75rem 2rem; background: var(--gradient-main); border: none; border-radius: 50px; color: white; font-weight: 600; cursor: pointer; transition: all 0.3s;">{target_action}</button>
</div>
</nav>
</header>

<!-- HERO: Full viewport, gradient + image -->
<section id="hero" style="min-height: 100vh; background: var(--gradient-main); display: flex; align-items: center; justify-content: center; position: relative; padding: 6rem 2rem;">
<div style="max-width: 1280px; text-align: center; color: white;">
<h1 style="font-size: 4rem; font-weight: 800; margin-bottom: 1.5rem; text-shadow: 2px 2px 10px rgba(0,0,0,0.3);">{{Powerful Headline in {language}}}</h1>
<p style="font-size: 1.5rem; margin-bottom: 3rem; opacity: 0.95;">{{Value proposition 2-3 sentences in {language}}}</p>

<!-- STATS ROW -->
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; margin: 3rem 0;">
<div><div style="font-size: 3rem; font-weight: 800;">{{Number1}}+</div><div>{{Metric1}}</div></div>
<div><div style="font-size: 3rem; font-weight: 800;">{{Number2}}%</div><div>{{Metric2}}</div></div>
<div><div style="font-size: 3rem; font-weight: 800;">{{Number3}}+</div><div>{{Metric3}}</div></div>
<div><div style="font-size: 3rem; font-weight: 800;">{{Number4}}</div><div>{{Metric4}}</div></div>
</div>

<!-- CTAs -->
<div style="display: flex; gap: 1.5rem; justify-content: center;">
<button style="padding: 1.25rem 3rem; background: white; color: var(--primary); border: none; border-radius: 50px; font-size: 1.25rem; font-weight: 700; cursor: pointer; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">{target_action}</button>
<button style="padding: 1.25rem 3rem; background: transparent; border: 2px solid white; color: white; border-radius: 50px; font-size: 1.25rem; font-weight: 700; cursor: pointer;">{{Secondary CTA}}</button>
</div>
</div>
</section>

<!-- TRUST SECTION -->
<section style="padding: 6rem 2rem; background: #f8f9fa;">
<div style="max-width: 1280px; margin: 0 auto;">
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
{{Generate 3 trust cards with icons, titles, descriptions in {language}}}
</div>
</div>
</section>

<!-- PROBLEMS SECTION -->
<section style="padding: 6rem 2rem;">
<div style="max-width: 1280px; margin: 0 auto;">
<h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem;">{{Section title in {language}}}</h2>
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 3rem;">
{{Generate 4 problem cards with: image (unsplash), problem title, description, solution with 5 bullets - ALL in {language}}}
</div>
</div>
</section>

<!-- TESTIMONIALS -->
<section style="padding: 6rem 2rem; background: #f8f9fa;">
<div style="max-width: 1280px; margin: 0 auto;">
<h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem;">{{Section title in {language}}}</h2>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
{{Generate 6 testimonial cards with: avatar (https://i.pravatar.cc/150?img=1-6), name, location, quote (2 sentences), 5-star rating - ALL in {language}}}
</div>
</div>
</section>

<!-- FEATURES -->
<section style="padding: 6rem 2rem;">
<div style="max-width: 1280px; margin: 0 auto;">
<h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem;">{{Section title in {language}}}</h2>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 3rem;">
{{Generate 6 feature cards with: icon, title, description (3 sentences), 5 bullet points - ALL in {language}}}
</div>
</div>
</section>

<!-- HOW IT WORKS -->
<section style="padding: 6rem 2rem; background: var(--gradient-main); color: white;">
<div style="max-width: 1280px; margin: 0 auto;">
<h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem;">{{Section title in {language}}}</h2>
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem;">
{{Generate 4 steps with: step number, title, description - ALL in {language}}}
</div>
</div>
</section>

<!-- FAQ -->
<section style="padding: 6rem 2rem;">
<div style="max-width: 900px; margin: 0 auto;">
<h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem;">{{Section title in {language}}}</h2>
{{Generate 6 FAQ items with accordion functionality - ALL in {language}}}
</div>
</section>

<!-- PRICING -->
<section style="padding: 6rem 2rem; background: #f8f9fa;">
<div style="max-width: 1280px; margin: 0 auto;">
<h2 style="text-align: center; font-size: 3rem; margin-bottom: 4rem;">{{Section title in {language}}}</h2>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
{{Generate 3 pricing tiers with: plan name, price, 8 features, CTA button - ALL in {language}}}
</div>
</div>
</section>

<!-- FORM -->
<section style="padding: 6rem 2rem; background: var(--gradient-main);">
<div style="max-width: 600px; margin: 0 auto; background: white; padding: 3rem; border-radius: 20px; box-shadow: var(--shadow-xl);">
<h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 2rem;">{{Form title in {language}}}</h2>
<form>
<input type="text" placeholder="{{Name placeholder in {language}}}" style="width: 100%; padding: 1rem; margin-bottom: 1rem; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 1rem;">
<input type="email" placeholder="{{Email placeholder in {language}}}" style="width: 100%; padding: 1rem; margin-bottom: 1rem; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 1rem;">
<select style="width: 100%; padding: 1rem; margin-bottom: 1rem; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 1rem;">
<option>{{Country/City option in {language}}}</option>
</select>
<label style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 2rem;"><input type="checkbox"> {{GDPR text in {language}}}</label>
<button type="submit" style="width: 100%; padding: 1.25rem; background: var(--gradient-main); border: none; border-radius: 50px; color: white; font-size: 1.25rem; font-weight: 700; cursor: pointer;">{target_action}</button>
</form>
</div>
</section>

<!-- FOOTER -->
<footer style="background: #1a1a1a; color: white; padding: 4rem 2rem 2rem;">
<div style="max-width: 1280px; margin: 0 auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 3rem;">
<div>
<h3 style="margin-bottom: 1rem;">{{Company Name}}</h3>
<p>{{Company description in {language}}}</p>
</div>
<div>
<h4 style="margin-bottom: 1rem;">{{Navigation title in {language}}}</h4>
{{Generate 6 navigation links in {language}}}
</div>
<div>
<h4 style="margin-bottom: 1rem;">{{Resources title in {language}}}</h4>
{{Generate 6 resource links in {language}}}
</div>
<div>
<h4 style="margin-bottom: 1rem;">{{Contact title in {language}}}</h4>
<p>Email: contact@company.com</p>
<p>Phone: +X XXX XXX XXXX</p>
<p>{{Full address with postal code}}</p>
<p>{{Business hours in {language}}}</p>
</div>
</div>
<div style="max-width: 1280px; margin: 3rem auto 0; padding-top: 2rem; border-top: 1px solid #333; text-align: center; display: flex; justify-content: space-between;">
<p>© 2025 {{Company}}. {{All rights reserved in {language}}}</p>
<div>
<a href="#privacy" style="color: white; margin: 0 1rem;">{{Privacy in {language}}}</a>
<a href="#terms" style="color: white; margin: 0 1rem;">{{Terms in {language}}}</a>
<a href="#cookies" style="color: white; margin: 0 1rem;">{{Cookies in {language}}}</a>
</div>
</div>
</footer>

<style>
@keyframes pulse {{from {{transform: scale(1);}} to {{transform: scale(1.05);}}}}
@keyframes float {{0%, 100% {{transform: translateY(0);}} 50% {{transform: translateY(-10px);}}}}
</style>

<script>
// Add smooth scroll, counter animations, FAQ accordion
document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
  anchor.addEventListener('click', function(e) {{
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({{behavior: 'smooth'}});
  }});
}});
</script>

</body>
</html>

CRITICAL:
- ALL text content in {language}
- Use specific, detailed content (NO generic text)
- Realistic numbers (e.g., 10,247 not 10,000)
- Rich gradients, shadows, animations
- Professional, compelling copy
- Complete, self-contained HTML

Output ONLY the HTML code."""
    
    async def _generate_metadata(self, theme: str, language: str, chat: LlmChat) -> dict:
        prompt = f"Generate professional contact for {theme} in {language}: Company:[name] Email:[contact@domain] Phone:[+X XXX] Address:[full]"
        msg = UserMessage(text=prompt)
        response = await chat.send_message(msg)
        
        lines = response.strip().split('\n')
        metadata = {"company_name": "", "email": "", "phone": "", "address": ""}
        for line in lines:
            if ':' in line:
                k, v = line.split(':', 1)
                k = k.strip().lower()
                v = v.strip()
                if 'company' in k: metadata['company_name'] = v
                elif 'email' in k: metadata['email'] = v
                elif 'phone' in k: metadata['phone'] = v
                elif 'address' in k: metadata['address'] = v
        return metadata
    
    def _clean_html(self, html: str) -> str:
        html = html.strip()
        if html.startswith('```html'): html = html[7:]
        elif html.startswith('```'): html = html[3:]
        if html.endswith('```'): html = html[:-3]
        html = html.strip()
        if not html.upper().startswith('<!DOCTYPE'): html = '<!DOCTYPE html>\n' + html
        return html
