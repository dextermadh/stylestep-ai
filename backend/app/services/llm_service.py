import httpx
import json
import base64
from app.core.config import settings
from app.schemas.fashion_response import StyleStepAnalysis

class LLMService: 
    def __init__(self): 
        # pointing our local lm studio instance
        self.url = f'{settings.LM_STUDIO_URL}/chat/completions'
        self.model = settings.MODEL_NAME

    async def analyze_image(self, image_bytes: bytes) -> StyleStepAnalysis:
        '''
        this function will send an image to local Gemma model and then validates the JSON output,
        and returns a StyleStepAnalysis object
        '''
        # encode image to base64
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')

        # define the JSON schema we want from the model
        fashion_schema = {
            "type": "object",
            "properties": {
                "is_footwear": {"type": "boolean", "description": "True if the image contains shoes, otherwise False"},
                "shoe_analysis": {
                    "type": "object",
                    "properties": {
                        "model_style": {"type": "string"},
                        "material_composition": {"type": "string"},
                        "perceived_vibe": {"type": "string"}
                    },
                    "required": ["model_style", "material_composition", "perceived_vibe"]
                },
                "color_palette": {
                    "type": "object",
                    "properties": {
                        "dominant": {
                            "type": "object",
                            "properties": {
                                "hex": {"type": "string"},
                                "name": {"type": "string"}
                            },
                            "required": ["hex", "name"]
                        },
                        "accents": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "hex": {"type": "string"},
                                    "name": {"type": "string"}
                                },
                                "required": ["hex", "name"]
                            }
                        }
                    },
                    "required": ["dominant", "accents"]
                },
                "coordinated_outfits": {
                    "type": "object",
                    "properties": {
                        "trousers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "color_name": {"type": "string"},
                                    "hex": {"type": "string"},
                                    "reason": {"type": "string"}
                                },
                                "required": ["color_name", "hex", "reason"]
                            }
                        },
                        "shirts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "color_name": {"type": "string"},
                                    "hex": {"type": "string"},
                                    "reason": {"type": "string"}
                                },
                                "required": ["color_name", "hex", "reason"]
                            }
                        }
                    },
                    "required": ["trousers", "shirts"]
                },
                "metadata": {
                    "type": "object",
                    "properties": {
                        "lighting_assessment": {"type": "string"},
                        "confidence_score": {"type": "number"}
                    },
                    "required": ["lighting_assessment", "confidence_score"]
                }
            },
            "required": ["is_footwear", "shoe_analysis", "color_palette", "coordinated_outfits", "metadata"]
        }

        # construct the payload
        payload = {
            'model': self.model,
            'messages': [
                {'role': 'system', 'content': settings.SYSTEM_PROMPT},
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': 'Analyse this footwear for StyleStep AI'
                        },
                        {
                            'type': 'image_url',
                            'image_url': {'url': f'data:image/jpeg;base64, {image_b64}'}
                        }
                    ]
                }
            ],
            'temperature': 0.1,
            'response_format': {
                'type': 'json_schema',
                'json_schema': {
                    'name': 'fashion_analysis_schema',
                    'schema': fashion_schema
                }
            }
        }
        

        # execute the API call
        async with httpx.AsyncClient(timeout=300.0) as client: 
            try: 
                response = await client.post(self.url, json=payload)
                response.raise_for_status()
            except httpx.RequestException as e:
                raise HTTPException(status_code=502, detail=f"LLM Service Unavailable: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Unexpected LLM Error: {str(e)}")

            
            result = response.json()
            raw_content = result['choices'][0]['message']['content']
            
            # parse string to dict
            try: 
                data = json.loads(raw_content)
            except json.JSONDecodeError as e:
                raise HTTPException(status_code=500, detail=f"Invalid JSON from LLM: {str(e)}")

            # if the model says it is not a footwear, we nullify the fashion fields 
            # this prevents pydantic validation errors if the model returned "null" strings
            if not data.get('is_footwear', True): 
                data['shoe_analysis'] = None
                data['color_palette'] = None
                data['coordinated_outfits'] = None

            return StyleStepAnalysis(**data)

llm_service = LLMService()
