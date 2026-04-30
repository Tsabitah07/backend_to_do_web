"""
controllers/task_controller.py
──────────────────────────────
Controller layer: semua logika bisnis ada di sini.
Menerima data dari router, memanipulasi model (LinkedList),
dan mengembalikan hasil. Tidak ada detail HTTP di sini.
"""

from fastapi import HTTPException
from models import LinkedList, Node, TaskCreate, TaskUpdate


class TaskController:
    """
    Mengenkapsulasi semua operasi CRUD + linked-list operations.
    Satu instance di-share untuk seluruh sesi (in-memory store).
    """

    def __init__(self) -> None:
        self._list = LinkedList()
        self._seed()

    # ── SEED ─────────────────────────────────────────────────────────────────

    def _seed(self) -> None:
        seeds = [
            ("Belajar Struktur Data", "Implementasi Linked List di Python & visualisasi node-by-node", "high", "in_progress"),
            ("Review Pull Request", "Cek kode teman, berikan komentar konstruktif di GitHub", "medium", "todo"),
            ("Olahraga Pagi", "Lari 30 menit di taman, pemanasan dulu 5 menit", "low", "done"),
            ("Meeting Sprint Planning", "Siapkan backlog & estimasi story points sebelum meeting", "high", "todo"),
        ]
        for title, desc, priority, status in seeds:
            self._list.append(Node(title=title, description=desc, priority=priority, status=status))

    # ── READ ─────────────────────────────────────────────────────────────────

    def get_all(self) -> dict:
        """Traverse linked list dan kembalikan seluruh task."""
        return {
            "tasks":     self._list.to_list(),
            "total":     self._list.size,
            "structure": "Singly Linked List",
        }

    def get_by_id(self, task_id: str) -> dict:
        """Cari task berdasarkan ID — O(n) traversal."""
        node = self._list.find(task_id)
        if not node:
            raise HTTPException(status_code=404, detail=f"Task '{task_id}' tidak ditemukan")
        return node.to_dict()

    def get_visualization(self) -> dict:
        """Kembalikan metadata tiap node untuk keperluan visualisasi."""
        return {
            "head":  self._list.head.task_id if self._list.head else None,
            "nodes": self._list.to_viz(),
            "size":  self._list.size,
        }

    # ── CREATE ───────────────────────────────────────────────────────────────

    def create(self, payload: TaskCreate) -> dict:
        """
        Tambah task baru ke linked list.
        Posisi insert ditentukan oleh payload.position:
          "start"    → prepend  O(1)
          "end"      → append   O(n)
          <task_id>  → insert_after  O(n)
        """
        new_node = Node(
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=payload.status,
        )

        if payload.position == "start":
            self._list.prepend(new_node)
            op = "prepend — O(1)"
        elif payload.position == "end":
            self._list.append(new_node)
            op = "append — O(n)"
        else:
            if not self._list.insert_after(payload.position, new_node):
                raise HTTPException(
                    status_code=404,
                    detail=f"Node target '{payload.position}' tidak ditemukan untuk insert_after",
                )
            op = f"insert_after({payload.position[:8]}…) — O(n)"

        return {
            "task":      new_node.to_dict(),
            "operation": op,
            "list_size": self._list.size,
        }

    # ── UPDATE ───────────────────────────────────────────────────────────────

    def update(self, task_id: str, payload: TaskUpdate) -> dict:
        """Update field task secara in-place tanpa mengubah posisi node."""
        node = self._list.find(task_id)
        if not node:
            raise HTTPException(status_code=404, detail=f"Task '{task_id}' tidak ditemukan")

        if payload.title       is not None: node.title       = payload.title
        if payload.description is not None: node.description = payload.description
        if payload.priority    is not None: node.priority    = payload.priority
        if payload.status      is not None:
            node.status    = payload.status
            node.completed = (payload.status == "done")
        if payload.completed   is not None:
            node.completed = payload.completed
            if payload.completed:
                node.status = "done"
            elif node.status == "done":
                node.status = "todo"

        return {"task": node.to_dict(), "operation": "update in-place — O(n)", "list_size": self._list.size}

    # ── DELETE ───────────────────────────────────────────────────────────────

    def delete(self, task_id: str) -> dict:
        """Hapus node dari linked list — O(n)."""
        if not self._list.delete(task_id):
            raise HTTPException(status_code=404, detail=f"Task '{task_id}' tidak ditemukan")
        return {
            "message":   "Task berhasil dihapus",
            "operation": "delete — O(n)",
            "list_size": self._list.size,
        }

    # ── REORDER ──────────────────────────────────────────────────────────────

    def move_to_top(self, task_id: str) -> dict:
        """Pindahkan node ke posisi HEAD — O(n)."""
        if not self._list.move_to_head(task_id):
            raise HTTPException(status_code=404, detail=f"Task '{task_id}' tidak ditemukan")
        node = self._list.find(task_id)
        return {
            "task":      node.to_dict(),
            "operation": "move_to_head — O(n)",
            "list_size": self._list.size,
        }


# ── Singleton instance (shared across requests) ───────────────────────────────
task_controller = TaskController()
