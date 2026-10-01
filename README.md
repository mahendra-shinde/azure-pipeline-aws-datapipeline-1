# Deploy and run an AWS Databricks Asset Bundle

This lab uses Azure Pipelines to validate, deploy, and run a Databricks Asset
Bundle in an AWS Databricks development workspace. The bundle deploys a
notebook job that counts distinct customers by country and overwrites a managed
analytics table.

## Prerequisites

- An AWS Databricks workspace and an approved development compute policy.
- An Azure DevOps variable group named `databricks-development`, authorized for
  this pipeline, with secret variables `DATABRICKS_HOST` and
  `DATABRICKS_TOKEN`.
- A deployment identity that can use the compute policy, read the source table,
  create or replace the target table, and deploy and run jobs.

Do not commit workspace hosts or credentials. For production, use the
organization's approved workload identity or service principal instead of a
long-lived personal token.

## Configure the development target

Before running the pipeline, set the following non-secret variables in the
`databricks-development` variable group:

| Variable | Purpose |
| --- | --- |
| `BUNDLE_VAR_compute_policy_id` | ID of the approved development compute policy |
| `BUNDLE_VAR_source_table` | Permitted fully qualified governed source table |
| `BUNDLE_VAR_target_table` | Permitted fully qualified managed target table |

The source must contain `customer_id` and `country` columns. The example table
names in `databricks.yml` are intentionally placeholders. The cluster values in
`resources/customer_metrics.job.yml` are AWS examples; adjust them if required
by the approved policy. Policy defaults are applied automatically.

## Pipeline

`azure-pipelines.yml` installs Databricks CLI 1.19.0 and then runs:

```text
databricks bundle validate --target dev
databricks bundle deploy --target dev
databricks bundle run customer_metrics --target dev
```

The Databricks host and token are exposed only to the commands that need them.
