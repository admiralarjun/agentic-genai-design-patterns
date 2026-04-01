from google.adk.agents.llm_agent import Agent
import requests

import requests
import time

def get_pypi_info(package: str, version: str = None, retries: int = 2) -> dict:
    """
    Fetch package metadata from PyPI using the package name and version (if available).
    """

    url = f"https://pypi.org/pypi/{package}/{version}/json" if version else f"https://pypi.org/pypi/{package}/json"

    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, timeout=3)

            if resp.status_code == 404:
                return {
                    "status": "not_found",
                    "package": package
                }

            if resp.status_code != 200:
                return {
                    "status": "error",
                    "package": package,
                    "error": f"status {resp.status_code}"
                }

            data = resp.json()

            return {
                "status": "success",
                "package": package,
                "version": data["info"]["version"],
                "summary": data["info"].get("summary", "")
            }

        # To Handle timeout exceptions
        except requests.exceptions.Timeout:
            if attempt < retries:
                time.sleep(1)
                continue
            return {
                "status": "timeout",
                "package": package
            }

        except Exception as e:
            return {
                "status": "error",
                "package": package,
                "error": str(e)
            }

def check_osv(package: str, version: str = None, retries: int = 2) -> dict:
    """
    Check vulnerabilities for a package using OSV.dev
    """

    url = "https://api.osv.dev/v1/query"

    payload = {
        "package": {
            "name": package,
            "ecosystem": "PyPI"
        }
    }

    if version:
        payload["version"] = version

    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, json=payload, timeout=3)

            if resp.status_code != 200:
                return {
                    "status": "error",
                    "package": package,
                    "error": f"status {resp.status_code}"
                }

            data = resp.json()
            vulns = data.get("vulns", [])

            return {
                "status": "success",
                "package": package,
                "vulnerabilities": [v["id"] for v in vulns],
                "severity": "high" if vulns else "low"
            }

        except requests.exceptions.Timeout:
            if attempt < retries:
                time.sleep(1)
                continue
            return {
                "status": "timeout",
                "package": package
            }

        except Exception as e:
            return {
                "status": "error",
                "package": package,
                "error": str(e)
            }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='dependency_risk_agent',
    description='Analyzes dependencies using PyPI and OSV.',
    instruction="""
You are a dependency risk analysis agent.

For each package:

1. First call get_pypi_info
2. Call check_osv

Summarize with links, severity, 2-3 actions recommended 
""",
    tools=[get_pypi_info, check_osv],
)
