"""
16_test_portal.py

Test the HispeedCity Portal client.
"""

import sys
from pathlib import Path

# ============================================================
# Add project root to Python path
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# Import Portal Client
# ============================================================

from backend.portal.portal_client import PortalClient


# ============================================================
# Test Portal
# ============================================================

print("=" * 60)
print("HispeedCity Portal Test")
print("=" * 60)

portal = PortalClient()

print("\nPortal client loaded successfully.")

# ------------------------------------------------------------
# Test customer
# ------------------------------------------------------------

test_vehicle = "ABC1234"

print("\nChecking vehicle:", test_vehicle)

try:

    result = portal.get_parking_status(test_vehicle)

    print("\nPortal Result:")
    print("-" * 60)
    print(result)

except Exception as e:

    print("\nPortal Error:")
    print("-" * 60)
    print(type(e).__name__)
    print(str(e))


print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)