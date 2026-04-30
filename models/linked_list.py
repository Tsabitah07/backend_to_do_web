"""
models/linked_list.py
─────────────────────
Model layer: definisi Node dan LinkedList (struktur data murni).
Tidak ada logika bisnis di sini — hanya representasi data.
"""

from __future__ import annotations
from typing import Optional
from datetime import datetime
import uuid


class Node:
    """
    Satu elemen dalam Singly Linked List.
    Menyimpan data task dan pointer ke node berikutnya.
    """

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        status: str = "todo",
        task_id: Optional[str] = None,
    ) -> None:
        self.task_id: str = task_id or str(uuid.uuid4())
        self.title: str = title
        self.description: str = description
        self.priority: str = priority          # "low" | "medium" | "high"
        self.status: str = status              # "todo" | "in_progress" | "done"
        self.completed: bool = (status == "done")
        self.created_at: str = datetime.now().isoformat()
        self.next: Optional[Node] = None       # ← pointer ke node berikutnya

    # ── Serialisasi ──────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "task_id":     self.task_id,
            "title":       self.title,
            "description": self.description,
            "priority":    self.priority,
            "status":      self.status,
            "completed":   self.completed,
            "created_at":  self.created_at,
        }

    def __repr__(self) -> str:  # pragma: no cover
        nxt = self.next.task_id[:8] if self.next else "NULL"
        return f"Node({self.task_id[:8]}… → {nxt})"


class LinkedList:
    """
    Singly Linked List untuk menyimpan urutan task.

    Operasi yang tersedia
    ─────────────────────
    append(node)              – tambah di akhir          O(n)
    prepend(node)             – tambah di awal           O(1)
    insert_after(id, node)    – sisipkan setelah node    O(n)
    delete(task_id)           – hapus node               O(n)
    find(task_id)             – cari node by ID          O(n)
    move_to_head(task_id)     – pindah ke posisi HEAD    O(n)
    to_list()                 – traverse → list[dict]    O(n)
    """

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self._size: int = 0

    # ── INSERT ───────────────────────────────────────────────────────────────

    def append(self, node: Node) -> None:
        """Tambahkan node di akhir list (tail insert) — O(n)."""
        node.next = None
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node
        self._size += 1

    def prepend(self, node: Node) -> None:
        """Tambahkan node di awal list (head insert) — O(1)."""
        node.next = self.head
        self.head = node
        self._size += 1

    def insert_after(self, target_id: str, new_node: Node) -> bool:
        """Sisipkan new_node tepat setelah node ber-id target_id — O(n)."""
        cur = self.head
        while cur:
            if cur.task_id == target_id:
                new_node.next = cur.next
                cur.next = new_node
                self._size += 1
                return True
            cur = cur.next
        return False

    # ── DELETE ───────────────────────────────────────────────────────────────

    def delete(self, task_id: str) -> bool:
        """Hapus node berdasarkan task_id — O(n)."""
        if self.head is None:
            return False
        if self.head.task_id == task_id:
            self.head = self.head.next
            self._size -= 1
            return True
        cur = self.head
        while cur.next:
            if cur.next.task_id == task_id:
                cur.next = cur.next.next
                self._size -= 1
                return True
            cur = cur.next
        return False

    # ── SEARCH ───────────────────────────────────────────────────────────────

    def find(self, task_id: str) -> Optional[Node]:
        """Cari dan kembalikan node berdasarkan task_id — O(n)."""
        cur = self.head
        while cur:
            if cur.task_id == task_id:
                return cur
            cur = cur.next
        return None

    # ── REORDER ──────────────────────────────────────────────────────────────

    def move_to_head(self, task_id: str) -> bool:
        """Pindahkan node ke posisi HEAD tanpa mengubah urutan node lain — O(n)."""
        if self.head is None or self.head.task_id == task_id:
            return True
        cur = self.head
        while cur.next:
            if cur.next.task_id == task_id:
                node = cur.next
                cur.next = node.next
                node.next = self.head
                self.head = node
                return True
            cur = cur.next
        return False

    # ── UTILITY ──────────────────────────────────────────────────────────────

    def to_list(self) -> list[dict]:
        """Traverse seluruh list dan kembalikan sebagai array of dict — O(n)."""
        result, cur = [], self.head
        while cur:
            result.append(cur.to_dict())
            cur = cur.next
        return result

    def to_viz(self) -> list[dict]:
        """Kembalikan metadata tiap node untuk keperluan visualisasi."""
        result, cur, idx = [], self.head, 0
        while cur:
            result.append({
                "index":    idx,
                "task_id":  cur.task_id,
                "title":    cur.title,
                "has_next": cur.next is not None,
                "next_id":  cur.next.task_id if cur.next else None,
            })
            cur = cur.next
            idx += 1
        return result

    @property
    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.head is None

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:  # pragma: no cover
        nodes = " → ".join(n["task_id"][:8] for n in self.to_viz())
        return f"LinkedList({nodes} → NULL, size={self._size})"
