import ridemate

def test_ridemate():
    # Initialize the system
    print("Initializing system...")
    ridemate.init_system()
    
    # Test authentication
    print("\nTesting customer authentication...")
    customer_id = ridemate.authenticate_customer("user1", "password123")
    if customer_id > 0:
        print(f"✅ Successfully logged in as customer ID: {customer_id}")
        
        # Test getting available vehicles
        print("\nFetching available vehicles...")
        try:
            vehicles = ridemate.get_available_vehicles()
            print(f"✅ Found {len(vehicles)} available vehicles:")
            for i, vehicle in enumerate(vehicles, 1):
                print(f"   {i}. {vehicle['make']} {vehicle['model']} - ${vehicle['rate_per_day']}/day")
        except Exception as e:
            print(f"❌ Error getting vehicles: {e}")
        
        # Save all data
        print("\nSaving data...")
        ridemate.save_all()
        print("✅ Data saved successfully")
    else:
        print("❌ Authentication failed. Please check your credentials.")

if __name__ == "__main__":
    test_ridemate()
