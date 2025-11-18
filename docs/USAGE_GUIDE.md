# Netskope Real-Time Protection - Usage Guide

Complete guide for deploying and managing Netskope real-time protection policies for cancer clinical care and research organizations.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Configuration](#configuration)
3. [Deploying Policies](#deploying-policies)
4. [Managing Policies](#managing-policies)
5. [Custom Policies](#custom-policies)
6. [Monitoring and Compliance](#monitoring-and-compliance)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

## Getting Started

### Prerequisites

1. **Netskope Tenant Access**
   - Admin access to your Netskope tenant
   - Permissions to create and manage policies

2. **API Token**
   - Navigate to: Settings > Tools > REST API v2
   - Click "New Token"
   - Select appropriate permissions:
     - Policy Management (Read/Write)
     - DLP (Read/Write)
     - Threat Protection (Read/Write)
   - Save the token securely

3. **Python Environment**
   - Python 3.8 or higher
   - pip package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd netskope-policy

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Test connection
python scripts/deploy_policies.py --test-only
```

## Configuration

### Environment Variables

Create a `.env` file with your credentials:

```bash
NETSKOPE_TENANT=yourcompany
NETSKOPE_API_TOKEN=your-api-token-here
ORGANIZATION_NAME=Your Cancer Center
```

### Configuration File

Alternatively, use `config/netskope_config.json`:

```bash
cp config/netskope_config.json.example config/netskope_config.json
# Edit the file with your settings
```

## Deploying Policies

### Quick Deployment

Deploy foundation healthcare policies:

```bash
python scripts/deploy_policies.py \
  --profile healthcare-foundation \
  --org-name "Your Cancer Center"
```

### Deployment Profiles

#### 1. Healthcare Foundation
Core policies for PHI protection and threat prevention:

```bash
python scripts/deploy_policies.py --profile healthcare-foundation
```

**Includes:**
- PHI DLP policies
- Ransomware protection
- Phishing protection
- C2 blocking

#### 2. PHI Protection Only
HIPAA-compliant PHI protection policies:

```bash
python scripts/deploy_policies.py --profile phi-protection
```

**Includes:**
- PHI detection patterns (MRN, SSN, DOB, ICD-10)
- Email protection
- File sharing controls
- Cloud app DLP

#### 3. Threat Protection
Comprehensive threat protection:

```bash
python scripts/deploy_policies.py --profile threat-protection
```

**Includes:**
- Ransomware protection
- Malware detection
- Phishing prevention
- Command & Control blocking

#### 4. Research Data Protection
Clinical research data protection:

```bash
python scripts/deploy_policies.py --profile research-protection
```

**Includes:**
- Clinical trial data protection
- Genomic data protection
- Subject ID protection
- Biospecimen tracking

#### 5. All Policies
Complete healthcare policy suite:

```bash
python scripts/deploy_policies.py --profile all
```

### Dry Run

Test deployment without making changes:

```bash
python scripts/deploy_policies.py --profile all --dry-run
```

## Managing Policies

### List All Policies

```bash
python scripts/manage_policies.py list
```

### Get Policy Details

```bash
python scripts/manage_policies.py details --policy-id <policy-id>
```

### Enable/Disable Policies

```bash
# Enable a policy
python scripts/manage_policies.py enable --policy-id <policy-id>

# Disable a policy
python scripts/manage_policies.py disable --policy-id <policy-id>
```

### Delete Policies

```bash
# Delete with confirmation
python scripts/manage_policies.py delete --policy-id <policy-id>

# Force delete without confirmation
python scripts/manage_policies.py delete --policy-id <policy-id> --force
```

### Export Policies

Export all policies to JSON:

```bash
python scripts/manage_policies.py export --output policies_backup.json
```

## Custom Policies

### Custom PHI Patterns

Create organization-specific PHI protection:

```python
from netskope_sdk import NetskopeClient
from policies import HealthcarePolicy

client = NetskopeClient(
    tenant="your-tenant",
    api_token="your-token"
)

healthcare = HealthcarePolicy(client, "Your Org")

# Define custom patterns
custom_patterns = [
    {
        "name": "Custom Patient ID",
        "pattern_type": "regex",
        "pattern": r"\bPT-[0-9]{6}\b",
        "match_count": 1,
        "proximity": 50,
        "description": "Your custom patient ID format"
    }
]

# Create policy
policy = healthcare.create_custom_phi_policy(
    name="Custom PHI Protection",
    custom_patterns=custom_patterns,
    action="block"
)
```

See `examples/custom_phi_patterns.py` for more details.

### Department-Specific Policies

Create policies for specific departments:

```python
# Oncology department
oncology_policies = healthcare.create_department_policy(
    department_name="Oncology",
    user_group="oncology_users",
    allowed_apps=["Epic MyChart", "Cerner", "Box"],
    block_external_sharing=True
)
```

See `examples/department_policies.py` for more details.

### Vendor Access Policies

Create policies for business associates:

```python
# CRO partner access
cro_policies = healthcare.create_vendor_access_policy(
    vendor_name="CRO Partner",
    user_group="vendor_cro",
    allowed_apps=["Box"],
    enable_dlp=True
)
```

See `examples/vendor_access.py` for more details.

## Monitoring and Compliance

### View DLP Incidents

List recent DLP incidents:

```bash
# Last 7 days (default)
python scripts/manage_policies.py dlp-incidents

# Last 30 days
python scripts/manage_policies.py dlp-incidents --days 30
```

### View Threat Incidents

List recent threat incidents:

```bash
# Last 7 days (default)
python scripts/manage_policies.py threat-incidents

# Last 30 days
python scripts/manage_policies.py threat-incidents --days 30
```

### Audit Logs

All deployment and management operations are logged:

- `logs/deployment_*.log` - Deployment operations
- `logs/api_calls.log` - API interactions
- `logs/policy_changes.log` - Policy modifications

### Compliance Reports

Generate compliance reports using the SDK:

```python
from netskope_sdk.dlp import DLPManager
from datetime import datetime, timedelta

dlp = DLPManager(client)

# Get statistics
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=30)

stats = dlp.get_dlp_statistics(
    start_time=start_time.isoformat(),
    end_time=end_time.isoformat()
)
```

## Troubleshooting

### Connection Issues

**Problem:** "Connection failed" error

**Solutions:**
1. Verify API token is valid
2. Check tenant name (should be without .goskope.com)
3. Ensure API token has required permissions
4. Check network connectivity to Netskope

```bash
# Test connection
python scripts/deploy_policies.py --test-only
```

### Authentication Errors

**Problem:** "401 Unauthorized" error

**Solutions:**
1. Regenerate API token
2. Verify token hasn't expired
3. Check token permissions

### Policy Creation Failures

**Problem:** Policy creation fails with validation error

**Solutions:**
1. Review policy configuration
2. Check for duplicate policy names
3. Verify user groups exist
4. Ensure app names are correct

### Rate Limiting

**Problem:** "429 Too Many Requests" error

**Solutions:**
1. The SDK automatically retries with backoff
2. Reduce concurrent operations
3. Contact Netskope to increase rate limits

## Best Practices

### Pre-Deployment

1. **Test in Monitor Mode**
   - Deploy policies with action="alert" first
   - Monitor for false positives
   - Tune patterns and thresholds
   - Switch to action="block" after validation

2. **Use Pilot Groups**
   - Start with small user groups
   - Monitor impact
   - Expand gradually

3. **Document Changes**
   - Keep policy documentation current
   - Document custom patterns
   - Maintain change log

### Policy Management

1. **Regular Reviews**
   - Review policies quarterly
   - Update patterns for new PHI types
   - Remove obsolete policies
   - Audit policy effectiveness

2. **Naming Conventions**
   - Use organization prefix
   - Include department/function
   - Specify policy type
   - Example: "CancerCenter - Oncology - PHI Protection"

3. **Version Control**
   - Store configurations in git
   - Track policy changes
   - Enable rollback capability

### Security

1. **API Token Management**
   - Rotate tokens every 90 days
   - Store in secure vault (e.g., AWS Secrets Manager)
   - Never commit tokens to source control
   - Use environment variables

2. **Access Control**
   - Limit who can deploy policies
   - Use least-privilege principle
   - Audit policy changes
   - Require change approval

3. **Monitoring**
   - Review incidents daily
   - Set up alerts for critical incidents
   - Integrate with SIEM
   - Maintain incident response procedures

### Compliance

1. **HIPAA Alignment**
   - Document policy mappings to HIPAA controls
   - Maintain audit logs
   - Regular compliance reviews
   - Update for regulatory changes

2. **Business Associate Management**
   - Ensure BAAs are in place
   - Monitor vendor access
   - Regular vendor reviews
   - Document vendor policies

3. **Incident Response**
   - Define escalation procedures
   - Breach notification workflows
   - Evidence preservation
   - Post-incident reviews

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review example scripts
3. Check Netskope documentation
4. Contact your security team

## Additional Resources

- [Netskope Documentation](https://docs.netskope.com/)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- Example scripts in `examples/` directory
