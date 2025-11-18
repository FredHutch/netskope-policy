# Quick Start Guide

Get up and running with Netskope real-time protection for your cancer clinical care and research organization in 15 minutes.

## Step 1: Obtain API Token (5 minutes)

1. Log in to your Netskope tenant admin console
2. Navigate to: **Settings** > **Tools** > **REST API v2**
3. Click **"New Token"**
4. Configure token:
   - **Name**: "Healthcare Policy Automation"
   - **Permissions**:
     - ✓ Policy Management (Read/Write)
     - ✓ DLP (Read/Write)
     - ✓ Threat Protection (Read/Write)
5. Click **"Generate"** and copy the token
6. **IMPORTANT**: Save the token securely (you can't view it again)

## Step 2: Setup Environment (5 minutes)

```bash
# Clone the repository
git clone <repository-url>
cd netskope-policy

# Install dependencies
pip install -r requirements.txt

# Configure credentials
cp .env.example .env

# Edit .env file with your credentials
nano .env
```

Update `.env` with your information:
```bash
NETSKOPE_TENANT=yourcompany          # Your tenant name
NETSKOPE_API_TOKEN=your-token-here   # Token from Step 1
ORGANIZATION_NAME=Your Cancer Center  # Your organization name
```

## Step 3: Test Connection (2 minutes)

```bash
# Test API connectivity
python scripts/deploy_policies.py --test-only
```

Expected output:
```
✓ Connection successful!
```

If you see an error, verify your credentials in `.env`.

## Step 4: Deploy Foundation Policies (3 minutes)

Deploy core healthcare protection policies:

```bash
python scripts/deploy_policies.py \
  --profile healthcare-foundation \
  --org-name "Your Cancer Center"
```

This deploys:
- ✓ PHI protection (MRN, SSN, DOB, ICD-10 codes)
- ✓ Ransomware protection
- ✓ Phishing protection
- ✓ Command & Control blocking
- ✓ Malware detection

## What's Next?

### Option A: Deploy All Policies

For comprehensive protection:

```bash
python scripts/deploy_policies.py --profile all
```

### Option B: Customize Policies

1. **Add Custom PHI Patterns**
   ```bash
   python examples/custom_phi_patterns.py
   ```

2. **Create Department Policies**
   ```bash
   python examples/department_policies.py
   ```

3. **Setup Vendor Access**
   ```bash
   python examples/vendor_access.py
   ```

### Option C: Monitor First (Recommended)

Before blocking, monitor for false positives:

1. Deploy policies in alert mode
2. Review incidents for 1-2 weeks
3. Tune patterns and thresholds
4. Switch to block mode

## Common Next Steps

### View Deployed Policies

```bash
python scripts/manage_policies.py list
```

### Check Recent Incidents

```bash
# DLP incidents
python scripts/manage_policies.py dlp-incidents

# Threat incidents
python scripts/manage_policies.py threat-incidents
```

### Export Policies for Backup

```bash
python scripts/manage_policies.py export --output backup.json
```

## Policy Overview

### PHI Protection Policies

**What's Protected:**
- Medical Record Numbers (MRN)
- Social Security Numbers (SSN)
- Dates of Birth (DOB)
- ICD-10 Diagnosis Codes
- Health Insurance Information
- Patient Names and IDs

**Actions:**
- Block uploads to unsanctioned apps
- Encrypt PHI in emails
- Alert on file sharing with PHI

### Threat Protection Policies

**Protection Against:**
- Ransomware (behavioral + signature)
- Malware (all types)
- Phishing and credential theft
- Command & Control (C2) communications
- Cryptominers and botnets

**Actions:**
- Block all malicious traffic
- Quarantine suspicious files
- Alert security team

## Quick Reference

### Deployment Commands

```bash
# Foundation policies
python scripts/deploy_policies.py --profile healthcare-foundation

# PHI protection only
python scripts/deploy_policies.py --profile phi-protection

# Threat protection only
python scripts/deploy_policies.py --profile threat-protection

# Research data protection
python scripts/deploy_policies.py --profile research-protection

# Everything
python scripts/deploy_policies.py --profile all

# Dry run (test without deploying)
python scripts/deploy_policies.py --profile all --dry-run
```

### Management Commands

```bash
# List all policies
python scripts/manage_policies.py list

# Enable policy
python scripts/manage_policies.py enable --policy-id <id>

# Disable policy
python scripts/manage_policies.py disable --policy-id <id>

# View incidents
python scripts/manage_policies.py dlp-incidents --days 7
python scripts/manage_policies.py threat-incidents --days 7

# Export policies
python scripts/manage_policies.py export --output backup.json
```

## Troubleshooting

### "Connection failed"
- Verify tenant name in `.env` (without .goskope.com)
- Check API token is correct
- Ensure token has required permissions

### "401 Unauthorized"
- API token may have expired
- Regenerate token from Netskope console
- Update `.env` with new token

### "Policy already exists"
- Use `manage_policies.py list` to see existing policies
- Delete or rename conflicting policies
- Or update existing policy instead

## Getting Help

- **Documentation**: See `docs/USAGE_GUIDE.md` for detailed instructions
- **Examples**: Check `examples/` directory for sample code
- **Configuration**: Review `config/netskope_config.json.example`

## Important Security Notes

1. **Never commit** `.env` or tokens to source control
2. **Rotate API tokens** every 90 days
3. **Test policies** in monitor mode before enforcement
4. **Review incidents** daily during initial deployment
5. **Maintain backups** of policy configurations

## Compliance Checklist

After deployment, ensure:

- [ ] PHI protection policies deployed
- [ ] Threat protection policies active
- [ ] Incident monitoring configured
- [ ] Audit logging enabled
- [ ] Policy documentation updated
- [ ] Security team trained on incident response
- [ ] Compliance officer notified of new controls

## Support

For issues or questions:
1. Review the [Usage Guide](USAGE_GUIDE.md)
2. Check example scripts in `examples/`
3. Contact your information security team

---

**Time to Protection: ~15 minutes** ✓

Congratulations! Your cancer clinical care and research organization now has enterprise-grade real-time protection against data loss and cyber threats.
