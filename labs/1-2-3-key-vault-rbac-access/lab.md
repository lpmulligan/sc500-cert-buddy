---
created: 2026-10-25T10:23
updated: 2026-10-25T13:01
---
# Grant least-privileged access to secrets in KV1 by using Azure RBAC

| Field | Value |
| --- | --- |
| Objective | 1.2.3 Configure access to Key Vault |
| Domain | Manage identity, access, and governance (`identity`) |
| Subdomain | 1.2 Secure secrets and keys by using Azure Key Vault |
| Category | key-vault |
| Primary path | Azure CLI (Bash) |
| Estimated time | 20-25 minutes |
| Lab ID | `1-2-3-key-vault-rbac-access` |

## Scenario

Lucerne Publishing stores application secrets in Azure Key Vault. The security team at Lucerne Publishing wants to stop granting broad roles such as Owner and Contributor to people who only need to read secrets. You need to ensure that a principal can read secret values in a vault named KV1 without being able to create or change secrets.

## License and cost gate

> **Tier:** `PAYG`
>
> - **Requirements:** An Azure subscription (Sub1) in a dedicated lab tenant. No Microsoft Entra ID P1 or P2 license and no Defender plan is required.
> - **Cost driver:** Key Vault Standard bills per operation. This lab runs a handful of secret operations. Soft-deleted Standard vaults do not incur charges.
> - **Trial option:** None needed. An Azure free account works.
> - **Pricing:** Do not rely on a quoted price. Check the [Key Vault pricing page](https://azure.microsoft.com/pricing/details/key-vault/) or the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).
> - **Stop the cost:** Cleanup step C3 deletes RG1, and step C4 purges the soft-deleted KV1 so the vault name is released.
> - **Safety note:** This lab does **not** turn on purge protection. Purge protection cannot be turned off after it is turned on, and it would keep the vault name reserved for the full retention period.

Licensing source: [Azure RBAC for Key Vault data plane operations](https://learn.microsoft.com/azure/key-vault/general/rbac-guide) and [Key Vault soft-delete overview](https://learn.microsoft.com/azure/key-vault/general/soft-delete-overview).

## Prerequisites

- A **dedicated lab tenant and lab subscription** (Sub1). Never run this lab against production.
- The **Owner** role on Sub1. Owner is required here for two reasons: you create role assignments, and purging a soft-deleted vault requires the subscription owner or the **Key Vault Purge Operator** role.
- Azure CLI **2.90.0 or later**, which supports Key Vault API version 2026-02-01 and creates new vaults with Azure RBAC by default. Check with **az version**.
- A Bash shell (Azure Cloud Shell works).

## Starting state

- No resource group named RG1 exists in Sub1.
- You have no Key Vault data plane role (for example, **Key Vault Administrator** or **Key Vault Secrets Officer**) inherited at the subscription or management group scope. If you do, the deny tests in Task 2 and Task 4 succeed when they should fail. Check with the command in step 1.

## Background: two planes, two kinds of roles

Key Vault has a **control plane** (management.azure.com: create, delete, and configure vaults) and a **data plane** (`<vault-name>.vault.azure.net`: keys, secrets, and certificates). When a vault uses the Azure RBAC permission model, control plane roles such as **Owner**, **Contributor**, and **Key Vault Contributor** do not grant access to secret values. You assign a Key Vault data plane role, such as **Key Vault Secrets User** or **Key Vault Secrets Officer**, for that. Source: [Key Vault access model overview](https://learn.microsoft.com/azure/key-vault/general/rbac-guide#key-vault-access-model-overview).

---

## Task 1: Deploy KV1 with the Azure RBAC permission model

1. Sign in with Microsoft Entra ID, select Sub1, and set the lab variables. The vault name gets a random suffix because Key Vault names are globally unique.

   ```bash
   az login
   az account set --subscription "<Sub1-subscription-id>"

   RG=RG1
   LOCATION=centralus
   KV=kv1$RANDOM$RANDOM
   SUB_ID=$(az account show --query id -o tsv)
   ME=$(az ad signed-in-user show --query id -o tsv)
   echo "Vault name: $KV"

   # Starting-state check: list your Key Vault roles inherited at Sub1 scope (expect none)
   az role assignment list --assignee "$ME" --scope "/subscriptions/$SUB_ID" \
     --query "[?contains(roleDefinitionName, 'Key Vault')].roleDefinitionName" -o tsv
   ```

   Write down the vault name. You need it if your shell session ends.

2. Create RG1 and KV1. The **--enable-rbac-authorization true** argument is explicit so the lab behaves the same on older CLI versions.

   ```bash
   az group create --name $RG --location $LOCATION
   az keyvault create --name $KV --resource-group $RG --location $LOCATION \
     --sku standard --enable-rbac-authorization true
   KV_ID=$(az keyvault show --name $KV --query id -o tsv)
   ```

### Validation gate 1

```bash
az keyvault show --name $KV --query "properties.enableRbacAuthorization" -o tsv
```

Record the output as **`rbac_enabled`** in your submission.

Source: [Plan for Azure RBAC as the default access control model in Key Vault](https://learn.microsoft.com/azure/key-vault/general/access-control-default).

---

## Task 2: Prove that a control plane role does not open the data plane

3. As Owner of Sub1, try to list the secrets in KV1.

   ```bash
   az keyvault secret list --vault-name $KV
   ```

   The command fails with a `(Forbidden) Caller is not authorized to perform action on resource` error. Find the line that starts with `Action:` in the error.

4. Inspect the data actions of the **Key Vault Contributor** built-in role, which many teams assign to vault operators.

   ```bash
   az role definition list --name "Key Vault Contributor" \
     --query "length([0].permissions[0].dataActions)" -o tsv
   ```

### Validation gate 2

- Record the full action string from the `Action:` line in step 3 as **`owner_denied_action`**.
- Record the number returned by step 4 as **`kv_contributor_data_actions`**.

Why this matters: a principal with **Contributor** on a vault that still uses access policies can grant itself data plane access by editing an access policy. Azure RBAC closes that gap, because changing role assignments requires `Microsoft.Authorization/roleAssignments/write`. Source: [Managing administrative access to Key Vault](https://learn.microsoft.com/azure/key-vault/general/rbac-guide#managing-administrative-access-to-key-vault).

---

## Task 3: Grant write access and create Secret1

5. Assign yourself **Key Vault Secrets Officer** at the KV1 scope (not at RG1 or Sub1). This is the vault scope that Microsoft Learn recommends for role assignments.

   ```bash
   az role assignment create --role "Key Vault Secrets Officer" \
     --assignee-object-id "$ME" --assignee-principal-type User --scope "$KV_ID"
   ```

   Wait one to five minutes for the assignment to propagate. A `Forbidden` error right after assignment usually means propagation is not complete.

6. Create a secret named Secret1. The value is generated at run time and is never written to a file.

   ```bash
   az keyvault secret set --vault-name $KV --name Secret1 \
     --value "$(openssl rand -base64 24)" --query "attributes.enabled" -o tsv
   ```

### Validation gate 3

Record the output of step 6 as **`secret1_enabled`**.

Source: [Key Vault scope role assignment](https://learn.microsoft.com/azure/key-vault/general/rbac-guide#key-vault-scope-role-assignment).

---

## Task 4: Swap to the least-privileged read role and test it

7. Remove **Key Vault Secrets Officer** and assign **Key Vault Secrets User** at the KV1 scope. Key Vault Secrets User can read secret contents but cannot create, change, or delete secrets.

   ```bash
   az role assignment delete --role "Key Vault Secrets Officer" \
     --assignee "$ME" --scope "$KV_ID"
   az role assignment create --role "Key Vault Secrets User" \
     --assignee-object-id "$ME" --assignee-principal-type User --scope "$KV_ID"
   ```

   Wait one to five minutes for propagation. If you get unexpected results, run **az account get-access-token --resource https://vault.azure.net** to confirm that you are signed in, then retry.

8. Read Secret1. Print only the length of the value so the secret does not appear on the screen.

   ```bash
   az keyvault secret show --vault-name $KV --name Secret1 --query "value" -o tsv | wc -c
   ```

9. Try to change Secret1.

   ```bash
   az keyvault secret set --vault-name $KV --name Secret1 --value "$(openssl rand -base64 24)"
   ```

   The command fails with a `Forbidden` error. Find the `Action:` line in the error.

### Validation gate 4

- If step 8 returned a number greater than zero, record **`secrets_user_can_read`** as `yes`. Otherwise record `no`.
- Record the full action string from the `Action:` line in step 9 as **`secrets_user_denied_action`**.

Source: [Azure built-in roles for Key Vault data plane operations](https://learn.microsoft.com/azure/key-vault/general/rbac-guide#azure-built-in-roles-for-key-vault-data-plane-operations).

---

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `VaultAlreadyExists` on **az keyvault create** | The name is taken or a soft-deleted vault holds it. Generate a new `KV` value, or run **az keyvault list-deleted --resource-type vault** to find and purge your own leftover vault. |
| The step 3 or step 9 command succeeds instead of failing | You inherit a Key Vault data plane role from Sub1 or a management group. Rerun the starting-state check in step 1, and remove the inherited assignment only if this is your lab subscription. |
| `Forbidden` right after a role assignment | Role assignments take one to five minutes to propagate. Wait and retry. |
| `enableRbacAuthorization` is empty or `false` | You are on an older CLI version or omitted the argument. Run **az keyvault update --name $KV --enable-rbac-authorization true** (requires Owner or User Access Administrator plus Key Vault Contributor). |
| **az ad signed-in-user show** fails | You signed in as a service principal or managed identity. Sign in as a user for this lab. |

Source: [Common error codes for Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/common-error-codes).

---

## Cleanup (mandatory)

Run every step, in order. No resource locks or purge protection were set, so the vault can be purged immediately.

- **C1.** Remove the lab role assignment.

  ```bash
  az role assignment delete --role "Key Vault Secrets User" --assignee "$ME" --scope "$KV_ID"
  ```

- **C2.** Confirm that no Key Vault role assignment remains for you at the KV1 scope (expect empty output).

  ```bash
  az role assignment list --assignee "$ME" --scope "$KV_ID" --query "[].roleDefinitionName" -o tsv
  ```

- **C3.** Delete RG1. This deletes KV1, which moves into the soft-deleted state.

  ```bash
  az group delete --name $RG --yes
  ```

- **C4.** Purge the soft-deleted vault so the name is released.

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

Create `labs/1-2-3-key-vault-rbac-access/submission.json` with one value per check:

```json
{
  "rbac_enabled": "",
  "owner_denied_action": "",
  "kv_contributor_data_actions": "",
  "secret1_enabled": "",
  "secrets_user_can_read": "",
  "secrets_user_denied_action": "",
  "rg1_deleted": "",
  "kv1_soft_deleted_count": ""
}
```

Then run **/grade 1-2-3-key-vault-rbac-access**.

## Exam takeaways

- **Owner** and **Contributor** are control plane roles. On an Azure RBAC vault, they do not read or write secrets.
- **Key Vault Contributor** manages vaults only. It has no data actions.
- **Key Vault Secrets User** reads secret values. **Key Vault Secrets Officer** manages secrets. **Key Vault Administrator** covers keys, secrets, and certificates, but cannot manage role assignments.
- Assign roles at the vault scope. Use per-secret scope only for narrow cases, such as a shared secret between applications.
- **Key Vault Data Access Administrator** can delegate Key Vault data roles without holding full **User Access Administrator** rights.

## References

- [Provide access to Key Vault keys, certificates, and secrets with Azure RBAC](https://learn.microsoft.com/azure/key-vault/general/rbac-guide)
- [Plan for Azure RBAC as the default access control model in Key Vault](https://learn.microsoft.com/azure/key-vault/general/access-control-default)
- [Add role assignment conditions for Key Vault secrets by using Azure CLI (preview)](https://learn.microsoft.com/azure/key-vault/general/howto-abac-conditions-cli)
- [Azure Key Vault soft-delete overview](https://learn.microsoft.com/azure/key-vault/general/soft-delete-overview)
- [Key Vault recovery management with soft delete and purge protection](https://learn.microsoft.com/azure/key-vault/general/key-vault-recovery)
- [Common error codes for Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/common-error-codes)
