"""
Test Portal Service
"""

from backend.portal.portal_service import PortalService


print("=" * 60)
print("HispeedCity Portal Service Test")
print("=" * 60)


service = PortalService()


# =========================================================
# Test 1: Active parking
# =========================================================

print("\n")
print("=" * 60)
print("TEST 1: Active Parking")
print("=" * 60)

vehicle = "ABC1234"

result = service.check_parking(vehicle)

print("\nVehicle:", vehicle)
print("Result:")
print(result)


# =========================================================
# Test 2: Expired parking
# =========================================================

print("\n")
print("=" * 60)
print("TEST 2: Expired Parking")
print("=" * 60)

vehicle = "XYZ5678"

result = service.check_parking(vehicle)

print("\nVehicle:", vehicle)
print("Result:")
print(result)


# =========================================================
# Test 3: Unknown vehicle
# =========================================================

print("\n")
print("=" * 60)
print("TEST 3: Unknown Vehicle")
print("=" * 60)

vehicle = "UNKNOWN123"

result = service.check_parking(vehicle)

print("\nVehicle:", vehicle)
print("Result:")
print(result)


# =========================================================
# Test 4: Barrier - active vehicle
# =========================================================

print("\n")
print("=" * 60)
print("TEST 4: Barrier - Active Vehicle")
print("=" * 60)

vehicle = "ABC1234"

result = service.check_barrier(vehicle)

print("\nVehicle:", vehicle)
print("Result:")
print(result)


# =========================================================
# Test 5: Barrier - expired vehicle
# =========================================================

print("\n")
print("=" * 60)
print("TEST 5: Barrier - Expired Vehicle")
print("=" * 60)

vehicle = "XYZ5678"

result = service.check_barrier(vehicle)

print("\nVehicle:", vehicle)
print("Result:")
print(result)


print("\n")
print("=" * 60)
print("TEST COMPLETED")
print("=" * 60)