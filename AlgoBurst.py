import base64, binascii, urllib.parse, html, codecs, string, os, re

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class AlgoBurstMaster:
    def __init__(self):
        self.results = []
        self.printable = set(string.printable)

    def clean_input(self, data):
        """Kachra saaf karke raw hex nikaalta hai"""
        lines = data.strip().split('\n')
        cleaned = ""
        for line in lines:
            # Remove addresses like 00000000
            line = re.sub(r'^[0-9a-fA-F]{8}', '', line)
            # Remove sidebar preview
            if "|" in line: line = line.split("|")[0]
            cleaned += line.strip() + " "
        
        # Agar Hex format hai toh spaces khatam karo
        if any(c in 'abcdefABCDEF' for c in cleaned) or " " in cleaned:
            tmp = re.sub(r'[^0-9a-fA-F]', '', cleaned)
            if len(tmp) % 2 == 0 and len(tmp) > 0:
                return tmp
        return data.strip()

    def get_methods(self):
        return [
            ("Base64", lambda d: base64.b64decode(d).decode('utf-8')),
            ("Hex", lambda d: binascii.unhexlify(d).decode('utf-8')),
            ("URL", lambda d: urllib.parse.unquote(d)),
            ("ROT13", lambda d: codecs.encode(d, 'rot_13')),
            ("ROT47", lambda d: "".join([chr(33 + ((ord(c) - 33 + 47) % 94)) if 33 <= ord(c) <= 126 else c for c in d])),
            ("Decimal", lambda d: "".join([chr(int(x)) for x in re.findall(r'\d+', d) if 31 < int(x) < 127])),
        ]

    def burst_all(self, data):
        """Har algorithm ko try karke result store karega chahe wo readable ho ya na ho"""
        cleaned = self.clean_input(data)
        
        # First Layer Trial
        for name, func in self.get_methods():
            try:
                decoded = func(cleaned)
                if decoded:
                    self.results.append([name, decoded])
                    
                    # Second Layer Trial (Recursive)
                    for n2, f2 in self.get_methods():
                        try:
                            d2 = f2(decoded.strip())
                            if d2 and d2 != decoded:
                                self.results.append([f"{name} -> {n2}", d2])
                        except: continue
            except: continue

def main():
    while True:
        os.system('clear')
        console.print(Panel.fit("💀 ALGOBURST: FULL VERBOSE MODE 💀", style="bold red"))
        
        payload = console.input("[bold yellow]Paste Data >>> [/bold yellow]").strip()
        if payload.lower() == 'q': break
        
        master = AlgoBurstMaster()
        master.burst_all(payload)
        
        if master.results:
            table = Table(title="All Possible Decodings", show_lines=True)
            table.add_column("Algorithm(s) Applied", style="cyan", no_wrap=True)
            table.add_column("Result (Raw Output)", style="green")

            for recipe, output in master.results:
                # Agar output mein 'hello' hai toh red color mein dikhao
                display_output = output
                if "hello" in output.lower():
                    display_output = f"[bold red reverse] {output} [/bold red reverse] 🔥"
                
                table.add_row(recipe, display_output)
            
            console.print(table)
        else:
            console.print("[bold red][!] Decoding failed on all methods.[/bold red]")
        
        input("\n[dim]Press Enter for next scan...[/dim]")

if __name__ == "__main__":
    main()