Set obj = CreateObject("Scripting.FileSystemObject") 'Calls the File System Object
Const TemporaryFolder = 2
Dim tempFolder: tempFolder= obj.GetSpecialFolder(TemporaryFolder)
'WScript.CreateObject("Scripting.FileSystemObject").GetSpecialFolder(2)
fullPath=obj.BuildPath(tempfolder,"NextSom/settingsFile.txt")
if obj.FileExists(fullPath) then
    obj.DeleteFile(fullPath) 'Deletes the file throught the DeleteFile function
End if