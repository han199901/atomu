#include <stdio.h>
#include <windows.h>
#include <Shlwapi.h>

int wmain(int argc, wchar_t *argv[])
{
	WCHAR path[MAX_PATH + 1];
	WCHAR gtkpath[MAX_PATH + 1];
	WCHAR exepath[MAX_PATH + 1];

	HMODULE hModule = GetModuleHandleW(NULL);
	GetModuleFileNameW(hModule, path, MAX_PATH);
	PathRemoveFileSpecW(path);

	snwprintf(gtkpath, MAX_PATH + 1, L"%ls%ls", path, L"\\bin");
	SetDllDirectoryW(gtkpath);
	
	snwprintf(exepath, MAX_PATH + 1, L"%ls%ls", path, L"\\bin\\atomudesktop.exe");

	
	SHELLEXECUTEINFOW ShExecInfo = {0};
	ShExecInfo.cbSize = sizeof(SHELLEXECUTEINFOW);
	ShExecInfo.fMask = SEE_MASK_DEFAULT;
	ShExecInfo.hwnd = NULL;
	ShExecInfo.lpVerb = NULL;
	ShExecInfo.lpFile = exepath;        
	ShExecInfo.lpParameters = NULL;   
	ShExecInfo.lpDirectory = path;
	if (argc > 1 && wcscmp(argv[1], L"-debug") == 0)
		ShExecInfo.nShow = SW_SHOW;
	else
		ShExecInfo.nShow = SW_HIDE;
	ShExecInfo.hInstApp = NULL; 
	ShellExecuteExW(&ShExecInfo);
	return 0;
}
