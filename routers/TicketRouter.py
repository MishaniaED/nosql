from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from models.Ticket import Ticket
from services.TicketService import TicketService

router = APIRouter()


@router.post("/book/{id}", response_model=bool, responses={
    404: {"description": "Ticket not found"},
    400: {"description": "Ticket already booked or purchased"},
    503: {"description": "Failed to lock ticket"},
    500: {"description": "Server error"},
})
async def book_ticket(ticket_id: int):
    try:
        result = await TicketService.book_ticket(ticket_id)
        return result
    except Exception as e:
        if "Ticket not found" in str(e):
            raise HTTPException(status_code=404, detail="Ticket not found")
        elif "Ticket already booked or purchased" in str(e):
            raise HTTPException(status_code=400, detail="Ticket already booked or purchased")
        elif "Failed to lock ticket" in str(e):
            raise HTTPException(status_code=503, detail="Failed to lock ticket")
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.post("/purchase/{id}", response_model=bool, responses={
    404: {"description": "Ticket not found"},
    400: {"description": "Ticket not booked"},
    500: {"description": "Payment processing error"},
})
async def purchase_ticket(ticket_id: int):
    try:
        result = await TicketService.purchase_ticket(ticket_id)
        return result
    except Exception as e:
        if "Ticket not found" in str(e):
            raise HTTPException(status_code=404, detail="Ticket not found")
        elif "Ticket not booked" in str(e):
            raise HTTPException(status_code=400, detail="Ticket not booked")
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/search-tickets/", response_model=List[Ticket])
async def search_tickets_route(train_id: int, status: str, comfort_class: str):  ### ПАРАМЕТРЫ ПОИСКА
    try:
        return await TicketService.search_tickets(train_id, status, comfort_class)  ### ПАРАМЕТРЫ ПОИСКА
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=Ticket, responses={
    404: {"description": "Ticket not found"},
    500: {"description": "Server error"},
})
async def get_ticket(ticket_id: int):
    try:
        result = await TicketService.get_ticket(ticket_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return Ticket(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=Ticket, responses={
    409: {"description": "Ticket with this ID already exists"}
})
async def add_ticket(ticket_request: Ticket):
    try:
        result = await TicketService.add_ticket(ticket_request)
        if result is None:
            raise HTTPException(status_code=409, detail="Ticket with this ID already exists")
        return Ticket(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
