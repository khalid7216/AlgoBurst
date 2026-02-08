import base64, binascii, urllib.parse, html, codecs, string, os, subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class AlgoBurstMaster:
    def __init__(self):
        self.results = []
        # Sirf printable characters aur common symbols
        self.printable = set(string.printable)

    def is_readable(self, text):
        if not text or len(text) < 2: return False
        # Junk character detection logic
        non_printable = sum(1 for char in text if char not in self.printable)
        # Agar 10% se zyada junk characters hain toh reject kar do
        if non_printable / len(text) > 0.10: return False
        # Agar text mein ajeeb symbols (like ) hain toh reject karo
        if "" in text: return False
        return True

    def add(self, cat, method, val, original):
        try:
            val_str = str(val).strip()
            # Validation: Junk filter + Anti-Echo logic
            if val_str != original and self.is_readable(val_str):
                # Duplicate check
                if not any(val_str == res[2] for res in self.results):
                    self.results.append([cat, method, val_str])
        except: pass

    def burst(self, data):
        self.results = []
        # --- BASE FAMILY ---
        try: self.add("Base", "Base64", base64.b64decode(data).decode('utf-8'), data)
        except: pass
        try: self.add("Base", "Base32", base64.b32decode(data).decode('utf-8'), data)
        except: pass
        try: self.add("Base", "Hex", binascii.unhexlify(data).decode('utf-8'), data)
        except: pass

        # --- WEB & URL ---
        try: self.add("Web", "URL/Percent", urllib.parse.unquote(data), data)
        except: pass
        try: self.add("Web", "HTML Entity", html.unescape(data), data)
        except: pass

        return self.results

def update_tool():
    console.print("[bold yellow][*] Checking for updates...[/bold yellow]")
    try:
        subprocess.run(["git", "pull"], check=True)
        console.print("[bold green][+] Tool updated successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red][!] Update failed: {e}[/bold red]")

def main():
    os.system('clear')
    console.print(Panel.fit("💀 ALGOBURST ULTIMATE 💀\n[dim]Press 'u' to Update | 'q' to Quit[/dim]", style="bold green"))
    
    payload = console.input("[bold yellow]Input Encoded Data: [/bold yellow]")
    
    if payload.lower() == 'u':
        update_tool()
        return
    elif payload.lower() == 'q':
        return
    
    master = AlgoBurstMaster()
    results = master.burst(payload)
    
    if results:
        table = Table(title="Clean Decoded Results", show_header=True, header_style="bold cyan")
        table.add_column("Category", style="magenta")
        table.add_column("Algorithm", style="yellow")
        table.add_column("Output", style="green")
        for r in results: table.add_row(r[0], r[1], r[2])
        console.print(table)
    else:
        console.print("[bold red][!] No valid readable data found.[/bold red]")

if __name__ == "__main__":
    main()