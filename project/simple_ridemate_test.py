import ridemate

def main():
    print("Testing ridemate module...")
    
    # List all callable attributes
    print("\nAvailable callable functions:")
    for name in dir(ridemate):
        if not name.startswith('__') and callable(getattr(ridemate, name)):
            print(f"- {name}")
    
    # Try to call init_system if it exists
    if hasattr(ridemate, 'init_system'):
        print("\nCalling init_system()...")
        try:
            ridemate.init_system()
            print("✅ init_system() called successfully")
        except Exception as e:
            print(f"❌ Error calling init_system(): {e}")
    else:
        print("\ninit_system() not found in the module")
    
    print("\nTest completed!")

if __name__ == "__main__":
    main()
