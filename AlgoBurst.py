import base64, binascii, urllib.parse, html, codecs, string, os, subprocess, re, zlib, gzip

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class CyberChefKitchen:
    def __init__(self):
        self.printable = set(string.printable)

    def is_readable(self, text):
        if not text or len(text) < 1: return False
        printable_chars = sum(1 for char in text if char in self.printable)
        return (printable_chars / len(text)) > 0.85

    def sanitize(self, data):
        """CyberChef Hexdump & Junk Cleaner"""
        if "|" in data or re.search(r'^[0-9a-fA-F]{8}', data):
            lines = data.split('\n')
            cleaned = ""
            for line in lines:
                line = re.sub(r'^[0-9a-fA-F]{8}', '', line) # Remove Address
                if "|" in line: line = line.split("|")[0] # Remove ASCII Preview
                cleaned += line.strip() + " "
            return cleaned.replace(" ", "")
        return data.replace(" ", "").replace("\n", "").strip()

    def get_methods(self):
        """All CyberChef-style operations in one place"""
        return [
            ("Base64", lambda d: base64.b64decode(d).decode('utf-8')),
            ("Hex", lambda d: binascii.unhexlify(d).decode('utf-8')),
            ("URL", lambda d: urllib.parse.unquote(d)),
            ("HTML", lambda d: html.unescape(d)),
            ("ROT13", lambda d: codecs.encode(d, 'rot_13')),
            ("ROT47", lambda d: "".join([chr(33 + ((ord(c) - 33 + 47) % 94)) if 33 <= ord(c) <= 126 else c for c in d])),
            ("Zlib", lambda d: zlib.decompress(base64.b64decode(d)).decode('utf-8')),
            ("Gzip", lambda d: gzip.decompress(base64.b64decode(d)).decode('utf-8')),
            ("Unicode", lambda d: codecs.decode(d, 'unicode_escape')),
            ("Decimal", lambda d: "".join([chr(int(n)) for n in re.findall(r'\d+', d) if 31 < int(n) < 127])),
        ]

class AlgoBurstMaster:
    def __init__(self):
        self.kitchen = CyberChefKitchen()
        self.results = []

    def burst_recursive(self, data, depth=0, chain=""):
        if depth > 5: return
        
        # Try both Raw and Sanitized data
        to_test = [data, self.kitchen.sanitize(data)]
        
        for test_data in set(to_test):
            for name, func in self.kitchen.get_methods():
                try:
                    decoded = func(test_data)
                    if decoded and decoded != test_data and self.kitchen.is_readable(decoded):
                        new_chain = f"{chain} -> {name}" if chain else name
                        
                        # Store current success
                        if not any(decoded == res[2] for res in self.results):
                            self.results.append(["Recursive", new_chain, decoded])
                        
                        # Go Deeper
                        self.burst_recursive(decoded, depth + 1, new_chain)
                except: continue

def main():
    while True:
        os.system('clear')
        console.print(Panel.fit("💀 ALGOBURST ULTIMATE: CYBERCHEF-POWERED 💀", style="bold magenta"))
        
        payload = console.input("[bold yellow]Paste Data (Hexdump/Encoded/Raw): [/bold yellow]").strip()
        if payload.lower() == 'q': break
        
        master = AlgoBurstMaster()
        master.burst_recursive(payload)
        
        if master.results:
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Type", style="magenta")
            table.add_column("Recipe (Chain)", style="yellow")
            table.add_column("Result", style="green")
            for r in master.results: table.add_row(r[0], r[1], r[2])
            console.print(table)
        else:
            console.print("[bold red][!] No valid decoding recipe found.[/bold red]")
        
        input("\n[dim]Press Enter to continue...[/dim]")

if __name__ == "__main__":
    main()