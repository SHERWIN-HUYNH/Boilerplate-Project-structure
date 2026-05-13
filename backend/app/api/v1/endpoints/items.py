from fastapi import APIRouter

router = APIRouter()


@router.get("")
def list_items() -> list[dict[str, str]]:
    return []
