import json
import threading
from pathlib import Path

_lock = threading.Lock()
_file = Path(__file__).resolve().parent.parent / 'history.json'


def append_entry(entry: dict):
    """Append an entry to history.json in a thread-safe way."""
    with _lock:
        history = []
        if _file.exists():
            try:
                history = json.loads(_file.read_text(encoding='utf-8'))
            except Exception:
                history = []
        history.insert(0, entry)
        # keep only last 50
        history = history[:50]
        _file.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding='utf-8')


def read_history():
    with _lock:
        if not _file.exists():
            return []
        try:
            return json.loads(_file.read_text(encoding='utf-8'))
        except Exception:
            return []


def delete_entry(index: int):
    with _lock:
        history = []
        if _file.exists():
            try:
                history = json.loads(_file.read_text(encoding='utf-8'))
            except Exception:
                history = []
        if 0 <= index < len(history):
            history.pop(index)
            _file.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding='utf-8')


def clear_history():
    with _lock:
        if _file.exists():
            _file.write_text('[]', encoding='utf-8')


def update_entry(index: int, updates: dict):
    """Update a history entry at index with keys from updates."""
    with _lock:
        history = []
        if _file.exists():
            try:
                history = json.loads(_file.read_text(encoding='utf-8'))
            except Exception:
                history = []
        if 0 <= index < len(history):
            entry = history[index]
            entry.update(updates)
            history[index] = entry
            _file.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding='utf-8')


def stats():
    """Return simple stats: counts per project and per mode."""
    with _lock:
        try:
            history = json.loads(_file.read_text(encoding='utf-8'))
        except Exception:
            history = []
    projects = {}
    modes = {}
    for h in history:
        p = h.get('project') or 'default'
        m = h.get('mode') or 'screenplay'
        projects[p] = projects.get(p, 0) + 1
        modes[m] = modes.get(m, 0) + 1
    return {'projects': projects, 'modes': modes, 'total': len(history)}
