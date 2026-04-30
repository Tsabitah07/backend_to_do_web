"""
routers/task_router.py
──────────────────────
Router layer: hanya mendefinisikan endpoint HTTP.
Semua logika bisnis didelegasikan ke TaskController.
"""

from fastapi import APIRouter
from models import TaskCreate, TaskUpdate
from controllers import task_controller

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", summary="Ambil semua task")
def get_tasks():
    return task_controller.get_all()


@router.post("", status_code=201, summary="Tambah task baru")
def create_task(body: TaskCreate):
    return task_controller.create(body)


@router.get("/{task_id}", summary="Cari task by ID")
def get_task(task_id: str):
    return task_controller.get_by_id(task_id)


@router.patch("/{task_id}", summary="Update task")
def update_task(task_id: str, body: TaskUpdate):
    return task_controller.update(task_id, body)


@router.delete("/{task_id}", summary="Hapus task")
def delete_task(task_id: str):
    return task_controller.delete(task_id)


@router.patch("/{task_id}/move-top", summary="Pindah ke HEAD")
def move_to_top(task_id: str):
    return task_controller.move_to_top(task_id)
