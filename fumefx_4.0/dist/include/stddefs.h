//-----------------------------------------------------------------------------------------
//
//			This file is copyright 2006-2013 by Sitni Sati d.o.o., Zagreb, Croatia
//		Unathorized viewving, usage, copying and reproduction is strictly prohibited
//
//									www.afterworks.com
//-----------------------------------------------------------------------------------------


#include "vfTypes.h"

#ifndef _STDDEFS_H_
#define _STDDEFS_H_

#ifdef _MSC_VER

 #ifndef IMPORTING_DLL
  #define VFDLLEXPORT __declspec(dllexport)
 #else
  #define VFDLLEXPORT __declspec(dllimport)
 #endif

 #define VFDLLLOCAL
#else
// #define VFDLLEXPORT __attribute__ ((visibility("default")))
 //#define VFDLLLOCAL __attribute__ ((visibility("hidden")))
#endif

	#ifndef vfmax
	#define vfmax(a,b)            (((a) > (b)) ? (a) : (b))
	#endif

	#ifndef vfmin
	#define vfmin(a,b)            (((a) < (b)) ? (a) : (b))
	#endif

#ifndef WIN32
 DWORD timeGetTime();
#endif

#endif
