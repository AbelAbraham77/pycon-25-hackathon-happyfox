#!/usr/bin/env python3
"""
Demo script to showcase both CLI and GUI functionality
"""

import os
import sys
import time

def demo_cli():
    """Demonstrate CLI functionality"""
    print("🎯 DEMO: Command Line Interface")
    print("=" * 50)
    
    print("Running: python assign_tickets.py")
    os.system("python assign_tickets.py")
    
    print("\n✅ CLI Demo Complete!")
    print("📁 Check output_result.json for results")
    print("=" * 50)

def demo_gui():
    """Demonstrate GUI functionality"""
    print("\n🖥️ DEMO: Graphical User Interface")
    print("=" * 50)
    
    print("Launching GUI application...")
    print("💡 Use the GUI to:")
    print("   1. Load the dataset")
    print("   2. Process assignments")
    print("   3. View detailed results")
    print("   4. Export to custom file")
    
    try:
        os.system("python ticket_assignment_gui.py")
    except KeyboardInterrupt:
        print("\n👋 GUI Demo closed by user")
    
    print("✅ GUI Demo Complete!")

def main():
    """Main demo function"""
    print("🚀 PyCon25 Hackathon - Ticket Assignment System Demo")
    print("=" * 60)
    
    while True:
        print("\nChoose demo mode:")
        print("1. 💻 Command Line Interface (CLI)")
        print("2. 🖥️ Graphical User Interface (GUI)")  
        print("3. 🔄 Both (CLI then GUI)")
        print("4. ❌ Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            demo_cli()
        elif choice == "2":
            demo_gui()
        elif choice == "3":
            demo_cli()
            input("\nPress Enter to launch GUI...")
            demo_gui()
        elif choice == "4":
            print("👋 Demo ended. Thank you!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()