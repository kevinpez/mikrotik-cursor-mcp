# 🧠 Intelligent Workflow - Complete Flow Diagram

## **User Request Flow**

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER REQUEST                                │
│  "Add firewall rule to block 192.168.99.0/24"                 │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│              INTELLIGENT WORKFLOW MANAGER                      │
│  • Receives user request                                       │
│  • Parses command                                              │
│  • Initiates risk assessment                                   │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                RISK ASSESSMENT ENGINE                          │
│  • Pattern matching against 50+ command patterns              │
│  • Classifies into LOW/MEDIUM/HIGH/CRITICAL                   │
│  • Generates specific warnings                                 │
│  • Determines safety requirements                              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────▼────────┐        ┌────────▼────────┐
│   LOW RISK     │        │   HIGH RISK     │
│   PATH         │        │   PATH          │
└───────┬────────┘        └────────┬────────┘
        │                           │
        ▼                           ▼
┌───────────────┐        ┌─────────────────┐
│ DIRECT EXEC   │        │ SAFETY WORKFLOW │
│               │        │                 │
│ 1. Execute    │        │ 1. Dry-run      │
│ 2. Check logs │        │ 2. User approval│
│ 3. Return     │        │ 3. Safe Mode    │
└───────────────┘        │ 4. Execute      │
                         │ 5. Monitor      │
                         │ 6. Verify       │
                         │ 7. Exit Safe    │
                         └─────────────────┘
```

## **Detailed High-Risk Workflow**

```
┌─────────────────────────────────────────────────────────────────┐
│                HIGH-RISK OPERATION WORKFLOW                    │
└─────────────────────────────────────────────────────────────────┘

1. RISK ASSESSMENT
   ↓
   • Pattern: /ip firewall filter add
   • Level: HIGH
   • Warnings: Network security impact
   • Safety: Safe Mode required
   ↓

2. DRY-RUN PREVIEW
   ↓
   🔍 DRY-RUN PREVIEW & APPROVAL REQUIRED
   
   Command: /ip firewall filter add chain=input src-address=192.168.99.0/24 action=drop
   
   Risk Assessment:
   - Level: HIGH
   - Impact: Network security changes
   
   Warnings:
   - ⚠️ This operation may affect network connectivity
   - ⚠️ Firewall rule addition may block legitimate traffic
   
   Safety Measures:
   - ✅ Safe Mode will be used
   - ✅ Log monitoring will be performed
   - ✅ Automatic rollback available
   
   To proceed, please approve this operation.
   ↓

3. USER APPROVAL
   ↓
   User: "Yes, I approve this firewall rule"
   ↓

4. SAFE MODE ENTRY
   ↓
   • Execute: /system safe-mode generic-timeout=15m
   • RouterOS enters Safe Mode
   • 15-minute timeout activated
   • All changes now temporary
   ↓

5. COMMAND EXECUTION
   ↓
   • Execute: /ip firewall filter add chain=input src-address=192.168.99.0/24 action=drop
   • RouterOS adds firewall rule
   • Rule is active but temporary
   ↓

6. LOG MONITORING
   ↓
   • Execute: /log print where time>"00:00:01"
   • Check for errors or warnings
   • Verify rule was added successfully
   ↓

7. STATE VERIFICATION
   ↓
   • Execute: /system resource print
   • Verify system is responsive
   • Check network connectivity
   ↓

8. SAFE MODE EXIT
   ↓
   • Execute: /system safe-mode
   • RouterOS exits Safe Mode
   • All changes become permanent
   ↓

9. COMPLETION REPORT
   ↓
   ✅ HIGH RISK OPERATION COMPLETED
   
   Command: /ip firewall filter add chain=input src-address=192.168.99.0/24 action=drop
   Result: [Firewall rule added successfully]
   Safe Mode: Used
   Logs Checked: Yes
   State Verified: Yes
```

## **Risk Level Decision Tree**

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMMAND INPUT                               │
│  "/system reboot"                                              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                PATTERN MATCHING                                │
│  • Check against LOW risk patterns (15 patterns)              │
│  • Check against MEDIUM risk patterns (12 patterns)           │
│  • Check against HIGH risk patterns (16 patterns)             │
│  • Check against CRITICAL risk patterns (11 patterns)         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────▼────────┐        ┌────────▼────────┐
│   NO MATCH     │        │   MATCH FOUND   │
│                │        │                 │
│ Default to     │        │ Use matched     │
│ MEDIUM risk    │        │ risk level      │
└────────────────┘        └─────────────────┘
```

## **Safety Integration Points**

```
┌─────────────────────────────────────────────────────────────────┐
│                SAFETY INTEGRATION                              │
└─────────────────────────────────────────────────────────────────┘

INTELLIGENT WORKFLOW
        │
        ├─── DRY-RUN MODE
        │    • Preview commands before execution
        │    • Show what would happen
        │    • No actual changes made
        │
        ├─── SAFE MODE
        │    • RouterOS native safe mode
        │    • Automatic rollback on timeout/disconnect
        │    • Temporary changes until committed
        │
        ├─── LOG MONITORING
        │    • Check system logs for errors
        │    • Verify operation success
        │    • Detect issues early
        │
        └─── STATE VERIFICATION
             • Verify system responsiveness
             • Check network connectivity
             • Confirm operation results
```

## **Error Handling & Rollback**

```
┌─────────────────────────────────────────────────────────────────┐
│                ERROR HANDLING FLOW                             │
└─────────────────────────────────────────────────────────────────┘

COMMAND EXECUTION
        │
        ├─── SUCCESS
        │    • Continue to monitoring
        │    • Verify state
        │    • Exit Safe Mode
        │
        └─── FAILURE
             │
             ├─── SAFE MODE ACTIVE
             │    • Automatic rollback triggered
             │    • Changes reverted automatically
             │    • Report rollback status
             │
             └─── NO SAFE MODE
                  • Report failure
                  • Suggest manual recovery
                  • Log error details
```

## **User Experience Flow**

```
┌─────────────────────────────────────────────────────────────────┐
│                USER EXPERIENCE                                 │
└─────────────────────────────────────────────────────────────────┘

USER REQUEST
    │
    ├─── LOW RISK
    │    • Immediate execution
    │    • Quick results
    │    • Minimal interaction
    │
    └─── HIGH RISK
         │
         ├─── PREVIEW PHASE
         │    • Show detailed preview
         │    • Explain risks and warnings
         │    • Request explicit approval
         │
         ├─── EXECUTION PHASE
         │    • Enter Safe Mode
         │    • Execute with monitoring
         │    • Real-time status updates
         │
         └─── COMPLETION PHASE
              • Verify results
              • Exit Safe Mode
              • Comprehensive report
```

This intelligent workflow ensures that every MikroTik operation gets the appropriate level of safety protection, automatically adapting to the risk level and providing a smooth, safe user experience.
