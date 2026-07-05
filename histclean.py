#!/usr/bin/env python3
import os
import sys
import argparse
from collections import OrderedDict, Counter

def get_history_path():
    """Detects if you use bash or zsh and finds the history file."""
    shell = os.environ.get('SHELL', '')
    if 'zsh' in shell:
        return os.path.expanduser("~/.zsh_history")
    else:
        return os.path.expanduser("~/.bash_history")

def clean_history(filepath, show_top=False, danger=False):
    """Main function to read, clean, and save the history."""
    
    # Check if the history file actually exists
    if not os.path.exists(filepath):
        print(f"❌ Error: History file not found at {filepath}")
        return

    # 1. Read the messy history
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    print(f"📖 Read {len(lines)} total lines from history.")

    # 2. The Cleaning Process
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        
        # --- FILTER 1: Hide secrets (case insensitive) ---
        lower_line = line.lower()
        secrets = ['password', 'token', 'secret', 'api_key', 'key=']
        if any(secret in lower_line for secret in secrets):
            continue

        # --- FILTER 2: Remove absolute junk commands ---
        junk_commands = ['ls', 'pwd', 'clear', 'exit', 'history', 'cd', 'cd..']
        if line in junk_commands:
            continue

        # --- FILTER 3: Remove terminal echo comments ---
        if line.startswith('#'):
            continue

        cleaned.append(line)

    # 3. Deduplicate: Keep the LAST occurrence of each command (most recent)
    unique_commands = list(OrderedDict.fromkeys(reversed(cleaned)))[::-1]

    print(f"🧹 Filtered down to {len(unique_commands)} unique, safe commands.")

    # 4. The "Top 10" Feature (if user asks for it)
    if show_top:
        print("\n🏆 YOUR TOP 10 MOST USED COMMANDS:")
        counter = Counter(cleaned)
        for cmd, count in counter.most_common(10):
            print(f"   {count}x  {cmd}")
        return  # Exit here, don't save a file

    # 5. Save the result (SAFE MODE by default)
    if danger:
        # DANGER MODE: Replace the actual history (with a backup)
        backup_path = filepath + ".backup"
        os.rename(filepath, backup_path)
        with open(filepath, 'w') as f:
            f.write("\n".join(unique_commands))
        print(f"⚠️  OVERWROTE original history! Backup saved to {backup_path}")
    else:
        # SAFE MODE: Save as a new .clean file
        output_path = filepath + ".clean"
        with open(output_path, 'w') as f:
            f.write("\n".join(unique_commands))
        print(f"✅ SAFE MODE: Cleaned file saved to {output_path}")
        print("💡 Run with --danger if you trust it and want to replace your real history.")

if __name__ == "__main__":
    # This is where we handle the commands the user types (like --top10)
    parser = argparse.ArgumentParser(description="HistClean: Declutter your terminal history.")
    parser.add_argument("--top10", action="store_true", help="Show your most used commands.")
    parser.add_argument("--danger", action="store_true", help="Overwrite the actual history file.")
    parser.add_argument("--file", help="Manually specify a history file path.")
    
    args = parser.parse_args()
    
    # Determine which history file to use
    history_file = args.file if args.file else get_history_path()
    
    # Run the cleaner
    clean_history(history_file, show_top=args.top10, danger=args.danger)
