import os, sys

sys.stdout.reconfigure(encoding='utf-8')

tpl_path = r"C:\Users\Admin\Desktop\chenyz.app\panel_stream\templates\index.html"
with open(tpl_path, "r", encoding="utf-8") as f:
    html = f.read()

print("Contains btnCompileNow:", "btnCompileNow" in html)
print("Contains recordingLiveStatusBadge:", "recordingLiveStatusBadge" in html)
print("Contains recordingsFileList:", "recordingsFileList" in html)
print("Contains refreshRecordingsList:", "refreshRecordingsList" in html)
print("Contains compileAndDownloadMasterRecording:", "compileAndDownloadMasterRecording" in html)
print("Contains deleteRecordingFile:", "deleteRecordingFile" in html)
