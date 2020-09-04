//-----------------------------------------------------------------------------------------
//
//			This file is copyright 2006-2013 by Sitni Sati d.o.o., Zagreb, Croatia
//		Unathorized viewving, usage, copying and reproduction is strictly prohibited
//
//									www.afterworks.com
//-----------------------------------------------------------------------------------------

#ifndef __LINUX_PORTING_H__
#define __LINUX_PORTING_H__

//#define VF_TIME_SOLVER        // comment to supress timing output

#ifdef VF_TIME_SOLVER
    #define VF_TIMER_START(t)                               \
        SINGLE_THREAD_SECTION                               \
            t = timeGetTime();                              \
        END_SINGLE_THREAD_SECTION
#else
    #define VF_TIMER_START(t)
#endif

#ifdef VF_TIME_SOLVER
    #define VF_TIMER_STOP(t, file, str)                     \
        SINGLE_THREAD_SECTION                               \
            t = timeGetTime() - t;                          \
            if ((file!=NULL) && (str!=NULL))                \
                fprintf(file, str, t);                      \
        END_SINGLE_THREAD_SECTION
#else
    #define VF_TIMER_STOP(t, file, str)
#endif


#ifdef WIN32

#include "windows.h"
//Had to do it this way as wxWidgets can complain about Sleep() define
#define awSleep(a)                Sleep(a)
#define awstricmp(str1, str2)     _stricmp(str1, str2)
#define awRAND_MAX RAND_MAX

#else

#include <cstdlib>
#include <cstring>
#include <stdint.h>
#include <unistd.h>
#include <stdint.h>
#include <time.h>
#include <ctype.h>

#include <errno.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <sys/time.h>

#include <sys/ioctl.h>
#include <linux/hdreg.h>

#include <GL/glx.h>

#define INVALID_SOCKET  -1
#define SOCKET_ERROR    -1

#define WSACleanup()
#define closesocket(fd)     close(fd)

#define __stdcall               // xxx
#define __nullterminated        // xxx
#define __cdecl                 // xxx
#define __fastcall              // xxx

#define awRAND_MAX 0x7fff
//On Unix sleep() is in seconds !!!
#define awSleep(a)                   usleep(a*1000)
#define awstricmp(str1, str2)        strcasecmp(str1, str2)

//#define LINUX_LOG_FILE          "/home/kresimir/Desktop/maya.log"
#define LINUX_LOG_FILE          "/tmp/maya.log"
#define LINUX_TIME_FILE         "/home/kresimir/Desktop/times.csv"

typedef uint32_t                UINT32;
typedef uint64_t                UINT64;
typedef int64_t                 __int64;
typedef int64_t                 __time64_t;
typedef int32_t                 LONG;
typedef uint32_t                ULONG;
typedef int32_t                 BOOL;
typedef uint32_t                DWORD;
typedef unsigned char           BYTE;
typedef int16_t                 SHORT;
typedef uint16_t                WORD;
typedef char                    CHAR;
typedef intptr_t                INT_PTR;
typedef char                    TCHAR;
typedef __nullterminated CHAR   *LPSTR;
typedef __nullterminated const CHAR   *LPCSTR;
typedef LPCSTR                  LPTSTR;
typedef LPSTR                   LPCTSTR;
typedef uint32_t                UINT;
typedef uint64_t                ULONGLONG;
typedef void                    VOID;
typedef void                    *PVOID;
typedef void*                   LPVOID;
#if __WORDSIZE == 64
typedef unsigned long int       UINT_PTR;
#else  //__WORDSIZE
typedef unsigned long long int  UINT_PTR;
#endif //__WORDSIZE
typedef int64_t                 LONG_PTR;
//typedef UINT_PTR                WPARAM;
//typedef LONG_PTR                LPARAM;
//typedef LONG_PTR                LRESULT;
typedef struct sockaddr_in      SOCKADDR_IN;
typedef struct sockaddr         *LPSOCKADDR;
typedef struct tm               SYSTEMTIME;
typedef LONG                    HRESULT;
typedef void*                   LPPAINTSTRUCT;  // TODO: change this
typedef pthread_mutex_t         CRITICAL_SECTION;
typedef DWORD                   COLORREF;
typedef GLXContext              HGLRC;
typedef GLXDrawable             HDC;
typedef UINT_PTR                WPARAM;
typedef LONG_PTR                LPARAM;
typedef int64_t                 PAINTSTRUCT;

#ifndef  WINAPI
# define WINAPI      __stdcall
#endif

#ifndef CALLBACK
# define CALLBACK    __stdcall
#endif

typedef size_t SERVICE_STATUS_HANDLE;   // xxx
typedef size_t SERVICE_STATUS;   // xxx
#ifndef HWND
    #define HWND uintptr_t
#endif
typedef size_t HINSTANCE, SYSTEM_INFO, LPHOSTENT; // xxx

typedef int HANDLE;  // for file handling
typedef int SOCKET; // ok

typedef struct tagRECT {
    LONG    left;
    LONG    top;
    LONG    right;
    LONG    bottom;
} RECT, *PRECT, *NPRECT, *LPRECT;

#define _strtime(out) {time_t rawtime; time(&rawtime); strftime(out, 80, "%X", localtime(&rawtime));}
#define _strdate(out) {time_t rawtime; time(&rawtime); strftime(out, 80, "%x", localtime(&rawtime));}
#define _tzset()

#define __forceinline inline

#define MAX_PATH    2048    // xxx

#define INVALID_HANDLE_VALUE    -1    // OK

#ifndef TRUE
# define TRUE   1
# define FALSE  0
#endif

#define CW_USEDEFAULT   0

#define GENERIC_WRITE   O_WRONLY
#define GENERIC_READ    O_RDONLY
#define _O_RDONLY       O_RDONLY
#define _O_BINARY       0x0         // check
#define CREATE_ALWAYS   O_EXCL      // check
#define OPEN_ALWAYS     O_NONBLOCK  // check
#define OPEN_EXISTING   0x0         // check

static inline bool CreateDirectory(const char *path, void*) {
	mode_t dirPerm = umask(0);	// get mask (and put some other)
	umask(dirPerm);				// put mask back
	return !mkdir(path, 0777 ^ dirPerm);
}

static inline char* strupr(char* s) {
    char* p = s;
    while ((*p = toupper(*p))) p++;
    return s;
}

static inline char* strlwr(char* s) {
    char* p = s;
    while ((*p = tolower(*p))) p++;
    return s;
}

static inline void InitializeCriticalSection(CRITICAL_SECTION *cs) {
    pthread_mutexattr_t ma;
    pthread_mutexattr_settype(&ma, PTHREAD_MUTEX_RECURSIVE_NP);
    pthread_mutex_init(cs, &ma);
    pthread_mutexattr_destroy(&ma);
}

static inline void SetRect(LPRECT lprc, int xLeft, int yTop, int xRight, int yBottom) {
        lprc->left    = xLeft;
        lprc->right   = xRight;
        lprc->top     = yTop;
        lprc->bottom  = yBottom;
}


extern int32_t DestroyWindow(uintptr_t hwnd);

#define MessageBox(parent, msg, title, btn)     printf("[%s] %s\n", title, msg)        // TODO: change this
#define CreateFile(path, rw_f, a, b, opn_f, att_f, c)   open(path, rw_f | opn_f)
#define CreateDirectory(path,void)             (!mkdir(path,0755))
#define WriteFile(fd, ptr, size, out, p)       write(fd, ptr, size)
#define ReadFile(fd, ptr, size, out, a)        read(fd, ptr, size)
#define FlushFileBuffers(fd)                   //flush(fd)
#define CloseHandle(fd)                        close(fd)
#define MoveFile(from, to)                     rename(from, to)
#define _open(path, flags)                     open(path, flags)
#define _topen(path, flags)                    open(path, flags)
#ifndef  _tfopen
# define _tfopen(path,flags)                   fopen(path, flags)
#endif
#define _read(fd, buf, count)                  read(fd, buf, count)
#define _lseek(fd, offset, whence)             lseek(fd, offset, whence)
#define _close(fd)                             close(fd)
#ifndef  _tcslen
# define _tcslen(a)                             strlen(a)
#endif
#define _tsplitpath(path,drive,dir,name,ext)	splitpath(path,drive,dir,name,ext)
#define _tmakepath(path,drive,dir,name,ext)		makepath(path,drive,dir,name,ext)
#ifndef  _stprintf
# define _stprintf						        sprintf
#endif
#define _tcscpy(to,from)						strcpy(to,from)
#define _tcscat(to,from)						strcat(to,from)
#define _sntprintf snprintf
#define _tremove                                remove
#define _tcsupr(str)                            strupr(str)
#define _tcslwr(str)                            strlwr(str)
#define _tcsnccpy( str1, str2, len)             strncpy( str1, str2, len)
#define _tcstok( str1, str2)                    strtok( str1, str2)
#define _tcsnccmp( str1, str2, len)             strncmp( str1, str2, len)
#define _vsntprintf                             vsnprintf
#define LocalFree(loc)                          free(loc)
#define _tcsncpy(to, from, n)                   strncpy(to, from, n)
#define FAILED(x)                               ((x) < 0)
#define EnterCriticalSection(cs)                pthread_mutex_lock(cs)
#define LeaveCriticalSection(cs)                pthread_mutex_unlock(cs)
#define DeleteCriticalSection(cs)               pthread_mutex_destroy(cs)

/*
 * MessageBox() Flags
 */
#define MB_OK                       0x00000000L
#define MB_OKCANCEL                 0x00000001L
#define MB_ABORTRETRYIGNORE         0x00000002L
#define MB_YESNOCANCEL              0x00000003L
#define MB_YESNO                    0x00000004L
#define MB_RETRYCANCEL              0x00000005L
#define MB_CANCELTRYCONTINUE        0x00000006L

#define MB_ICONHAND                 0x00000010L
#define MB_ICONQUESTION             0x00000020L
#define MB_ICONEXCLAMATION          0x00000030L
#define MB_ICONASTERISK             0x00000040L

#define MB_USERICON                 0x00000080L
#define MB_ICONWARNING              MB_ICONEXCLAMATION
#define MB_ICONERROR                MB_ICONHAND


#define MB_ICONINFORMATION          MB_ICONASTERISK
#define MB_ICONSTOP                 MB_ICONHAND

/*
 * Dialog Box Command IDs
 */
#define IDOK                1
#define IDCANCEL            2
#define IDABORT             3
#define IDRETRY             4
#define IDIGNORE            5
#define IDYES               6
#define IDNO                7
#define IDCLOSE         8
#define IDHELP          9
#define IDTRYAGAIN      10
#define IDCONTINUE      11

//# define GetLastError()         (-1)
#define WSAGetLastError()      (-1)

// bitmaps
enum { BI_RGB=0, BI_RLE8=1, BI_RLE4=2, BI_BITFIELDS=3, BI_JPEG=4, BI_PNG=5 };

typedef DWORD FOURCC;

typedef struct tagRGBQUAD {
  BYTE rgbBlue;
  BYTE rgbGreen;
  BYTE rgbRed;
  BYTE rgbReserved;
} RGBQUAD;

typedef struct tagBITMAPINFOHEADER {
  DWORD biSize;
  LONG  biWidth;
  LONG  biHeight;
  WORD  biPlanes;
  WORD  biBitCount;
  DWORD biCompression;
  DWORD biSizeImage;
  LONG  biXPelsPerMeter;
  LONG  biYPelsPerMeter;
  DWORD biClrUsed;
  DWORD biClrImportant;
} BITMAPINFOHEADER, *PBITMAPINFOHEADER;

typedef struct tagBITMAPINFO {
  BITMAPINFOHEADER bmiHeader;
  RGBQUAD          bmiColors[1];
} BITMAPINFO, *PBITMAPINFO;

typedef PBITMAPINFO LPBITMAPINFO;

#pragma pack(1)
typedef struct tagBITMAPFILEHEADER {
  WORD  bfType;
  DWORD bfSize;
  WORD  bfReserved1;
  WORD  bfReserved2;
  DWORD bfOffBits;
} BITMAPFILEHEADER, *PBITMAPFILEHEADER;
#pragma pack()


///////THREADS////////
typedef struct
{
    pthread_mutex_t mtx;
    pthread_cond_t cond;
    bool manual_reset;
    bool signaled;
}THANDLE,*PHANDLE;

#define INFINITE            0xFFFFFFFF
#define WAIT_TIMEOUT        0x00000102L
#define WAIT_OBJECT_0       0
#define WAIT_ABANDONED_0    0x00000080L
#define WAIT_FAILED         ((DWORD)0xFFFFFFFF)

/*
PHANDLE CreateEvent(void *pSec,bool bManualReset,bool bInitialState,char *pStr);
void CloseHandle(PHANDLE handle);
//void CloseHandle(pthread_t *handle);
BOOL SetEvent(PHANDLE handle);
BOOL ResetEvent(PHANDLE handle);
DWORD WaitForSingleObject(PHANDLE handle,unsigned int timeout);
DWORD WaitForMultipleObjects(DWORD nCount, PHANDLE *lpHandles, BOOL bWaitAll, DWORD dwMilliseconds);
DWORD WaitForMultipleObjects(DWORD nCount, pthread_t *lpHandles, BOOL bWaitAll, DWORD dwMilliseconds);
*/
//#define CreateThread(pattribs, dwStackSize, startRoutine, param, creatFlags, thrID)   pthread_create()
#define ExitThread(exitCode)    pthread_exit(NULL)     // WARNING: radi ok samo za exicCode==0
DWORD WaitForMultipleObjects(DWORD nCount, pthread_t *lpHandles, BOOL bWaitAll, DWORD dwMilliseconds);


/////////////////////

#endif //WIN32

#ifdef WIN32
   #ifdef  BUILD_SD
	#define DLLExport __declspec( dllexport )
   #else
	#define DLLExport __declspec( dllimport )
   #endif
#else  //WIN32
   #ifdef  BUILD_SD
	#define DLLExport __attribute__ ((visibility ("default")))
   #else
	#define DLLExport __attribute__ ((visibility("hidden")))
   #endif
#endif //WIN32



#endif //__LINUX_PORTING_H__

