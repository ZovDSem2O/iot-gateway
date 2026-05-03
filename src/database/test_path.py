import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

print("sys.path:", sys.path)
print("\nCurrent directory:", os.getcwd())
print("\nScript directory:", os.path.dirname(__file__))

try:
    from database.database import DataStorage
    print("\n[OK] Import successful!")
except Exception as e:
    print(f"\n[ERROR] Import failed: {e}")
    import traceback
    traceback.print_exc()