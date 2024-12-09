from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, Response

router = APIRouter()

@router.get("/events/csv")
async def export_csv():
    csv_content = "id,title,start_time,end_time\n1,Event 1,2024-03-21T14:00:00,2024-03-21T15:00:00"
    return PlainTextResponse(content=csv_content, media_type="text/csv")

@router.get("/events/pdf")
async def export_pdf():
    # Simuler un PDF vide
    return Response(content=b"%PDF-1.4\n%EOF", media_type="application/pdf") 