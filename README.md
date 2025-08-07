# KubeNightShift (Kubernetes Cron Deployment Auto Scaler)

Automate Kubernetes deployment scaling in GKE, AKS or EKS based on work hours and weekends, using CronJobs and a Python client. Save costs by scheduling replicas up and down, with original counts restored automatically.

---

## 🚀 Overview

This open-source project enables **automatic, scheduled scaling** of Kubernetes Deployments in GKE, AKS or EKS clusters:

- **Scales down** deployments on weekday evenings and keeps them down during weekends.
- **Restores** deployments to their original replica counts on weekday mornings.
- **Lowers costs** by running workloads only during active business hours.
- **Uses annotations** to remember original replica counts for reliable restoration.

---

## ✨ Features

- **Automatic Scaling**: No manual intervention needed for routine scaling.
- **Flexible Scheduling**: Easily adjust work hours and business days.
- **Safe Restoration**: Always restores deployments to their original replica count.
- **Secure by Default**: Uses Kubernetes RBAC and Service Accounts.
- **Cloud Native**: Works seamlessly with any Kubernetes provider.

---

## 🛠️ Architecture

- **Python script** runs as a Kubernetes Job/CronJob.
- **RBAC** restricts permissions to only what's necessary.
- **Annotations** on deployments record original replica counts before scaling down.
- **Two CronJobs**:
  - **Scale down:** Weekdays at 19:00 CET (18:00 UTC), Mon–Fri.
  - **Scale up:** Weekdays at 06:00 CET (05:00 UTC), Mon–Fri.
  - **Weekends:** Deployments remain scaled down.

---

## 📅 CronJob Schedules

| Operation   | CET Time | UTC Time | Cron Schedule     | Days          |
|-------------|----------|----------|-------------------|---------------|
| Scale Up    | 06:00    | 05:00    | `0 5 * * 1-5`     | Mon–Fri       |
| Scale Down  | 19:00    | 18:00    | `0 18 * * 1-5`    | Mon–Fri       |

> **Note:** CronJobs use UTC for scheduling.

---

## 🧑‍💻 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/chetanxrathore/KubeNightShift.git
cd KubeNightShift
```

### 2. Build and Push Docker Image

```bash
docker build -t yourregistry.azurecr.io/kubenightshift:latest .
docker push yourregistry.azurecr.io/kubenightshitft:latest
```

### 3. Apply RBAC and CronJobs

```bash
kubectl apply -f rbac.yaml
kubectl apply -f cronjob-scale-down.yaml
kubectl apply -f cronjob-scale-up.yaml
```
## 🛠️ Manual Execution

**Manually trigger scaling for testing:**
```bash
kubectl create job --from=cronjob/scale-down-deployments manual-scale-down -n kube-system
kubectl create job --from=cronjob/scale-up-deployments manual-scale-up -n kube-system
```
**Check logs:**
```bash
kubectl logs job/manual-scale-down -n kube-system
kubectl logs job/manual-scale-up -n kube-system
```
## 🔒 Security & Permissions

- Uses a dedicated Service Account with RBAC permissions to list, get, patch deployments and namespaces.
- Never exposes sensitive data.

## 🧪 Testing & Troubleshooting

- **Verify deployments**:
```bash
kubectl get deployments --all-namespaces
```

- **Check annotations**:
```bash
kubectl get deployment <deployment-name> -n <namespace> -o yaml | grep original_replicas
```

- **Time mismatch**:
```bash
Ensure your cluster runs on UTC and that cron schedules match your business hours.
```

## 🙋 FAQ
- **Q:** Will it work with deployments that already have custom annotations?

  **A:** Yes, it adds or removes only the original_replicas annotation.

- **Q:** How does the script authenticate to the cluster?

  **A:** It uses in-cluster config (service account) and RBAC.

- **Q:** Can I change the schedule or workdays?

  **A:** Absolutely! Edit the schedule field in the CronJob YAMLs.

## 📄 License

MIT License. See LICENSE file for details.

## 💡 Contributing

Pull requests and suggestions are welcome! Please open an issue to discuss changes or improvements.
