import ridemate

print("Available functions in ridemate module:")
for func in dir(ridemate):
    if not func.startswith('__'):
        print(f"- {func}")

# Try to get the docstring
print("\nModule docstring:")
print(ridemate.__doc__ or "No docstring available")
