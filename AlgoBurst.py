import base64, binascii, urllib.parse, html, codecs, json, yaml, zlib, gzip, bz2, re
try:
    import base58, base62, brotli, base91
except ImportError:
    pass

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class AlgoBurstMaster:
    def __init__(self):
        self.results = []

    def add(self, cat, method, val):
        if val and str(val).strip():
            self.results.append([cat, method, str(val)[:100] + "..." if len(str(val)) > 100 else str(val)])

    def burst(self, data):
        self.results = []
        raw_bytes = data.encode('utf-8', errors='ignore')
        
        # 1. BASE FAMILY (100% Coverage)
        try: self.add("Base", "Base16 (Hex)", binascii.unhexlify(data).decode('utf-8', 'ignore'))
        except: pass
        try: self.add("Base", "Base32", base64.b32decode(data).decode('utf-8', 'ignore'))
        except: pass
        try: self.add("Base", "Base58 (Bitcoin)", base58.b58decode(data).decode('utf-8', 'ignore'))
        except: pass
        try: self.add("Base", "Base62", base62.decode(data))
        except: pass
        try: self.add("Base", "Base64", base64.b64decode(data).decode('utf-8', 'ignore'))
        except: pass
        try: self.add("Base", "Base85 (Ascii85)", base64.b85decode(data).decode('utf-8', 'ignore'))
        except: pass
        try: self.add("Base", "Base91", base91.decode(data).decode('utf-8', 'ignore'))
        except: pass

        # 2. BINARY / SYSTEM / ENCODING
        try:
            binary_clean = data.replace(" ", "")
            if all(c in '01' for c in binary_clean):
                n = int(binary_clean, 2)
                self.add("Binary", "Binary -> Text", n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())
        except: pass
        try: self.add("System", "Octal", ''.join([chr(int(x, 8)) for x in re.findall(r'\\([0-7]{3})', data)]))
        except: pass
        try: self.add("System", "Decimal", ''.join([chr(int(x)) for x in re.findall(r'\d+', data) if 31 < int(x) < 127]))
        except: pass

        # 3. WEB / URL / EMAIL
        try: self.add("Web", "URL/Percent", urllib.parse.unquote(data))
        except: pass
        try: self.add("Web", "HTML Entity", html.unescape(data))
        except: pass
        try: self.add("Email", "Quoted-Printable", codecs.decode(raw_bytes, 'quopri').decode('utf-8', 'ignore'))
        except: pass
        try: self.add("Email", "UUEncode", codecs.decode(raw_bytes, 'uu').decode('utf-8', 'ignore'))
        except: pass

        # 4. COMPRESSION (Decompression)
        try: 
            b64_raw = base64.b64decode(data)
            try: self.add("Compression", "Zlib", zlib.decompress(b64_raw).decode('utf-8', 'ignore'))
            except: pass
            try: self.add("Compression", "Gzip", gzip.decompress(b64_raw).decode('utf-8', 'ignore'))
            except: pass
            try: self.add("Compression", "Brotli", brotli.decompress(b64_raw).decode('utf-8', 'ignore'))
            except: pass
        except: pass

        # 5. CHARACTER SETS / LEGACY (The Full List)
        charsets = [
            'utf-8', 'utf-16', 'utf-32', 'ascii', 'latin-1', 'iso-8859-1', 'iso-8859-2', 
            'iso-8859-6', 'iso-8859-8', 'cp1250', 'cp1252', 'shift-jis', 'gbk', 'big5', 'koi8-r'
        ]
        for s in charsets:
            try:
                dec = raw_bytes.decode(s)
                if dec != data and len(dec) > 2:
                    self.add("Charset/Legacy", s.upper(), dec)
            except: pass

        # 6. DATA & PROGRAMMING
        try: 
            if "{" in data or "[" in data:
                self.add("Data", "JSON/YAML", json.loads(data))
        except: pass
        try: self.add("Programming", "Unicode Escape", codecs.decode(data, 'unicode_escape'))
        except: pass

        return self.results

def main():
    master = AlgoBurstMaster()
    console.print(Panel.fit("💀 ALGOBURST ULTIMATE: NO COMPROMISE EDITION 💀", style="bold red"))
    
    payload = console.input("[bold yellow]Input Encoded Data: [/bold yellow]")
    
    results = master.burst(payload)
    
    if results:
        table = Table(title="Decoded Results", show_header=True, header_style="bold blue")
        table.add_column("Category", style="cyan")
        table.add_column("Algorithm", style="green")
        table.add_column("Output", style="white")
        
        for r in results:
            table.add_row(r[0], r[1], r[2])
        console.print(table)
    else:
        console.print("[bold red][!] No matching algorithm found for this input.[/bold red]")

if __name__ == "__main__":
    main()