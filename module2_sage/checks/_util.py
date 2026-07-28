"""Shared helpers for check scripts. Nothing to edit here."""
import sys
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))


def ok(msg):
    print(f"  ✅ {msg}")


def fail(msg, hint=None):
    print(f"  ❌ {msg}")
    if hint:
        print(f"     💡 {hint}")
    sys.exit(1)


def done(step):
    print(f"\n✅ {step} looks right. On to the next section of the README.")


def _friendly_crash(exc_type, exc, tb):
    import traceback

    traceback.print_exception(exc_type, exc, tb)
    print(
        "\n💡 The check crashed inside your step file — the traceback above "
        "points at the code that isn't finished (or isn't right) yet. "
        "An unfilled `...` or a leftover `raise NotImplementedError` is the "
        "usual suspect.",
        file=sys.stderr,
    )


sys.excepthook = _friendly_crash
