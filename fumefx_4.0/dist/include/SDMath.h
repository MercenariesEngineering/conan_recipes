//-----------------------------------------------------------------------------------------
//
//			This file is copyright 2006-2013 by Sitni Sati d.o.o., Zagreb, Croatia
//		Unathorized viewing, usage, copying and reproduction is strictly prohibited
//			Redistribution of header files is not allowed under any circumstances.
//	Redistribution of library (dll) files is allowed only by written permission from Sitni Sati d.o.o.
//
//									www.afterworks.com
//-----------------------------------------------------------------------------------------


#ifndef SDMATH
#define SDMATH

#include "stdafx.h"
#include "vfTypes.h"

#include <string.h>

#include "SDPoint3.h"
#include "limits.h"


#ifndef SmokeExport
#ifdef WIN32

   #ifdef  BUILD_SD
	#define SmokeExport __declspec( dllexport )
   #else
	#define SmokeExport __declspec( dllimport )
   #endif

#else
   #ifdef  BUILD_SD
	#define SmokeExport __attribute__ ((visibility ("default")))
   #else
	#define SmokeExport __attribute__ ((visibility("hidden")))
   #endif

#endif
#endif



class SDRay {
	public:
	SDPoint3 p, dir;
};

class SDMatrix3;
class SDMatrix4;

class SDBox {

	public:
	SDPoint3 pmin, pmax;

	void Init(){
		pmin.x=pmin.y=pmin.z = FLT_MAX;
		pmax.x=pmax.y=pmax.z = FLT_MIN;
	}
	SDBox () { 
		pmin.x=pmin.y=pmin.z = FLT_MAX;
		pmax.x=pmax.y=pmax.z = FLT_MIN;
	}
	SDBox (SDPoint3 _pmin, SDPoint3 _pmax){
			pmin = _pmin;
			pmax = _pmax;
	}

	int IsEmpty() const { 
		if (pmin.x>pmax.x) return 1;
		if (pmin.y>pmax.y) return 1;
		if (pmin.z>pmax.z) return 1;
		return 0;
	}


	SDPoint3 Center() const { return 0.5f*(pmin+pmax); }

	void EnlargeBy(float val){
		pmin.x-=val;
		pmin.y-=val;
		pmin.z-=val;

		pmax.x+=val;
		pmax.y+=val;
		pmax.z+=val;
	}

	void Scale(float s) { // scale box about center
		SDPoint3 c = Center();
		pmin = (pmin-c)*s + c;
		pmax = (pmax-c)*s + c;
	}

	inline SDBox& operator+=(const SDPoint3& p);
	inline SDBox& operator+=(const SDBox& b);
	inline SDBox operator*(const SDMatrix3 &m) const;
	inline SDPoint3 operator[] (int i) const;
};

//Flags
#define POS_IDENT  1
#define ROT_IDENT  2
#define SCL_IDENT  4
#define MAT_IDENT (POS_IDENT|ROT_IDENT|SCL_IDENT)

/*! 
 VoxelFlow's 4x3 transformation matrix
*/
class SDMatrix3 {

	public:

	float data[12];
	DWORD flags;

	///
	/// Constructor
	///
	SDMatrix3() { memset(data,0,sizeof(float)*12); flags = 0; };
	
	SDMatrix3(const float val){
		memset(data,0,sizeof(float)*12);
		data[0]=val;
		data[4]=val;
		data[8]=val;
		flags = 0;
	}
	
	SDMatrix3(const SDMatrix4 &m);

	SmokeExport SDMatrix3(const SDPoint3 &r1, const SDPoint3 &r2, const SDPoint3 &r3, const SDPoint3 &r4);
	
	void IdentityMatrix(){
		memset(data, 0, sizeof(float)*12);
		data[0]=1.f;
		data[4]=1.f;
		data[8]=1.f;
	}

	///
	/// Performs point transformation
	///
	SDPoint3 operator*(SDPoint3 &p)
	{

		float x = p.x*data[0] + p.y*data[3] + p.z*data[6] + data[9];
		float y = p.x*data[1] + p.y*data[4] + p.z*data[7] + data[10];
		float z = p.x*data[2] + p.y*data[5] + p.z*data[8] + data[11];

		return SDPoint3(x,y,z);
	}

	SDPoint3 operator*(const SDPoint3 &p) const
	{

		float x = p.x*data[0] + p.y*data[3] + p.z*data[6] + data[9];
		float y = p.x*data[1] + p.y*data[4] + p.z*data[7] + data[10];
		float z = p.x*data[2] + p.y*data[5] + p.z*data[8] + data[11];

		return SDPoint3(x,y,z);
	}


	inline SDMatrix3 operator*(const SDMatrix3& b) const;

	///
	/// Performs point transformation
	///
	SDPoint3 PointTransform(const SDPoint3 &p) const
	{
		float x = p.x*data[0] + p.y*data[3] + p.z*data[6] + data[9];
		float y = p.x*data[1] + p.y*data[4] + p.z*data[7] + data[10];
		float z = p.x*data[2] + p.y*data[5] + p.z*data[8] + data[11];
		return SDPoint3(x,y,z);
	}

	SDPoint3 VectorTransform(const SDPoint3 &p) const
	{
		float x = p.x*data[0] + p.y*data[3] + p.z*data[6];
		float y = p.x*data[1] + p.y*data[4] + p.z*data[7];
		float z = p.x*data[2] + p.y*data[5] + p.z*data[8];
		return SDPoint3(x,y,z);
	}


	/*
	SDPoint3 operator* (const SDMatrix3& M, const SDPoint3& p) 
	{
		float x = p.x*data[0] + p.y*data[3] + p.z*data[6] + data[9];
		float y = p.x*data[1] + p.y*data[4] + p.z*data[7] + data[10];
		float z = p.x*data[2] + p.y*data[5] + p.z*data[8] + data[11];

		return SDPoint3(x,y,z);
	}


	SDPoint3 operator* (const SDPoint3& p, const SDMatrix3& M) 
	{		
	   	float x = p.x*data[0] + p.y*data[3] + p.z*data[6] + data[9];
		float y = p.x*data[1] + p.y*data[4] + p.z*data[7] + data[10];
		float z = p.x*data[2] + p.y*data[5] + p.z*data[8] + data[11];

		return SDPoint3(x,y,z);
	}
*/
	float operator[](int i) const { return data[i]; }
	SmokeExport SDPoint3 GetRow(int i) const;
	SmokeExport void SetRow(int i, const SDPoint3 &r);

	SmokeExport SDPoint3 GetColumn3(int i) const;

	SmokeExport void Scale(const SDPoint3 &s, bool trans = false);
	SmokeExport void Translate(const SDPoint3 &t);

	SmokeExport int Equals(const SDMatrix3& M, float epsilon = 1.0E-6f) const;
};


inline SDMatrix3 SDMatrix3::operator*(const SDMatrix3& b)const{

		SDMatrix3 res;
		const float *bdata = &(b.data[0]);

		res.data[0] = data[0]*bdata[0] + data[1]*bdata[3] + data[2]*bdata[6];
		res.data[1] = data[0]*bdata[1] + data[1]*bdata[4] + data[2]*bdata[7];
		res.data[2] = data[0]*bdata[2] + data[1]*bdata[5] + data[2]*bdata[8];

		res.data[3] = data[3]*bdata[0] + data[4]*bdata[3] + data[5]*bdata[6];
		res.data[4] = data[3]*bdata[1] + data[4]*bdata[4] + data[5]*bdata[7];
		res.data[5] = data[3]*bdata[2] + data[4]*bdata[5] + data[5]*bdata[8];

		res.data[6] = data[6]*bdata[0] + data[7]*bdata[3] + data[8]*bdata[6];
		res.data[7] = data[6]*bdata[1] + data[7]*bdata[4] + data[8]*bdata[7];
		res.data[8] = data[6]*bdata[2] + data[7]*bdata[5] + data[8]*bdata[8];

		res.data[9]  = data[9]*bdata[0] + data[10]*bdata[3] + data[11]*bdata[6] + bdata[9];
		res.data[10] = data[9]*bdata[1] + data[10]*bdata[4] + data[11]*bdata[7] + bdata[10];
		res.data[11] = data[9]*bdata[2] + data[10]*bdata[5] + data[11]*bdata[8] + bdata[11];

		return res;	
}

inline SDPoint3 operator*(const SDPoint3 &p, const SDMatrix3 &m) {
	//if ((m.flags&MAT_IDENT)==MAT_IDENT) return p;

	return SDPoint3(
		p.x * m.data[0] + p.y * m.data[3] + p.z * m.data[6] + m.data[9 ],
		p.x * m.data[1] + p.y * m.data[4] + p.z * m.data[7] + m.data[10],
		p.x * m.data[2] + p.y * m.data[5] + p.z * m.data[8] + m.data[11]
	);
}



typedef int TimeValue; //< Used to represent time in 3ds max and in VoxelFlow

SmokeExport SDMatrix3 Inverse(const SDMatrix3 &m);
SDPoint3 VectorTransform(const SDMatrix3 &m, const SDPoint3 &p);
SDPoint3 VectorTransform(const SDPoint3 &p, const SDMatrix3 &m);

inline SDBox& SDBox::operator+=(const SDPoint3& p) {
	if (IsEmpty()) {
		pmin.x = p.x;
		pmin.y = p.y;
		pmin.z = p.z;
		pmax.x = p.x + FLT_EPSILON;
		pmax.y = p.y + FLT_EPSILON;
		pmax.z = p.z + FLT_EPSILON;
	}
	else {
		if (pmin.x>p.x) pmin.x = p.x;
		if (pmin.y>p.y) pmin.y = p.y;
		if (pmin.z>p.z) pmin.z = p.z;

		if (pmax.x<p.x) pmax.x = p.x;
		if (pmax.y<p.y) pmax.y = p.y;
		if (pmax.z<p.z) pmax.z = p.z;
	}

	return *this;
}

inline SDBox& SDBox::operator+=(const SDBox& b) {
	if (IsEmpty()) {
		pmin.x = b.pmin.x;
		pmin.y = b.pmin.y;
		pmin.z = b.pmin.z;
		pmax.x = b.pmax.x + FLT_EPSILON;
		pmax.y = b.pmax.y + FLT_EPSILON;
		pmax.z = b.pmax.z + FLT_EPSILON;
	}
	else {
		if (pmin.x>b.pmin.x) pmin.x = b.pmin.x;
		if (pmin.y>b.pmin.y) pmin.y = b.pmin.y;
		if (pmin.z>b.pmin.z) pmin.z = b.pmin.z;

		if (pmax.x<b.pmax.x) pmax.x = b.pmax.x;
		if (pmax.y<b.pmax.y) pmax.y = b.pmax.y;
		if (pmax.z<b.pmax.z) pmax.z = b.pmax.z;
	}

	return *this;
}
	
inline SDPoint3 SDBox::operator[] (int i) const {	 
	return SDPoint3((i&1)? pmax.x : pmin.x, (i&2)? pmax.y : pmin.y ,(i&4)? pmax.z : pmin.z);
}


inline SDBox SDBox::operator*(const SDMatrix3& tm) const {

	SDBox box;	
	box += tm * (operator[](0));
	box += tm * (operator[](1));
	box += tm * (operator[](2));
	box += tm * (operator[](3));
	box += tm * (operator[](4));
	box += tm * (operator[](5));
	box += tm * (operator[](6));
	box += tm * (operator[](7));

	return box;
}

#endif
