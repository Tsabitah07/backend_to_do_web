"""
main.py
───────
Entry point aplikasi FastAPI.
Hanya mendaftarkan router — tidak ada logika bisnis di sini.

Arsitektur MVC:
  Model      → models/linked_list.py  (struktur data & schemas)
  Controller → controllers/task_controller.py  (logika bisnis)
  Router     → routers/task_router.py, ll_router.py  (HTTP layer)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import task_router, ll_router

app = FastAPI(
    title="TaskChain API — MVC + Linked List",
    description="To-Do app menggunakan Singly Linked List. Arsitektur Model-Controller-Router.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ──────────────────────────────────────────────────────────
app.include_router(task_router)
app.include_router(ll_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "app":          "TaskChain API",
        "version":      "2.0.0",
        "architecture": "MVC (Model → Controller → Router)",
        "data_structure": "Singly Linked List",
        "docs":         "/docs",
    }
