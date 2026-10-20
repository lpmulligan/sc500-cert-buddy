# SC-500 lab requirements matrix

Every SC-500 objective gets a lab. Some labs run on any Azure subscription; others need a premium license, a paid plan, or a resource that bills by the hour. This matrix tells the lab creator (and the learner) which is which **before** the lab starts, so nobody discovers a license wall or a surprise bill halfway through.

Requirements were grounded in Microsoft Learn on **2026-10-20**. Licensing changes often. Re-verify through the `mslearn` MCP server before you publish a lab, and update this file in the same change.

## Requirement tiers

| Tier | Meaning |
| --- | --- |
| `FREE` | Any Azure subscription or Microsoft Entra tenant. No premium license. Little or no cost. |
| `PAYG` | Any Azure subscription, but the lab creates resources that bill while they exist (often by the hour). Cleanup stops the cost. |
| `TRIAL` | A paid Microsoft Defender for Cloud plan (or similar) that offers a free trial. Disable the plan before the trial ends to avoid charges. |
| `ENTRA-P1` | Microsoft Entra ID P1 (standalone, or in Microsoft 365 E3, E5, or Business Premium). |
| `ENTRA-P2` | Microsoft Entra ID P2 or Microsoft Entra ID Governance (standalone, or in Microsoft 365 E5). |
| `ENTRA-SSE` | Microsoft Entra Private Access or Microsoft Entra Suite, on top of Entra ID P1 or P2. |
| `M365` | A Microsoft 365 tenant with the listed Microsoft 365, Purview, or Copilot licensing. |
| `AGENT365` | Microsoft Agent 365 (included in Microsoft 365 E7, or an add-on paired with at least Entra ID P1 or Microsoft 365 E3). |
| `SCU` | Microsoft Security Copilot capacity: at least one provisioned Security Compute Unit (SCU), billed by the hour, unless the tenant is auto-provisioned through Microsoft 365 E5 or E7. |

A lab can carry more than one tier. The lab creator lists every tier in the lab's **License and cost gate** callout.

## Domain 1 -- Manage identity, access, and governance

| Objective | Tier | What you need | Cost and cleanup note |
| --- | --- | --- | --- |
| 1.1.1 PIM | `ENTRA-P2` | Entra ID P2 or Entra ID Governance for every user with an eligible or time-bound assignment, and for approvers | Trial licenses exist. When a trial expires, eligible assignments are removed. |
| 1.1.2 Conditional Access | `ENTRA-P1` | Entra ID P1 for users targeted by policies. Risk-based policies need `ENTRA-P2`. | **Lockout risk.** Exclude a break-glass account and start in **Report-only** mode. |
| 1.1.3 Authentication methods, MFA, passwordless | `FREE` | Passkeys (FIDO2) are available in all Entra ID editions, including Free | Enforcing a method through a Conditional Access authentication strength needs `ENTRA-P1`. |
| 1.1.4 Enterprise apps and app registrations | `FREE` | Application Administrator or Cloud Application Administrator role | Delete the test app registration. |
| 1.1.5 OAuth permission grants and consent | `FREE` | Privileged Role Administrator, or Cloud Application Administrator for app consent | Restore the original consent settings. |
| 1.1.6 Managed identities | `FREE` | Azure subscription | The resource that hosts the identity might bill. |
| 1.2.1 -- 1.2.5 Key Vault deploy, settings, access, firewall, keys, secrets, certificates | `PAYG` | Azure subscription, Key Vault Administrator or Owner on the resource group | Per-operation charges. Purge protection keeps a deleted vault name reserved for the retention period. |
| 1.2.6 Secret scanning with Defender CSPM | `TRIAL` | Defender CSPM plan, enabled by the subscription **Owner** so agentless scanning turns on | 30-day trial per plan. Disable the plan after the lab. |
| 1.2.7 Defender for Key Vault | `TRIAL` | Defender for Key Vault plan | 30-day trial. Disable the plan after the lab. |
| 1.3.1 Azure Policy | `FREE` | Resource Policy Contributor or Owner | Remove assignments and custom definitions. |
| 1.3.2 Regulatory compliance in Defender for Cloud | `FREE` / `TRIAL` | Microsoft cloud security benchmark is free with Foundational CSPM. Other standards need Defender CSPM. | Remove added standards. |
| 1.3.3 Security standards and recommendations | `FREE` | Foundational CSPM (free) | None. |
| 1.3.4 Resource locks | `FREE` | Owner or User Access Administrator | Remove the lock before cleanup, or cleanup fails. |
| 1.3.5 Built-in role assignments | `FREE` | Owner or User Access Administrator | Remove test assignments. |
| 1.3.6 Custom roles (Azure and Entra) | `FREE` / `ENTRA-P1` | Azure custom roles are free. Entra custom roles need Entra ID P1 (verify in Learn before publishing). | Delete custom role definitions. |
| 1.3.7 Overprivileged RBAC assignments | `FREE` | Reader plus role assignment read access | Optional CIEM insights need Defender CSPM. |
| 1.3.8 Azure Backup security features | `PAYG` | Recovery Services vault and a small protected VM or file share | Soft delete and immutability can block deletion for days. Plan the cleanup order. |
| 1.3.9 Security controls with infrastructure as code | `FREE` | Bicep or Azure CLI | Deployed resources might bill. |

## Domain 2 -- Secure storage, databases, and networking

| Objective | Tier | What you need | Cost and cleanup note |
| --- | --- | --- | --- |
| 2.1.1, 2.1.2, 2.1.4 Storage account security, firewall, access policies | `PAYG` | Azure subscription | Low cost. Delete the storage account. |
| 2.1.3 Defender for Storage | `TRIAL` | Defender for Storage plan | 30-day trial. Malware scanning bills per GB scanned after the trial. |
| 2.2.1, 2.2.2 Azure SQL platform security and auditing | `PAYG` | Azure SQL Database (a serverless or Basic tier keeps cost low). SQL Managed Instance is expensive; use a walkthrough for the Managed Instance portion. | Audit logs land in storage or Log Analytics, which bills. |
| 2.2.3 Defender for Databases | `TRIAL` | Defender for Databases plan | 30-day trial. Disable the plan after the lab. |
| 2.3.1 NSGs and ASGs | `FREE` | Virtual network | A test VM bills while it runs. |
| 2.3.2 Azure Virtual Network Manager | `PAYG` | Azure Virtual Network Manager instance | Charged per virtual network with an active deployed configuration. |
| 2.3.3 Virtual WAN security | `PAYG` | Virtual WAN hub, optionally a secured hub with Azure Firewall | Hubs and firewalls bill by the hour. Delete immediately after the lab. |
| 2.3.4 VPN connections | `PAYG` | VPN gateway | Gateways bill by the hour and take time to deploy and delete. |
| 2.3.5 Microsoft Entra Private Access | `ENTRA-SSE` | Entra ID P1 or P2 **plus** Entra Private Access or Entra Suite, a Windows server for the private network connector, and a Windows 10 or 11 client with the Global Secure Access client | Trial licenses exist. Turn off the Private Access traffic forwarding profile after the lab. |
| 2.3.6 Private endpoints for PaaS | `PAYG` | Private endpoint plus a PaaS resource such as a storage account | Private endpoints bill by the hour plus data processed. |
| 2.3.7 Private Link service | `PAYG` | Standard Load Balancer and a back-end VM | Load balancer and VM bill while they exist. |
| 2.3.8 Azure Firewall | `PAYG` | Azure Firewall (Basic or Standard) | One of the most expensive lab resources per hour. Delete immediately after the lab. |
| 2.3.9 Network Watcher diagnostics | `FREE` | Network Watcher (enabled per region) and a test VM | The VM bills while it runs. Flow logs and traffic analytics bill for storage and ingestion. |

## Domain 3 -- Secure compute

### 3.1 Security for AI

| Objective | Tier | What you need | Cost and cleanup note |
| --- | --- | --- | --- |
| 3.1.1 SharePoint data overexposure | `M365` | Office 365 or Microsoft 365 E3 or E5 base license **plus** SharePoint Advanced Management (included with Microsoft 365 Copilot, or as an add-on) for data access governance reports | None. |
| 3.1.2 Purview DSPM for Copilot and AI apps | `M365` | A Purview-supporting license, Purview Audit on, Microsoft 365 Copilot licenses for Copilot interaction insights. Other AI apps need Purview pay-as-you-go billing. | Remove one-click policies created during the lab. |
| 3.1.3 Real-time protection for Copilot Studio agents | `AGENT365` / `M365` | Copilot Studio license and environment, Security Administrator, Power Platform administrator help. Since **July 1, 2026**, agent security capabilities for Copilot Studio require an Agent 365 license; the Defender for Cloud Apps real-time protection path stays available for tenants that already use it. | Remove custom blocking rules. |
| 3.1.4 Conditional Access for Entra Agent ID | `AGENT365` + `ENTRA-P1` | Microsoft 365 E7, or Agent 365 plus Entra ID P1 or Microsoft 365 E3. Agent risk-based policies need `ENTRA-P2`. Conditional Access Administrator. At least one agent identity. | Start in **Report-only** mode. Delete the policy after the lab. |
| 3.1.5 Blast radius analysis for Agent ID in Defender XDR | `AGENT365` | Agent 365 (Defender agent security is powered by Agent 365 observability logs), Defender portal access | None. |
| 3.1.6 Manage Entra Agent ID access | `FREE` / `AGENT365` | Agent ID itself is available to all Entra customers. Governance features such as access packages need Agent 365 plus at least Entra ID P1. Agent ID Administrator role. | Remove test access packages and assignments. |
| 3.1.7 AI Gateway in API Management for Foundry | `PAYG` | Microsoft Foundry resource with a model deployment, and an API Management v2 tier instance (creating one from the Foundry portal provisions Basic v2) | API Management bills while it exists; model calls bill per token. |
| 3.1.8 Defender for AI Services | `TRIAL` | Defender for AI Services plan, Owner or Contributor | 30-day trial capped at 75 billion tokens scanned. Disable the plan after the lab. |
| 3.1.9 Foundry guardrails for agent security | `PAYG` | Microsoft Foundry project and a model deployment | Model calls bill per token. Delete the deployment. |
| 3.1.10 Data and AI security dashboard | `TRIAL` | Defender CSPM with sensitive data discovery, Defender for Storage, Defender for Databases, and AI threat protection. Security explorer role. | Several 30-day trials at once. Disable every plan after the lab. |
| 3.1.11 Manage agents in Microsoft 365 admin center | `FREE` / `M365` / `AGENT365` | Viewing the agent inventory needs only the AI Reader role. Governance actions need Microsoft 365, Copilot, or Agent 365 licensing and the AI Administrator role. Risk signals need E7 or Agent 365. | Revert any agent availability changes. |

### 3.2 Servers and virtual machines

| Objective | Tier | What you need | Cost and cleanup note |
| --- | --- | --- | --- |
| 3.2.1 Disk encryption | `PAYG` | Small VM and a Key Vault for customer-managed keys | VM bills while it runs. |
| 3.2.2 Azure Bastion | `PAYG` | Bastion host and a VM | Bastion bills by the hour. Delete immediately after the lab. |
| 3.2.3 JIT VM access | `TRIAL` | **Defender for Servers Plan 2** on the subscription | 30-day trial. Plan 2 cannot be enabled per resource. |
| 3.2.4 Azure Arc for hybrid servers | `FREE` / `PAYG` | A non-Azure machine to onboard (a local VM works). Arc control plane is free. | Services enabled on the Arc server bill separately. |
| 3.2.5, 3.2.6 Onboard to Defender for Servers and configure scanning and EDR | `TRIAL` | Defender for Servers Plan 1 or Plan 2 | 30-day trial. Disable the plan after the lab. |
| 3.2.7 Agentless scanning | `TRIAL` | Defender for Servers Plan 2 or Defender CSPM, enabled by the subscription Owner | 30-day trial. |
| 3.2.8 Trusted launch features (secure boot, vTPM, integrity monitoring, security type) | `PAYG` | A Gen2 VM size that supports Trusted launch | VM bills while it runs. |
| 3.2.9 Azure Machine Configuration | `FREE` / `PAYG` | No extra charge for Azure VMs. Arc servers are charged unless covered by Software Assurance, Windows Server pay-as-you-go, or Defender for Servers Plan 2. | Remove policy assignments. |

### 3.3 Application platform services

| Objective | Tier | What you need | Cost and cleanup note |
| --- | --- | --- | --- |
| 3.3.1 Defender for Containers | `TRIAL` | Defender for Containers plan and an AKS cluster | 30-day trial plus cluster cost. |
| 3.3.2 AKS security controls | `PAYG` | Small AKS cluster | Nodes bill while they run. |
| 3.3.3 Container Registry security | `PAYG` | Container Registry. Network rules and private endpoints need the Premium tier (verify before publishing). | Delete the registry. |
| 3.3.4 Container Instances and Container Apps | `PAYG` | Consumption-based | Low cost. |
| 3.3.5 Azure Functions authentication and network access | `PAYG` | Function app. Some network features need a plan beyond Consumption. | Low cost. |
| 3.3.6 Logic Apps security | `PAYG` | Logic app (Consumption or Standard) | Low cost. |
| 3.3.7 App Service security | `PAYG` | App Service plan. Some networking features need Basic or higher. | Delete the plan, not only the app. |
| 3.3.8 Web Application Firewall | `PAYG` | Application Gateway WAF_v2 or Azure Front Door Premium | Bills by the hour. Delete immediately after the lab. |
| 3.3.9 API Management back-end protection | `PAYG` | API Management (Consumption or a v2 tier) | Developer and Premium tiers take a long time to provision. |

## Domain 4 -- Manage and monitor security posture

| Objective | Tier | What you need | Cost and cleanup note |
| --- | --- | --- | --- |
| 4.1.1 Security risks with Defender CSPM | `TRIAL` | Defender CSPM, enabled by the subscription Owner (attack path analysis, security explorer) | 30-day trial. |
| 4.1.2 Compliance against frameworks | `FREE` / `TRIAL` | Microsoft cloud security benchmark is free. Other frameworks need Defender CSPM. | Remove added standards. |
| 4.1.3 Workload protection plans | `TRIAL` | Security Admin or Owner | Each plan gets its own 30-day trial. Disable plans after the lab. |
| 4.1.4 Connect AWS and GCP | `FREE` / `TRIAL` | An AWS account or GCP project you control. Foundational CSPM is free; paid plans on the connector start one trial per account or project. | Delete the connector and the cloud-side resources the onboarding template created. |
| 4.1.5 Defender Vulnerability Management for Azure VMs | `TRIAL` | Defender for Servers (premium Defender Vulnerability Management capabilities come with Plan 2) | 30-day trial. |
| 4.1.6 Defender EASM | `TRIAL` | Defender EASM resource (Contributor). Defender CSPM also includes an EASM integration. | Each new EASM resource gets a 30-day trial, then bills per approved asset. Delete the resource. |
| 4.2.1 -- 4.2.3 Sentinel workspaces, roles, content hub | `TRIAL` | Log Analytics workspace with Microsoft Sentinel | First 10 GB per day free for 31 days. Removing Sentinel does not delete the workspace; delete the workspace too. |
| 4.2.4 Microsoft data connectors for Azure resources | `TRIAL` | Sentinel workspace | Azure Activity and Defender for Cloud alerts are free data sources. |
| 4.2.5 Syslog and CEF collection | `TRIAL` + `PAYG` | Linux VM as a log forwarder with the Azure Monitor Agent | VM bills while it runs; ingestion bills after the trial. |
| 4.2.6 Windows Security events with data collection rules and WEF | `TRIAL` + `PAYG` | Windows VM with the Azure Monitor Agent | VM bills while it runs. |
| 4.2.7 Custom log tables | `TRIAL` | Sentinel workspace | Ingestion bills after the trial. |
| 4.2.8 Automation rules and playbooks | `TRIAL` + `PAYG` | Sentinel workspace and a Logic Apps playbook | Logic Apps bills per run. |
| 4.2.9 Data retention | `TRIAL` | Sentinel workspace | 90 days of analytics retention free; longer retention bills. |
| 4.2.10 Purview Audit in Defender XDR | `M365` | Microsoft 365 tenant with Purview Audit (Standard), and Compliance Administrator or Exchange Organization Management | None. |
| 4.3.1 -- 4.3.4 Security Copilot workspaces, roles, plugins, agents | `SCU` | At least one provisioned SCU in an Azure subscription, or Security Copilot auto-provisioned through Microsoft 365 E5 or E7 | Provisioned SCUs bill in hourly blocks with a one-hour minimum, and turning off an agent does not stop SCU billing. Deprovision SCUs at the end of the lab. |

## How labs handle a gate the learner cannot meet

The lab creator still writes the lab. It adds two things:

1. A **License and cost gate** callout at the top that lists the tiers, the trial option if one exists, and the cleanup step that stops the cost.
2. A **No-license path**: a read-only walkthrough of the same portal screens, CLI help output, or Learn documentation, so the learner can still study the objective. Checks in the answer key that need the license are marked `"requires_license": true` so a learner on the no-license path can skip them.

## Sources (Microsoft Learn, verified 2026-10-20)

- PIM licensing: https://learn.microsoft.com/entra/id-governance/privileged-identity-management/pim-getting-started
- Conditional Access licensing: https://learn.microsoft.com/entra/identity/conditional-access/overview
- Passkeys in all Entra editions: https://learn.microsoft.com/entra/identity/authentication/how-to-authentication-passkeys-fido2
- Global Secure Access licensing: https://learn.microsoft.com/entra/global-secure-access/overview-what-is-global-secure-access
- Entra licensing, Agent ID, and Conditional Access for agents: https://learn.microsoft.com/entra/fundamentals/licensing
- Conditional Access for agents: https://learn.microsoft.com/entra/identity/conditional-access/agent-id
- Agent security transition to Agent 365: https://learn.microsoft.com/defender-xdr/security-for-ai/transition-agent-security-to-agent-365
- Agent registry and Microsoft 365 admin center licensing: https://learn.microsoft.com/entra/agent-id/agent-registry-convergence
- SharePoint Advanced Management prerequisites: https://learn.microsoft.com/sharepoint/sharepoint-advanced-management-prerequisites
- Purview DSPM prerequisites: https://learn.microsoft.com/purview/data-security-posture-management-considerations
- Defender for Cloud free trial: https://learn.microsoft.com/azure/defender-for-cloud/free-trial
- Defender CSPM plans: https://learn.microsoft.com/azure/defender-for-cloud/concept-cloud-security-posture-management
- Defender for AI Services trial: https://learn.microsoft.com/azure/defender-for-cloud/ai-threat-protection
- Data and AI security dashboard prerequisites: https://learn.microsoft.com/azure/defender-for-cloud/data-aware-security-dashboard-overview
- JIT requires Defender for Servers Plan 2: https://learn.microsoft.com/azure/defender-for-cloud/enable-just-in-time-access
- Defender for Servers plans: https://learn.microsoft.com/azure/defender-for-cloud/defender-for-servers-overview
- Defender EASM billing: https://learn.microsoft.com/azure/external-attack-surface-management/understanding-billable-assets
- Sentinel free trial and billing: https://learn.microsoft.com/azure/sentinel/billing
- Security Copilot SCU billing: https://learn.microsoft.com/copilot/security/security-compute-units-capacity
- AI Gateway in Foundry: https://learn.microsoft.com/azure/foundry/configuration/enable-ai-api-management-gateway-portal
- Azure Virtual Network Manager pricing: https://learn.microsoft.com/azure/virtual-network-manager/faq
- Azure Arc and Machine Configuration pricing: https://learn.microsoft.com/azure/azure-arc/servers/windows-server-management-overview
- Purview Audit search in the Defender portal: https://learn.microsoft.com/defender-office-365/audit-log-search-defender-portal
