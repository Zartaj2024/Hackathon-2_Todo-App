import uvicorn
import sys
import os

# Change to the backend directory
os.chdir('D:/zartaj/Todo_App/phase_2/backend')

try:
    print("Starting backend server...")
    sys.path.insert(0, 'D:/zartaj/Todo_App/phase_2/backend')
    from main import app
    
    print("App imported successfully")
    
    # Run the server
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()