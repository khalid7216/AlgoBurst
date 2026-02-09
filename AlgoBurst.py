import base64, binascii, urllib.parse, html, codecs, string, os, re, zlib, gzip, subprocess
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class CyberChefTools:
    """CyberChef-style utility functions for parsing and decoding"""
    @staticmethod
    def sanitize_hexdump(data):
        # Hexdump pattern (address followed by hex values and optional ASCII sidebar)
        lines = data.strip().split('\n')
        cleaned_hex = ""
        for line in lines:
            # Remove memory addresses (e.g., 00000000)
            line = re.sub(r'^[0-9a-fA-F]{8}', '', line)
            # Remove ASCII side preview (anything after '|')
            if "|" in line:
                line = line.split("|")[0]
            cleaned_hex += line.strip() + " "
        
        # Sirf hex characters bachaao
        final_hex = re.sub(r'[^0-9a-fA-F]', '', cleaned_hex)
        return final_hex

    @staticmethod
    def rot47(text):
        x = []
        for i in range(len(text)):
            j = ord(text[i])
            if 33 <= j <= 126:
                x.append(chr(33 + ((j - 33 + 47) % 94)))
            else:
                x.append(text[i])
        return "".join(x)

class AlgoBurstMaster:
    def __init__(self):
        self.results = []
        self.printable = set(string.printable)

    def is_readable(self, text):
        if not text or len(text) < 1: return False
        # Human-readable check (90% printable characters)
        printable_count = sum(1 for char in text if char in self.printable)
        return (printable_count / len(text)) > 0.9

    def get_methods(self):
        """All major algorithms from CyberChef and beyond"""
        return [
            ("Base64", lambda d: base64.b64decode(d).decode('utf-8')),
            ("Hex", lambda d: binascii.unhexlify(d).decode('utf-8')),
            ("URL", lambda d: urllib.parse.unquote(d)),
            ("HTML", lambda d: html.unescape(d)),
            ("ROT13", lambda d: codecs.encode(d, 'rot_13')),
            ("ROT47", lambda d: CyberChefTools.rot47(d)),
            ("Unicode-Escape", lambda d: codecs.decode(d, 'unicode_escape')),
            ("Base32", lambda d: base64.b32decode(d).decode('utf-8')),
            ("Decimal", lambda d: "".join([chr(int(x)) for x in re.findall(r'\d+', d) if 31 < int(x) < 127]))
        ]

    def burst_recursive(self, data, depth=0, chain=""):
        if depth > 5: return # Max 5 layers of encoding
        
        # Try both: raw input and cleaned hexdump
        attempts = [data, CyberChefTools.sanitize_hexdump(data)]
        
        for current_input in set(attempts):
            if not current_input: continue
            
            for name, func in self.get_methods():
                try:
                    decoded = func(current_input)
                    if decoded and decoded != current_input and self.is_readable(decoded):
                        new_chain = f"{chain} -> {name}" if chain else name
                        
                        # Store unique result
                        if not any(decoded == res[2] for res in self.results):
                            self.results.append(["Deep Scan", new_chain, decoded])
                        
                        # Dig deeper into the decoded string
                        self.burst_recursive(decoded, depth + 1, new_chain)
                except: continue

def update_tool():
    console.print("[bold yellow][*] Pulling latest updates from GitHub...[/bold yellow]")
    try:
        subprocess.run(["git", "pull"], check=True)
        console.print("[bold green][+] Update success! Please restart.[/bold green]")
    except Exception as e:
        console.print(f"[bold red][!] Update failed: {e}[/bold red]")

def main():
    while True:
        os.system('clear')
        console.print(Panel.fit(
            "💀 [bold red]ALGOBURST ULTIMATE[/bold red] 💀\n"
            "[bold cyan]The All-in-One Decoding Engine[/bold cyan]\n"
            "[dim]'u' Update | 'q' Quit | 'c' Clear Screen[/dim]", 
            style="bold green"
        ))
        
        payload = console.input("[bold yellow]Input Data >>> [/bold yellow]").strip()
        
        if payload.lower() == 'q': break
        if payload.lower() == 'u': update_tool(); input("\nPress Enter..."); continue
        if payload.lower() == 'c': continue
        if not payload: continue
        
        master = AlgoBurstMaster()
        master.burst_recursive(payload)
        
        if master.results:
            table = Table(title="Decoded Recipe Chains", show_header=True, header_style="bold cyan")
            table.add_column("Mode", style="magenta")
            table.add_column("Recipe (Chain)", style="yellow")
            table.add_column("Final Output", style="green")
            for r in master.results: table.add_row(r[0], r[1], r[2])
            console.print(table)
        else:
            console.print("[bold red][!] No valid decoding chain found. Check your input.[/bold red]")
        
        input("\n[dim]Press Enter for next scan...[/dim]")

if __name__ == "__main__":
    main()