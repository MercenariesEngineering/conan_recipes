//-----------------------------------------------------------------------------------------
//
//			This file is copyright 2006-2013 by Sitni Sati d.o.o., Zagreb, Croatia
//		Unathorized viewing, usage, copying and reproduction is strictly prohibited
//			Redistribution of header files is not allowed under any circumstances.
//	Redistribution of library (dll) files is allowed only by written permission from Sitni Sati d.o.o.
//
//									www.afterworks.com
//-----------------------------------------------------------------------------------------

#pragma once

#ifndef WIN32
	#include "stddefs.h"
#endif


#ifdef WIN32
	#include "tchar.h"
	#include "windows.h"
#endif

#include "stdio.h"
#include "assert.h"
#include "math.h"
#include "float.h"
#include "limits.h"


#ifdef WIN32
#include <windows.h>
#endif

// Some standard library includes
#include <stdlib.h>
#include <stdio.h>

class INode;
class ShadeContext;
#include "SDMath.h"

TCHAR *GetString(int id);

