<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2,6,12&height=170&section=header&text=Omi%20Job%20Assistant&fontSize=48&fontAlignY=35&animation=twinkling&fontColor=ffffff&desc=Voice-Activated%20Job%20Applications%20with%20Omi%20AI%20Wearable&descAlignY=55&descSize=18" width="100%" />

[![Omi DevKit](https://img.shields.io/badge/Omi-DevKit%202-FF6B6B?style=for-the-badge)](.)
[![Claude API](https://img.shields.io/badge/Claude-Powered-8B5CF6?style=for-the-badge&logo=anthropic&logoColor=white)](.)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](.)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](.)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Say "Apply to [job URL]" — your Omi wearable handles the rest.**

</div>

---

## What This Does

Omi Job Assistant bridges the Omi AI wearable with the Job Application Automator. Speak a voice command, and the system automatically extracts the job posting, matches it against your resume, and submits a tailored application — hands-free.

---

## Architecture

```
┌──────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  Omi DevKit  │     │   FastAPI Webhook    │     │  Job Automator      │
│  (wearable)  │────▶│   Server             │────▶│  Engine             │
│              │     │                      │     │                     │
│  "Apply to   │     │  • Parse voice cmd   │     │  • Scrape job page  │
│   [job URL]" │     │  • Extract URL       │     │  • Match resume     │
│              │     │  • Trigger pipeline   │     │  • Fill application │
│              │     │  • Send notification  │     │  • Submit           │
└──────────────┘     └─────────────────────┘     └─────────────────────┘
         ▲                                                │
         │                                                │
         └──────── Notification: "Applied ✅" ◀───────────┘
```

---

## How It Works

| Step | Action | Technology |
|------|--------|------------|
| **1** | Wear Omi — always listening for commands | Omi DevKit 2 |
| **2** | Say "Apply to [job URL]" | Voice recognition |
| **3** | Webhook receives transcript + extracts URL | FastAPI |
| **4** | Job page scraped, fields extracted | Claude API + Browser Automation |
| **5** | Application auto-filled from stored resume | Job Automator MCP |
| **6** | Omi notifies you: "Applied successfully ✅" | Push notification |

---

## Quick Start

```bash
git clone https://github.com/ajay-automates/omi-job-assistant.git
cd omi-job-assistant
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key
python main.py
```

Configure your Omi DevKit webhook URL to point to `http://your-server:8000/webhook`.

---

## Tech Stack

`Omi DevKit 2` `FastAPI` `Claude API` `Python` `Webhook Integration` `Browser Automation`

---

## Related Projects

| Project | Description |
|---------|-------------|
| [Job Application Automator MCP](https://github.com/ajay-automates/job-application-automator-mcp) | Core MCP server powering autonomous applications |
| [EazyApply](https://github.com/ajay-automates/eazyapply) | Chrome extension for manual one-click filling |
| [AI Voice Agent](https://github.com/ajay-automates/ai-voice-agent) | Voice-powered document Q&A with Whisper + GPT-4o |

---

<div align="center">

**Built by [Ajay Kumar Reddy Nelavetla](https://github.com/ajay-automates)** · October 2025

*Apply to jobs without touching your keyboard.*

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2,6,12&height=100&section=footer" width="100%" />

</div>
