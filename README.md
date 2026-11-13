# 🎧 AuraDesk AI — Multi-Agent Customer Support System

An intelligent, autonomous customer support desk built with **Microsoft AutoGen** and **Streamlit**. AuraDesk AI uses dynamic LLM-driven routing to triage incoming customer tickets, dispatch them to specialized department agents, audit responses for policy compliance and tone, and deliver customer-ready resolutions.

---

## ✨ Features

* **🧭 Dynamic Query Routing:** The Triage Router Agent evaluates incoming queries and automatically dispatches tickets to the right department specialist using AutoGen's `speaker_selection_method="auto"`.
* **🎯 Specialized Department Agents:** Dedicated agents for **Billing**, **Technical Support**, and **Shipping & Logistics** craft accurate, domain-specific resolutions.
* **🛡️ Built-in Quality & Compliance Audit:** A Policy Auditor Agent reviews drafts for empathy, brand tone, and company guidelines before delivery.
* **🎨 Modern Streamlit UI:** Features custom CSS styling, gradient banners, responsive cards, one-click sample tickets, and an expandable behind-the-scenes agent collaboration log.

---

## 🏗️ Multi-Agent Architecture

```text
User Ticket ──▶ [ 🧭 Triage Router Agent ]
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
[ 💳 Billing ]   [ 🔧 Technical ]  [ 📦 Shipping ]
        │               │               │
        └───────────────┼───────────────┘
                        ▼
             [ 🛡️ Policy Auditor Agent ]
                        │
                        ▼
           [ 🚀 Customer Delivery Agent ]
