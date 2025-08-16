import sys
import os
import pkgutil

def test_ridemate():
    print("Testing ridemate module...")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    # Try to import the module
    try:
        import ridemate
        print("✅ Successfully imported ridemate module")
    except Exception as e:
        print(f"❌ Error importing ridemate: {e}")
        return
    
    # List all members of the module
    print("\nModule members:")
    for name in dir(ridemate):
        if not name.startswith('__'):
            member = getattr(ridemate, name)
            print(f"- {name}: {type(member).__name__}")
    
    # Try to call a function if available
    if hasattr(ridemate, 'init_system'):
        print("\nCalling init_system()...")
        try:
            ridemate.init_system()
            print("✅ init_system() called successfully")
        except Exception as e:
            print(f"❌ Error calling init_system(): {e}")

if __name__ == "__main__":
    test_ridemate()
