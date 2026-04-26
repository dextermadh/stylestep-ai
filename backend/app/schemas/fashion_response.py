from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
import re

class ColorDetail(BaseModel): 
    hex: str = Field(..., description="hex color code of the item")
    name: str = Field(..., description="Color in Name")

    @field_validator('hex')
    @classmethod
    def validate_hex(cls, v: str) -> str: 
        # this will automatically fixes common AI mistakes (missing # or extra spaces)
        v = v.strip()
        if v.lower() == 'null' or not v: 
            return "#000000" # fallback for invalid AI output
        if not v.startswith('#'): 
            v = f'#{v}'
        if not re.match(r'^#[0-9a-fA-F]{6}$', v):
            raise ValueError('Invalid hex code provided')
        return v

class OutfitItem(BaseModel): 
    color_name: str
    hex: str
    reason: str

    @field_validator('hex')
    @classmethod
    def validate_hex(cls, v: str) -> str: 
        v = v.strip()
        if v.lower() == 'null' or not v: 
            return "#000000"
        if not v.startswith('#'): 
            v = f'#{v}'
        if not re.match(r'^#[0-9a-fA-F]{6}$', v):
            raise ValueError('Invalid hex code provided')
        return v

class ShoeAnalysis(BaseModel): 
    model_style: str
    material_composition: str
    perceived_vibe: str

class ColorPalette(BaseModel): 
    dominant: ColorDetail
    accents: List[ColorDetail]

class CoordinatedOutfits(BaseModel): 
    trousers: List[OutfitItem]
    shirts: List[OutfitItem]

class Metadata(BaseModel): 
    lighting_assessment: str
    confidence_score: float = Field(ge=0, le=1)

class StyleStepAnalysis(BaseModel): 
    '''
    this is the main response schema for StyleStep AI
    this matches the heirarchial JSON structure returned by our local Modal (Gemma 4 E2B)
    '''
    model_config = ConfigDict(populated_by_name=True)

    is_footwear: bool = Field(..., description='True if the image contains shoes, otherwise False')

    shoe_analysis: Optional[ShoeAnalysis] = None
    color_palette: Optional[ColorPalette] = None
    coordinated_outfits: Optional[CoordinatedOutfits] = None
    metadata: Metadata


    