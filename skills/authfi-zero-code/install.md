---
type: Howto
title: "Install Zero-Code on a cluster"
description: "Connect a Kubernetes cluster to an AuthFI project with one Helm command, check that every node is covered, and upgrade or remove the install."
tags: [authfi, zero-code, kubernetes, helm, install]
sources:
  - id: zero-code-install
    resource: https://authfi.io/docs/zero-code/install
    title: "Install Zero-Code on a cluster"
---

# Install Zero-Code on a cluster

One Helm release puts Zero-Code on a cluster. A new install runs in monitor mode: it records what happens and denies nothing.

## Before you begin

- A plan that includes Zero-Code.
- The `read:kubernetes` permission in the project. AuthFI permissions decide who can see a cluster in the console, not Kubernetes RBAC.
- `helm` and `kubectl`, with access to the cluster.
- Kubernetes 1.30 or newer, Linux nodes on x86-64, kube-proxy in iptables mode, and outbound HTTPS from the nodes to the project's issuer. The full requirements table is on the docs page.

## Install

1. In the console, open **Zero-Code > Kubernetes** and choose **Install on a cluster**.
2. The **Install the node agent** dialog shows the command. **Copy the command from the dialog. Do not write one from memory.**
3. The chart and both images are signed. Verify them with `cosign` first, as your own supply-chain rules require.
4. Run the command in a shell connected to the cluster, then choose **Done**.

## Check that it works

The cluster appears under **Zero-Code > Kubernetes** when its first node checks in. From the cluster:

```bash
kubectl -n authfi-system get agentrt
```

When `READY` equals `DESIRED`, a node agent is running on every node.

## Settings

Everything is created in the namespace `authfi-system`. One custom resource, `AgentRuntime`, describes the install. The Helm chart writes it. Set values through Helm.

| Field | Default | Meaning |
| --- | --- | --- |
| `issuerUrl` | | Your project's issuer |
| `mode` | `observe` | `observe` is monitor mode. `enforce` lets the nodes deny. |
| `enforcementInhibit` | `false` | The brake, held by the cluster owner |
| `clusterName` | | The name shown in the console |

## Upgrade and remove

- Upgrade with `helm upgrade` on the release you installed. Node agents are replaced one node at a time, and rules in force stay in force.
- Remove with `helm uninstall "$RELEASE"`. Uninstalling hands every node back: enforcement is switched off and every rule is cleared before the release is gone. If a node cannot be reached, the uninstall stops and names that node.

## Detail

Requirements, what the install creates and every setting: [Install Zero-Code on a cluster](https://authfi.io/docs/zero-code/install)
