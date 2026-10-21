#!/usr/bin/env python3
"""
NumLookup - phone number metadata lookup.

Looks up a phone number's country, carrier/network, number type, timezone(s),
and validity using Google's libphonenumber data (via the `phonenumbers` package).

IMPORTANT / HONEST LIMITATIONS:
This tool reads PUBLIC NUMBERING-PLAN DATA (how numbers are allocated to
countries and carriers). It does NOT and CANNOT:
  - find the real-time GPS location of a phone
  - retrieve a device's IMEI
  - track, locate, or identify the person who owns the number
No legitimate tool can do those things from a number alone - that data is
only accessible to carriers, and only through a lawful process.
"""

import argparse
import json
import sys

try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
except ImportError:
    print(
        "Missing dependency. Install it with:\n"
        "    pip install -r requirements.txt\n"
        "or:\n"
        "    pip install phonenumbers rich",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import box

    RICH = True
    console = Console()
except ImportError:
    RICH = False


def lookup(raw_number: str, default_region: str = None) -> dict:
    """Parse a number and return everything libphonenumber's public data knows."""
    try:
        parsed = phonenumbers.parse(raw_number, default_region)
    except phonenumbers.NumberParseException as error:
        return {"input": raw_number, "error": str(error)}

    valid = phonenumbers.is_valid_number(parsed)
    possible = phonenumbers.is_possible_number(parsed)

    number_type_map = {
        phonenumbers.PhoneNumberType.MOBILE: "Mobile",
        phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed line",
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed line or mobile",
        phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-free",
        phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium rate",
        phonenumbers.PhoneNumberType.SHARED_COST: "Shared cost",
        phonenumbers.PhoneNumberType.VOIP: "VoIP",
        phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal number",
        phonenumbers.PhoneNumberType.PAGER: "Pager",
        phonenumbers.PhoneNumberType.UAN: "UAN",
        phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail",
        phonenumbers.PhoneNumberType.UNKNOWN: "Unknown",
    }

    region_code = phonenumbers.region_code_for_number(parsed)
    country_name = geocoder.description_for_number(parsed, "en") or "Unknown"
    network = carrier.name_for_number(parsed, "en") or "Unavailable (often true for mobile-ported or VoIP numbers)"
    zones = timezone.time_zones_for_number(parsed)

    return {
        "input": raw_number,
        "valid": valid,
        "possible": possible,
        "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164) if possible else None,
        "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL) if possible else None,
        "national": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL) if possible else None,
        "country_region_code": region_code,
        "country_or_region": country_name,
        "carrier": network,
        "number_type": number_type_map.get(phonenumbers.number_type(parsed), "Unknown"),
        "country_calling_code": parsed.country_code,
        "timezones": list(zones),
    }


def print_result(result: dict):
    if "error" in result:
        msg = f"Could not parse '{result['input']}': {result['error']}"
        if RICH:
            console.print(f"[bold red]{msg}[/]")
            console.print(
                "[dim]Tip: include the country code, e.g. +1 555 123 4567, "
                "or pass --region US[/]"
            )
        else:
            print(msg)
        return

    if not result["possible"]:
        msg = f"'{result['input']}' doesn't look like a possible phone number."
        print(f"[bold red]{msg}[/]" if False else msg)
        return

    if RICH:
        table = Table(box=box.ROUNDED, border_style="bright_cyan", show_header=False)
        table.add_column("Field", style="bright_cyan")
        table.add_column("Value", style="bright_green")
        table.add_row("Input", result["input"])
        table.add_row("Valid number", "Yes" if result["valid"] else "No (possible, but not a real assigned number)")
        table.add_row("E.164 format", result["e164"] or "-")
        table.add_row("International format", result["international"] or "-")
        table.add_row("National format", result["national"] or "-")
        table.add_row("Country / region", f"{result['country_or_region']} ({result['country_region_code']})")
        table.add_row("Country calling code", f"+{result['country_calling_code']}")
        table.add_row("Carrier / network", result["carrier"])
        table.add_row("Number type", result["number_type"])
        table.add_row("Timezone(s)", ", ".join(result["timezones"]) or "Unknown")
        console.print(Panel(table, title="[bold]NUMBER LOOKUP RESULT[/]", border_style="bright_green"))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")


def interactive():
    if RICH:
        console.print(
            Panel(
                "Enter a phone number in international format, e.g. [bright_green]+14155552671[/]\n"
                "Type [bright_cyan]exit[/] to quit.",
                title="[bold]NUMLOOKUP[/]",
                border_style="bright_cyan",
            )
        )
    else:
        print("NumLookup - enter a number in international format (+countrycode...), or 'exit'.")

    while True:
        try:
            raw = input("number> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw:
            continue
        if raw.lower() in ("exit", "quit"):
            break
        print_result(lookup(raw))
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Look up a phone number's country, carrier, type, and timezone "
        "from public numbering-plan data. Cannot locate a device or retrieve an IMEI."
    )
    parser.add_argument("number", nargs="?", help="Phone number, ideally with country code, e.g. +14155552671")
    parser.add_argument(
        "-r", "--region",
        help="Default region (2-letter code, e.g. US) to assume if the number has no country code",
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of a formatted table")
    args = parser.parse_args()

    if not args.number:
        interactive()
        return

    result = lookup(args.number, args.region)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_result(result)


if __name__ == "__main__":
    main()
