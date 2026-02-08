import base64, binascii, urllib.parse, html, codecs, string, os, subprocess, re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class AlgoBurstMaster:
    def __init__(self):
        self.results = []
        self.printable = set(string.printable)

    def is_readable(self, text):
        if not text: return False
        # Limit hata di hai, ab choti se choti string (2 chars) bhi pick hogi
        printable_chars = sum(1 for char in text if char in self.printable)
        ratio = printable_chars / len(text)
        # Junk filter: 80% readable ho toh kafi hai (taake code snippets miss na hon)
        return ratio > 0.8 

    def add(self, cat, method, val, original):
        try:
            val_str = str(val).strip()
            # Validation: Input se alag ho aur readable ho
            if val_str.lower() != original.lower() and self.is_readable(val_str):
                if not any(val_str == res[2] for res in self.results):
                    self.results.append([cat, method, val_str])
        except: pass

    def burst(self, data):
        self.results = []
        # Cleaning data: Agar aapne code se copy kiya hai toh extra spaces hata dega
        data = data.strip().split()[0] if data.strip() else ""
        if not data: return []

        # --- 1. BASE FAMILY (Full Power) ---
        try: self.add("Base", "Base64", base64.b64decode(data).decode('utf-8'), data)
        except: pass
        try: self.add("Base", "Base32", base64.b32decode(data).decode('utf-8'), data)
        except: pass
        try: self.add("Base", "Hex", binascii.unhexlify(data).decode('utf-8'), data)
        except: pass
        try: 
            import base58
            self.add("Base", "Base58", base58.b58decode(data).decode('utf-8'), data)
        except: pass

        # --- 2. WEB & SYSTEM ---
        try: self.add("Web", "URL/Percent", urllib.parse.unquote(data), data)
        except: pass
        try: self.add("Web", "HTML Entity", html.unescape(data), data)
        except: pass
        try: self.add("System", "Unicode Escape", codecs.decode(data, 'unicode_escape'), data)
        except: pass

        return self.results

def main():
    while True:
        os.system('clear')
        console.print(Panel.fit("💀 ALGOBURST: SOURCE REVIEW MODE 💀\n[dim]No Limits | 'u' Update | 'q' Quit[/dim]", style="bold cyan"))
        
        payload = console.input("[bold yellow]Paste String from Code: [/bold yellow]").strip()
        
        if payload.lower() == 'u':
            try:
                subprocess.run(["git", "pull"], check=True)
                console.print("[green]Updated![/green]"); input(); continue
            except: pass
        elif payload.lower() == 'q': break
        
        # Multiple strings handling (agar line mein space ho toh ye first part lega)
        master = AlgoBurstMaster()
        results = master.burst(payload)
        
        if results:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Category", style="cyan")
            table.add_column("Algo", style="yellow")
            table.add_column("Output", style="green")
            for r in results: table.add_row(r[0], r[1], r[2])
            console.print(table)
        else:
            console.print("[bold red][!] Nothing hidden here.[/bold red]")
        
        input("\n[dim]Press Enter for next string...[/dim]")

if __name__ == "__main__":
    main()