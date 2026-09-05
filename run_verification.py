import subprocess
import os
import sys

def run_tests():
    print("--- Initiating Comprehensive Test Suite ---")
    
    # Ensure PYTHONPATH is set to 'backend' directory for imports
    env = os.environ.copy()
    # Add backend directory to PYTHONPATH
    backend_path = os.path.join(os.getcwd(), "backend")
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{backend_path}{os.pathsep}{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = backend_path

    # Run pytest on all tests in backend/tests
    # We use -v (verbose) to clearly show each test being passed
    result = subprocess.run(
        ["pytest", "backend/tests/", "-v"],
        env=env,
        capture_output=True,
        text=True
    )

    print(result.stdout)
    
    if result.stderr:
        print("--- stderr Output ---")
        print(result.stderr)

    if result.returncode == 0:
        print("--- Result: All tests passed successfully ---")
    else:
        print(f"--- Result: Tests failed with exit code {result.returncode} ---")

if __name__ == "__main__":
    run_tests()
