#!/usr/bin/env python3
import argparse
import requests

def load_addresses(sources):
    addresses = []
    for source in sources:
        if source.startswith("http://") or source.startswith("https://"):
            response = requests.get(source)
            response.raise_for_status()
            addresses.extend(response.text.splitlines())
        else:
            with open(source, 'r') as file:
                addresses.extend(file.readlines())
    return [address.strip() for address in addresses if address.strip()]

def generate_pac_file(addresses, proxy_server, proxy_type, output_file):
    pac_template = """
function FindProxyForURL(url, host) {{
{proxy_rules}
    return "DIRECT";
}}
"""
    proxy_rules = []
    for address in addresses:
        proxy_rules.append(f'    if (shExpMatch(host, "{address}")) return "{proxy_type} {proxy_server}";')
    pac_content = pac_template.format(proxy_rules="\n    ".join(proxy_rules))

    with open(output_file, 'w') as file:
        file.write(pac_content)

def main():
    parser = argparse.ArgumentParser(description="Generate PAC file from a list of addresses.")
    parser.add_argument('sources', nargs='+', help='Paths to the addresses files or URLs')
    parser.add_argument('proxy_server', help='Proxy server to be used in the PAC file (e.g., proxy.example.com:1080)')
    parser.add_argument('proxy_type', help='Proxy type to be used in the PAC file (e.g., PROXY, SOCKS, SOCKS5)')
    parser.add_argument('output_file', help='Output PAC file path')

    args = parser.parse_args()

    addresses = load_addresses(args.sources)
    generate_pac_file(addresses, args.proxy_server, args.proxy_type, args.output_file)
    print(f"PAC file generated: {args.output_file}")

if __name__ == "__main__":
    main()