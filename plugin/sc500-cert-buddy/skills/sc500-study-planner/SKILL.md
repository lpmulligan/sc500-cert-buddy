---
name: sc500-study-planner
description: Generates a personalized SC-500 study plan based on the learner's self-assessed confidence across the four SC-500 domains and their 12 sub-areas, prioritizing weak areas with estimated hours, Microsoft Learn module links, and a lab plan that respects the learner's licenses. Use when the learner asks for a study plan, is unsure what to study, or wants exam prep guidance for the Microsoft Cloud and AI Security Engineer Associate certification.
---

# Skill: sc500.study_planner.personalized

**Description:** Generates a personalized SC-500 (Implementing End-to-End Security Controls for Cloud and AI Workloads) study plan based on the learner's self-assessed confidence across exam domains and sub-areas. The plan prioritizes weak areas with estimated hours and Microsoft Learn module links, and marks which sub-areas the learner can practice hands-on with the licenses they have. SC-500 is an associate-level exam for practicing security engineers, so the plan favors hands-on configuration and troubleshooting over definitions.

## Grounding

**Required sources:**

- `.claude/skills/_references/sc500-objective-domain.md` (canonical SC-500 skills measured, synced verbatim from the Microsoft Learn study guide)
- `.claude/skills/_references/sc500-lab-requirements.md` (license and cost tier for every objective)
- Microsoft Learn (access via the **Microsoft Learn MCP server** `mslearn` using `microsoft_docs_search` for current Learn module URLs)
- Use `microsoft_docs_fetch` to verify Learn module links are current and active

## Workflow

1. **Present domains with weights.** Show the four SC-500 domains and their exam weight percentages:

   | Domain | Exam Weight |
   | --- | --- |
   | Manage identity, access, and governance | 20-25% |
   | Secure storage, databases, and networking | 25-30% |
   | Secure compute | 20-25% |
   | Manage and monitor security posture | 20-25% |

2. **Offer optional finer-grained confidence ratings.** SC-500 has four domains and 12 sub-areas. If the learner wants a more targeted plan, offer to rate each sub-area separately:

   **Domain 1 sub-areas (Manage identity, access, and governance):**
   - 1.1 Secure access to resources by using Microsoft Entra ID (PIM, Conditional Access, authentication methods, app identity, consent, managed identities)
   - 1.2 Secure secrets and keys by using Azure Key Vault (deploy, settings, access, firewall, keys, secrets, certificates, Defender CSPM secret scanning, Defender for Key Vault)
   - 1.3 Implement governance to enforce security and regulatory compliance (Azure Policy, regulatory compliance, security standards, resource locks, Azure RBAC, custom roles, Azure Backup security, infrastructure as code)

   **Domain 2 sub-areas (Secure storage, databases, and networking):**
   - 2.1 Implement security for storage accounts (storage security, firewall rules, Defender for Storage, access policies)
   - 2.2 Implement security for databases (Azure SQL platform security, auditing, Defender for Databases)
   - 2.3 Implement security for Azure network services (NSGs and ASGs, Azure Virtual Network Manager, Virtual WAN, VPN, Microsoft Entra Private Access, private endpoints, Private Link service, Azure Firewall, Network Watcher)

   **Domain 3 sub-areas (Secure compute):**
   - 3.1 Implement security for AI (SharePoint oversharing, Purview DSPM, Copilot Studio real-time protection, Microsoft Entra Agent ID, AI Gateway, Defender for AI Services, Foundry guardrails, Data and AI security dashboard, agent management in the Microsoft 365 admin center)
   - 3.2 Implement security for servers and VMs (disk encryption, Azure Bastion, JIT VM access, Azure Arc, Defender for Servers, agentless scanning, Trusted launch, Azure Machine Configuration)
   - 3.3 Implement security for application platform services (Defender for Containers, AKS, Container Registry, Container Instances and Container Apps, Functions, Logic Apps, App Service, Web Application Firewall, API Management)

   **Domain 4 sub-areas (Manage and monitor security posture):**
   - 4.1 Manage security posture by using Defender for Cloud (Defender CSPM, compliance frameworks, workload protection plans, AWS and GCP connectors, Defender Vulnerability Management, Defender EASM)
   - 4.2 Implement activity and event collection in Microsoft Sentinel (workspaces, roles, content hub, data connectors, syslog and CEF, Windows Security events, custom tables, automation, retention, Purview Audit in Defender XDR)
   - 4.3 Implement Microsoft Security Copilot (workspaces, roles, plugins, agents)

3. **Ask for confidence ratings.** Ask the learner to rate confidence in each area on a 1-5 scale, or use one of these levels if the learner prefers words:
   - **5 - Strong** -- configures this in production; needs only light review.
   - **4 - Comfortable** -- has configured it before; needs targeted reinforcement.
   - **3 - Moderate** -- understands the concepts but has little hands-on time.
   - **2 - Weak** -- limited experience; needs focused study.
   - **1 - New** -- no prior exposure; needs ground-up study.
   - **Unknown** -- not sure; treat as weak (level 2).

4. **Ask what the learner can lab with.** Hands-on practice matters on an associate exam, but several SC-500 objectives need premium licenses or paid plans. Ask which of these the learner has, or can get a trial of:
   - An Azure subscription they can use for labs (required for most of the exam).
   - Microsoft Entra ID P1 or P2 (Conditional Access, PIM).
   - A Microsoft 365 E5 tenant or trial (Purview, SharePoint Advanced Management, Defender XDR).
   - Microsoft Agent 365 (Entra Agent ID controls, agent security in Defender).
   - Security Copilot capacity (SCUs).

   Use `.claude/skills/_references/sc500-lab-requirements.md` to mark each sub-area as **Lab-ready**, **Partly lab-ready**, or **Quiz and walkthrough** for this learner. Unknown answers count as not available.

5. **Ask for a target exam window.** Offer three preset time-to-exam options and let the learner pick or supply a custom window:
   - **2 weeks** (intensive sprint; trims optional reading, doubles down on practice questions and the highest-weight labs)
   - **4 weeks** (balanced; the default recommendation)
   - **8 weeks** (thorough; adds extra Microsoft Learn modules, a lab for every lab-ready objective, and a second pass of practice questions)

   The total estimated hours range scales with the chosen window; per-day or per-week hour targets are produced from the totals.

6. **Generate a prioritized study plan.** Based on the ratings, the lab access, and the chosen window:
   - Order sub-areas from weakest to strongest.
   - Within equal confidence levels, prioritize sub-areas with higher exam weight (Domain 2 first at 25-30%, then the three 20-25% domains), and within a domain, prioritize sub-areas with more skills measured (3.1 Implement security for AI has 11).
   - For each sub-area, provide:
     - Estimated study hours (level 1-2: 10-14 hours, level 3: 6-8 hours, level 4-5: 2-4 hours; scale by the chosen window).
     - Two to three specific Microsoft Learn module links (grounded by way of the Microsoft Learn MCP server `mslearn`; do not invent URLs).
     - Key skills to focus on (pulled from `.claude/skills/_references/sc500-objective-domain.md`).
     - The lab status for this learner (**Lab-ready**, **Partly lab-ready**, or **Quiz and walkthrough**), and the license or plan that blocks any missing labs.
     - A pointer to the `sc500-item-creator` skill for a practice question batch on the sub-area, and to the `sc500-lab-creator` skill for a hands-on lab.
   - Include a total estimated hours range at the bottom, broken into per-day or per-week targets that fit the chosen window.

7. **Call out audience-fit context.** SC-500 has no required prerequisite certification, but Microsoft expects practical Azure and hybrid administration experience, strong Microsoft Entra ID familiarity, and familiarity with Microsoft 365 administration. If the learner reports weak Azure administration (virtual networks, VMs, storage, RBAC) or weak Entra ID basics, recommend a ramp on those fundamentals before the security sub-areas.

8. **Offer to start practicing.** After presenting the plan, ask: "Would you like to start with practice questions or a hands-on lab on **[first recommended sub-area]**?"

## Microsoft Learn topic anchors

Use the Microsoft Learn MCP server `mslearn` to search the SC-500 ecosystem. Anchor searches to current product names and topic clusters:

- **Identity** -- Microsoft Entra Privileged Identity Management, Conditional Access, authentication methods policy, passkeys, app registrations, admin consent workflow, managed identities
- **Secrets** -- Azure Key Vault RBAC, Key Vault network security, key rotation, certificates, Defender for Key Vault
- **Governance** -- Azure Policy definitions and effects, regulatory compliance in Defender for Cloud, Microsoft cloud security benchmark, resource locks, Azure RBAC, custom roles, Azure Backup security features, Bicep
- **Data** -- Azure Storage security, shared access signatures, Defender for Storage, Azure SQL security, Azure SQL auditing, Defender for Databases
- **Network** -- network security groups, application security groups, Azure Virtual Network Manager security admin rules, Virtual WAN, VPN Gateway, Microsoft Entra Private Access, private endpoints, Private Link service, Azure Firewall, Network Watcher
- **AI security** -- SharePoint Advanced Management, Purview Data Security Posture Management, Copilot Studio real-time protection, Microsoft Entra Agent ID, AI gateway in Azure API Management, Defender for AI Services, Foundry guardrails, Data and AI security dashboard, agent management in the Microsoft 365 admin center
- **Compute** -- Azure Disk Encryption, encryption at host, Azure Bastion, just-in-time VM access, Azure Arc-enabled servers, Defender for Servers, agentless scanning, Trusted launch, Azure Machine Configuration
- **App platform** -- Defender for Containers, AKS security, Container Registry security, Container Apps security, App Service authentication, Azure Functions networking, Logic Apps security, Web Application Firewall, API Management policies
- **Posture** -- Defender CSPM, attack path analysis, workload protection plans, AWS and GCP connectors, Defender Vulnerability Management, Defender EASM
- **Sentinel** -- Microsoft Sentinel workspaces, Sentinel roles, content hub, data connectors, syslog and CEF with the Azure Monitor Agent, data collection rules, custom tables, automation rules, playbooks, retention, Purview Audit
- **Security Copilot** -- Security Copilot workspaces, roles, plugins, agents, Security Compute Units

Always verify links with `microsoft_docs_fetch` before placing them in the final plan.

## Output format

```markdown
## Your Personalized SC-500 Study Plan

**Target exam window:** [2 weeks / 4 weeks / 8 weeks / custom]
**Exam:** SC-500 -- Implementing End-to-End Security Controls for Cloud and AI Workloads
**Pass score:** 700

### Priority 1: [Sub-area code and name] (domain weight: XX-XX%)

**Your confidence:** [1-5 or word rating]
**Estimated study time:** X-X hours
**Lab status:** [Lab-ready / Partly lab-ready / Quiz and walkthrough] -- [license or plan that blocks missing labs, if any]

**Focus skills:**
- [Skill 1]
- [Skill 2]
- [Skill 3]

**Recommended Microsoft Learn modules:**
- [Module title](URL)
- [Module title](URL)

**Next step:** Run the `sc500-item-creator` skill for a practice question batch on this sub-area, or the `sc500-lab-creator` skill for a hands-on lab.

---

### Priority 2: [Sub-area code and name] (domain weight: XX-XX%)

... (repeat for each sub-area; include all 12, even strong ones, with a light review recommendation)

---

**Total estimated study time:** XX-XX hours
**Suggested cadence:** [per-day or per-week hour targets that fit the chosen window]

**Audience fit:** SC-500 expects practical Azure and hybrid administration experience and strong Microsoft Entra ID familiarity. Comfortable with virtual networks, VMs, storage, and Azure RBAC? (yes / no / not sure)

Ready to start? I can generate practice questions or a hands-on lab on **[first recommended sub-area]**.
```

## Style

Plan prose follows the **Microsoft Writing Style Guide** (MWSG): warm, scannable, present-tense, sentence-style capitalization, Oxford commas, plain ASCII (no curly quotes, no en or em dashes -- use `--` and `->`). Override one MWSG convention: **no contractions** (the same rule the **Microsoft Worldwide Learning Exam Writing Style Guide** applies to exam items). When a plan mentions a fictional company in an example, draw from the WWL-approved list and use the full company name (a few common picks: A. Datum Corporation, Adventure Works Cycles, Blue Yonder Airlines, Contoso, Ltd., Fabrikam, Inc., Litware, Inc., Northwind Traders, Tailspin Toys, Wide World Importers, Woodgrove Bank). Always use current Microsoft product names; never use retired or legacy names.

## Guardrails

- Do not skip any of the 12 sub-areas. Even strong areas appear in the plan with a light review recommendation.
- Do not invent Microsoft Learn module URLs. Use the Microsoft Learn MCP server `mslearn` (`microsoft_docs_search`) to find real, current module links, and verify with `microsoft_docs_fetch`.
- Treat unknown confidence the same as weak (level 2), and unknown license access as not available.
- Always use current Microsoft product names. Use **Microsoft Entra ID**, never *Azure AD*. Use **Microsoft Defender for Cloud**, never *Azure Security Center*. Use **Microsoft Sentinel**, never *Azure Sentinel*. Use **Microsoft Defender XDR**, never *Microsoft 365 Defender*.
- No contractions.
- SC-500 has no required prerequisite certification. Do not invent prerequisites; instead, surface the audience-fit prompt described above.

## Delivery rules

Deliver the full study plan in a single message after the learner provides confidence ratings, lab access, and a target exam window. Do not split the plan across multiple messages.
