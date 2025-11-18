# HIPAA Compliance Mapping

This document maps Netskope real-time protection policies to specific HIPAA Security Rule requirements for cancer clinical care and research organizations.

## Overview

The HIPAA Security Rule requires covered entities and business associates to implement administrative, physical, and technical safeguards to protect electronic Protected Health Information (ePHI). This framework implements technical safeguards through Netskope real-time protection.

## HIPAA Security Rule Compliance Matrix

### Administrative Safeguards (§164.308)

#### §164.308(a)(1) - Security Management Process

**Requirement**: Implement policies and procedures to prevent, detect, contain, and correct security violations.

**Implementation**:
- **Risk Analysis**: DLP policies detect ePHI exposure risks
- **Risk Management**: Threat protection policies mitigate identified risks
- **Sanction Policy**: Policy enforcement with blocking/alerting actions
- **Information System Activity Review**: Incident logging and monitoring

**Policies Deployed**:
```python
# PHI Protection Policies
healthcare.deploy_phi_protection()
- Detects ePHI in data transfers
- Prevents unauthorized sharing
- Monitors for policy violations

# Threat Protection Policies
healthcare.deploy_ransomware_protection()
- Prevents ransomware attacks
- Blocks malware
- Protects against data breaches
```

**Compliance Evidence**:
- Policy deployment logs
- Incident reports (DLP and threat)
- Regular policy reviews

---

#### §164.308(a)(3) - Workforce Security

**Requirement**: Implement procedures to ensure workforce members have appropriate access to ePHI.

**Implementation**:
- Department-specific policies limit access
- Vendor access policies for business associates
- User group-based policy enforcement

**Policies Deployed**:
```python
# Department-specific access controls
healthcare.create_department_policy(
    department_name="Oncology",
    user_group="oncology_users",
    allowed_apps=["Epic MyChart", "Cerner", "Box"],
    block_external_sharing=True
)

# Vendor access controls
healthcare.create_vendor_access_policy(
    vendor_name="CRO Partner",
    user_group="vendor_cro",
    allowed_apps=["Box"],
    enable_dlp=True
)
```

**Compliance Evidence**:
- User group configurations
- Access control policies
- Vendor access logs

---

#### §164.308(a)(4) - Information Access Management

**Requirement**: Implement policies to authorize access to ePHI only for authorized persons.

**Implementation**:
- Cloud app access controls
- Sanctioned vs. unsanctioned app policies
- Activity-based access (upload, download, share)

**Policies Deployed**:
```python
# Cloud app controls
healthcare.deploy_cloud_app_controls()
- Allows only sanctioned healthcare apps
- Blocks personal cloud storage
- Controls file sharing activities
```

**Compliance Evidence**:
- App allow/block lists
- Activity logs
- Access violation incidents

---

#### §164.308(a)(5) - Security Awareness and Training

**Requirement**: Implement security awareness and training program.

**Implementation**:
- Policy alerts educate users on violations
- Incident reports inform training needs
- Policy documentation for staff

**Supporting Materials**:
- User incident notifications
- Training materials based on common violations
- Policy documentation in `docs/`

---

### Physical Safeguards (§164.310)

*Note: Physical safeguards are primarily addressed through datacenter controls. Netskope provides complementary cloud security controls.*

---

### Technical Safeguards (§164.312)

#### §164.312(a)(1) - Access Control

**Requirement**: Implement technical policies and procedures for systems that maintain ePHI to allow access only to authorized users.

**Implementation**:
- User-based policy enforcement
- Group-based access controls
- Application access restrictions

**Policies Deployed**:
```python
# User group-based access
- Department policies limit app access by user group
- Vendor policies restrict business associate access
- Role-based cloud app permissions
```

**Compliance Evidence**:
- User authentication logs
- Access control lists
- Policy enforcement logs

---

#### §164.312(b) - Audit Controls

**Requirement**: Implement hardware, software, and/or procedural mechanisms that record and examine activity.

**Implementation**:
- Comprehensive API activity logging
- DLP incident logging
- Threat incident logging
- Policy change tracking

**Audit Logs**:
```bash
logs/
├── api_calls.log          # All API interactions
├── policy_changes.log     # Policy modifications
├── deployment_*.log       # Deployment activities
└── security_events.log    # Security incidents
```

**Retrieving Audit Data**:
```bash
# DLP incidents
python scripts/manage_policies.py dlp-incidents --days 30

# Threat incidents
python scripts/manage_policies.py threat-incidents --days 30

# Export all policies (includes change history)
python scripts/manage_policies.py export --output audit.json
```

**Compliance Evidence**:
- Audit log files
- Incident reports
- Policy change history
- Access logs

---

#### §164.312(c)(1) - Integrity

**Requirement**: Implement policies to ensure ePHI is not improperly altered or destroyed.

**Implementation**:
- File integrity monitoring through malware detection
- Protection against ransomware
- Backup and recovery through cloud app controls

**Policies Deployed**:
```python
# Ransomware protection
threat_manager.create_ransomware_protection(
    enable_behavioral_detection=True,
    enable_file_type_blocking=True,
    enable_anomaly_detection=True
)

# Malware detection
threat_manager.create_malware_policy(
    scan_downloads=True,
    scan_uploads=True
)
```

**Compliance Evidence**:
- Malware detection logs
- Ransomware blocking events
- File modification alerts

---

#### §164.312(d) - Person or Entity Authentication

**Requirement**: Implement procedures to verify that a person or entity seeking access to ePHI is the one claimed.

**Implementation**:
- Integration with identity providers
- User identity verification in policy enforcement
- Multi-factor authentication support

**Note**: MFA is configured in Netskope tenant settings (not through API).

---

#### §164.312(e)(1) - Transmission Security

**Requirement**: Implement technical security measures to guard against unauthorized access to ePHI transmitted over electronic networks.

**Implementation**:
- DLP policies for data in transit
- Email encryption for ePHI
- Cloud app encryption enforcement
- Web traffic inspection

**Policies Deployed**:
```python
# Email PHI protection with encryption
dlp_manager.create_dlp_policy(
    name="PHI Email Protection",
    profile_id=phi_profile_id,
    action="encrypt",
    cloud_apps=["Gmail", "Office 365 Email"]
)

# File sharing protection
dlp_manager.create_dlp_policy(
    name="PHI File Sharing Protection",
    profile_id=phi_profile_id,
    action="alert",
    cloud_apps=["Box", "OneDrive", "Google Drive"]
)
```

**Compliance Evidence**:
- Email encryption logs
- Data transfer logs
- DLP policy enforcement records
- Blocked transmission attempts

---

## Protected Health Information (PHI) Coverage

### PHI Elements Protected

The DLP policies detect and protect the following PHI identifiers:

1. **Names** - Patient, subject, and participant names
2. **Dates** - Dates of birth, admission dates, discharge dates
3. **Telephone/Fax Numbers** - Contact information
4. **Email Addresses** - Patient email addresses
5. **Social Security Numbers** - SSNs in various formats
6. **Medical Record Numbers** - MRNs, patient IDs
7. **Health Plan Numbers** - Insurance policy/member numbers
8. **Account Numbers** - Patient account numbers
9. **Certificate/License Numbers** - Professional licenses
10. **Device Identifiers** - Medical device IDs
11. **IP Addresses** - (When associated with ePHI)
12. **Biometric Identifiers** - (Through custom patterns)
13. **Photographic Images** - (Through file type controls)
14. **Other Unique IDs** - Custom organizational identifiers

### Implementation

```python
# PHI Protection Profile includes:
phi_profile = dlp_manager.create_phi_protection_profile(
    include_mrn=True,          # Medical Record Numbers
    include_ssn=True,          # Social Security Numbers
    include_dob=True,          # Dates of Birth
    include_diagnosis_codes=True,  # ICD-10 codes
    custom_patterns=[...]      # Organization-specific identifiers
)
```

---

## Clinical Research Specific Requirements

### FDA 21 CFR Part 11 (Electronic Records)

For organizations conducting clinical trials:

**Requirement**: Controls for electronic records and signatures.

**Implementation**:
```python
# Research data protection
healthcare.deploy_research_data_protection()
- Clinical trial protocol protection
- Subject identifier protection
- Genomic data protection
- Biospecimen tracking
- IRB protocol protection
```

**Coverage**:
- Research protocol identifiers
- Subject/participant IDs
- Genomic markers (SNPs, gene IDs)
- Biospecimen identifiers
- IRB protocol numbers

---

## Business Associate Agreements (BAA)

### Vendor Access Management

**HIPAA Requirement**: Business associates must comply with applicable HIPAA requirements.

**Implementation**:
```python
# Vendor access with enhanced monitoring
healthcare.create_vendor_access_policy(
    vendor_name="Vendor Name",
    user_group="vendor_group",
    allowed_apps=["Specific Apps"],
    enable_dlp=True  # Enhanced monitoring
)
```

**Requirements**:
1. Signed BAA before access granted
2. Minimum necessary access
3. DLP monitoring enabled
4. Regular access reviews
5. Automatic deprovisioning
6. Breach notification procedures

---

## Breach Notification Compliance

### §164.404 - Notification to Individuals

**Detecting Breaches**:
```bash
# Review DLP incidents for potential breaches
python scripts/manage_policies.py dlp-incidents --days 30
```

**Breach Indicators**:
- PHI transmitted to unsanctioned apps
- External sharing of PHI
- Unauthorized access to PHI
- PHI exfiltration attempts

**Response Process**:
1. Review DLP/threat incidents daily
2. Investigate high-severity incidents
3. Determine if breach occurred
4. Follow breach notification procedures
5. Document incident and response

---

## Compliance Checklist

### Initial Deployment

- [ ] Deploy PHI protection policies
- [ ] Deploy threat protection policies
- [ ] Configure department-specific access controls
- [ ] Setup vendor access policies (if applicable)
- [ ] Enable audit logging
- [ ] Configure incident alerting
- [ ] Document policy mappings to HIPAA controls
- [ ] Train security team on incident response

### Ongoing Compliance

- [ ] Review incidents daily
- [ ] Conduct policy review quarterly
- [ ] Update PHI patterns as needed
- [ ] Review vendor access quarterly
- [ ] Maintain audit logs (6 years minimum)
- [ ] Update risk analysis annually
- [ ] Conduct security awareness training
- [ ] Review and update policies for regulation changes

### Documentation Requirements

- [ ] Policy deployment records
- [ ] Incident logs and investigations
- [ ] Risk assessments
- [ ] Policy review documentation
- [ ] Training records
- [ ] Vendor BAAs
- [ ] Breach notification procedures
- [ ] Incident response plans

---

## Evidence Collection for Audits

### Audit Preparation

1. **Export Current Policies**
   ```bash
   python scripts/manage_policies.py export --output audit_policies.json
   ```

2. **Collect Incident Reports**
   ```bash
   # Last 30 days of DLP incidents
   python scripts/manage_policies.py dlp-incidents --days 30 > dlp_audit.txt

   # Last 30 days of threat incidents
   python scripts/manage_policies.py threat-incidents --days 30 > threat_audit.txt
   ```

3. **Review Logs**
   - `logs/api_calls.log` - API activity
   - `logs/policy_changes.log` - Policy modifications
   - `logs/deployment_*.log` - Deployment history

4. **Document Controls**
   - Copy of deployed policies
   - Incident statistics
   - Response procedures
   - Training materials

---

## Contact Information

**Privacy Officer**: [Contact Information]
**Security Officer**: [Contact Information]
**Compliance Team**: [Contact Information]

---

## References

- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [HHS HIPAA FAQs](https://www.hhs.gov/hipaa/for-professionals/faq/index.html)
- [Netskope HIPAA Compliance](https://www.netskope.com/security-compliance)
- [FDA 21 CFR Part 11](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application)

---

**Document Version**: 1.0
**Last Updated**: [Date]
**Next Review**: [Date + 1 year]
