//-----------------------------------------------------------------------------------------
//
//			This file is copyright 2006-2013 by Sitni Sati d.o.o., Zagreb, Croatia
//		Unathorized viewing, usage, copying and reproduction is strictly prohibited
//			Redistribution of header files is not allowed under any circumstances.
//	Redistribution of library (dll) files is allowed only by written permission from Sitni Sati d.o.o.
//
//									www.afterworks.com
//-----------------------------------------------------------------------------------------


#ifndef __FFXSHADE_DATA__
#define __FFXSHADE_DATA__

#include "SDMath.h"
#include "SDPoint3.h"
#include "SDColor.h"

// Shader requirements
// ---------------------------------------------------------------------------------- //
#define FFXSHADER_REQ_FIRE		(1<<1)
#define FFXSHADER_REQ_DENS		(1<<2)
#define FFXSHADER_REQ_TEMP		(1<<3)
#define FFXSHADER_REQ_VEL		(1<<4)
#define FFXSHADER_REQ_TEX		(1<<5)
#define FFXSHADER_REQ_VORT		(1<<6)
#define FFXSHADER_REQ_FLAGS		(1<<7)
#define FFXSHADER_REQ_LEECH		(1<<8)
#define FFXSHADER_REQ_EXPORT	(1<<10)
#define FFXSHADER_REQ_COLOR		(1<<11)

// Passed between FumeFX & Shader, FumeFX and Smoke
// ---------------------------------------------------------------------------------- //
enum { fxsd_Vpt, fxsd_MS, fxsd_IM, fxsd_Arnie };

//x initialize with -10000, so that shader can easily know if FM data was present or not
#define FM_notpresent -10000


class FXFastShadeData {

public:

	void Reset(void){
		//if false, then shader need to return only resultCol/Opac
		//and not all components
		requireall=FALSE;

		//if shader didn't do anything, set this to false so that FFX can skip computations
		isempty=FALSE;

		fuelCol=fireCol=smokeCol=resultCol=SDColor(0,0,0);
		fuelOpac=fireOpac=smokeOpac=resultOpac=0.0f;
	}

	FXFastShadeData() { Reset(); }

	//input
	BOOL requireall;

	//output
	BOOL  isempty;

	SDColor fuelCol, fireCol, smokeCol, resultCol;
	float fuelOpac, fireOpac, smokeOpac, resultOpac;

};


class FXShadeData {

public:

	ShadeContext *origsc;

	FXShadeData(){
		type=fxsd_MS;
		origsc=NULL;
		UseIllumMap=FALSE;
		thisFire=thisRo=thisT=thisVort=ds=0.0f;
		thisFlags = 0;
		tVel=SDPoint3(0,0,0);
		texCoords=texCoordsb=SDPoint3(FM_notpresent,0,0);
		phasea=phaseb=0.0f;
		LightMapColor=SDColor(0,0,0);
		GIColor=SDColor(0,0,0);
		thisColor=SDColor(1,1,1);
		fallofStrength = 0.0f;
	}

	//Type of FXShadeData: could be for Viewport, Illumiation Map
	BOOL type, separateAlpha;

	// if users have selected 'Use Illumination Map', UseIllumMap=TRUE and
	// LightMapColor will contain interpolated color (sum of all calls to the Illuminate())
	BOOL  UseIllumMap;
	SDColor LightMapColor;
	SDColor GIColor;

	// Interpolated sim data values. ds is a rendering stride
	float thisFire, thisRo, thisT, thisVort, ds;
	SDColor thisColor;
	UINT thisFlags;
	SDPoint3 tVel; //velocity in world coordinates
	SDPoint3 texCoords, texCoordsb ; //Propagated coorinates, in local FFX coordinates
	float phasea, phaseb;

	float zdist; //positive distance from p0
	float fallofStrength;//computed falloff from the FFX UI
};

#endif
