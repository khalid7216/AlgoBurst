import base64
import binascii
import re
import os
from cryptography.fernet import Fernet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def analyze_string(data):
    results = {}
    # Base64 Check
    try:
        decoded_b64 = base64.b64decode(data).decode('utf-8')
        if len(decoded_b64) > 3:
            results['Base64'] = decoded_b64
    except: pass

    # Hex Check
    try:
        decoded_hex = binascii.unhexlify(data).decode('utf-8')
        if len(decoded_hex) > 3:
            results['Hex'] = decoded_hex
    except: pass
    
    return results

def scan_file(filepath):
    if not os.path.exists(filepath):
        console.print(f"[red]Error: {filepath} nahi mili![/red]")
        return

    with open(filepath, 'r') as f:
        content = f.read()

    # Regex to find potential encrypted/encoded strings
    potential_strings = re.findall(r'[A-Za-z0-9+/=]{10,}', content)
    
    table = Table(title=f"AlgoBurst Scan Results: {filepath}", show_header=True, header_style="bold magenta")
    table.add_column("Type", style="cyan")
    table.add_column("Decoded Content", style="green")

    found = False
    for s in potential_strings:
        detections = analyze_string(s)
        for dtype, dval in detections.items():
            table.add_row(dtype, dval)
            found = True

    if found:
        console.print(table)
    else:
        console.print("[yellow]Koi encrypted/encoded string nahi mili.[/yellow]")

def main():
    console.print(Panel.fit("🔥 ALGOBURST v1.0 🔥\n[dim]The Ultimate Decryption Scanner[/dim]", style="bold red"))
    
    choice = console.input("[bold yellow]Choose Option:[/bold yellow]\n1. Scan a File\n2. Decrypt a String\n> ")
    
    if choice == '1':
        fname = console.input("[bold cyan]Enter file path to scan: [/bold cyan]")
        scan_file(fname)
    elif choice == '2':
        text = console.input("[bold cyan]Enter string: [/bold cyan]")
        res = analyze_string(text)
        if res:
            for k, v in res.items():
                console.print(f"[bold green][+] {k}:[/bold green] {v}")
        else:
            console.print("[red]Kuch samajh nahi aaya![/red]")

if __name__ == "__main__":
    main()