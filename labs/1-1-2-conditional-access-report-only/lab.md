# Require a phishing-resistant authentication strength outside trusted locations by using a report-only Conditional Access policy

| Field | Value |
| --- | --- |
| Objective | 1.1.2 Implement conditional access policies |
| Domain | Manage identity, access, and governance (`identity`) |
| Subdomain | 1.1 Manage identity and access by using Microsoft Entra ID |
| Category | identity |
| Primary path | Microsoft Entra admin center, with Microsoft Graph PowerShell for read-only validation |
| Estimated time | 25-30 minutes, plus up to 15 minutes of sign-in log latency |
| Lab ID | `1-1-2-conditional-access-report-only` |

## Scenario

Humongous Insurance wants users to sign in with a phishing-resistant method, such as a passkey or Windows Hello for Business, whenever they are away from the main office. Before anyone is affected, the identity team at Humongous Insurance needs evidence of what the policy would do. You need to create a trusted named location, a custom authentication strength, and a Conditional Access policy in **Report-only** mode. Then you need to verify the impact by using the What If tool and the sign-in logs.

## License and cost gate

> **Tier:** `ENTRA-P1`
>
> - **Requirements:** Microsoft Entra ID P1 (standalone, or included in Microsoft 365 E3, E5, or Business Premium) for the users the policy targets. Risk-based conditions need Microsoft Entra ID P2, but this lab does not use them.
> - **Cost driver:** Per-user license. There are no Azure resources and no Azure subscription charges.
> - **Trial option:** A Microsoft Entra ID P1 or P2 free trial can be activated in the lab tenant. See [Microsoft Entra ID Premium trial](https://learn.microsoft.com/entra/fundamentals/get-started-premium).
> - **Stop the cost:** Delete CAPolicy1, AuthStrength1, and MainOffice1 in cleanup. Let the trial expire, or cancel it in the Microsoft 365 admin center. When Conditional Access licenses expire, policies are not deleted automatically. You can still view and delete them, but you cannot update them.
> - **Lockout risk:** Conditional Access can lock people out. This lab targets only Group1, excludes the break-glass account, and starts in **Report-only** mode.

Sources: [Conditional Access license requirements](https://learn.microsoft.com/entra/identity/conditional-access/overview#license-requirements) and [Microsoft Entra licensing](https://learn.microsoft.com/entra/fundamentals/licensing).

## Prerequisites

- A **dedicated lab tenant**. Never run this lab in a production tenant.
- Microsoft Entra ID P1 or a P1 or P2 trial active in the tenant.
- Admin1, your admin account, with these roles:
  - **Conditional Access Administrator**, to create the named location and the policy and to run the What If tool.
  - **Security Administrator**, the documented minimum role to create a custom authentication strength.
  - **Security Reader** (or higher) to read the sign-in logs. Security Administrator already covers this.
- **User1**, a non-admin test user who is a member of a security group named **Group1**. User1 has no passkey or Windows Hello for Business registered.
- **BreakGlass1**, an emergency access account. Every policy in this lab excludes it.
- Microsoft Graph PowerShell (`Microsoft.Graph.Identity.SignIns` module). Every Graph command in this lab is read-only and uses only the `Policy.Read.All` scope.
- A second browser profile or an InPrivate window for User1 sign-ins.

## Background: three building blocks

| Building block | What it does | Where it lives |
| --- | --- | --- |
| Named location | Defines public IPv4 or IPv6 ranges (or countries). IP-based locations can be marked as trusted. | **Entra ID** > **Conditional Access** > **Named locations** |
| Authentication strength | Defines which authentication method combinations satisfy a grant. There are three built-in strengths, and you can create up to 15 custom strengths. | **Entra ID** > **Authentication methods** > **Authentication strengths** |
| Report-only mode | Evaluates a policy at sign-in and logs the result, but does not enforce grant or session controls. Users are not prompted or blocked. | **Enable policy** toggle on the policy |

Sources: [Network assignment](https://learn.microsoft.com/entra/identity/conditional-access/concept-assignment-network), [Authentication strengths](https://learn.microsoft.com/entra/identity/authentication/concept-authentication-strengths), and [Report-only mode](https://learn.microsoft.com/entra/identity/conditional-access/concept-conditional-access-report-only).

---

## Task 1: Record the starting state

1. Connect with the narrowest read scope and record the security defaults setting and the existing policy count.

   ```powershell
   Connect-MgGraph -Scopes "Policy.Read.All"

   (Get-MgPolicyIdentitySecurityDefaultEnforcementPolicy).IsEnabled
   (Get-MgIdentityConditionalAccessPolicy -All).Count
   Get-MgPolicyAuthenticationStrengthPolicy -Filter "policyType eq 'builtIn'" |
     Select-Object DisplayName
   ```

   Write down the first two values in your own notes. Security defaults and Conditional Access policies are not meant to be combined. If security defaults are enabled, disable them in **Entra ID** > **Overview** > **Properties** > **Manage security defaults** and restore them in cleanup.

### Validation gate 1

Record the number of built-in authentication strengths that the third command returns as **`builtin_strength_count`**.

Source: [Security defaults](https://learn.microsoft.com/entra/fundamentals/security-defaults#disabling-security-defaults).

---

## Task 2: Create a trusted named location

2. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com) as Admin1. Go to **Entra ID** > **Conditional Access** > **Named locations**, and then select **IP ranges location**.
   - **Name:** `MainOffice1`
   - **IP range:** `203.0.113.0/24`. This is a documentation range, so your own sign-ins start **outside** the trusted location. You add your real address in Task 6.
   - Select **Mark as trusted location**, and then select **Create**.

   Named locations accept public ranges only. Entra ID sees the address your network uses to reach the internet, not a private LAN address such as 10.55.99.3.

Source: [IPv4 and IPv6 address ranges](https://learn.microsoft.com/entra/identity/conditional-access/concept-assignment-network#ipv4-and-ipv6-address-ranges).

---

## Task 3: Create a custom authentication strength

3. Go to **Entra ID** > **Authentication methods** > **Authentication strengths**, and then select **New authentication strength**.
   - **Name:** `AuthStrength1`
   - **Description:** `Phishing-resistant sign-in for Humongous Insurance users away from the main office`
   - Under the multifactor methods, select **only** the FIDO2 security key method (labeled **Passkeys (FIDO2)** in newer portal versions) and **Windows Hello for Business** (or **Windows Hello for Business or platform credential**).
   - Select **Next**, review, and then select **Create**.

Why custom instead of built-in: the built-in **Phishing-resistant MFA strength** also allows certificate-based authentication (multifactor). Humongous Insurance does not use certificates, so the custom strength allows exactly the two methods that the company deploys.

Source: [Create and manage custom authentication strengths](https://learn.microsoft.com/entra/identity/authentication/concept-authentication-strength-advanced-options).

---

## Task 4: Create the policy in report-only mode

4. Go to **Entra ID** > **Conditional Access** > **Policies**, and then select **New policy**.
   - **Name:** `CAPolicy1 - Require AuthStrength1 outside trusted locations`
   - **Users or workload identities** > **Include** > **Select users and groups** > **Group1**.
   - **Exclude** > **Users and groups** > **BreakGlass1**.
   - **Target resources** > **Resources (formerly cloud apps)** > **Include** > **All resources (formerly 'All cloud apps')**.
   - **Network** > **Configure** > **Yes**. **Include** > **Any network or location**. **Exclude** > **All trusted networks and locations**.
   - **Grant** > **Grant access** > **Require authentication strength** > **AuthStrength1** > **Select**.
   - **Enable policy** > **Report-only**. Select **Create**.

5. Validate the configuration from Graph.

   ```powershell
   $p = Get-MgIdentityConditionalAccessPolicy -All |
     Where-Object DisplayName -like "CAPolicy1*"
   $p.State
   $p.Conditions.Locations.ExcludeLocations

   $s = Get-MgPolicyAuthenticationStrengthPolicy -Filter "policyType eq 'custom'" |
     Where-Object DisplayName -eq "AuthStrength1"
   $s.AllowedCombinations.Count

   (Get-MgIdentityConditionalAccessNamedLocation |
     Where-Object DisplayName -eq "MainOffice1").AdditionalProperties["isTrusted"]
   ```

### Validation gate 2

- Record `$p.State` as **`policy_state`**.
- Record the value from `ExcludeLocations` as **`policy_exclude_location`**.
- Record the count of allowed combinations as **`auth_strength_combinations`**.
- Record the `isTrusted` value as **`named_location_trusted`**.

Sources: [Get-MgIdentityConditionalAccessPolicy](https://learn.microsoft.com/powershell/module/microsoft.graph.identity.signins/get-mgidentityconditionalaccesspolicy) and [Get-MgIdentityConditionalAccessNamedLocation](https://learn.microsoft.com/powershell/module/microsoft.graph.identity.signins/get-mgidentityconditionalaccessnamedlocation).

---

## Task 5: Simulate with the What If tool

The What If tool evaluates both enabled and report-only policies, so you can test without a real sign-in.

6. Go to **Entra ID** > **Conditional Access** > **Policies** > **What If**. Set **User** to **User1**, **Target resources** to **Office 365**, **Device platform** to **Windows**, **Client app** to **Browser**, and **IP address** to `198.51.100.10`. Select **What If**.
7. Change only the **IP address** to `203.0.113.10` (inside MainOffice1) and select **What If** again.

### Validation gate 3

- If CAPolicy1 appears under the policies that **apply** in step 6, record **`whatif_applies_outside`** as `yes`. Otherwise record `no`.
- If CAPolicy1 appears under the policies that **apply** in step 7, record **`whatif_applies_inside`** as `yes`. Otherwise record `no`. Note the reason shown for policies that do not apply. It is the first condition that was not satisfied.

Source: [Troubleshoot Conditional Access policies with the What If tool](https://learn.microsoft.com/entra/identity/conditional-access/what-if-tool).

---

## Task 6: Verify with real sign-ins, then enforce

8. In an InPrivate window, sign in as User1 to `https://myapps.microsoft.com`. Note whether you are prompted for a passkey or Windows Hello for Business, and whether you reach the My Apps portal.
9. As Admin1, go to **Entra ID** > **Monitoring & health** > **Sign-in logs**. Filter on User1 and open the newest entry. Wait up to 15 minutes if it is not there yet.
   - On the **Report-only** tab, note the result for CAPolicy1.
   - On the **Basic info** tab (or **Location** tab), copy the **IP address**. This is the address Entra ID actually sees. It might be IPv6.
10. Edit **MainOffice1** and add that address as a single-address range: `/32` for IPv4 or `/128` for IPv6. Select **Save**. Sign out User1, close the InPrivate window, sign in again as User1, and then open the newest sign-in log entry and its **Report-only** tab.
11. Now that the logs prove the location exclusion works, open CAPolicy1, set **Enable policy** to **On**, and select **Save**. Run step 6 again in the What If tool and confirm that CAPolicy1 still applies outside MainOffice1. Do not sign in as User1 from outside MainOffice1 while the policy is on, because User1 has no phishing-resistant method and would be blocked.

### Validation gate 4

- If User1 reached My Apps in step 8 **without** a passkey or Windows Hello prompt, record **`user1_prompted`** as `no`. Otherwise record `yes`.
- Record the CAPolicy1 result from the **Report-only** tab in step 10, exactly as shown, as **`result_after_trusted`**.

Why this matters: report-only mode shows you the effect before users feel it. The step 9 result (it is not graded, because it depends on what User1 has registered) shows that the policy would have applied. The step 10 result shows that your trusted location exclusion works.

Source: [Policy evaluation results](https://learn.microsoft.com/entra/identity/conditional-access/concept-conditional-access-report-only#policy-evaluation-results).

---

## Task 7: Check your understanding

Use the [authentication strengths](https://learn.microsoft.com/entra/identity/authentication/concept-authentication-strengths#built-in-and-custom-authentication-strengths) and [network assignment](https://learn.microsoft.com/entra/identity/conditional-access/concept-assignment-network#trusted-locations) pages.

- Record the name of the one built-in strength that **Microsoft Authenticator (phone sign-in)** does **not** satisfy, exactly as Learn names it, as **`authenticator_not_in_strength`**.
- Can a named location that is marked as trusted be deleted while it is still marked as trusted? Record `yes` or `no` as **`trusted_location_delete_allowed`**.

---

## No-license path

Use this path if the tenant has no Microsoft Entra ID P1 and you cannot start a trial. Add `"_path": "no-license"` to your submission. The grader leaves out the checks marked `requires_license`.

- Run step 1. The Graph read of built-in authentication strengths is read-only. If your tenant does not return the strengths, count them on the [authentication strengths](https://learn.microsoft.com/entra/identity/authentication/concept-authentication-strengths#built-in-and-custom-authentication-strengths) page.
- In the Microsoft Entra admin center, open **Entra ID** > **Conditional Access** and review **Policies**, **Named locations**, and the **Templates** gallery without creating anything. Open **Authentication methods** > **Authentication strengths** to view the built-in definitions, if the page is available.
- Read [Require phishing-resistant MFA for administrators](https://learn.microsoft.com/entra/identity/conditional-access/policy-admin-phish-resistant-mfa) and map each portal step to Task 4.
- Complete Task 7.

---

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| **New policy** is unavailable, or a banner says security defaults are on | Disable security defaults (record the starting value first), or verify that the P1 trial is active. |
| **New authentication strength** is unavailable | Sign in with an account that has **Security Administrator** or higher. |
| The step 10 result is still not **Report-only: Not applied** | The address you added does not match what Entra ID sees. Use the exact IP from the sign-in log, including IPv6. Wait a few minutes after you save the named location, and sign in from a fresh InPrivate window. |
| No **Report-only** tab in the sign-in log entry | No report-only policy was evaluated for that sign-in. Confirm that User1 is in Group1 and that CAPolicy1 is in **Report-only**. |
| User1 was prompted for a passkey in step 8 | Another enabled policy (or security defaults) applies to User1. Check the **Conditional Access** tab in the sign-in log. |
| Cannot delete AuthStrength1 | A policy still references it. Delete CAPolicy1 first. |
| Cannot delete MainOffice1 | Clear **Mark as trusted location** and save, then delete it. |

---

## Cleanup (mandatory)

Delete in this order, because a referenced authentication strength and a trusted location cannot be deleted.

- **C1.** Delete **CAPolicy1** in **Conditional Access** > **Policies**.
- **C2.** Delete **AuthStrength1** in **Authentication methods** > **Authentication strengths**.
- **C3.** Open **MainOffice1**, clear **Mark as trusted location**, select **Save**, and then delete it.
- **C4.** If security defaults were enabled at the start **and** no other Conditional Access policies exist, re-enable security defaults.
- **C5.** If you created User1, Group1, or a trial only for this lab, remove them.

Deleted policies and named locations remain restorable for 30 days in soft delete.

### Cleanup validation

```powershell
(Get-MgIdentityConditionalAccessPolicy -All | Where-Object DisplayName -like "CAPolicy1*").Count
(Get-MgIdentityConditionalAccessNamedLocation | Where-Object DisplayName -eq "MainOffice1").Count
(Get-MgPolicyAuthenticationStrengthPolicy -Filter "policyType eq 'custom'" |
  Where-Object DisplayName -eq "AuthStrength1").Count
(Get-MgPolicyIdentitySecurityDefaultEnforcementPolicy).IsEnabled
Disconnect-MgGraph
```

If the first three commands each return `0` and security defaults match your starting value, record **`cleanup_done`** as `yes`.

Source: [Recover from deletions](https://learn.microsoft.com/entra/architecture/recover-from-deletions#conditional-access-policies).

---

## Record your results

Create `labs/1-1-2-conditional-access-report-only/submission.json` with one value per check:

```json
{
  "builtin_strength_count": "",
  "named_location_trusted": "",
  "auth_strength_combinations": "",
  "policy_state": "",
  "policy_exclude_location": "",
  "whatif_applies_outside": "",
  "whatif_applies_inside": "",
  "user1_prompted": "",
  "result_after_trusted": "",
  "authenticator_not_in_strength": "",
  "trusted_location_delete_allowed": "",
  "cleanup_done": ""
}
```

Then run **/grade 1-1-2-conditional-access-report-only**.

## Exam takeaways

- Report-only mode evaluates and logs, but never prompts or blocks. It does not cover the **User actions** scope.
- The four report-only results are **Success**, **Failure**, **User action required**, and **Not applied**. A user who is excluded, or a sign-in from an excluded location, produces **Not applied**.
- The usual pattern is **Include: Any network or location** and **Exclude: All trusted networks and locations**. **All trusted networks and locations** also includes MFA trusted IPs, if they are configured.
- Named locations must use public IP ranges, with CIDR masks greater than /8. Only IP-based locations can be marked as trusted, and a trusted location must be untrusted before it can be deleted.
- The three built-in authentication strengths are **Multifactor authentication strength**, **Passwordless MFA strength**, and **Phishing-resistant MFA strength**. Built-in strengths cannot be edited. Custom strengths (up to 15) cannot be deleted while a policy references them.
- Always exclude break-glass accounts, start in report-only mode, confirm with the What If tool and the sign-in logs, and then switch to **On**.

## References

- [What is Conditional Access? (license requirements)](https://learn.microsoft.com/entra/identity/conditional-access/overview#license-requirements)
- [Analyze Conditional Access policy impact (report-only mode)](https://learn.microsoft.com/entra/identity/conditional-access/concept-conditional-access-report-only)
- [Conditional Access: Network assignment](https://learn.microsoft.com/entra/identity/conditional-access/concept-assignment-network)
- [Conditional Access authentication strengths](https://learn.microsoft.com/entra/identity/authentication/concept-authentication-strengths)
- [Create and manage custom authentication strengths](https://learn.microsoft.com/entra/identity/authentication/concept-authentication-strength-advanced-options)
- [Troubleshoot Conditional Access policies with the What If tool](https://learn.microsoft.com/entra/identity/conditional-access/what-if-tool)
- [Require phishing-resistant MFA for administrators](https://learn.microsoft.com/entra/identity/conditional-access/policy-admin-phish-resistant-mfa)
- [Plan a Conditional Access deployment](https://learn.microsoft.com/entra/identity/conditional-access/plan-conditional-access)
- [Security defaults in Microsoft Entra ID](https://learn.microsoft.com/entra/fundamentals/security-defaults)
- [Manage emergency access accounts](https://learn.microsoft.com/entra/identity/role-based-access-control/security-emergency-access)
