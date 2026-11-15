# Access design decisions

| Symptom | Inspect before changing access | Evidence to retain |
| --- | --- | --- |
| User sees object but cannot edit field | Object update, field update, record access, page behavior, automation | User/assignment snapshot and exact failing operation |
| Field is still visible after muting | Profile, direct sets and other groups granting it | All grant paths, not only the edited group |
| Admin works, agent fails | Actual agent/action running user, CRUD/FLS and row scope | Target-identity execution result |
| User sees too many records | Org-wide defaults, hierarchy, sharing, broad privileges and applicable restrictions | Unexpected record IDs using synthetic data |

Separate UI convenience from security. A hidden component or field on a layout does not establish data authorization. A permission set cannot subtract another independent grant. Do not promise restriction-rule support for every object or execution mode; fetch current object-specific guidance.

For every proposed change, record the smallest required privilege and who will maintain it. Treat broad grants and sharing changes as impact-bearing mutations, not debugging shortcuts. If no target user session can be tested, deliver an unverified access plan rather than a passed security result.

Primary source: [Permission Set Groups](https://help.salesforce.com/s/articleView?id=platform.perm_set_groups.htm&release=264.0.0&type=5), reviewed 2026-11-15. Use the current guide for code execution/security context.

## Maintainable grants

Choose task-based permission sets and persona groups with a named owner. Do not mechanically generate every object/CRUD combination. Explain exceptions and all independent grant paths, including View All Fields where supported. Include a direct-grant-versus-group-muting test.

Additional official evidence: [Object Permissions](https://help.salesforce.com/s/articleView?id=platform.users_profiles_object_perms.htm&release=264.0.0&type=5) and [Field Permissions](https://help.salesforce.com/s/articleView?id=platform.users_profiles_fls.htm&release=264.0.0&type=5), fetched 2026-11-15. Check View All Fields and permission dependencies, including API-specific dependency handling.
