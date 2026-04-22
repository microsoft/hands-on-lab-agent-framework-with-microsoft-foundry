# Contoso - GitHub Issue Writing Guidelines

## 📋 Table of Contents
1. [Introduction](#introduction)
2. [Standard Issue Structure](#standard-structure)
3. [Issue Titles](#issue-titles)
4. [Labels and Classifications](#labels-classifications)
5. [Assignment and Responsibilities](#assignment-responsibilities)
6. [Practical Examples](#practical-examples)
7. [Validation Process](#validation-process)
8. [Best Practices](#best-practices)

## 🎯 Introduction

At Contoso, we use GitHub Issues to efficiently track bugs, feature requests, and development tasks. This guide establishes standard conventions to ensure clear communication and optimal project management.

### Guide Objectives
- Standardize issue creation
- Improve problem traceability
- Facilitate prioritization and assignment
- Optimize team collaboration

## 📝 Standard Issue Structure

### Bug Report Template
```markdown
## 🐛 Bug Description
[Clear and concise description of the problem]

## 📋 Reproduction Steps
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. Observe the error

## ✅ Expected Behavior
[Description of what should happen]

## ❌ Observed Behavior
[Description of what actually happens]

## 🖥️ Environment
- OS: [e.g. Windows 10, macOS 12.1]
- Browser: [e.g. Chrome 95, Firefox 94]
- App Version: [e.g. 2.1.3]

## 📎 Screenshots/Logs
[Add screenshots if applicable]

## 🔍 Additional Information
[Any other useful context]
```

### Feature Request Template
```markdown
## 🚀 Feature Request
[One-sentence summary of the requested feature]

## 💡 Problem/Need
[Describe the problem this feature would solve]

## 🎯 Proposed Solution
[Detailed description of the envisioned solution]

## 📋 Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## 🔄 Alternatives Considered
[Other solutions considered and why they were dismissed]

## 📈 Business Impact
- Users impacted: [number/percentage]
- Business priority: [High/Medium/Low]
- Estimated ROI: [if applicable]

## 🛠️ Technical Considerations
[Anticipated technical constraints or challenges]
```

## 🏷️ Issue Titles

### Standard Format
`[TYPE] [COMPONENT] - Short description`

### Issue Types
- **[BUG]** - Problem in existing code
- **[FEATURE]** - New functionality
- **[ENHANCEMENT]** - Improvement of existing feature
- **[DOCS]** - Documentation update
- **[REFACTOR]** - Code refactoring
- **[SECURITY]** - Security issue
- **[PERFORMANCE]** - Performance issue

### Title Examples
- `[BUG] Auth - Login fails with Azure AD`
- `[FEATURE] Dashboard - Add real-time charts`
- `[ENHANCEMENT] API - Improve endpoint response time`
- `[SECURITY] Login - XSS vulnerability in form`

## 🏷️ Labels and Classifications

### Mandatory Labels

#### Priority
- `priority/critical` - Major production impact
- `priority/high` - Important feature blocked
- `priority/medium` - Moderate impact
- `priority/low` - Nice to have

#### Team
- `team/frontend` - UI/UX Team
- `team/backend` - API/Services Team
- `team/devops` - Infrastructure Team
- `team/qa` - Quality Team
- `team/security` - Security Team

#### Status
- `status/triage` - Awaiting classification
- `status/in-progress` - Under development
- `status/review` - In code review
- `status/testing` - In testing phase
- `status/blocked` - Blocked by dependency

#### Complexity
- `complexity/simple` - < 1 day
- `complexity/medium` - 1-3 days
- `complexity/complex` - > 3 days

### Optional Labels
- `good-first-issue` - Suitable for new contributors
- `help-wanted` - External help welcome
- `breaking-change` - Breaking change
- `duplicate` - Already reported issue

## 👥 Assignment and Responsibilities

### Assignment Rules
1. **Initial Triage**: Product Owner or Tech Lead
2. **Assignment**: Technical lead of the concerned team
3. **Maximum**: 3 people assigned per issue

### Responsibilities by Role

#### Product Owner
- Validation of acceptance criteria
- Issue prioritization
- Stakeholder communication

#### Tech Lead
- Assignment to developers
- Technical validation of solutions
- Complexity estimation

#### Assigned Developer
- Solution implementation
- Status updates
- Change documentation

## 💡 Practical Examples

### Example 1: Critical Bug
```
Title: [BUG] Payment - Credit card payment failures

Labels: priority/critical, team/backend, status/triage
Assigned: @john.doe, @jane.smith

Description:
Users can no longer make credit card payments since 2:30 PM today. 
Error 500 returned by payment API.

Environment: Production - API Gateway v2.3.1
Impact: 100% of transactions failing
```

### Example 2: Feature Request
```
Title: [FEATURE] Dashboard - PDF data export

Labels: priority/medium, team/frontend, complexity/medium
Assigned: @ui.developer

Acceptance criteria:
- [ ] Export button visible on dashboard
- [ ] PDF generated with Contoso logo
- [ ] Data filtered according to selected period
- [ ] Confirmation email sent to user
```

## ✅ Validation Process

### Mandatory Steps
1. **Creation** - Use appropriate template
2. **Triage** - Product Owner validates and labels (24h max)
3. **Estimation** - Tech Lead estimates complexity (48h max)
4. **Assignment** - Assignment to developers
5. **Development** - Implementation with tests
6. **Review** - Mandatory code review
7. **Testing** - QA testing if applicable
8. **Closure** - Final validation and closure

### Closure Criteria
- ✅ Solution implemented and tested
- ✅ Documentation updated
- ✅ Code review approved
- ✅ Automated tests added (if applicable)
- ✅ Product Owner validation

## 🚀 Best Practices

### Do ✅
- Use provided templates
- Add screenshots for visual bugs
- Reference related issues with `#issueNumber`
- Update status regularly
- Comment on blockers or difficulties
- Close issue when completed

### Avoid ❌
- Vague titles ("it doesn't work")
- Overly broad issues (break them down)
- Assignment without consulting the person
- Modifying labels without authorization
- Leaving issues open indefinitely
- Duplicating existing issues

### Communication
- Use `@mention` to notify
- Comment before changing assignment
- Document important decisions
- Link to relevant documentation

## 📊 Metrics and Tracking

### Contoso KPIs
- Average resolution time by priority
- Bug/feature ratio
- Issue reopening rate
- Team satisfaction (monthly survey)

### Automated Reports
- Weekly tracking dashboard
- Alerts for unassigned critical issues
- Monthly performance report by team

---

## 📞 Support and Questions

For any questions about these conventions:
- **Slack**: #github-support
- **Email**: devops@contoso.com
- **Wiki**: [Link to complete documentation]

**Version**: 1.2  
**Last updated**: December 2024  
**Owner**: Contoso DevOps Team  

---
*This document is a living standard, regularly updated based on team feedback.*