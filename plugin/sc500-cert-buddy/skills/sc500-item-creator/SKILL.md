---
name: sc500-item-creator
description: Generate SC-500 practice questions that feel like the real Microsoft Cloud and AI Security Engineer Associate exam without copying it. Every item is grounded in current Microsoft Learn content, uses current Microsoft product names (Microsoft Entra ID, Azure Key Vault, Microsoft Defender for Cloud, Microsoft Sentinel, Microsoft Security Copilot, Microsoft Purview, Microsoft Foundry), and follows the Microsoft Worldwide Learning Exam Writing Style Guide (WWL). Use when the user asks for practice questions, quiz items, or exam prep.
---

# Skill: sc500.practice_questions.exam_realistic

**Description:** Generate SC-500 practice questions that feel like the real Microsoft Cloud and AI Security Engineer Associate exam without copying it. Every item is grounded in current Microsoft Learn content, uses current Microsoft product names, and follows Microsoft-style exam item rules: scenario-first stems, plausible distractors, parallel choices, no trick wording.

## Exam facts (canonical)

- **Exam:** SC-500 -- Implementing End-to-End Security Controls for Cloud and AI Workloads
- **Certification:** Microsoft Certified: Cloud and AI Security Engineer Associate
- **Skills measured date:** not published on the study guide page as of the last sync (see the objective domain file)
- **Pass score:** 700
- **Study guide URL:** https://learn.microsoft.com/credentials/certifications/resources/study-guides/sc-500
- **Audience profile:** security engineers who protect systems and data across cloud and hybrid environments, with practical Azure and hybrid administration experience (compute, network, and storage), strong familiarity with Microsoft Entra ID, and familiarity with Microsoft 365 administration.

## Style precedence

The **Microsoft Worldwide Learning Exam Writing Style Guide** (WWL) is authoritative for every item. The **Microsoft Writing Style Guide** (MWSG) governs prose voice and tone where WWL is silent. When the two guides conflict, **WWL wins**.

Two MWSG conventions overridden by WWL for exam items:

- **No contractions** anywhere in an item.
- **All uppercase** for key names: TAB, ENTER, CTRL+ALT+DELETE.

## Grounding

**Required sources:**

- Microsoft Learn (truth source for objectives and product behavior). Access via the **Microsoft Learn MCP server** `mslearn` using `microsoft_docs_search` and `microsoft_docs_fetch`.
- Microsoft Learn code samples (for Azure CLI, Azure PowerShell, Bicep, Kusto Query Language (KQL), and Azure Policy definition accuracy). Access via `microsoft_code_sample_search`.
- Canonical SC-500 objective domain file: `.claude/skills/_references/sc500-objective-domain.md` (verbatim mirror, dated 2026-10-20).

Grounding-first rule: query the Microsoft Learn MCP before any other source. Never substitute generic web search.

## SC-500 domains (canonical)

| Domain | Key | Weight |
| --- | --- | --- |
| Manage identity, access, and governance | `identity` | 20-25% |
| Secure storage, databases, and networking | `storage-network` | 25-30% |
| Secure compute | `compute` | 20-25% |
| Manage and monitor security posture | `posture` | 20-25% |

Pull specific objectives and sub-domains from `.claude/skills/_references/sc500-objective-domain.md`. If that file is unavailable, query the Microsoft Learn MCP server `mslearn` for the SC-500 study guide.

## Style and word usage (WWL, mandatory)

### Question sentence

- Begin with **What** (stand-alone interrogative pronoun) or **Which** (followed by a noun).
- The auxiliary in question sentences is **should**. Do not use *can, must, might, do, would,* or *may* in question sentences.
- Approved stems: *What should you do?* / *What should you recommend?* / *What should you configure?* / *Which service should you use?* / *Which two actions should you perform?* / *What are two possible ways to achieve this goal?*
- For Choose-N items, embed the count and use a plural noun: *Which two actions should you perform? Each correct answer presents part of the solution.*
- Avoid negatives. If a negative is unavoidable, **CAP** and **bold** it (for example, **NOT**).
- Goal statements use *You need to ...* or *You need to ensure that ...*
- Use *of the following* sparingly, only when answer choices are non-parallel.
- True/False stems are not allowed.

### Word usage

- **named**, not *called*, when introducing a name.
- **report**, not *complain*, when describing user feedback.
- Avoid **determine**. Use *verify, clarify, identify, set, discover, establish, calculate, decide*.
- Avoid **may**. Use *can* (valid action) or *might* (possibility).
- Avoid **would** in questions; use *should*. Avoid **would like**; use *want* or *need*.
- Avoid **using** alone; use *by using*. Avoid **with** in place of *by using*.
- Avoid specific determiners: *all, none, only, always, never*.
- Avoid indefinite qualifiers: *few, many, multiple, several, some, usually, a number of*.
- *site* is logical; *location* is physical -- never interchange.
- Use **plural**; do not use *(s)*.
- Present tense throughout.

### People (WWL legal rule)

- Never use a personal name in an item. Use **the user**.
- For multiple people, use **User1, User2, User3** (no spaces).
- For administrators, use **Admin1, Admin2** in the same pattern.

### Approved fictional companies (WWL Fictitious Names List)

Use only these companies. Always use the **entire** company name on every mention (write *Litware, Inc.*, not *Litware*; write *Contoso, Ltd.*, not *Contoso*). Randomize across the full list -- do not default to Contoso, Ltd.

| Company | Approved URL |
| --- | --- |
| A. Datum Corporation | adatum.com |
| Adventure Works Cycles | adventure-works.com |
| Alpine Ski House | alpineskihouse.com |
| Bellows College | bellowscollege.com |
| Best For You Organics Company | bestforyouorganics.com |
| Blue Yonder Airlines | blueyonderairlines.com |
| City Power & Light | cpandl.com |
| Coho Vineyard | cohovineyard.com |
| Coho Winery | cohowinery.com |
| Coho Vineyard & Winery | cohovineyardandwinery.com |
| Consolidated Messenger | consolidatedmessenger.com |
| Contoso, Ltd. | contoso.com |
| Contoso Pharmaceuticals | contoso.com |
| Contoso Suites | contososuites.com |
| Fabrikam, Inc. | fabrikam.com |
| Fabrikam Residences | fabrikamresidences.com |
| First Up Consultants | firstupconsultants.com |
| Fourth Coffee | fourthcoffee.com |
| Graphic Design Institute | graphicdesigninstitute.com |
| Humongous Insurance | humongousinsurance.com |
| Lamna Healthcare Company | lamnahealthcare.com |
| Liberty's Delightful Bakery & Cafe | libertysdelightfulbakeryandcafe.com |
| Litware, Inc. | litwareinc.com |
| Lucerne Publishing | lucernepublishing.com |
| Margie's Travel | margiestravel.com |
| Munson's Pickles and Preserves Farm | munsonspicklesandpreservesfarm.com |
| Nod Publishers | nodpublishers.com |
| Northwind Electric Cars | northwindelectriccars.com |
| Northwind Traders | northwindtraders.com |
| Proseware, Inc. | proseware.com |
| Relecloud | relecloud.com |
| School of Fine Art | fineartschool.net |
| Southridge Video | southridgevideo.com |
| Tailspin Toys | tailspintoys.com |
| The Phone Company | thephone-company.com |
| Trey Research | treyresearch.net |
| VanArsdel, Ltd. | vanarsdelltd.com |
| Wide World Importers | wideworldimporters.com |
| Wingtip Toys | wingtiptoys.com |
| Woodgrove Bank | woodgrovebank.com |

### Approved cities (WWL city list)

Use without state, province, or country: Atlanta, Boston, Chicago, Dallas, Denver, Detroit, Los Angeles, Mexico City, Montreal, New York, Ottawa, Quebec, San Diego, San Francisco, Seattle, Toronto, Vancouver; Amsterdam, Athens, Barcelona, Berlin, Brussels, Budapest, Copenhagen, Dublin, Frankfurt, Geneva, Glasgow, Hamburg, Helsinki, Lisbon, London, Madrid, Moscow, Oslo, Paris, Prague, Rome, Stockholm, Vienna, Warsaw; Beijing, Hong Kong, Kyoto, Osaka, Seoul, Shanghai, Taipei, Tokyo; Auckland, Bangkok, Calcutta, Jakarta, Manila, Melbourne, New Delhi, Perth, Singapore, Sydney; Ankara, Baghdad, Damascus, Riyadh, Tel Aviv; Cairo, Cape Town, Johannesburg, Lagos, Nairobi, Tangier; Bogota, Buenos Aires, Caracas, Lima, Rio de Janeiro, Santiago, Sao Paulo.

### Resource names (WWL conventions)

- **Servers:** Server1, Server2; Exch1, Exch2; SQL1, SQL2; DC1, DC2; DNS1, DNS2 (no space between the noun and the digit).
- **Virtual machines:** VM1, VM2. **Computers:** Computer1, Computer2.
- **Applications:** App1, App2. **Agents:** Agent1, Agent2.
- **Virtual networks:** VNet1, VNet2. **Subnets:** Subnet1, Subnet2. **Sites:** Site1, Site2.
- **Subscriptions:** Sub1, Sub2. **Resource groups:** RG1, RG2.
- **Key vaults:** KV1, KV2. **Storage accounts:** storage1, storage2 (storage account names are lowercase).
- **Workspaces:** Workspace1, Workspace2. **Policies:** Policy1, Policy2. **Groups:** Group1, Group2.
- **Offices:** *main office*, *branch office*, *satellite office* (lowercase).
- Define each name on first mention.

### Answer choices (WWL)

- Default 4 choices (A-D) for SC-500 single-correct items: 1 correct + 3 distractors.
- Choose-N items: *N* correct + at least 2 distractors.
- Choices are **mutually exclusive** -- no overlap between any two.
- Choices are **parallel** in form, length, detail, and grammatical structure.
- Choices match the syntax of the question sentence (imperative stem -> imperative choices).
- All choices are sentence fragments (lowercase initial, no end punctuation) **OR** all complete sentences (capitalized, period). Do not mix.
- No *all of the above*, *none of the above*, *both A and B*.
- Eliminate redundant lead-in wording from every choice; move it to the stem.
- Distractors must reference real Microsoft services, Microsoft Entra features, Defender for Cloud plans, Azure RBAC roles, Azure Policy effects, network controls, or Sentinel features. Never invent fake names, roles, plans, or capabilities.
- No explanations inside answer choices.
- Order choices logically (numerical order; shortest to longest; related pairs together). Disable randomization when answers are numerical.

### Formatting

- **Bold** for UI element names and PowerShell cmdlets.
- **All uppercase** for key names: TAB, ENTER, CTRL+ALT+DELETE.
- File names labelled with the word *file*: *the main.bicep file*, not *main.bicep* alone.
- Code, KQL queries, and policy JSON appear in fenced code blocks inside the stem when the item needs them.
- Sentence-style capitalization elsewhere, except product names and proper nouns.
- Oxford comma in every list of three or more.
- Plain ASCII only -- no curly quotes, en or em dashes. Use `--` and `->`.
- Spell out zero through nine; numerals for 10 and above.
- **should** = recommendation; **must** = requirement.
- Acronyms: spell out + acronym in parens on first mention (*just-in-time (JIT) VM access*); acronym only after.

### Globalization

- Sentences 15-20 words.
- Active voice (subject + verb + object).
- Simple verb tenses.
- No `/` or `-` as punctuation. Replace *create/edit/display* with *create, edit, and display*.
- No possessives on product names.
- No nominalizations, noun stacks, idioms, slang, or US-only references.

## Terminology rename table (non-negotiable)

Always use current Microsoft product names. Never use a retired or legacy name, even if the user does. Silently map to the current name. If Microsoft Learn shows a different current name, prefer the Learn name.

| Retired / legacy name | Current name |
| --- | --- |
| Azure Active Directory (Azure AD) | Microsoft Entra ID |
| Azure AD tenant | Microsoft Entra tenant |
| Azure AD Conditional Access | Microsoft Entra Conditional Access |
| Azure AD Privileged Identity Management | Microsoft Entra Privileged Identity Management |
| Azure AD Identity Protection | Microsoft Entra ID Protection |
| Azure AD B2B / Azure AD B2C | Microsoft Entra External ID |
| Azure AD Application Proxy | Microsoft Entra application proxy |
| Azure Security Center | Microsoft Defender for Cloud |
| Azure Defender | Microsoft Defender for Cloud workload protection plans |
| Azure Security Benchmark | Microsoft cloud security benchmark |
| Azure Sentinel | Microsoft Sentinel |
| Microsoft 365 Defender | Microsoft Defender XDR |
| Microsoft Defender ATP | Microsoft Defender for Endpoint |
| Azure Advanced Threat Protection (Azure ATP) | Microsoft Defender for Identity |
| Microsoft Cloud App Security (MCAS) | Microsoft Defender for Cloud Apps |
| Threat and Vulnerability Management | Microsoft Defender Vulnerability Management |
| Microsoft Copilot for Security | Microsoft Security Copilot |
| Azure Purview / Microsoft 365 compliance center | Microsoft Purview |
| Azure Policy Guest Configuration / Automanage Machine Configuration | Azure Machine Configuration |
| Log Analytics agent (MMA, OMS agent) | Azure Monitor Agent |
| Azure AI Studio / Azure AI Foundry | Microsoft Foundry |
| Azure OpenAI Service (standalone) | Azure OpenAI in Microsoft Foundry |
| Azure Cognitive Services | Azure AI services |

Retired services such as Azure Blueprints can appear only as a distractor, and only if Microsoft Learn still documents them as a valid but deprecated option. Never use a retired service as the correct answer.

## Authentication in code (non-negotiable)

- Code in an item uses Microsoft Entra ID authentication: **az login**, **Connect-AzAccount**, managed identities, or `DefaultAzureCredential`.
- Never show storage account keys, SQL passwords, or connection strings as the recommended pattern. The exception is an objective that is about those mechanisms itself (for example, shared access signatures and stored access policies in objective 2.1.4); then show them, and name the more secure alternative in the rationale.

## Guardrails

- **Exam integrity:** Do not recreate or paraphrase real exam questions. Do not reference braindumps. Write original scenarios and original stems every time.
- **Item quality:** Single skill measured per item. No trivia. No hidden requirements. One problem, one decision.
- **Audience fit:** Items target an associate-level security engineer who administers Azure and hybrid environments and knows Microsoft Entra ID well. Expect configuration decisions, least-privilege trade-offs, and troubleshooting, not definitions. Do not require Microsoft 365 depth beyond what the objective names.
- **Real features only:** Do not invent Microsoft products, services, roles, plans, or capabilities. Confine items to features described in the SC-500 study guide and validated through the Microsoft Learn MCP server `mslearn`.
- **Licensing accuracy:** When the correct answer depends on a license or plan (for example, Entra ID P2 for PIM, or Defender for Servers Plan 2 for JIT VM access), state the license in the scenario or make the license the decision. Check `.claude/skills/_references/sc500-lab-requirements.md` and re-ground in Learn.

## Answer choice randomization (non-negotiable)

You MUST randomize which letter (A, B, C, or D) is the correct answer for each question. Do not default to any single letter position.

### Batch balance rule

When delivering 4 or more items in a single response:

- **4 to 7 items:** every letter (A, B, C, D) must be the correct answer at least once.
- **8 to 11 items:** every letter must appear at least twice.
- **12 or more items:** target an even split of 25 percent per letter; allowed drift is +/- 1.

**Procedure before delivery:**

1. Count how many times each letter is the correct answer across the drafted batch.
2. If any letter is missing or under the floor, pick one item where the correct answer falls in an over-represented letter and **rewrite the item** so that the correct answer moves to the under-represented letter. Re-shuffle distractor wording so the rewrite is still mutually exclusive and the rationale still maps cleanly.
3. Re-count. Repeat until the batch is balanced.
4. In the batch summary, state the final A/B/C/D distribution (for example, *Answer position distribution: A=2, B=3, C=2, D=3*).

Position must carry no signal.

## Workflow

1. Pull the target objective from `.claude/skills/_references/sc500-objective-domain.md` (or query the Microsoft Learn MCP server `mslearn` for the SC-500 study guide if the file is unavailable).
2. Ground the intended correct behavior in Microsoft Learn using `microsoft_docs_search` first, then `microsoft_docs_fetch` for full-page detail.
3. If the item touches Azure CLI, Azure PowerShell, Bicep, KQL, Azure Policy JSON, or API Management policy syntax, run `microsoft_code_sample_search` to confirm syntax.
4. Pick a random WWL-approved fictional company. Draft a workplace scenario stem that forces a real SC-500 candidate decision (which control, which role, which plan, which policy effect, which network feature, which Sentinel collection method).
5. Randomly assign the correct answer to A, B, C, or D. Write 1 correct answer and 3 distractors based on common-but-wrong assumptions. After the batch is drafted, apply the **batch balance rule**.
6. Run a mutual exclusivity check on answer choices.
7. Run a **WWL style sweep**: stem starts with What/Which + should; no banned auxiliaries (can, must, might, do, would, may); no specific determiners; no indefinite qualifiers; no contractions; no parenthetical clauses; choices are parallel and consistent (all fragments or all complete sentences); resource names follow the VM1/VNet1/KV1/App1 pattern; companies use the full WWL name; people use *the user* or User1/User2.
8. Run a terminology check: every product name matches the rename table above.
9. Run a candidate clarity check: single skill measured, no trivia, no hidden requirements, associate-level depth, and any license dependency stated.
10. Prepare rationale internally but do not deliver it yet (see delivery rules).

## Invalid answer handling

When presenting questions interactively:

- **hint:** Provide a clue that eliminates one distractor. Re-present the question with all four choices visible but the eliminated option noted.
- **skip** or **I do not know:** Immediately reveal the correct answer and full rationale (Phase 2), then move on.
- **Unrecognized input:** Prompt: *Please reply with **A**, **B**, **C**, or **D**. You can also enter **hint** for a clue or **skip** to see the answer.*

## Progress tracking

When multiple questions are requested:

- Prefix each with **Question N of M**.
- After the final question, present a summary: total correct, total incorrect, total skipped, and any weak domains identified.

## Scenario-first stem guidance

The stem opens with a workplace scenario before asking the question. Keep stems tight; one problem, one decision.

**Good example:**

> Fabrikam, Inc. has an Azure subscription named Sub1 that contains 40 virtual machines. Administrators connect to the virtual machines by using RDP over the internet. You need to ensure that inbound RDP is closed by default and opens only for an approved administrator, for a limited time, from a specific source IP address.
>
> What should you configure?

**Bad example (no scenario, banned auxiliary):**

> Which feature can close RDP ports?

## Plausible distractor guidance

Distractors reference real Microsoft security services, features, roles, or plans that are genuinely related to the topic but incorrect for the specific scenario.

**Good distractors** (real but wrong):

- Configure an Azure Bastion host in VNet1.
- Assign Admin1 the Virtual Machine Contributor role by using Microsoft Entra Privileged Identity Management.
- Create an Azure Virtual Network Manager security admin rule that denies TCP port 3389.

**Bad distractors** (fake or implausible):

- Enable the **RDP Shield** feature in Defender for Cloud. (Fake feature.)
- Assign Admin1 the Port Opener role. (Fake role.)

## Delivery rules (non-negotiable)

**Phase 1 -- Question only:**

- Show metadata, scenario stem, and choices (A-D).
- Do **NOT** include correct answer, rationale, or references.
- End the message and wait for the user to reply.

**Phase 2 -- Evaluation:**

- After the user replies, show:
  - Whether they were correct or incorrect.
  - The correct answer letter.
  - Full rationale for every choice (exactly 2 sentences each).
  - References (Microsoft Learn URLs).

If multiple questions were requested, repeat the Phase 1 / Phase 2 cycle sequentially.

## Output format

**Phase 1 message (question only):**

- **metadata**
  - exam: SC-500
  - domain: "`<one of the four SC-500 domains>`"
  - objective: "`<specific objective line from .claude/skills/_references/sc500-objective-domain.md>`"
  - bloom: "`<Remember | Understand | Apply | Analyze | Evaluate>`"
  - difficulty: "`<easy | medium | hard>`"
- **question**
  - stem:
    - `<scenario + question. Tight. One problem. One decision.>`
  - choices:
    - A: "`<choice>`"
    - B: "`<choice>`"
    - C: "`<choice>`"
    - D: "`<choice>`"

*(Stop here. Wait for the user to answer.)*

**Phase 2 message (evaluation, after user replies):**

- **result:** *Correct! / Incorrect.* The correct answer is `<A | B | C | D>`.
- **rationale:**
  - A: "`<2 sentences. Sentence 1: correct or incorrect, and why. Sentence 2: candidate-level context -- when this would apply, the misconception it tests, or how it differs from the correct answer.>`"
  - B: "`<same 2-sentence format>`"
  - C: "`<same 2-sentence format>`"
  - D: "`<same 2-sentence format>`"
- **references:**
  - "`<Microsoft Learn URL 1>`"
  - "`<Microsoft Learn URL 2 if needed>`"
- **quality_checklist:**
  - Stem starts with What or Which and uses *should* as the auxiliary.
  - No banned auxiliaries in the question sentence (can, must, might, do, would, may).
  - No specific determiners (all, none, only, always, never) and no indefinite qualifiers (few, many, multiple, several, some, usually).
  - Scenario is realistic for an associate-level SC-500 security engineer.
  - Exactly one skill is being measured.
  - Correct answer is unambiguously correct given Learn docs, including any license or plan dependency.
  - Distractors are plausible, real, and unambiguously wrong.
  - No contractions; minimal negatives; no trick phrasing.
  - Choices are parallel in grammar, length, and scope, and either all fragments or all complete sentences.
  - At least one Microsoft Learn reference is included.
  - All product names use current terminology (rename table).
  - Each rationale entry is exactly 2 sentences.
  - Correct answer position is randomized (not always A).
  - Across a 4+ item batch, every letter A/B/C/D appears at least once; across an 8+ item batch, every letter appears at least twice.
  - Fictional company is from the WWL approved list and uses the full company name (not always Contoso, Ltd.).
  - Resource names follow VM1/VNet1/KV1/App1/Subnet1/Site1 patterns; people are *the user* or User1/User2.

---

## Prompt template

You are writing NEW SC-500 practice questions that feel exam-realistic without copying the exam.

**Inputs:**

- count: {{count}}
- domain: {{domain}} (or pick from `.claude/skills/_references/sc500-objective-domain.md`)
- bloom: {{bloom}}
- constraints: {{constraints}}

**Requirements:**

1. Ground every question in Microsoft Learn first using the Microsoft Learn MCP server `mslearn`.
2. Use `microsoft_code_sample_search` for Azure CLI, Azure PowerShell, Bicep, KQL, or policy syntax accuracy when applicable.
3. Follow guardrails and output format exactly.
4. Randomize the correct answer position across A, B, C, D and apply the batch balance rule.
5. Randomize the WWL-approved fictional company name (full list embedded above).

Deliver {{count}} items.
