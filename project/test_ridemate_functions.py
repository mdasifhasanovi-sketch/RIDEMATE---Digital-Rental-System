import ridemate

def list_module_functions():
    print("Available functions in ridemate module:")
    for func in dir(ridemate):
        if not func.startswith('__'):
            print(f"- {func}")

def test_basic_functionality():
    print("\nTesting basic functionality...")
    
    # 1. Test initialization
    print("\n1. Initializing system...")
    try:
        ridemate.init_system()
        print("✅ System initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        return
    
    # 2. Test authentication
    print("\n2. Testing authentication...")
    try:
        # Try with default credentials
        customer_id = ridemate.authenticate_customer("user1", "password123")
        if customer_id > 0:
            print(f"✅ Authenticated as customer ID: {customer_id}")
            
            # 3. Test getting available vehicles
            print("\n3. Testing get_available_vehicles...")
            try:
                vehicles = ridemate.get_available_vehicles()
                print(f"✅ Found {len(vehicles)} available vehicles")
                for i, v in enumerate(vehicles, 1):
                    print(f"   {i}. {v}")
            except Exception as e:
                print(f"❌ Error getting vehicles: {e}")
        else:
            print("❌ Authentication failed. Please check if default credentials exist.")
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
    
    # 4. Test saving data
    print("\n4. Testing save_all...")
    try:
        ridemate.save_all()
        print("✅ Data saved successfully")
    except Exception as e:
        print(f"❌ Error saving data: {e}")

if __name__ == "__main__":
    list_module_functions()
    test_basic_functionality()
