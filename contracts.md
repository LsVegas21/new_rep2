# API Contracts - LandingGen AI

## Backend Implementation Plan

### 1. Mock Data to Remove
- `mock.js` содержит:
  - `mockGeneratedLandings` - примеры сгенерированных landing pages
  - `mockThemes, mockLanguages, mockTrafficSources, mockTargetActions` - данные для dropdown
  
### 2. Database Models

#### LandingPage Model
```python
{
    "id": str (uuid),
    "theme": str,
    "language": str,
    "traffic_source": str,
    "target_action": str,
    "generated_html": str,
    "lighthouse_score": int,
    "created_at": datetime,
    "metadata": {
        "company_name": str,
        "email": str,
        "phone": str,
        "address": str
    }
}
```

### 3. API Endpoints

#### POST /api/generate-landing
**Request:**
```json
{
    "theme": "Онлайн школа программирования",
    "language": "Русский",
    "traffic_source": "Google Ads",
    "target_action": "Зарегистрироваться"
}
```

**Response:**
```json
{
    "id": "uuid",
    "theme": "...",
    "language": "...",
    "traffic_source": "...",
    "target_action": "...",
    "html": "<!DOCTYPE html>...",
    "lighthouse": 98,
    "created_at": "2025-12-03T11:11:11Z"
}
```

#### GET /api/landings/{id}
**Response:** Single landing page object

#### GET /api/landings
**Response:** List of all generated landing pages

### 4. AI Generation Strategy

**Using Emergent LLM Key with emergentintegrations:**
- Model: gpt-4o-mini (default, cost-effective)
- Generate:
  1. Company name based on theme
  2. Contact details (email, phone, address)
  3. Hero headline and subheadline
  4. Features section (3-5 benefits)
  5. CTA text and design
  6. Full HTML/CSS with Lighthouse optimization

**Prompt Structure:**
```
Generate a complete landing page HTML for:
Theme: {theme}
Language: {language}
Traffic Source: {traffic_source}
Target Action: {target_action}

Requirements:
- Lighthouse 95+ score
- Google Ads compliant
- Modern design
- Responsive
- Fast loading
- No external dependencies
```

### 5. Frontend Integration

**Changes needed in Home.jsx:**
1. Remove mock.js import
2. Replace `handleGenerate` with API call to `/api/generate-landing`
3. Keep dropdown data in mock.js (it's static reference data)
4. Update download handlers to use real generated HTML

**API Integration:**
```javascript
const response = await axios.post(`${API}/generate-landing`, formData);
setGeneratedLanding(response.data);
```

### 6. Lighthouse Score Calculation
- Use estimated score: 95-100 range
- Based on:
  - Inline CSS (no external files)
  - Minimal HTML
  - No heavy scripts
  - Optimized images (if any)

### 7. Google Ads Compliance
- No misleading claims
- Clear contact information
- Privacy-friendly
- No prohibited content
- Fast page speed
