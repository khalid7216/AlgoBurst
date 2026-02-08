import base64, binascii, urllib.parse, html, codecs, string, os, subprocess

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class AlgoBurstMaster:
    def __init__(self):
        self.results = []
        self.printable = set(string.printable)

    def is_readable(self, text):
        """Checks if the output is human-readable and not junk/Chinese symbols."""
        if not text or len(text) < 2: return False
        printable_chars = sum(1 for char in text if char in self.printable)
        ratio = printable_chars / len(text)
        return ratio > 0.9  # 90% readable text required

    def rot13_decode(self, text):
        return codecs.encode(text, 'rot_13')

    def rot47_decode(self, text):
        x = []
        for i in range(len(text)):
            j = ord(text[i])
            if 33 <= j <= 126:
                x.append(chr(33 + ((j - 33 + 47) % 94)))
            else:
                x.append(text[i])
        return "".join(x)

    def try_decode_layer(self, data):
        """Tries all algorithms on a single layer of data."""
        methods = [
            ("Base64", lambda d: base64.b64decode(d).decode('utf-8')),
            ("Hex", lambda d: binascii.unhexlify(d).decode('utf-8')),
            ("URL", lambda d: urllib.parse.unquote(d)),
            ("HTML", lambda d: html.unescape(d)),
            ("ROT13", lambda d: self.rot13_decode(d)),
            ("ROT47", lambda d: self.rot47_decode(d)),
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
        """Recursive function to handle multiple layers of encoding."""
        if depth > 5: return # Stop after 5 layers to prevent infinite loops
        
        decodings = self.try_decode_layer(data)
        
        for name, decoded in decodings:
            new_chain = f"{chain} -> {name}" if chain else name
            # Check if we can decode it further (Recursive call)
            deeper_results = self.try_decode_layer(decoded)
            
            if deeper_results:
                self.burst_recursive(decoded, depth + 1, new_chain)
            else:
                # Store final result
                if not any(decoded == res[2] for res in self.results):
                    self.results.append(["Recursive", new_chain, decoded])

def update_tool():
    console.print("[bold yellow][*] Pulling latest updates...[/bold yellow]")
    try:
        subprocess.run(["git", "pull"], check=True)
        console.print("[bold green][+] Tool updated successfully![/bold green]")
    except:
        console.print("[bold red][!] Git pull failed.[/bold red]")

def main():
    while True:
        os.system('clear')
        console.print(Panel.fit("💀 ALGOBURST ULTIMATE: RECURSIVE EDITION 💀\n[dim]'u' Update | 'q' Quit | 'c' Clear[/dim]", style="bold magenta"))
        
        payload = console.input("[bold yellow]Input Encoded Data: [/bold yellow]").strip()
        
        if payload.lower() == 'u': update_tool(); input("\nEnter to continue..."); continue
        elif payload.lower() == 'q': break
        elif not payload: continue
        
        master = AlgoBurstMaster()
        master.burst_recursive(payload)
        
        if master.results:
            table = Table(title="Decoded Chains (Multi-Layer)", show_header=True, header_style="bold cyan")
            table.add_column("Type", style="magenta")
            table.add_column("Algorithm Chain", style="yellow")
            table.add_column("Final Output", style="green")
            for r in master.results: table.add_row(r[0], r[1], r[2])
            console.print(table)
        else:
            console.print("[bold red][!] No valid decoding chain found.[/bold red]")
        
        input("\n[dim]Press Enter for next scan...[/dim]")

if __name__ == "__main__":
    main()