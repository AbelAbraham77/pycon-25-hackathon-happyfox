#!/usr/bin/env python3
"""
Quick launcher for the Ticket Assignment System GUI
"""

import sys
import os

try:
    import tkinter as tk
    from ticket_assignment_gui import main
    
    print("🚀 Launching Ticket Assignment System GUI...")
    main()
    
except ImportError as e:
    print(f"❌ Error: Missing required module: {e}")
    print("💡 Make sure you have tkinter installed (usually comes with Python)")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Error launching GUI: {e}")
    sys.exit(1)