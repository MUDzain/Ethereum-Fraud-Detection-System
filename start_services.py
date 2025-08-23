#!/usr/bin/env python3
"""
Service Startup Script for Fraud Detection System
This script helps you start all services in the correct order
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_info(message):
    print(f"ℹ️  {message}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def check_port_available(port):
    """Check if a port is available"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def start_ml_api():
    """Start the ML API service"""
    print_header("Starting ML API Service")
    
    if not check_port_available(5000):
        print_error("Port 5000 is already in use!")
        print_info("Make sure no other service is running on port 5000")
        return False
    
    print_info("Starting ML API on port 5000...")
    print_info("This will start the Flask API serving your fraud detection model")
    
    try:
        # Start the ML API
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], cwd=Path(__file__).parent / "src")
        
        # Wait a bit for the service to start
        time.sleep(3)
        
        if process.poll() is None:
            print_success("ML API started successfully!")
            print_info("Service is running on http://localhost:5000")
            return process
        else:
            print_error("ML API failed to start")
            return False
            
    except Exception as e:
        print_error(f"Failed to start ML API: {str(e)}")
        return False

def start_web_interface():
    """Start the web interface service"""
    print_header("Starting Web Interface Service")
    
    if not check_port_available(8081):
        print_error("Port 8081 is already in use!")
        print_info("Make sure no other service is running on port 8081")
        return False
    
    print_info("Starting Web Interface on port 8081...")
    print_info("This will start the user-friendly web interface")
    
    try:
        # Start the web interface
        process = subprocess.Popen([
            sys.executable, "web_interface.py"
        ], cwd=Path(__file__).parent / "src")
        
        # Wait a bit for the service to start
        time.sleep(3)
        
        if process.poll() is None:
            print_success("Web Interface started successfully!")
            print_info("Service is running on http://localhost:8081")
            return process
        else:
            print_error("Web Interface failed to start")
            return False
            
    except Exception as e:
        print_error(f"Failed to start Web Interface: {str(e)}")
        return False

def main():
    """Main function to start all services"""
    print("🚀 Fraud Detection System - Service Startup")
    print("This script will help you start all services")
    
    # Check if we're in the right directory
    if not Path("src/app.py").exists():
        print_error("Please run this script from the project root directory")
        print_info("Current directory:", os.getcwd())
        return
    
    print_header("Service Status Check")
    
    # Check if services are already running
    ml_running = not check_port_available(5000)
    web_running = not check_port_available(8081)
    
    if ml_running:
        print_info("ML API is already running on port 5000")
    if web_running:
        print_info("Web Interface is already running on port 8081")
    
    if ml_running and web_running:
        print_success("All services are already running!")
        print_info("You can now:")
        print_info("1. Test the web interface at http://localhost:8081")
        print_info("2. Test the API at http://localhost:5000")
        print_info("3. Run the oracle service: python src/oracle_service.py")
        return
    
    # Start services that aren't running
    processes = []
    
    if not ml_running:
        ml_process = start_ml_api()
        if ml_process:
            processes.append(("ML API", ml_process))
        else:
            print_error("Failed to start ML API. Stopping startup process.")
            return
    
    if not web_running:
        web_process = start_web_interface()
        if web_process:
            processes.append(("Web Interface", web_process))
        else:
            print_error("Failed to start Web Interface. Stopping startup process.")
            return
    
    if processes:
        print_header("Services Started Successfully!")
        print_info("All services are now running:")
        for name, _ in processes:
            print_info(f"  - {name}")
        
        print_info("\nYou can now:")
        print_info("1. Open your web browser and go to http://localhost:8081")
        print_info("2. Test the API at http://localhost:5000")
        print_info("3. Run the oracle service: python src/oracle_service.py")
        
        print_info("\nTo stop services, press Ctrl+C in this terminal")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
                # Check if any process has stopped
                for name, process in processes:
                    if process.poll() is not None:
                        print_error(f"{name} has stopped unexpectedly")
                        return
        except KeyboardInterrupt:
            print_info("\n🛑 Stopping services...")
            for name, process in processes:
                process.terminate()
                print_info(f"Stopped {name}")
            print_success("All services stopped")

if __name__ == "__main__":
    main()
