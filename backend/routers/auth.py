from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)