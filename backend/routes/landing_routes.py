from fastapi import APIRouter, HTTPException
from models import LandingPageCreate, LandingPage, LandingPageMetadata
from landing_generator_v3 import LandingPageGenerator
from typing import List
import uuid
from datetime import datetime

router = APIRouter()
generator = LandingPageGenerator()

# In-memory storage (for MVP, will use MongoDB later)
landings_db = {}

@router.post("/generate-landing", response_model=LandingPage)
async def generate_landing(request: LandingPageCreate):
    """
    Generate a new landing page using AI
    """
    try:
        # Generate landing page
        result = await generator.generate_landing_page(
            theme=request.theme,
            language=request.language,
            traffic_source=request.traffic_source,
            target_action=request.target_action
        )
        
        # Create landing page object
        landing = LandingPage(
            id=str(uuid.uuid4()),
            theme=request.theme,
            language=request.language,
            traffic_source=request.traffic_source,
            target_action=request.target_action,
            html=result['html'],
            lighthouse=result['lighthouse'],
            created_at=datetime.utcnow(),
            metadata=LandingPageMetadata(**result['metadata'])
        )
        
        # Store in database
        landings_db[landing.id] = landing
        
        return landing
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating landing page: {str(e)}")

@router.get("/landings/{landing_id}", response_model=LandingPage)
async def get_landing(landing_id: str):
    """
    Get a specific landing page by ID
    """
    if landing_id not in landings_db:
        raise HTTPException(status_code=404, detail="Landing page not found")
    
    return landings_db[landing_id]

@router.get("/landings", response_model=List[LandingPage])
async def get_all_landings():
    """
    Get all generated landing pages
    """
    return list(landings_db.values())