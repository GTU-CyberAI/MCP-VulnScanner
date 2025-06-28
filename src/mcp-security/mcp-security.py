from typing import Any
import subprocess
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("nmap")

def run_nmap_command(args: list[str]) -> str:
    """Run a safe Nmap command and return the output."""
    try:
        result = subprocess.run(
            ["nmap"] + args,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout
    except Exception as e:
        return f"Error running Nmap: {str(e)}"

@mcp.tool()
def simple_scan(target: str) -> str:
    """Perform a basic Nmap scan on the target.

    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-T4", target])

@mcp.tool()
def port_scan(target: str, ports: str) -> str:
    """Scan specific ports on a target.

    Args:
        target: IP address or hostname
        ports: Port range (e.g., 20-80 or 22,80,443)
    """
    return run_nmap_command(["-p", ports, "-T4", target])

@mcp.tool()
def os_detection(target: str) -> str:
    """Attempt OS detection on a target.

    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-O", target])

@mcp.tool()
def full_scan(target: str) -> str:
    """Perform a full TCP scan with service detection.

    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sS", "-sV", "-T4", "-A", target])

@mcp.tool()
def ping_scan(target: str) -> str:
    """Perform a Ping Scan to check if the host is up.

    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sn", target])

@mcp.tool()
def scan_specific_port(target: str, port: str) -> str:
    """Scan a specific port on the target.

    Args:
        target: IP address or hostname
        port: Port number (e.g., 80)
    """
    return run_nmap_command(["-p", port, "-T4", target])

@mcp.tool()
def service_version_detection(target: str) -> str:
    """Detect the versions of services running on open ports.

    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sV", target])

@mcp.tool()
def aggressive_scan(target: str) -> str:
    """Perform an aggressive scan (OS, service detection, traceroute).

    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-A", target])

@mcp.tool()
def scan_port_range(target: str, port_range: str) -> str:
    """Scan a range of ports on the target.

    Args:
        target: IP address or hostname
        port_range: Port range (e.g., 1-1000)
    """
    return run_nmap_command(["-p", port_range, "-T4", target])

@mcp.tool()
def http_title_scan(target: str) -> str:
    """Scan for HTTP titles on port 80.

    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-p", "80", "--script", "http-title", target])

@mcp.tool()
def traceroute_scan(target: str) -> str:
    """Perform a traceroute to the target.

    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["--traceroute", target])

# Vulscan tools
@mcp.tool()
def vulscan_basic(target: str, database: str = "cve.csv") -> str:
    """Perform a vulnerability scan using Vulscan with a specific database."""
    return run_nmap_command([
        "-sV",
        "--script=vulscan/vulscan.nse",
        "--script-args", f"\"vulscandb={database}\"",
        target
    ])


@mcp.tool()
def vulscan_output_limit(target: str, database: str = "cve.csv", limit: int = 10) -> str:
    """Perform a vulnerability scan and limit the number of results."""
    command_args = [
        "-sV",
        "--script=vulscan/vulscan.nse",
        "--script-args", f"\"vulscandb={database},vulscanshowall=0,vulscanoutput='{{id}} - {{title}}'\"",
        target
    ]
    full_output = run_nmap_command(command_args)
    output_lines = full_output.splitlines()
    limited_results = "\n".join(output_lines[:limit])
    return limited_results


@mcp.tool()
def vulscan_interactive(target: str, database: str = "cve.csv") -> str:
    """Run Vulscan in interactive mode to manually select vulnerabilities to report."""
    return run_nmap_command([
        "-sV",
        "--script=vulscan/vulscan.nse",
        "--script-args", f"\"vulscandb={database},vulscaninteractive=1\"",
        target
    ])


@mcp.tool()
def vulscan_custom_output(target: str, database: str = "cve.csv", custom_template: str = '{id} - {title}') -> str:
    """Run Vulscan with a custom output format."""
    return run_nmap_command([
        "-sV",
        "--script=vulscan/vulscan.nse",
        "--script-args", f"\"vulscandb={database},vulscanoutput='{custom_template}'\"",
        target
    ])

@mcp.tool()
def ping_subnet_scan(subnet: str) -> str:
    """Perform a ping scan to discover active devices on a subnet.
    
    Args:
        subnet: Network subnet (e.g., 192.168.1.1/24)
    """
    return run_nmap_command(["-sP", subnet])

@mcp.tool()
def single_host_scan(target: str) -> str:
    """Scan a single host for 1000 well-known ports.
    
    Args:
        target: IP address or hostname (e.g., scanme.nmap.org)
    """
    return run_nmap_command([target])

@mcp.tool()
def stealth_scan(target: str) -> str:
    """Perform a stealth SYN scan without completing the TCP handshake.
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sS", target])

@mcp.tool()
def scan_multiple_hosts(hosts: str) -> str:
    """Scan multiple hosts simultaneously.
    
    Args:
        hosts: Space-separated list of hosts (e.g., "192.168.1.1 192.168.1.2")
    """
    host_list = hosts.split()
    return run_nmap_command(host_list)

@mcp.tool()
def scan_ip_range(ip_range: str) -> str:
    """Scan a range of IP addresses using wildcards or hyphens.
    
    Args:
        ip_range: IP range (e.g., "192.168.1.*" or "192.168.1.1-255")
    """
    return run_nmap_command([ip_range])

@mcp.tool()
def scan_tcp_port(target: str, port: str) -> str:
    """Scan specific TCP port on target.
    
    Args:
        target: IP address or hostname
        port: TCP port (e.g., "T:80,443" or just "80")
    """
    return run_nmap_command(["-p", port, target])

@mcp.tool()
def scan_top_ports(target: str, num_ports: int = 10) -> str:
    """Scan the top N most common ports.
    
    Args:
        target: IP address or hostname
        num_ports: Number of top ports to scan (default: 10)
    """
    return run_nmap_command(["--top-ports", str(num_ports), target])

@mcp.tool()
def scan_from_file(file_path: str) -> str:
    """Scan hosts listed in a file.
    
    Args:
        file_path: Path to file containing list of IP addresses/hostnames
    """
    return run_nmap_command(["-iL", file_path])

@mcp.tool()
def verbose_scan(target: str) -> str:
    """Perform a scan with verbose output for detailed information.
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-v", target])

@mcp.tool()
def scan_with_normal_output(target: str, output_file: str = "output.txt") -> str:
    """Perform scan and save results to text file.
    
    Args:
        target: IP address or hostname
        output_file: Output filename (default: output.txt)
    """
    return run_nmap_command(["-oN", output_file, target])

@mcp.tool()
def scan_with_xml_output(target: str, output_file: str = "output.xml") -> str:
    """Perform scan and save results to XML file.
    
    Args:
        target: IP address or hostname
        output_file: Output filename (default: output.xml)
    """
    return run_nmap_command(["-oX", output_file, target])

@mcp.tool()
def scan_with_all_formats(target: str, output_base: str = "output") -> str:
    """Perform scan and save results in all available formats.
    
    Args:
        target: IP address or hostname
        output_base: Base filename for outputs (will create .xml, .nmap, .gnmap files)
    """
    return run_nmap_command(["-oA", output_base, target])

@mcp.tool()
def nmap_help() -> str:
    """Display Nmap help with all available options and flags."""
    return run_nmap_command(["-h"])

@mcp.tool()
def udp_scan(target: str) -> str:
    """Perform UDP port scan on target.
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sU", target])

@mcp.tool()
def fin_scan(target: str) -> str:
    """Perform FIN scan (stealth scan using FIN packets).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sF", target])

@mcp.tool()
def xmas_scan(target: str) -> str:
    """Perform Xmas scan (FIN, PSH, and URG flags set).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sX", target])

@mcp.tool()
def null_scan(target: str) -> str:
    """Perform NULL scan (no flags set).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sN", target])

@mcp.tool()
def tcp_connect_scan(target: str) -> str:
    """Perform TCP Connect scan (completes full TCP handshake).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sT", target])

@mcp.tool()
def stealth_scan_no_ping(target: str) -> str:
    """Perform stealth SYN scan without ping (skip host discovery).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sS", "-Pn", target])

@mcp.tool()
def tcp_connect_scan_no_ping(target: str) -> str:
    """Perform TCP Connect scan without ping (skip host discovery).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sT", "-Pn", target])

@mcp.tool()
def udp_scan_no_ping(target: str) -> str:
    """Perform UDP scan without ping (skip host discovery).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sU", "-Pn", target])

@mcp.tool()
def service_version_scan_no_ping(target: str) -> str:
    """Perform service version detection without ping (skip host discovery).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sV", "-Pn", target])

@mcp.tool()
def aggressive_scan_no_ping(target: str) -> str:
    """Perform aggressive scan without ping (skip host discovery).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-A", "-Pn", target])

@mcp.tool()
def port_scan_no_ping(target: str, ports: str) -> str:
    """Scan specific ports without ping (skip host discovery).
    
    Args:
        target: IP address or hostname
        ports: Port range (e.g., 20-80 or 22,80,443)
    """
    return run_nmap_command(["-p", ports, "-Pn", target])

@mcp.tool()
def fin_scan_no_ping(target: str) -> str:
    """Perform FIN scan without ping (skip host discovery).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sF", "-Pn", target])

@mcp.tool()
def xmas_scan_no_ping(target: str) -> str:
    """Perform Xmas scan without ping (skip host discovery).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sX", "-Pn", target])

@mcp.tool()
def null_scan_no_ping(target: str) -> str:
    """Perform NULL scan without ping (skip host discovery).
    
    Args:
        target: IP address or hostname
    """
    return run_nmap_command(["-sN", "-Pn", target])

@mcp.tool()
def top_ports_scan_no_ping(target: str, num_ports: int = 10) -> str:
    """Scan top ports without ping (skip host discovery).
    
    Args:
        target: IP address or hostname
        num_ports: Number of top ports to scan (default: 10)
    """
    return run_nmap_command(["--top-ports", str(num_ports), "-Pn", target])

@mcp.tool()
def execute_custom_nmap_command(command: str) -> str:
    """Execute any nmap command and return the output. This should be executed if the user wants to run a custom nmap command that is not predefined in the MCP tools.
    Args:
        command: Complete nmap command to execute (e.g., "-sS -p 80,443 scanme.nmap.org")
        
    Examples:
        execute_custom_nmap_command("nmap -sS -O 192.168.1.1")
        execute_custom_nmap_command("nmap -sV --script=vulscan/vulscan.nse -p 80,443 scanme.nmap.org")
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Return both stdout and stderr if available
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        if result.returncode != 0:
            output += f"Return Code: {result.returncode}\n"
            
        return output if output else "Command executed successfully with no output."
        
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 120 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport='stdio')
