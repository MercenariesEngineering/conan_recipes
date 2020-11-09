//-----------------------------------------------------------------------------------------
//
//			This file is copyright 2006-2013 by Sitni Sati d.o.o., Zagreb, Croatia
//		Unathorized viewing, usage, copying and reproduction is strictly prohibited
//			Redistribution of header files is not allowed under any circumstances.
//	Redistribution of library (dll) files is allowed only by written permission from Sitni Sati d.o.o.
//
//									www.afterworks.com
//-----------------------------------------------------------------------------------------


#ifndef _VFTYPES_H_
#define _VFTYPES_H_


#ifndef WIN32

	#include <inttypes.h>
    #include "LinuxPorting.h"

__attribute__ ((visibility ("default")))
void splitpath( const char *path,char *drive, char *dir, char *fname, char *ext );

__attribute__ ((visibility ("default")))
void makepath( char *path,const char *drive, const char *dir, const char *fname, const char *ext);

    #ifndef  ZeroMemory
    # define ZeroMemory(loc, len)    memset(loc, 0, len)
    #endif

	typedef int BOOL;
/*
	#ifndef TRUE
       #define TRUE true
    #endif
    #ifndef FALSE
       #define FALSE false
    #endif
*/
	//odustajemo: typedef wchar_t TCHAR;
	typedef char TCHAR;

	#ifndef  WINAPI
    # define WINAPI      __stdcall
    #endif

    #ifndef CALLBACK
    # define CALLBACK    __stdcall
    #endif

//	#define MAX_PATH 2000
	#define _MAX_PATH 2000
	#define _MAX_DRIVE 1000
	#define _MAX_FNAME 1000
	#define _MAX_DIR 1000
	#define _MAX_EXT 100

	//NE smije #define MAX_PATH FILENAME_MAX // zbog http://www.delorie.com/gnu/docs/glibc/libc_652.html, Usage Note
/*	typedef unsigned int UINT;
	typedef unsigned long ULONG;
	typedef unsigned char BYTE;
	typedef unsigned long DWORD;
	typedef unsigned short WORD;*/


	//#define DWORD unsigned long
	typedef void VOID;
//	typedef long long __int64;

    #ifndef  _tfopen
	# define _tfopen(path,flags)    fopen(path, flags)
	#endif
	#define _T
	#define _tcscmp strcmp
	#ifndef  _tcslen
    # define _tcslen(a)                              strlen(a)
    #endif

	 class FFXWINDOW {
    public:
        Display *dpy;
        Window win;

        FFXWINDOW() { dpy = NULL; win = 0; }
        FFXWINDOW(Display *dpy, Window win) : dpy(dpy), win(win) {}

        bool operator!(void) { return ((!dpy) || (!win)); }
    };

    static const FFXWINDOW FFXNULLWINDOW(NULL, 0);

#else
	#include "stdafx.h"
	#include <Mmsystem.h>

	#ifndef M_PI
		#define M_PI 3.1415926525f
	#endif

   typedef HWND FFXWINDOW;
   static const FFXWINDOW FFXNULLWINDOW(NULL);

#endif

#endif
