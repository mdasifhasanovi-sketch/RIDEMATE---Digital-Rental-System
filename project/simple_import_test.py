print("Attempting to import ridemate...")
try:
    import ridemate
    print("✅ Successfully imported ridemate module")
except Exception as e:
    print(f"❌ Error importing ridemate: {e}")
