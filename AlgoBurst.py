import base64, binascii, urllib.parse, html, codecs, string, os, re, subprocess

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class AlgoBurstMaster:
    def __init__(self):
        self.results = []
        self.printable = set(string.printable)

    def clean_input(self, data):
        """CyberChef Hexdump aur kachra saaf karne ke liye"""
        data_stripped = data.strip()
        # Agar data Hexdump format mein hai
        if re.search(r'^[0-9a-fA-F]{8}', data_stripped):
            lines = data_stripped.split('\n')
            cleaned = ""
            for line in lines:
                line = re.sub(r'^[0-9a-fA-F]{8}', '', line) # Remove Address
                if "|" in line: line = line.split("|")[0] # Remove Sidebar
                cleaned += line.strip() + " "
            return re.sub(r'[^0-9a-fA-F]', '', cleaned)
        return data_stripped

    def is_readable(self, text):
        """Smart validation for small and large strings"""
        if not text or len(text) < 1: return False
        p_count = sum(1 for char in text if char in self.printable)
        # Choti strings ke liye 100% printable hona chahiye
        if len(text) < 10: return p_count == len(text)
        # Lambi strings ke liye 85% kafi hai
        return (p_count / len(text)) > 0.85

    def get_methods(self):
        """CyberChef ke top algorithms ki list"""
        return [
            ("Base64", lambda d: base64.b64decode(d).decode('utf-8')),
            ("Hex", lambda d: binascii.unhexlify(re.sub(r'\s+', '', d)).decode('utf-8')),
            ("URL", lambda d: urllib.parse.unquote(d)),
            ("HTML", lambda d: html.unescape(d)),
            ("ROT13", lambda d: codecs.encode(d, 'rot_13')),
            ("ROT47", lambda d: "".join([chr(33 + ((ord(c) - 33 + 47) % 94)) if 33 <= ord(c) <= 126 else c for c in d])),
            ("Base32", lambda d: base64.b32decode(d).decode('utf-8')),
            ("Decimal", lambda d: "".join([chr(int(x)) for x in re.findall(r'\d+', d) if 31 < int(x) < 127])),
            ("Unicode-Escape", lambda d: codecs.decode(d, 'unicode_escape'))
        ]

    def burst_recursive(self, data, depth=0, chain=""):
        # 10 layers ki limit (Hacker bhi itni encryption nahi karta)
        if depth > 10: return 
        
        # Raw aur Cleaned dono versions try karein
        to_test = list(set([data, self.clean_input(data)]))
        
        for current in to_test:
            if not current: continue
            for name, func in self.get_methods():
                try:
                    decoded = func(current)
                    if decoded and decoded != current and self.is_readable(decoded):
                        new_chain = f"{chain} -> {name}" if chain else name
                        
                        # Sirf unique results save karein
                        if not any(decoded == res[2] for res in self.results):
                            self.results.append(["DEEP", new_chain, decoded])
                        
                        # Agli layer check karein
                        self.burst_recursive(decoded, depth + 1, new_chain)
                except: continue

def main():
    while True:
        os.system('clear')
        console.print(Panel.fit("💀 ALGOBURST ULTIMATE: NO LIMITS 💀", style="bold magenta"))
        
        payload = console.input("[bold yellow]Paste Encoded Data (q to quit): [/bold yellow]").strip()
        if payload.lower() in ['q', 'exit']: break
        if not payload: continue
        
        master = AlgoBurstMaster()
        master.burst_recursive(payload)
        
        if master.results:
            table = Table(title="Decoded Results Found", show_header=True, header_style="bold cyan")
            table.add_column("Mode", style="magenta")
            table.add_column("Recipe Chain", style="yellow")
            table.add_column("Plaintext", style="green")
            for r in master.results:
                table.add_row(r[0], r[1], r[2])
            console.print(table)
        else:
            console.print("[bold red][!] No valid decoding chain found.[/bold red]")
        
        input("\n[dim]Press Enter for next scan...[/dim]")

if __name__ == "__main__":
    main()