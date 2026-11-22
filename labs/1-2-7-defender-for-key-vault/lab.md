# Turn on Defender for Key Vault for Sub1 and validate alerting

| Field | Value |
| --- | --- |
| Objective | 1.2.7 Implement Defender for Key Vault |
| Domain | Manage identity, access, and governance (`identity`) |
| Subdomain | 1.2 Secure secrets and keys by using Azure Key Vault |
| Category | key-vault |
| Primary path | Azure CLI for the plan, Azure portal for sample alerts |
| Estimated time | 15-20 minutes, plus up to 10 minutes for sample alerts to appear |
| Lab ID | `1-2-7-defender-for-key-vault` |

## Scenario

Alpine Ski House stores booking platform secrets in Azure Key Vault. The security team at Alpine Ski House wants to be told when someone accesses a vault from a TOR exit node or a suspicious IP address, or pulls an unusual number of secrets. You need to turn on Microsoft Defender for Key Vault for a subscription named Sub1. You also need to verify that alerts reach the Defender for Cloud security alerts page.

## License and cost gate

> **Tier:** `TRIAL`
>
> - **Requirements:** An Azure subscription (Sub1) in a dedicated lab tenant, with the **Defender for Key Vault** plan in Microsoft Defender for Cloud. No Microsoft Entra ID P1 or P2 license is required.
> - **Roles:** **Security Admin** or **Owner** on Sub1 to turn the plan on and off. **Contributor** (or higher) on Sub1 to create sample alerts.
> - **Cost driver:** The plan is enabled at subscription scope and covers every key vault in Sub1. After the trial, it bills as shown on the Defender for Cloud pricing page.
> - **Trial option:** Azure gives a 30-day free trial the first time each Defender plan is activated on a subscription. A subscription that already used its Key Vault plan trial bills immediately.
> - **Pricing:** Do not rely on a quoted price. Check the [Defender for Cloud pricing page](https://azure.microsoft.com/pricing/details/defender-for-cloud/) or the [Defender for Cloud cost calculator](https://learn.microsoft.com/azure/defender-for-cloud/cost-calculator).
> - **Stop the cost:** Cleanup step C2 sets the `KeyVaults` plan back to the **Free** tier with **az security pricing create --name KeyVaults --tier free**.
>
> No resources are deployed in this lab. Sample alerts use simulated resources, so you do not need a key vault.

Sources: [Protect your key vaults with Defender for Key Vault](https://learn.microsoft.com/azure/defender-for-cloud/tutorial-enable-key-vault-plan), [Check the status of your free trial](https://learn.microsoft.com/azure/defender-for-cloud/free-trial), and [Validate alerts in Microsoft Defender for Cloud](https://learn.microsoft.com/azure/defender-for-cloud/alert-validation).

## Prerequisites

- A **dedicated lab tenant and lab subscription** (Sub1). Never run this lab against production. Turning a Defender plan on or off changes protection for every key vault in the subscription.
- **Security Admin** on Sub1 is the least-privileged role for the plan change. You also need **Contributor** on Sub1 for Task 3. **Owner** covers both.
- Defender for Cloud enabled on Sub1 (the free Foundational CSPM tier is enough).
- Azure CLI 2.90.0 or later. Azure Cloud Shell works for this lab.

## Starting state

Record the current state of the plan **before** you change anything, so cleanup can restore it.

```bash
az login
az account set --subscription "<Sub1-subscription-id>"
az security pricing show --name KeyVaults --query "{tier:pricingTier, subPlan:subPlan}" -o table
```

- In a dedicated lab subscription, the tier is `Free`. Write down the tier and subplan in your own notes.
- If the tier is already `Standard`, someone else turned the plan on. Do not turn it off in cleanup. Restore it to `Standard` instead.

---

## Task 1: Find the plan name and turn the plan on

1. List the Defender plan names on Sub1 and find the one for Key Vault.

   ```bash
   az security pricing list --query "value[].name" -o tsv
   ```

   If that query returns nothing on your CLI version, use **az security pricing list --query "[].name" -o tsv**.

2. Turn on the plan at subscription scope by setting its tier to **Standard**. This command is the CLI equivalent of **Microsoft Defender for Cloud** > **Environment settings** > Sub1 > **Defender plans** > **Key Vault** > **On** > **Save**.

   ```bash
   az security pricing create --name KeyVaults --tier standard
   ```

3. Confirm the tier and check the trial.

   ```bash
   az security pricing show --name KeyVaults \
     --query "{tier:pricingTier, subPlan:subPlan, trialRemaining:freeTrialRemainingTime}" -o table
   ```

   A `trialRemaining` value such as `30.00:00:00` means the 30-day trial is active. A value of `0:00:00` means the trial was already used and the plan bills now. If that is not acceptable, go straight to cleanup step C2.

### Validation gate 1

- Record the plan name from step 1 as **`plan_name_cli`**.
- Record the **tier** from step 3 as **`plan_tier_enabled`**.

---

## Task 2: Know the alerts before you see them

Defender for Key Vault raises alerts for unusual and potentially harmful access to vaults. Open the [Alerts for Azure Key Vault](https://learn.microsoft.com/azure/defender-for-cloud/alerts-azure-key-vault) reference and find the alert named **Access from a TOR exit node to a key vault**.

4. Read the alert type ID (shown in parentheses under the alert name) and the severity.

### Validation gate 2

- Record the alert type ID as **`tor_alert_type`**.
- Record the severity as **`tor_alert_severity`**.

Why this matters: exam scenarios name an alert type and ask which plan raises it or how to respond. The `KV_` prefix ties an alert to Defender for Key Vault.

---

## Task 3: Generate sample alerts

Sample alerts validate that the plan and your alert pipeline (email notifications, workflow automation, and SIEM connectors) work, without a real attack.

5. In the Azure portal, go to **Microsoft Defender for Cloud** > **Security alerts**.
6. On the toolbar, select **Sample alerts**.
7. Select Sub1, select only the **Key Vault** plan, and then select **Create sample alerts**.
8. Wait up to 10 minutes and refresh **Security alerts**. Filter the list by entering `key vault` in the search box.

### Validation gate 3

- If at least one Key Vault sample alert appears in **Security alerts**, record **`sample_alerts_created`** as `yes`. Otherwise record `no`.

Note: sample alerts reference simulated resources. They do not appear on a real vault **Security** page. Real Defender for Key Vault alerts appear on the vault **Security** page, in workload protections, and on the Defender for Cloud **Security alerts** page.

Source: [Create sample alerts](https://learn.microsoft.com/azure/defender-for-cloud/alert-validation#create-sample-alerts).

---

## Task 4: Walk the response playbook

Open a Key Vault sample alert and select **View full details**. Then open [Respond to Microsoft Defender for Key Vault alerts](https://learn.microsoft.com/azure/defender-for-cloud/defender-for-key-vault-usage#respond-to-microsoft-defender-for-key-vault-alerts) and compare it with what the alert offers.

9. In **Step 2: Respond accordingly**, find what Microsoft Learn tells you to enable first when the traffic came from an unrecognized IP address. Choose the matching control from this list: **Key Vault firewall**, **purge protection**, or **Azure RBAC**.
10. In **Step 4: Take action**, find the single verb that describes what you do with every secret, key, and certificate that the suspicious caller accessed.

### Validation gate 4

- Record the control from step 9, exactly as written in the list, as **`unknown_ip_first_control`**.
- Record the verb from step 10, in lowercase, as **`accessed_secrets_action`**.

Why this matters: Defender for Key Vault detects. It does not block. The fix is a control you already practiced: the firewall in lab 1.2.4 and Azure RBAC in lab 1.2.3. Microsoft Learn also warns not to dismiss an alert just because you recognize the user or application, because the plan is designed to catch stolen credentials.

---

## No-license path

Use this path if you cannot start the trial, or if the trial on Sub1 was already used. Add `"_path": "no-license"` to your submission. The grader leaves out the checks marked `requires_license`.

- Run step 1 (listing plan names is read-only) and record **`plan_name_cli`**.
- Run the starting-state command to see the plan tier without changing it. Do not run step 2.
- Complete Task 2 and Task 4 by using the Microsoft Learn pages. For Task 4, read the response steps instead of opening a sample alert.
- In the portal, go to **Microsoft Defender for Cloud** > **Environment settings** > Sub1 > **Defender plans** and find the **Key Vault** row. Read the pricing and resource count without changing the toggle.
- Skip cleanup step C2 if you did not change the plan, and record **`plan_tier_after_cleanup`** from the starting-state command.

---

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| **az security pricing create** returns `AuthorizationFailed` | You need **Security Admin** or **Owner** on Sub1. Contributor alone cannot change plans in every tenant configuration. |
| **Environment settings** sends you to the Microsoft Defender portal | Your tenant moved cloud security plan management to the Defender portal. Use **Cloud security** > **Define Cloud Security plans** there, or use the CLI commands in this lab. |
| **Sample alerts** is missing from the toolbar | Confirm that you have **Contributor** on Sub1 and that you selected **Security alerts**, not **Recommendations**. |
| No sample alerts appear after 10 minutes | Confirm that the Key Vault plan tier is `Standard`, then create the sample alerts again. |
| `trialRemaining` shows zero | Sub1 already used its Key Vault plan trial. Turn the plan off now (C2) or switch to the no-license path. |

---

## Cleanup (mandatory)

- **C1.** Dismiss the sample alerts so they do not clutter the alert queue. In **Security alerts**, select the Key Vault sample alerts, select **Change status**, and then select **Dismissed**.
- **C2.** Turn off the plan. If your recorded starting tier was `Standard`, skip this step.

  ```bash
  az security pricing create --name KeyVaults --tier free
  ```

### Cleanup validation

```bash
az security pricing show --name KeyVaults --query "pricingTier" -o tsv
```

Record the output as **`plan_tier_after_cleanup`**. It must match the starting tier you recorded.

Source: [Manage and respond to security alerts](https://learn.microsoft.com/azure/defender-for-cloud/manage-respond-alerts).

---

## Record your results

Create `labs/1-2-7-defender-for-key-vault/submission.json` with one value per check:

```json
{
  "plan_name_cli": "",
  "plan_tier_enabled": "",
  "tor_alert_type": "",
  "tor_alert_severity": "",
  "sample_alerts_created": "",
  "unknown_ip_first_control": "",
  "accessed_secrets_action": "",
  "plan_tier_after_cleanup": ""
}
```

If you followed the no-license path, add `"_path": "no-license"` and leave out `plan_tier_enabled` and `sample_alerts_created`. Then run **/grade 1-2-7-defender-for-key-vault**.

## Exam takeaways

- Defender for Key Vault is a Defender for Cloud plan. You turn it on at **subscription** scope, and it covers every vault in that subscription.
- It **detects** suspicious access, such as TOR exit nodes, suspicious IP addresses, unusual users or applications, and secret list-then-get patterns. It does not block access.
- Respond with the vault controls: turn on the firewall for an unknown IP address, remove or restrict the principal for an unknown identity, and rotate every object that was accessed.
- Turning plans on and off needs **Security Admin** or **Owner**. Creating sample alerts needs **Contributor**.
- Each Defender plan gets its own 30-day trial per subscription.

## References

- [Overview of Microsoft Defender for Key Vault](https://learn.microsoft.com/azure/defender-for-cloud/defender-for-key-vault-introduction)
- [Protect your key vaults with Defender for Key Vault](https://learn.microsoft.com/azure/defender-for-cloud/tutorial-enable-key-vault-plan)
- [Alerts for Azure Key Vault](https://learn.microsoft.com/azure/defender-for-cloud/alerts-azure-key-vault)
- [Validate alerts in Microsoft Defender for Cloud](https://learn.microsoft.com/azure/defender-for-cloud/alert-validation)
- [Check the status of your free trial](https://learn.microsoft.com/azure/defender-for-cloud/free-trial)
- [Manage cloud security plans in the Defender portal](https://learn.microsoft.com/azure/defender-for-cloud/defender-portal/manage-plans-defender-portal)
- [az security pricing](https://learn.microsoft.com/cli/azure/security/pricing)
