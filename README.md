<div align="center">

# 📞 PhoneIntel

**Phone number metadata lookup — country, carrier, type & timezone**

![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux%20%7C%20macOS%20%7C%20Windows-green)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

</div>

---

## ⚠️ What this tool actually does (read this first)

NumLookup reads **public phone-numbering-plan data** (the same data Google's
[libphonenumber](https://github.com/google/libphonenumber) uses). From a
number it can tell you:

- The **country / region** the number is allocated to
- The **carrier / network operator** (where publicly mapped — not available
  for all countries, and often unavailable for ported or VoIP numbers)
- The **number type** (mobile, fixed line, VoIP, toll-free, etc.)
- The number's **timezone(s)**
- Whether the number is validly formatted / assigned

### What it does NOT do, and why

| Claim | Reality |
|---|---|
| GPS location of the phone | **Impossible from a number alone.** Only the carrier can locate a device, and only via a lawful process (warrant, emergency trace, or the device owner's own consent through their OS). Any tool claiming to do this from just a number is misleading or malicious. |
| IMEI number | **Unrelated data.** A phone number identifies a SIM/subscription; an IMEI identifies a physical handset. There is no public or private database mapping one to the other. The only legitimate way to see a device's IMEI is on the device itself (dial `*#06#`) or its box/receipt. |

This project will not add those features because they don't exist as real,
working capabilities — not because of a policy choice.

## ✨ Features

- Country / region name and ISO region code
- Carrier / network name (public data)
- Number type (mobile, fixed line, VoIP, toll-free, premium rate, etc.)
- Timezone(s)
- E.164 / international / national formatting
- Validity and "possible number" checks
- Interactive mode, single-shot CLI mode, and `--json` output for scripting

## 🚀 Installation

### Termux
```bash
pkg update && pkg install python git -y
git clone https://github.com/krishnadipchoudhury/phoneintel
cd numlookup
pip install -r requirements.txt
python numlookup.py
```

### Linux / macOS / Windows
```bash
git clone https://github.com/<your-username>/numlookup.git
cd numlookup
pip install -r requirements.txt
python3 numlookup.py
```

## 🕹️ Usage

**Interactive mode:**
```bash
python numlookup.py
```

**Single lookup:**
```bash
python numlookup.py "+14155552671"
```

**No country code? Supply a default region:**
```bash
python numlookup.py "4155552671" --region US
```

**Machine-readable output:**
```bash
python numlookup.py "+442071838750" --json
```

### Example output
```
┌───────────────── NUMBER LOOKUP RESULT ─────────────────┐
│ Input                   +14155552671                    │
│ Valid number            Yes                              │
│ E.164 format            +14155552671                     │
│ International format    +1 415-555-2671                  │
│ National format          (415) 555-2671                  │
│ Country / region         United States (US)               │
│ Country calling code     +1                               │
│ Carrier / network        Unavailable (ported/VoIP likely) │
│ Number type               Fixed line or mobile             │
│ Timezone(s)                America/Los_Angeles             │
└──────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
numlookup/
├── numlookup.py        # main CLI tool
├── requirements.txt    # dependencies
├── README.md           # this file
├── LICENSE             # MIT license
└── .gitignore
```

## 🤝 Contributing

PRs welcome — e.g. batch lookups from a CSV, a simple web UI, more output formats.
Please don't open PRs attempting to add location-tracking or IMEI-lookup
"features" — see the limitations section above for why that can't work.

## 📜 License

Released under the [MIT License](LICENSE).
