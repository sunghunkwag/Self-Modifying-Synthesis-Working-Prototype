import verify_organic
import sys

# Override print to avoid spam
# sys.stdout = open('verify_output.txt', 'w')

print("Running verify_organic with 1 cycle...")
try:
    verify_organic.run_organic_evolution(cycles=1)
    print("SUCCESS: verify_organic ran 1 cycle.")
except Exception as e:
    print(f"FAILURE: {e}")
