from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.llm_service import llm_service
from app.schemas.fashion_response import StyleStepAnalysis

router = APIRouter() 

@router.post('/analyze', response_model=StyleStepAnalysis)
async def analyze_shoe(file: UploadFile = File(...)):
    # validate the file type
    if not file.content_type.startswith('image/'): 
        raise HTTPException(status_code=400, detail='File provided is not an Image')

    try: 
        # read the file bytes
        image_bytes = await file.read() 

        # call the llm service
        analysis = await llm_service.analyze_image(image_bytes)

        if not analysis.is_footwear or analysis.metadata.confidence_score < 0.4:
            raise HTTPException(
                status_code=400,
                detail='No footwear detected. Please upload a clear photo of your shoes.'
            )
        else: 
            return analysis

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e: 
        print(f'Error during the analysis: {str(e)}')
        raise HTTPException(
            status_code=500,
            detail='AI Analysis failed, Please ensure the necessary LLM service is running.'
        ) 
    finally: 
        await file.close() 