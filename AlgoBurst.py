import base64, binascii, urllib.parse, html, codecs, string, os, subprocess, re

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class AlgoBurstMaster:
    def __init__(self):
        self.results = []
        self.printable = set(string.printable)

    def sanitize_input(self, data):
        """CyberChef style hexdump aur extra junk ko saaf karta hai."""
        # 1. Agar hexdump format hai (address 00000000 aur sidebars |...|)
        if "|" in data or re.search(r'^[0-9a-fA-F]{8}', data):
            # Sirf hex wala part nikaalte hain (address aur ASCII side preview hata kar)
            # Lines ko split karke middle part uthate hain
            lines = data.split('\n')
            cleaned_hex = ""
            for line in lines:
                # Remove address (starts with 8 hex chars)
                line = re.sub(r'^[0-9a-fA-F]{8}', '', line)
                # Remove ASCII preview (part after '|')
                if "|" in line:
                    line = line.split("|")[0]
                cleaned_hex += line.strip() + " "
            return cleaned_hex.replace(" ", "")
        
        # 2. Normal cleaning (extra spaces aur newlines)
        return data.replace(" ", "").replace("\n", "").strip()

    def is_readable(self, text):
        if not text or len(text) < 1: return False
        printable_chars = sum(1 for char in text if char in self.printable)
        return (printable_chars / len(text)) > 0.85

    def rot13_decode(self, text):
        return codecs.encode(text, 'rot_13')

    def try_decode_layer(self, data):
        """Single layer decoding with more algorithms."""
        methods = [
            ("Base64", lambda d: base64.b64decode(d).decode('utf-8')),
            ("Hex", lambda d: binascii.unhexlify(d).decode('utf-8')),
            ("URL", lambda d: urllib.parse.unquote(d)),
            ("ROT13", lambda d: self.rot13_decode(d)),
            ("Unicode-Escape", lambda d: codecs.decode(d, 'unicode_escape'))
        ]
        
        valid_decodings = []
        for name, func in methods:
            try:
                decoded = func(data)
                if decoded.strip() and decoded != data and self.is_readable(decoded):
                    valid_decodings.append((name, decoded))
            except: continue
        return valid_decodings

    def burst_recursive(self, data, depth=0, chain=""):
        if depth > 5: return
        
        # First attempt with original data
        decodings = self.try_decode_layer(data)
        
        # If it fails, try sanitizing it (Hexdump cleaning)
        if not decodings:
            sanitized = self.sanitize_input(data)
            if sanitized != data:
                decodings = self.try_decode_layer(sanitized)

        for name, decoded in decodings:
            new_chain = f"{chain} -> {name}" if chain else name
            deeper_results = self.try_decode_layer(decoded)
            
            if deeper_results:
                self.burst_recursive(decoded, depth + 1, new_chain)
            else:
                if not any(decoded == res[2] for res in self.results):
                    self.results.append(["Recursive", new_chain, decoded])

def main():
    while True:
        os.system('clear')
        console.print(Panel.fit("💀 ALGOBURST ULTIMATE: CYBERCHEF CLEANER 💀", style="bold magenta"))
        
        console.print("[dim]Paste Hexdump, Base64 or Encoded string below:[/dim]")
        payload = console.input("[bold yellow]>>> [/bold yellow]").strip()
        
        if payload.lower() == 'q': break
        elif not payload: continue
        
        master = AlgoBurstMaster()
        master.burst_recursive(payload)
        
        if master.results:
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Type", style="magenta")
            table.add_column("Algorithm Chain", style="yellow")
            table.add_column("Final Output", style="green")
            for r in master.results: table.add_row(r[0], r[1], r[2])
            console.print(table)
        else:
            console.print("[bold red][!] Decoding failed. Try cleaning the input manually.[/bold red]")
        
        input("\n[dim]Press Enter for next scan...[/dim]")

if __name__ == "__main__":
    main()