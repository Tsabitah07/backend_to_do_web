"""
routers/ll_router.py
────────────────────
Router untuk endpoint visualisasi / debugging linked list.
"""

from fastapi import APIRouter
from controllers import task_controller

router = APIRouter(prefix="/linked-list", tags=["Linked List"])


@router.get("/visualize", summary="Visualisasi struktur linked list")
def visualize():
    return task_controller.get_visualization()
