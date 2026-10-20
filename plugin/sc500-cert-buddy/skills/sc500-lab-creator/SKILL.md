---
name: sc500-lab-creator
description: Create short SC-500 practice labs (15-30 minutes) that are executable and self-validating. Every lab opens with a license and cost gate, then includes prerequisites, exact tasks, validation steps, expected outputs, and cleanup. Scope covers Microsoft Entra ID, Azure Key Vault, Azure Policy and RBAC, storage and database security, Azure network security, AI security, VM and container security, Microsoft Defender for Cloud, Microsoft Sentinel, and Microsoft Security Copilot. Use when the user asks for a hands-on lab, practice exercise, or guided walkthrough.
---

# Skill: sc500.practice_labs.micro.validated

**Description:** Create short SC-500 practice labs (15-30 minutes) that are executable and self-validating. Every lab includes a license and cost gate, prerequisites, exact tasks, validation steps, expected outputs, and cleanup.

## Audience profile

The SC-500 audience is an associate-level security engineer. Learners have practical experience administering Azure and hybrid environments (compute, network, and storage), strong familiarity with Microsoft Entra ID, and familiarity with Microsoft 365 administration. Lab prose stays direct and assumes the learner can find their way around the Azure portal and run Azure CLI or Azure PowerShell. Explain *why* a control matters, not *where* the **Create** button is.

## Style precedence

Follow the **Microsoft Worldwide Learning Exam Writing Style Guide** (WWL) for any text that mirrors exam phrasing (titles, goal statements, named resources, company references). Follow the **Microsoft Writing Style Guide** (MWSG) for the lab prose itself: warm, scannable, present-tense, sentence-style capitalization. Two MWSG conventions overridden by WWL for our labs: **no contractions** and **all uppercase for key names** (TAB, ENTER, CTRL+ALT+DELETE).

## Every objective gets a lab

The learner wants a lab for **every** SC-500 objective, including the ones that need a premium license or a paid plan. Never refuse a lab because of licensing. Instead, look up the objective in `.claude/skills/_references/sc500-lab-requirements.md` and:

1. Put a **License and cost gate** callout at the top of the lab. List every requirement tier for the objective (`FREE`, `PAYG`, `TRIAL`, `ENTRA-P1`, `ENTRA-P2`, `ENTRA-SSE`, `M365`, `AGENT365`, `SCU`), the trial option when one exists, and the exact cleanup step that stops the cost.
2. When the tier is anything other than `FREE` or `PAYG`, add a **No-license path**: a read-only walkthrough of the same portal pages, CLI help output, or Learn documentation, so the learner can still study the objective without the license.
3. Re-ground the licensing in Microsoft Learn before you publish. Licensing changes often. If Learn disagrees with the matrix, follow Learn and tell the learner the matrix needs an update.

## Lab categories

SC-500 labs span these categories, which map to the four exam domains:

- **identity** -- Microsoft Entra ID: PIM, Conditional Access, authentication methods, enterprise apps and app registrations, consent settings, managed identities, custom roles.
- **key-vault** -- Azure Key Vault deployment, access (Azure RBAC), firewall and private access, keys, secrets, certificates, Defender for Key Vault, and Defender CSPM secret scanning.
- **governance** -- Azure Policy (built-in and custom definitions), regulatory compliance in Defender for Cloud, resource locks, Azure RBAC role assignments, Azure Backup security features, and infrastructure as code.
- **storage-data** -- Storage account security, Storage firewall, access policies and shared access signatures, Defender for Storage, Azure SQL platform security and auditing, and Defender for Databases.
- **network** -- NSGs and ASGs, Azure Virtual Network Manager security admin rules, Virtual WAN, VPN, Microsoft Entra Private Access, private endpoints, Private Link service, Azure Firewall, and Network Watcher diagnostics.
- **ai-security** -- SharePoint oversharing, Purview DSPM, Copilot Studio real-time protection, Microsoft Entra Agent ID, AI Gateway in API Management for Microsoft Foundry, Defender for AI Services, Foundry guardrails, the Data and AI security dashboard, and agent management in the Microsoft 365 admin center.
- **compute** -- Disk encryption, Azure Bastion, JIT VM access, Azure Arc, Defender for Servers onboarding and settings, agentless scanning, Trusted launch, and Azure Machine Configuration.
- **app-platform** -- Defender for Containers, AKS, Container Registry, Container Instances and Container Apps, Azure Functions, Logic Apps, App Service, Web Application Firewall, and API Management back-end protection.
- **posture** -- Defender CSPM, compliance frameworks, workload protection plans, AWS and GCP connectors, Defender Vulnerability Management, and Defender EASM.
- **sentinel** -- Workspaces, roles, content hub, data connectors, syslog and CEF, Windows Security events with data collection rules, custom log tables, automation rules and playbooks, retention, and Purview Audit in Defender XDR.
- **security-copilot** -- Workspaces, roles, plugins, and Microsoft and Security Store agents.

Default authoring tools by category:

- **Portal path first** for configuration that the exam tests in the portal: the Azure portal, the Microsoft Entra admin center, the Microsoft Defender portal, the Microsoft Purview portal, the Microsoft 365 admin center, the Microsoft Foundry portal, and the Security Copilot portal.
- **Azure CLI** or **Azure PowerShell** for Azure resource operations, and **Microsoft Graph PowerShell** for Entra ID operations, when automation or validation needs a command.
- **Bicep** for the infrastructure as code objective (1.3.9) and whenever a lab deploys more than two resources.
- **KQL** for Sentinel, Defender XDR advanced hunting, and Log Analytics validation.

## Grounding

**Required sources:**

- Microsoft Learn (truth source for service capabilities, configuration, licensing, and architecture). Access via the **Microsoft Learn MCP server** (`mslearn`) using `microsoft_docs_search` and `microsoft_docs_fetch`.
- Microsoft Learn code samples (for Azure CLI, Azure PowerShell, Microsoft Graph PowerShell, Bicep, KQL, and policy JSON accuracy). Access via `microsoft_code_sample_search`.
- Canonical SC-500 objective domain file: `.claude/skills/_references/sc500-objective-domain.md`.
- License and cost matrix: `.claude/skills/_references/sc500-lab-requirements.md`.

Always ground first. Do not invent service capabilities, roles, SKUs, plan names, or portal paths.

## SC-500 domains (canonical)

| Domain | Key | Weight |
| --- | --- | --- |
| Manage identity, access, and governance | `identity` | 20-25% |
| Secure storage, databases, and networking | `storage-network` | 25-30% |
| Secure compute | `compute` | 20-25% |
| Manage and monitor security posture | `posture` | 20-25% |

## Style and word usage

### Resource and people naming (WWL)

- **Companies:** Use only WWL-approved fictional companies from `.claude/skills/_references/fictional-companies.md`. Use the **entire** company name on every mention. Randomize across the list -- do not default to Contoso, Ltd.
- **People:** *the user*, **User1, User2, User3**, or **Admin1, Admin2** (no spaces).
- **Resources:** VM1, VNet1, Subnet1, KV1, RG1, Sub1, App1, Workspace1, Policy1, Group1. Storage accounts are lowercase with a unique suffix (for example, `storage1` plus random digits), because storage account names are global.
- **Offices:** *main office*, *branch office*, *satellite office*. **Cities:** WWL-approved (Atlanta, Boston, Cairo, Frankfurt, London, New York, Paris, Seattle, Singapore, Sydney, Tokyo, and so on).
- Define each name on first mention.

### Word usage (WWL)

- **named**, not *called*.
- **report**, not *complain*.
- Avoid *determine*; use *verify, identify, set, establish, calculate, decide*.
- Avoid *may*; use *can* or *might*.
- Avoid *using* alone; use *by using*.
- Avoid specific determiners (*all, none, only, always, never*) and indefinite qualifiers (*few, many, multiple, several, some, usually*).
- *site* logical, *location* physical -- never interchange.
- Plural over *(s)*.
- Goal statements: *You need to ...* / *You need to ensure that ...*

### Formatting

- **Bold** for clickable UI elements, Azure CLI and PowerShell commands, and cmdlet names that are typed verbatim.
- Input-neutral verbs: *select* (not *click*), *enter* (not *type*), *go to*, *open*, *close*.
- Imperative mood in procedure steps.
- File names labelled with *file*: *the main.bicep file*, *the policy.json file*.
- **All uppercase** for key names: TAB, ENTER, CTRL+ALT+DELETE.
- Sentence-style capitalization elsewhere; product names and proper nouns are exceptions.
- Oxford comma in lists of three or more.
- Plain ASCII -- no curly quotes, en or em dashes; use `--` and `->`.
- Spell out zero through nine; numerals for 10 and above.

### Globalization

- Sentences 15-20 words. Active voice. Simple tenses.
- No `/` or `-` as punctuation (replace *create/edit/display* with *create, edit, and display*).
- No possessives on product names. No nominalizations. No noun stacks.

## Terminology rename table (non-negotiable)

Always use current Microsoft product names. Never use a retired or legacy name, even if the user does. Silently map to the current name. The full table lives in the **sc500-item-creator** skill; the names labs hit most often are:

| Retired / legacy name | Current name |
| --- | --- |
| Azure Active Directory (Azure AD) | Microsoft Entra ID |
| Azure AD Conditional Access | Microsoft Entra Conditional Access |
| Azure AD PIM | Microsoft Entra Privileged Identity Management |
| Azure AD Identity Protection | Microsoft Entra ID Protection |
| Azure Security Center / Azure Defender | Microsoft Defender for Cloud |
| Azure Sentinel | Microsoft Sentinel |
| Microsoft 365 Defender | Microsoft Defender XDR |
| Microsoft Copilot for Security | Microsoft Security Copilot |
| Azure Policy Guest Configuration | Azure Machine Configuration |
| Log Analytics agent (MMA, OMS agent) | Azure Monitor Agent |
| Azure AI Studio / Azure AI Foundry | Microsoft Foundry |

## Authentication defaults (non-negotiable)

For any command or code-based step:

- Sign in with **az login**, **Connect-AzAccount**, or **Connect-MgGraph** with the narrowest scopes the lab needs (for example, `Connect-MgGraph -Scopes "Policy.Read.All"`). Never use a broader scope than the step requires.
- Code uses **DefaultAzureCredential** from the **azure.identity** package, or a managed identity when the code runs in Azure.
- Never embed an account key, SQL password, client secret, or connection string in code, environment files, or configuration files. When an objective is about a key-based mechanism (for example, shared access signatures and stored access policies in objective 2.1.4), generate the value at run time, keep it out of files, and expire or revoke it in cleanup.
- Grant the learner the least-privileged role for the lab, and name it as a starting-state requirement (for example, **Key Vault Administrator** on RG1, or **Conditional Access Administrator** in the tenant).

## Tenant and subscription safety (non-negotiable)

SC-500 labs change security controls that can lock people out or affect a whole tenant. Every lab follows these rules:

- **Use a dedicated lab tenant and lab subscription.** Never run a lab against production. State this in the prerequisites.
- **Conditional Access:** exclude an emergency access (break-glass) account from every policy, create the policy in **Report-only** mode, verify the result in the sign-in logs, and only then switch to **On**. Cleanup deletes the policy.
- **Authentication methods and security defaults:** record the starting settings before you change them, and restore them in cleanup.
- **Defender for Cloud plans** are enabled at subscription scope and start a trial per plan. Cleanup turns off every plan the lab turned on.
- **Resource locks** block cleanup. Remove locks before deleting resources.
- **Key Vault purge protection** cannot be turned off after it is turned on. Labs use soft delete only, unless the objective requires purge protection; then warn that the vault name stays reserved for the retention period.
- **Azure Backup soft delete and immutability** can delay deletion. Order the cleanup steps so the learner is not stuck with a vault that cannot be deleted.
- **Security Copilot SCUs** bill in hourly blocks. Cleanup deprovisions every SCU the lab provisioned.

## Guardrails

- Stay within SC-500 scope (implementing and monitoring security controls). Avoid deep architecture design work that belongs to an expert-level exam.
- Prefer the lowest-cost path: the smallest VM size that supports the feature, consumption tiers, Basic SKUs where the feature allows, and free trials.
- **No contractions** anywhere in the lab.
- No ambiguous *click around until* steps. Every step has an exact UI label, exact CLI or PowerShell command, exact KQL query, or exact Bicep snippet.
- Always include cleanup or rollback, with a validation step that proves it worked.

## Cleanup expectations (non-negotiable)

Cleanup is non-negotiable in every lab. Common SC-500 cleanup targets include:

- **Resource groups** that contain lab-only resources, deleted with **az group delete --name RG1 --yes --no-wait** (remove resource locks first).
- **Defender for Cloud plans** turned on by the lab, turned off with **az security pricing create --name `<plan>` --tier free** or from **Environment settings** in the portal.
- **Conditional Access policies, authentication method changes, and consent settings**, deleted or restored to the recorded starting state.
- **PIM eligible assignments** and **role assignments** created by the lab.
- **Azure Policy assignments, custom definitions, and initiatives**.
- **Custom roles** (Azure and Microsoft Entra).
- **App registrations and enterprise applications** created by the lab.
- **Microsoft Sentinel**: remove the solution and delete the Log Analytics workspace (removing Sentinel alone does not delete the workspace).
- **Hourly-billed network resources**: Azure Firewall, VPN gateways, Virtual WAN hubs, Azure Bastion, Application Gateway, private endpoints.
- **Security Copilot capacity**: deprovision SCUs.
- **AWS or GCP connectors** and the cloud-side resources the onboarding template created.
- **Local artifacts**: downloaded files, generated keys, and local virtual environments.

Cleanup validation confirms that the deletion succeeded by listing the parent scope and showing that the resource is gone, or by showing that the setting is back to its starting value.

## License and cost gate placement

The **License and cost gate** callout appears immediately after the lab title and objective, **before** prerequisites. It states:

- Every requirement tier from `.claude/skills/_references/sc500-lab-requirements.md`.
- The cost driver (for example, *Azure Firewall bills by the hour while it exists*).
- The trial option, if any (for example, *Defender for Servers Plan 2 includes a 30-day trial per subscription*).
- The cleanup step that stops the cost.

Do not quote exact prices. Prices change by region and over time; point to the pricing page or the cost calculator instead.

## Fictional company randomization (non-negotiable)

Randomize across the WWL approved list. Do not default to Contoso, Ltd. Always use the full company name.

## Timebox guidance

A lab contains no more than 12 steps total across all tasks. If the lab requires more, split it into two narrower labs. Target completion time is 15-30 minutes, not counting resource deployment wait time. Call out long deployments (VPN gateways, API Management, Virtual WAN hubs) and suggest starting them first.

## Workflow

1. Choose a single SC-500 objective from `.claude/skills/_references/sc500-objective-domain.md` and state it at the top of the lab.
2. Look up the objective in `.claude/skills/_references/sc500-lab-requirements.md` and draft the **License and cost gate**.
3. Ground the intended configuration and the licensing in Microsoft Learn by using `microsoft_docs_search`.
4. Pick one primary path that matches the lab category (portal, Azure CLI, Azure PowerShell, Microsoft Graph PowerShell, Bicep, or KQL).
5. Use `microsoft_code_sample_search` to verify any CLI, PowerShell, Bicep, KQL, or policy JSON snippets.
6. Use `microsoft_docs_fetch` for full-page detail on any service capability, role, or configuration step.
7. Add validation gates after each major step (portal state, CLI or PowerShell output, KQL query result, sign-in log entry, or Defender for Cloud recommendation state).
8. Add a **No-license path** when the tier is not `FREE` or `PAYG`.
9. Add cleanup that exactly reverses the work, with a final validation that confirms deletion or restoration.
10. Run a **WWL style sweep**: company names full and approved; resource names follow the VM1/VNet1/KV1 pattern; people are *the user*, User1, or Admin1; no contractions; no banned word usage; UI labels bolded; key names uppercase; current product names only.

## Output format

```yaml
lab:
  title: "<Action + artifact, for example, 'Enforce just-in-time access to VM1 by using Defender for Servers'>"
  objective: "<objective number and text from the objective domain file>"
  domain: "<Manage identity, access, and governance | Secure storage, databases, and networking | Secure compute | Manage and monitor security posture>"
  subdomain: "<for example, Implement security for servers and virtual machines (VMs)>"
  category: "<identity | key-vault | governance | storage-data | network | ai-security | compute | app-platform | posture | sentinel | security-copilot>"
  estimated_time: "<15-30 min, plus deployment wait time if any>"
  license_and_cost_gate:
    tiers: ["<FREE | PAYG | TRIAL | ENTRA-P1 | ENTRA-P2 | ENTRA-SSE | M365 | AGENT365 | SCU>"]
    requirements: "<what the learner needs, from the matrix and re-grounded in Learn>"
    cost_driver: "<what bills, and how>"
    trial: "<trial option, or 'none'>"
    stop_cost: "<the exact cleanup step that stops the cost>"
  prerequisites:
    - "<Dedicated lab tenant and lab subscription -- never production>"
    - "<Least-privileged role, for example, Owner on RG1 or Conditional Access Administrator>"
    - "<Azure CLI, Azure PowerShell, or Microsoft Graph PowerShell, and the sign-in command>"
  starting_state:
    - "<What must already exist, including recorded starting settings for anything the lab changes>"
  tasks:
    - name: "<Task 1 name>"
      steps: |
        <Numbered steps when sequencing matters. Use exact UI labels, exact commands, or exact queries.>
      validation:
        - "<Validation command or check and what success looks like>"
    - name: "<Task 2 name>"
      steps: |
        <...>
      validation:
        - "<...>"
  no_license_path:
    - "<Only when the tier is not FREE or PAYG. Read-only walkthrough steps that cover the same objective.>"
  troubleshooting:
    - symptom: "<common failure, for example, the JIT request option is unavailable on VM1>"
      fix: "<precise fix, for example, verify that Defender for Servers Plan 2 is enabled on Sub1>"
  cleanup:
    steps: |
      <Exact deletion and restoration steps, in an order that works around locks, soft delete, and dependencies>
    validation:
      - "<Listing command or check that confirms the resource is gone or the setting is restored>"
  references:
    - "<Microsoft Learn URL or URLs, including the licensing source>"
```

## Delivery rules

Labs are delivered in full (all sections in a single message). Unlike practice questions, there is no interactive hold-back. If multiple labs are requested, deliver each lab sequentially in the same message.

## Quality checklist

- Single objective, single outcome.
- The **License and cost gate** lists every tier from the matrix, and the licensing was re-grounded in Learn.
- A **No-license path** exists when the tier is not `FREE` or `PAYG`.
- Every task has an explicit validation gate.
- Cleanup is complete and safe, follows the tenant and subscription safety rules, and includes a deletion or restoration check.
- Instructions use Microsoft formatting rules for UI labels, commands, and queries.
- All product names use current terminology.
- No contractions.
- Fictional company is randomized and uses the full WWL-approved name (not always Contoso, Ltd.).
- Resource names follow VM1/VNet1/KV1/App1 patterns; people are *the user*, User1, or Admin1.
- Lab category is one of the categories listed above.
- Commands use Microsoft Entra ID sign-in and least-privileged scopes; no embedded keys or secrets.

---

## Prompt template

```text
Create {{count}} SC-500 micro-labs.

Inputs:

- domain: {{domain}} (or select from .claude/skills/_references/sc500-objective-domain.md)
- objective: {{objective}} (or derive from Learn)
- category: {{category}} (identity | key-vault | governance | storage-data | network | ai-security | compute | app-platform | posture | sentinel | security-copilot)
- tool_preference: {{tool_preference}} (Portal | Azure CLI | Azure PowerShell | Microsoft Graph PowerShell | Bicep | KQL)
- timebox: {{timebox}} (default 25 minutes)

Requirements:

1. Ground the lab outcome and the licensing in Microsoft Learn first by using the Microsoft Learn MCP server (mslearn).
2. Use microsoft_code_sample_search for CLI, PowerShell, Bicep, KQL, or policy syntax accuracy.
3. Open with the License and cost gate from .claude/skills/_references/sc500-lab-requirements.md.
4. Use Microsoft Entra ID sign-in with least-privileged scopes. Do not embed keys or secrets.
5. Output by using output_format exactly.
6. Randomize the WWL-approved fictional company name. Use the full company name on every mention.
```


## Gradable output (labs/<slug>/) -- required

Every lab must be emitted as a gradable document, not just printed in chat. Save two files under `labs/<slug>/`, where `<slug>` is a short kebab-case name that starts with the objective number (for example, `3-2-3-jit-vm-access`):

1. **`labs/<slug>/lab.md`** -- the learner-facing lab: the license and cost gate, objective, prerequisites, numbered steps, a validation gate after each major step, the no-license path when applicable, troubleshooting, and a mandatory cleanup step. Cite Microsoft Learn URLs for every service, command, and licensing claim.

2. **`labs/<slug>/answer-key.json`** -- the canonical answer key, following the schema in `labs/README.md`. Provide a `checks` array; each check has a stable `id`, a `description`, an `expected` value the grader can compare against (keep it short and unambiguous, for example `"yes"`, a role name, a policy effect, or a literal string the learner should see), and `points`. The `points` must sum to `total_points`. Set `"requires_license": true` on any check that the no-license path cannot complete.

Design each check so it maps to a validation gate in `lab.md`, and so a learner can fill in `labs/<slug>/submission.json` by recording one value per check `id`. A learner who follows the no-license path adds `"_path": "no-license"` to the submission, and the grader leaves the licensed checks out of the score. After writing both files, tell the learner where they were saved and that `/grade <slug>` will score a submission against the answer key. Do not reveal the answer key values inside `lab.md`; the key lives only in `answer-key.json`.
