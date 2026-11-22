# Restrict data plane access to KV1 by using the Key Vault firewall

| Field | Value |
| --- | --- |
| Objective | 1.2.4 Configure firewall settings on Key Vault |
| Domain | Manage identity, access, and governance (`identity`) |
| Subdomain | 1.2 Secure secrets and keys by using Azure Key Vault |
| Category | key-vault |
| Primary path | Azure CLI (Bash, on your local computer) |
| Estimated time | 20-25 minutes |
| Lab ID | `1-2-4-key-vault-firewall` |

## Scenario

Fourth Coffee keeps payment integration secrets in Azure Key Vault. An audit at Fourth Coffee found that the vault accepts data plane requests from any public IP address. You need to ensure that only the main office public IP address and trusted Microsoft services can reach the secrets in a vault named KV1. You also need to verify what happens when public network access is disabled.

## License and cost gate

> **Tier:** `PAYG`
>
> - **Requirements:** An Azure subscription (Sub1) in a dedicated lab tenant. No Microsoft Entra ID P1 or P2 license and no Defender plan is required. The Key Vault firewall is part of the vault at no extra charge.
> - **Cost driver:** Key Vault Standard bills per operation. This lab runs a handful of secret operations. Soft-deleted Standard vaults do not incur charges.
> - **Trial option:** None needed. An Azure free account works.
> - **Pricing:** Do not rely on a quoted price. Check the [Key Vault pricing page](https://azure.microsoft.com/pricing/details/key-vault/) or the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).
> - **Stop the cost:** Cleanup step C2 deletes RG1, and step C3 purges the soft-deleted KV1 so the vault name is released.
> - **Safety note:** This lab does **not** turn on purge protection, which cannot be turned off after it is turned on.

Sources: [Configure network security for Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/network-security) and [Key Vault soft-delete overview](https://learn.microsoft.com/azure/key-vault/general/soft-delete-overview).

## Prerequisites

- A **dedicated lab tenant and lab subscription** (Sub1). Never run this lab against production.
- The **Owner** role on Sub1. You create a role assignment, and purging a soft-deleted vault requires the subscription owner or the **Key Vault Purge Operator** role.
- Azure CLI **2.90.0 or later** in a Bash shell on your **local computer**. Do not use Azure Cloud Shell for this lab: its outbound IP address is not your own and can change between sessions, so the IP rule test gives misleading results.
- `curl`, to look up your public IPv4 address.
- Completing lab `1-2-3-key-vault-rbac-access` first is helpful but not required.

## Starting state

- No resource group named RG1 exists in Sub1.
- You know whether your network uses a stable public IPv4 address. A VPN or a carrier-grade NAT can change your egress address during the lab. If you use a VPN, disconnect it or keep it connected for the entire lab.

## Background: what the firewall does and does not cover

- A new key vault has the firewall **disabled**. Any network can reach it, but every request still needs Microsoft Entra authentication and an authorization grant.
- Firewall rules apply to **data plane** operations only (`<vault-name>.vault.azure.net`). Control plane operations through Azure Resource Manager (`management.azure.com`) are not filtered by the firewall.
- IP rules accept **public IPv4** addresses and CIDR ranges only. RFC 1918 private ranges (10.x, 172.16-31.x, and 192.168.x) are not allowed.
- **Allow trusted Microsoft services to bypass this firewall** lets services on the trusted services list through. Setting public network access to **Disabled** still honors that bypass.

Source: [Configure network security for Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/network-security).

---

## Task 1: Deploy KV1 and create Secret1

1. Sign in with Microsoft Entra ID, select Sub1, and set the lab variables.

   ```bash
   az login
   az account set --subscription "<Sub1-subscription-id>"

   RG=RG1
   LOCATION=eastus
   KV=kv1$RANDOM$RANDOM
   ME=$(az ad signed-in-user show --query id -o tsv)
   MYIP=$(curl -s https://api.ipify.org)
   echo "Vault name: $KV   Public IP: $MYIP"
   ```

   The `api.ipify.org` service is a third-party helper, not a Microsoft service. Confirm that `MYIP` shows a public IPv4 address, not a 10.x, 172.16-31.x, or 192.168.x address. Write down the vault name.

2. Create RG1 and KV1 by using the Azure RBAC permission model.

   ```bash
   az group create --name $RG --location $LOCATION
   az keyvault create --name $KV --resource-group $RG --location $LOCATION \
     --sku standard --enable-rbac-authorization true
   KV_ID=$(az keyvault show --name $KV --query id -o tsv)
   ```

3. Assign yourself **Key Vault Secrets Officer** at the KV1 scope, wait one to five minutes for propagation, and then create Secret1. The value is generated at run time and is never written to a file.

   ```bash
   az role assignment create --role "Key Vault Secrets Officer" \
     --assignee-object-id "$ME" --assignee-principal-type User --scope "$KV_ID"

   az keyvault secret set --vault-name $KV --name Secret1 \
     --value "$(openssl rand -base64 24)" --query "attributes.enabled" -o tsv
   ```

   The second command returns `true`. If it returns `Forbidden`, wait and retry. That error is role propagation, not the firewall, because the firewall is still disabled.

Source: [Key Vault scope role assignment](https://learn.microsoft.com/azure/key-vault/general/rbac-guide#key-vault-scope-role-assignment).

---

## Task 2: Turn on the firewall with a deny default

4. Set the default action to **Deny** and allow trusted Microsoft services to bypass the firewall. This matches the portal option **Allow public access from specific virtual networks and IP addresses** with the **Allow trusted Microsoft services to bypass this firewall** exception selected.

   ```bash
   az keyvault update --resource-group $RG --name $KV \
     --default-action Deny --bypass AzureServices
   ```

### Validation gate 1

```bash
az keyvault show --name $KV \
  --query "{defaultAction:properties.networkAcls.defaultAction, bypass:properties.networkAcls.bypass}" -o table
```

- Record the **DefaultAction** value as **`default_action`**.
- Record the **Bypass** value as **`bypass`**.

---

## Task 3: Prove the data plane is blocked and the control plane is not

5. Try to read Secret1 from your computer. Firewall changes can take a minute to apply, so retry if the read still succeeds.

   ```bash
   az keyvault secret show --vault-name $KV --name Secret1 --query "id" -o tsv
   ```

   The command fails with a `Forbidden` error. Look for the error code in the response (it is also listed in the inner error).

6. Read the vault properties through Azure Resource Manager.

   ```bash
   az keyvault show --name $KV --query "name" -o tsv
   ```

### Validation gate 2

- Record the Key Vault error code from step 5 as **`firewall_error_code`**. It is a single word, not `Forbidden`.
- If step 6 printed the vault name, record **`control_plane_still_works`** as `yes`. Otherwise record `no`.

Why this matters: the firewall protects secret, key, and certificate operations. It does not stop someone with a control plane role from changing the vault configuration. That is why Azure RBAC (lab 1.2.3) and the firewall work together.

Source: [Common error codes for Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/common-error-codes).

---

## Task 4: Allow the main office IP address

7. Add your public IP address as the Fourth Coffee main office address, then list the IP rules.

   ```bash
   az keyvault network-rule add --resource-group $RG --name $KV --ip-address "$MYIP"
   az keyvault network-rule list --resource-group $RG --name $KV --query "ipRules[].value" -o tsv
   ```

8. Wait about one minute, and then read Secret1 again.

   ```bash
   az keyvault secret show --vault-name $KV --name Secret1 --query "attributes.enabled" -o tsv
   ```

9. Try to add a private address range. A developer at Fourth Coffee suggested this to "allow the office LAN."

   ```bash
   az keyvault network-rule add --resource-group $RG --name $KV --ip-address "10.0.0.0/24"
   az keyvault network-rule list --resource-group $RG --name $KV --query "length(ipRules)" -o tsv
   ```

### Validation gate 3

- Record the number of IP rules that the **second** command in step 9 returns as **`ip_rule_count`**.
- If step 8 printed `true`, record **`secret_read_after_ip_rule`** as `yes`. Otherwise record `no`.
- If the first command in step 9 returned an error and the 10.0.0.0/24 range does not appear in the rule list, record **`private_range_rejected`** as `yes`. Otherwise record `no`.

Why this matters: Key Vault sees the public address that your traffic leaves from, never your LAN address. To allow traffic from inside Azure without public IP addresses, use a virtual network service endpoint rule or a private endpoint.

---

## Task 5: Disable public network access

10. Disable public network access, wait about one minute, and try to read Secret1 again from the allowed IP address.

    ```bash
    az keyvault update --resource-group $RG --name $KV --public-network-access Disabled
    az keyvault show --name $KV --query "properties.publicNetworkAccess" -o tsv

    az keyvault secret show --vault-name $KV --name Secret1 --query "id" -o tsv
    ```

    The read fails even though your IP rule still exists. With public access disabled, only private endpoints (and trusted services through the bypass) reach the vault.

### Validation gate 4

Record the output of the **az keyvault show** command in step 10 as **`public_network_access`**.

Source: [Public access disabled (private endpoint only)](https://learn.microsoft.com/azure/key-vault/general/network-security#public-access-disabled-private-endpoint-only).

---

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Step 5 still returns the secret | Firewall changes take a short time to apply. Wait one to two minutes and retry. Also confirm that `defaultAction` is `Deny`. |
| Step 8 still fails after you add the IP rule | Your egress IP address changed, or you are on a VPN or proxy. Run **curl -s https://api.ipify.org** again and compare it with the rule. If you used Cloud Shell, switch to a local terminal. |
| Step 3 returns `Forbidden` | Role propagation takes one to five minutes. The firewall is not on yet at this point, so the cause is the role assignment. |
| You cannot see secrets in the Azure portal after Task 2 | Expected. The portal calls the data plane from your browser, so the firewall applies to it too. |
| `VaultAlreadyExists` on **az keyvault create** | Generate a new `KV` value, or run **az keyvault list-deleted --resource-type vault** to find and purge your own leftover vault. |

---

## Cleanup (mandatory)

Run every step, in order. No resource locks or purge protection were set. Firewall settings do not block cleanup, because deletion and purge are control plane operations.

- **C1.** Remove the lab role assignment.

  ```bash
  az role assignment delete --role "Key Vault Secrets Officer" --assignee "$ME" --scope "$KV_ID"
  ```

- **C2.** Delete RG1. KV1 moves into the soft-deleted state.

  ```bash
  az group delete --name $RG --yes
  ```

- **C3.** Purge the soft-deleted vault so the name is released.

  ```bash
  az keyvault purge --name $KV --location $LOCATION
  ```

### Cleanup validation

```bash
az group exists --name $RG
az keyvault list-deleted --resource-type vault --query "length([?name=='$KV'])" -o tsv
```

- If the first command returns `false`, record **`rg1_deleted`** as `yes`.
- Record the number returned by the second command as **`kv1_soft_deleted_count`**.

Source: [Key Vault recovery management with soft delete and purge protection](https://learn.microsoft.com/azure/key-vault/general/key-vault-recovery).

---

## Record your results

Create `labs/1-2-4-key-vault-firewall/submission.json` with one value per check:

```json
{
  "default_action": "",
  "bypass": "",
  "firewall_error_code": "",
  "control_plane_still_works": "",
  "ip_rule_count": "",
  "secret_read_after_ip_rule": "",
  "private_range_rejected": "",
  "public_network_access": "",
  "rg1_deleted": "",
  "kv1_soft_deleted_count": ""
}
```

Then run **/grade 1-2-4-key-vault-firewall**.

## Exam takeaways

- A new vault has the firewall disabled. Turning it on means setting the default action to **Deny** and then adding allow rules.
- The firewall filters the **data plane** only. ARM operations, including ARM template deployment of secrets, are not filtered.
- IP rules accept public IPv4 addresses only, up to 1,000 rules. Virtual network rules (service endpoints) cover up to 200 subnets.
- **Allow trusted Microsoft services** applies only to services on the trusted services list. Azure DevOps is not on the list.
- **Disable public access** leaves private endpoints and the trusted services bypass. A network security perimeter in **Secure by perimeter** mode overrides even the bypass.
- The portal is also a data plane client. If your browser is outside the allowed ranges, you can see the vault but not list its secrets.

## References

- [Configure network security for Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/network-security)
- [Virtual network service endpoints for Azure Key Vault (trusted services)](https://learn.microsoft.com/azure/key-vault/general/overview-vnet-service-endpoints)
- [Access Azure Key Vault behind a firewall](https://learn.microsoft.com/azure/key-vault/general/access-behind-firewall)
- [Integrate Key Vault with Azure Private Link](https://learn.microsoft.com/azure/key-vault/general/private-link-service)
- [Common error codes for Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/common-error-codes)
- [Key Vault recovery management with soft delete and purge protection](https://learn.microsoft.com/azure/key-vault/general/key-vault-recovery)
