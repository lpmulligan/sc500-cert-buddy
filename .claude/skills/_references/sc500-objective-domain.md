# SC-500 Objective Domain

Verbatim local mirror of the Microsoft Learn study guide for **Exam SC-500: Implementing End-to-End Security Controls for Cloud and AI Workloads**, the exam for the **Microsoft Certified: Cloud and AI Security Engineer Associate** certification. This file is the canonical exam-objective reference for this repo. When any content conflicts with this file, this file wins -- or re-sync it from Microsoft Learn and update affected content in the same change.

## Currency

| Field | Value |
| --- | --- |
| Source URL | [https://learn.microsoft.com/credentials/certifications/resources/study-guides/sc-500](https://learn.microsoft.com/credentials/certifications/resources/study-guides/sc-500) |
| Certification page | [https://learn.microsoft.com/credentials/certifications/cloud-and-ai-security-engineer-associate/](https://learn.microsoft.com/credentials/certifications/cloud-and-ai-security-engineer-associate/) |
| Microsoft "skills measured as of" date | **Not published on the study guide page** as of the last sync. Confirm on the exam page before quoting a date. |
| Local mirror revision date (last MCP sync) | **2026-10-20** |
| Synced by | Lawrence Mulligan via Microsoft Learn MCP server (`microsoft_docs_fetch`) |

If Microsoft updates the upstream study guide, re-fetch the page and update the **skills measured as of** date and the **local mirror revision date** above in the same PR. Note any wording deltas in the [Change log](#change-log) at the bottom.

As of the last sync, the certification page states that the SC-500 practice assessment is not yet available. Practice assessments usually appear within eight weeks of an exam leaving beta.

## Purpose of the exam

The exam validates that the candidate can design, implement, and manage end-to-end security controls across Azure, hybrid, and AI-enabled environments to protect identities, data, applications, and infrastructure, and to maintain regulatory compliance.

A score of **700 or greater** is required to pass. Most questions cover features that are general availability (GA). The exam may contain questions on Preview features if those features are commonly used.

## Audience profile

As a candidate for this Microsoft Certification, you are a security engineer who protects organizational systems and data across cloud and hybrid environments by implementing comprehensive security controls that proactively help prevent unauthorized access and mitigate risks. Your role spans multiple security domains, including identity, network, application, data, and compute. You also help ensure that platforms, data, identities, and infrastructure used by AI workloads are securely implemented and monitored.

In this role, your responsibilities include:

- Securing access to resources by using Microsoft Entra ID and Azure Key Vault.
- Enforcing security and regulatory compliance.
- Securing storage, databases, and networking.
- Securing compute.
- Securing AI solutions.
- Managing and monitoring security posture.

You work closely with architects, administrators, engineers, analysts, and developers responsible for Azure, Microsoft 365, identity and access, information protection, security operations, DevOps, application development, database platforms, and networks.

For this exam, you should have practical experience in administration of Azure and hybrid environments, including compute, network, and storage. You need strong familiarity with Microsoft Entra ID and familiarity with Microsoft 365 administration.

## Skills at a glance

| # | Functional group | Domain key | Weight |
| --- | --- | --- | --- |
| 1 | Manage identity, access, and governance | `identity` | **20 -- 25%** |
| 2 | Secure storage, databases, and networking | `storage-network` | **25 -- 30%** |
| 3 | Secure compute | `compute` | **20 -- 25%** |
| 4 | Manage and monitor security posture | `posture` | **20 -- 25%** |

The domain keys are local to this repo. The slash commands, the skills, and the cert-buddy MCP server use them.

## Domain 1 -- Manage identity, access, and governance (20 -- 25%)

### 1.1 Secure access to resources by using Microsoft Entra ID

- 1.1.1 Implement and configure Privileged Identity Management (PIM)
- 1.1.2 Implement conditional access policies
- 1.1.3 Implement and configure authentication methods, including multifactor authentication (MFA) and passwordless
- 1.1.4 Implement and configure identity for applications, including enterprise applications and app registrations
- 1.1.5 Manage OAuth permission grants and consent settings
- 1.1.6 Implement and configure managed identities for Azure resources

### 1.2 Secure secrets and keys by using Azure Key Vault

- 1.2.1 Deploy Key Vault
- 1.2.2 Configure Key Vault settings
- 1.2.3 Configure access to Key Vault
- 1.2.4 Configure firewall settings on Key Vault
- 1.2.5 Manage keys, secrets, and certificates
- 1.2.6 Scan for secrets by using Defender Cloud Security Posture Management (Defender CSPM)
- 1.2.7 Implement Defender for Key Vault

### 1.3 Implement governance to enforce security and regulatory compliance

- 1.3.1 Implement and configure security controls by using Azure Policy, including built-in and custom policy definitions
- 1.3.2 Evaluate regulatory compliance by using Microsoft Defender for Cloud
- 1.3.3 Implement and configure security controls in Defender for Cloud, including security standards and recommendations
- 1.3.4 Implement resource locks
- 1.3.5 Manage Azure built-in role assignments
- 1.3.6 Manage custom roles, including Azure roles and Microsoft Entra roles
- 1.3.7 Evaluate and remediate overprivileged access assignments by using Azure role-based access control (RBAC)
- 1.3.8 Configure security controls for backup protection by using Azure Backup security features
- 1.3.9 Implement and configure security controls by using infrastructure as code

## Domain 2 -- Secure storage, databases, and networking (25 -- 30%)

### 2.1 Implement security for storage accounts

- 2.1.1 Implement and configure security for storage accounts
- 2.1.2 Configure Azure Storage firewall rules
- 2.1.3 Implement Defender for Storage threat protection configurations
- 2.1.4 Manage access to storage, including access policies

### 2.2 Implement security for databases

- 2.2.1 Implement platform-level security configurations in Azure SQL
- 2.2.2 Configure database auditing for Azure SQL Database and Azure SQL Managed Instance
- 2.2.3 Configure Defender for Databases protection across Azure database services

### 2.3 Implement security for Azure network services

- 2.3.1 Implement and manage network security groups (NSGs) and application security groups (ASGs)
- 2.3.2 Implement and configure network access policies by using Azure Virtual Network Manager
- 2.3.3 Configure security for an Azure Virtual WAN
- 2.3.4 Implement and configure security for virtual private network (VPN) connections
- 2.3.5 Implement and configure Microsoft Entra Private Access
- 2.3.6 Configure Azure private endpoints to secure access to Azure platform as a service (PaaS) resources
- 2.3.7 Configure Azure Private Link services to secure access to network resources
- 2.3.8 Implement and configure Azure Firewall
- 2.3.9 Evaluate effective security rules by using Azure Network Watcher diagnostics

## Domain 3 -- Secure compute (20 -- 25%)

### 3.1 Implement security for AI

- 3.1.1 Identify overexposure of data in SharePoint
- 3.1.2 Identify risks related to Microsoft Copilot and AI apps by using Microsoft Purview Data Security Posture Management (DSPM)
- 3.1.3 Enable and configure real-time protection for Microsoft Copilot Studio agents
- 3.1.4 Implement conditional access for Microsoft Entra Agent ID
- 3.1.5 Analyze blast radius for security risks related to Entra Agent ID by using Defender XDR
- 3.1.6 Manage Entra Agent ID access
- 3.1.7 Configure and deploy AI Gateway in Azure API Management for Microsoft Foundry
- 3.1.8 Enable Defender for AI Service in Cloud Workload Protection in Defender for Cloud
- 3.1.9 Configure guardrails for agent security in Foundry
- 3.1.10 Monitor AI security by using the Data and AI security dashboard in Defender for Cloud
- 3.1.11 Manage agents in Microsoft 365 admin center

### 3.2 Implement security for servers and virtual machines (VMs)

- 3.2.1 Implement and configure disk encryption
- 3.2.2 Plan and implement Azure Bastion
- 3.2.3 Enable and enforce use of just-in-time (JIT) VM access
- 3.2.4 Extend security controls to hybrid and multicloud servers by using Azure Arc
- 3.2.5 Onboard servers to Defender for Servers in Defender for Cloud, including hybrid and multicloud scenarios
- 3.2.6 Configure Defender for Servers settings, including vulnerability scanning, and endpoint detection and response (EDR)
- 3.2.7 Implement and manage agentless scanning for VMs in Defender for Servers
- 3.2.8 Configure security features on a VM, including secure boot, virtual Trusted Platform Module (vTPM), integrity monitoring, and security type
- 3.2.9 Enforce security configuration of Azure-managed servers by using Azure Machine Configuration

### 3.3 Implement security for application platform services

- 3.3.1 Detect misconfigurations and runtime risks in container workloads by using Defender for Containers
- 3.3.2 Implement and configure security controls for Azure Kubernetes Service (AKS)
- 3.3.3 Implement and configure security controls for Azure Container Registry
- 3.3.4 Implement and configure security controls for Azure Container Instances and Azure Container Apps
- 3.3.5 Implement and configure security controls for Azure Functions, including authentication and network access
- 3.3.6 Implement and configure security controls for Azure Logic Apps
- 3.3.7 Implement and configure security controls for Azure App Service
- 3.3.8 Implement and configure Azure Web Application Firewall
- 3.3.9 Implement security policies for back-end API protection by using API Management

## Domain 4 -- Manage and monitor security posture (20 -- 25%)

### 4.1 Manage security posture by using Defender for Cloud

- 4.1.1 Identify security risks by using Defender CSPM
- 4.1.2 Evaluate compliance against security frameworks by using Defender for Cloud
- 4.1.3 Enable and configure Defender for Cloud workload protection plans
- 4.1.4 Connect hybrid cloud and multicloud environments to Defender for Cloud, including Amazon Web Services (AWS) and Google Cloud Platform (GCP)
- 4.1.5 Configure Microsoft Defender Vulnerability Management settings for Azure VMs
- 4.1.6 Discover unprotected assets and vulnerabilities by using Microsoft Defender External Attack Surface Management (EASM)

### 4.2 Implement activity and event collection in Microsoft Sentinel

- 4.2.1 Create and connect workspaces in Microsoft Sentinel
- 4.2.2 Assign roles in Microsoft Sentinel
- 4.2.3 Implement and use content hub solutions
- 4.2.4 Configure and use Microsoft data connectors for Azure resources
- 4.2.5 Implement and configure syslog and Common Event Format (CEF) event collections
- 4.2.6 Implement and configure collection of Windows Security events by using data collection rules, including Windows Event Forwarding (WEF)
- 4.2.7 Create custom log tables in the workspace to store ingested data
- 4.2.8 Implement automation rules and playbooks in Microsoft Sentinel
- 4.2.9 Implement data retention in Microsoft Sentinel data stores
- 4.2.10 Query Microsoft Purview Audit in Defender XDR

### 4.3 Implement Microsoft Security Copilot

- 4.3.1 Configure workspaces for Security Copilot
- 4.3.2 Manage permissions and roles in Security Copilot
- 4.3.3 Enable and configure plugins
- 4.3.4 Enable and configure Microsoft agents and Security Store agents

## Coverage summary

| Domain | Sub-areas | Skills |
| --- | --- | --- |
| 1 -- Manage identity, access, and governance | 3 | 22 |
| 2 -- Secure storage, databases, and networking | 3 | 16 |
| 3 -- Secure compute | 3 | 29 |
| 4 -- Manage and monitor security posture | 3 | 20 |
| **Total** | **12** | **87** |

Lab license and cost requirements for every objective live in [`sc500-lab-requirements.md`](sc500-lab-requirements.md).

## Source-of-truth precedence

When facts conflict across files in this repo:

1. The current Microsoft Learn study guide for SC-500 (re-fetch via MCP if uncertain).
2. This file (`.claude/skills/_references/sc500-objective-domain.md`) -- treated as the verbatim local mirror of the above.
3. Skill and command files.

If a skill drifts from this file, fix the skill, not this file.

## Change log

| Local mirror date | Microsoft "skills measured as of" date | Notes |
| --- | --- | --- |
| 2026-10-20 | Not published | Initial SC-500 mirror, replacing the AI-901 mirror inherited from the upstream project. Four domains (20 -- 25% / 25 -- 30% / 20 -- 25% / 20 -- 25%), 12 sub-areas, 87 skills. The local 1.1.1 numbering is added for reference; Microsoft does not number the bullets. |
