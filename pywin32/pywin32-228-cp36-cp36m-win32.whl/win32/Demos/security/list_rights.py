import win32security,win32file,win32api,ntsecuritycon,win32con
from security_enums import TRUSTEE_TYPE,TRUSTEE_FORM,ACE_FLAGS,ACCESS_MODE

new_privs = ((win32security.LookupPrivilegeValue('',ntsecuritycon.SE_SECURITY_NAME),win32con.SE_PRIVILEGE_ENABLED),
             (win32security.LookupPrivilegeValue('',ntsecuritycon.SE_CREATE_PERMANENT_NAME),win32con.SE_PRIVILEGE_ENABLED),
             (win32security.LookupPrivilegeValue('','SeEnableDelegationPrivilege'),win32con.SE_PRIVILEGE_ENABLED) ##doesn't seem to be in ntsecuritycon.py ?
            )

ph = win32api.GetCurrentProcess()
th = win32security.OpenProcessToken(ph,win32security.TOKEN_ALL_ACCESS)  ##win32con.TOKEN_ADJUST_PRIVILEGES)
win32security.AdjustTokenPrivileges(th,0,new_privs)

policy_handle = win32security.GetPolicyHandle('',win32security.POLICY_ALL_ACCESS)

sidlist=win32security.LsaEnumerateAccountsWithUserRight(policy_handle,ntsecuritycon.SE_RESTORE_NAME)
for sid in sidlist:
    print(win32security.LookupAccountSid('',sid))

win32security.LsaClose(policy_handle)

