# Safe Testing Guide - v2.3.0 OpenVPN Development

**Branch:** `feature/v2.3.0-vpn-expansion`  
**Status:** Ready for testing  
**Safety:** ✅ Backup created (`pre-v2.3-development`)

---

## 🛡️ **SAFETY FIRST!**

### Pre-Testing Checklist

✅ **Backup Created:** `pre-v2.3-development.backup`  
✅ **Development Branch:** `feature/v2.3.0-vpn-expansion`  
✅ **Internet Working:** Verified (0% loss, 13ms)  
✅ **Code Committed:** Commit `35479db`

### How to Restore if Needed

```routeros
# If anything goes wrong:
/system backup load name=pre-v2.3-development.backup
# Router will reboot and restore to previous state
```

---

## 🔄 **RESTART CURSOR NOW**

**You MUST restart Cursor to load the new OpenVPN tools!**

1. Close Cursor completely
2. Reopen Cursor
3. Wait for MCP servers to load
4. Come back here to continue testing

---

## 🧪 **Testing Plan (After Restart)**

### Phase 1: READ-ONLY Tests (100% Safe) ✅

These commands only READ data - they CANNOT break your internet:

```python
# Test 1: List OpenVPN clients (safe - just reads config)
mikrotik_openvpn(action="list_openvpn_interfaces")
# Expected: Empty or list of existing OpenVPN clients

# Test 2: List OpenVPN servers (safe - just reads config)
mikrotik_openvpn(action="list_openvpn_servers")  
# Expected: Empty (unless you have OpenVPN configured)

# Test 3: Get server status (safe - just reads)
mikrotik_openvpn(action="get_openvpn_server_status")
# Expected: Server status or "not configured"
```

**Safety Level:** 🟢 **100% Safe** - These only READ, never WRITE

---

### Phase 2: CREATE Test (Careful - Creates NEW Interface)

**⚠️ This creates a NEW interface but doesn't touch existing ones:**

```python
# Test 4: Create test OpenVPN client (disabled by default)
mikrotik_openvpn(
    action="create_openvpn_client",
    name="ovpn-test-safe",
    connect_to="test.example.com",
    port=1194,
    comment="TEST ONLY - Safe to delete"
)
# This creates a NEW disabled interface - won't connect or affect internet
```

**Safety Level:** 🟡 **Mostly Safe** - Creates new interface but disabled

---

### Phase 3: VERIFY Creation (Safe)

```python
# Test 5: Verify test interface was created
mikrotik_openvpn(action="list_openvpn_interfaces")
# Should show: ovpn-test-safe (disabled)

# Test 6: Get status of test interface
mikrotik_openvpn(
    action="get_openvpn_status",
    name="ovpn-test-safe"
)
# Should show: configuration details
```

**Safety Level:** 🟢 **100% Safe** - Just reading

---

### Phase 4: CLEANUP Test (Safe - Removes Test Interface)

```python
# Test 7: Remove test interface
mikrotik_openvpn(
    action="remove_openvpn_interface",
    name="ovpn-test-safe"
)
# Removes only the test interface we created

# Test 8: Verify it's gone
mikrotik_openvpn(action="list_openvpn_interfaces")
# Should be empty again
```

**Safety Level:** 🟢 **Safe** - Only removes test interface

---

### Phase 5: Internet Connectivity Check

**After each test phase:**

```python
# Quick ping test
mikrotik_diagnostics(action="ping", address="8.8.8.8", count=4)
# Should always show 0% packet loss

# Or from Windows:
ping google.com
# Should always work
```

---

## ⚠️ **What NOT to Do During Testing**

❌ **DON'T** create OpenVPN on critical interfaces  
❌ **DON'T** modify ether1 (your WAN interface)  
❌ **DON'T** change existing firewall rules  
❌ **DON'T** disable bridgeLocal (your LAN)  
❌ **DON'T** modify existing routes  

---

## 🆘 **Emergency Recovery**

### If Internet Stops Working

**Option 1: Disable the test interface**
```python
mikrotik_openvpn(
    action="disable_openvpn_client",
    name="ovpn-test-safe"
)
```

**Option 2: Delete the test interface**
```python
mikrotik_openvpn(
    action="remove_openvpn_interface",
    name="ovpn-test-safe"
)
```

**Option 3: Restore from backup**
```python
mikrotik_backup(
    action="restore_backup",
    backup_name="pre-v2.3-development"
)
# Router will reboot to previous state
```

**Option 4: Via Winbox (if MCP fails)**
1. Open Winbox
2. Connect to 192.168.88.1
3. Interface → OVPN Client → Delete test interface
4. Or: System → Backup → Load `pre-v2.3-development`

---

## ✅ **Testing Checklist**

**Before Starting:**
- [ ] Cursor restarted
- [ ] MCP servers loaded
- [ ] Internet connectivity verified
- [ ] Backup confirmed created

**Phase 1 Tests (READ-ONLY):**
- [ ] list_openvpn_interfaces works
- [ ] list_openvpn_servers works
- [ ] get_openvpn_server_status works
- [ ] Internet still working ✅

**Phase 2 Tests (CREATE):**
- [ ] create_openvpn_client creates interface
- [ ] Interface is disabled by default
- [ ] Internet still working ✅

**Phase 3 Tests (VERIFY):**
- [ ] list shows new interface
- [ ] get_status shows details
- [ ] Internet still working ✅

**Phase 4 Tests (CLEANUP):**
- [ ] remove_openvpn_interface deletes interface
- [ ] list confirms it's gone
- [ ] Internet still working ✅

**Final Check:**
- [ ] All OpenVPN functions tested
- [ ] No errors encountered
- [ ] Internet never interrupted
- [ ] Router in clean state

---

## 📊 **What We're Testing**

**OpenVPN Functions (9 total):**
1. ✅ list_openvpn_interfaces - Safe
2. ✅ list_openvpn_servers - Safe
3. ✅ get_openvpn_server_status - Safe
4. ✅ create_openvpn_client - Test carefully
5. ✅ remove_openvpn_interface - Test carefully
6. ✅ update_openvpn_client - Test carefully
7. ✅ get_openvpn_status - Safe
8. ✅ enable_openvpn_client - Test carefully (won't connect if server doesn't exist)
9. ✅ disable_openvpn_client - Safe

---

## 🎯 **Expected Results**

**If successful:**
- All 9 OpenVPN functions work correctly
- No internet disruption
- Clean creation and deletion
- Ready to move to next feature (L2TP/IPSec)

**If issues:**
- Restore from backup
- Debug the problem
- Fix and retry
- Document any issues found

---

## 📝 **Current Status**

**Committed:** ✅ Yes (commit `35479db`)  
**Branch:** `feature/v2.3.0-vpn-expansion`  
**Backup:** `pre-v2.3-development.backup`  
**Next Step:** **→ RESTART CURSOR ←**

---

**After restart, say "ready to test" and we'll begin the safe testing sequence!** 🧪

