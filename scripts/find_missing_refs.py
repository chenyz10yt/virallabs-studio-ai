import re, os, sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

missing_ids = [
    'categoryTabs', 'chatMessagesBox', 'chatReplyInput', 'chatTargetPlatform',
    'chkMultiCustom', 'chkMultiFb', 'chkMultiKick', 'chkMultiTiktok', 'chkMultiTw', 'chkMultiYt',
    'connectedDevicesDisplay', 'cycleCountBadge', 'cycleElapsedPercent',
    'monetizationGoalText', 'monetizationTotalBar', 'monitorModeBadge',
    'panelCustom', 'panelFacebook', 'panelKick', 'panelMultistream', 'panelTiktok', 'panelTwitch', 'panelYoutube',
    'playlistContainer', 'telemetryBitrate', 'terminalLogs', 'testFeedbackBox', 'toast', 'btnPopoutYtChat'
]

lines = content.splitlines()
for mid in missing_ids:
    refs = [f"L{idx+1}: {l.strip()[:90]}" for idx, l in enumerate(lines) if mid in l]
    print(f"\n[{mid}] -> {len(refs)} matches:")
    for r in refs[:3]:
        print("  ", r)
