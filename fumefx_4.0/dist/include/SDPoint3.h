//-----------------------------------------------------------------------------------------
//
//			This file is copyright 2006-2013 by Sitni Sati d.o.o., Zagreb, Croatia
//		Unathorized viewing, usage, copying and reproduction is strictly prohibited
//			Redistribution of header files is not allowed under any circumstances.
//	Redistribution of library (dll) files is allowed only by written permission from Sitni Sati d.o.o.
//
//									www.afterworks.com
//-----------------------------------------------------------------------------------------

#ifndef _SDPOINT3_H 

#define _SDPOINT3_H

#include <math.h>

#include "SDColor.h"


class SDIPoint3 {
public:
	int x,y,z;
 
	SDIPoint3() {}
	SDIPoint3(const int X) : x(X), y(X), z(X) {}
	SDIPoint3(const unsigned X, const unsigned Y, const unsigned Z) : x((int)X), y((int)Y), z((int)Z) {}
};

	 

/*! 
 VoxelFlow's Point3, holding x,y,z coordinates
*/

class SDPoint3 {
public:

	float x,y,z; ///< x,y,z coordinates of a point.

	///
	/// Constructor
	///
	SDPoint3(){}

	///
	/// Constructor. All x,y,z are set to the specified value 
	///
	SDPoint3(float X)  { x = y = z = X; }

	///
	/// Constructor. All x,y,z are set to the specified values 
	///
	SDPoint3(float X, float Y, float Z)  { x = X; y = Y; z = Z;  }
	SDPoint3(double X, double Y, double Z) { x = (float)X; y = (float)Y; z = (float)Z; }
	SDPoint3(int X, int Y, int Z) { x = (float)X; y = (float)Y; z = (float)Z; }
	SDPoint3(unsigned X, unsigned Y, unsigned Z) { x = (float)X; y = (float)Y; z = (float)Z; }

	///
	/// Constructor. All x,y,z are set to the specified point  
	///
	SDPoint3(const SDPoint3& a) { x = a.x; y = a.y; z = a.z; }
	SDPoint3(const SDColor& c) { x = c.r; y = c.g; z = c.b; }
	SDPoint3(float af[3]) { x = af[0]; y = af[1]; z = af[2]; }
    
	///
	/// Access [] operator
	///
	float& operator[](int i) { return (&x)[i]; }
	const float& operator[](int i) const { return (&x)[i]; }  

	// Conversion function
	operator float*() { return(&x); }

	// Unary operators
	SDPoint3 operator-() const { return(SDPoint3(-x,-y,-z)); } 
	SDPoint3 operator+() const { return *this; }
        
	///
	/// Returns a length of a vector
	///
    float Length() const;

	///
	/// Returns a squared length of a vector
	///
	float LengthSquared() const;

	///
	/// Normalizes a vector
	///
	SDPoint3 Normalize() const;    
       
	///
	/// Assignment
	///
	inline SDPoint3& operator+=(const SDPoint3&);
	inline SDPoint3& operator-=(const SDPoint3&);	
	inline SDPoint3& operator*=(float); 
	inline SDPoint3& operator/=(float);
	inline SDPoint3& operator*=(const SDPoint3&);	// element-by-element multiply.

    inline SDPoint3& Set(float X, float Y, float Z);

	// Test for equality
	int operator==(const SDPoint3& p) const { return ((p.x==x)&&(p.y==y)&&(p.z==z)); }
	int operator!=(const SDPoint3& p) const { return ((p.x!=x)||(p.y!=y)||(p.z!=z)); }
    int Equals(const SDPoint3& p, float epsilon = 1E-6f) const;

	// Binary operators
	inline  SDPoint3 operator+(const SDPoint3&) const;
	inline  SDPoint3 operator-(const SDPoint3&) const;
	inline  SDPoint3 operator*(const SDPoint3&) const;
	inline  SDPoint3 operator/(const SDPoint3&) const;
	inline  SDPoint3 operator^(const SDPoint3&) const;
	inline  float operator%(const SDPoint3&) const;
};

inline float Length(const SDPoint3&); 
inline float LengthSquared(const SDPoint3&); 

inline SDPoint3 CrossProd(const SDPoint3& a, const SDPoint3& b) {
	return(SDPoint3(a.y*b.z-a.z*b.y, a.z*b.x-a.x*b.z, a.x*b.y-a.y*b.x));
}

inline float DotProd(const SDPoint3 &a, const SDPoint3 &b) {
	return a.x*b.x + a.y*b.y + a.z*b.z;
}

// Inline
inline float SDPoint3::Length() const {	
	return (float)sqrt(x*x+y*y+z*z);
	}
	

inline float SDPoint3::LengthSquared() const {	
	return (x*x+y*y+z*z);
	}

inline SDPoint3 SDPoint3::Normalize() const
{	
	float v = sqrtf(x*x+y*y+z*z);

	if (v!=0.0f)
		return(*this/v); 
	else 
		return SDPoint3(1,0,0);
}

inline float Length(const SDPoint3& v) { return v.Length(); }
inline float FLength(const SDPoint3& v) { return v.Length(); }
inline float LengthSquared(const SDPoint3& v) { return v.LengthSquared(); }

inline  SDPoint3 SDPoint3::operator^(const SDPoint3& v) const { return CrossProd(*this, v); }

inline  float SDPoint3::operator%(const SDPoint3& v) const { return x*v.x + y*v.y + z*v.z; }

inline SDPoint3& SDPoint3::operator-=(const SDPoint3& a) { 
	x -= a.x;	y -= a.y;	z -= a.z; 
	return *this;
}

inline SDPoint3& SDPoint3::operator+=(const SDPoint3& a) {
	x += a.x;	y += a.y;	z += a.z;
	return *this;
}

inline SDPoint3& SDPoint3::operator*=(float f) {
	x *= f;   y *= f;	z *= f;
	return *this;
}

inline SDPoint3& SDPoint3::operator/=(float f) { 
	x /= f;	y /= f;	z /= f;	
	return *this; 
}

inline SDPoint3& SDPoint3::operator*=(const SDPoint3& a) { 
	x *= a.x;	y *= a.y;	z *= a.z;	
	return *this; 
}

inline SDPoint3 SDPoint3::operator-(const SDPoint3& b) const{
	return(SDPoint3(x-b.x,y-b.y,z-b.z));
}

inline SDPoint3 SDPoint3::operator+(const SDPoint3& b) const{
	return(SDPoint3(x+b.x,y+b.y,z+b.z));
}

inline SDPoint3 SDPoint3::operator/(const SDPoint3& b) const{
	return SDPoint3(x/b.x,y/b.y,z/b.z);
}

inline SDPoint3 SDPoint3::operator*(const SDPoint3& b) const{  
	return SDPoint3(x*b.x, y*b.y, z*b.z);	
}

//Global

inline SDPoint3 operator+(const SDPoint3& a, const float f) {
	return(SDPoint3(a.x+f, a.y+f, a.z+f));
}

inline SDPoint3 operator*(const float f, const SDPoint3& a) {
	return(SDPoint3(a.x*f, a.y*f, a.z*f));
}

inline SDPoint3 operator*(const SDPoint3& a, const float f) {
	return(SDPoint3(a.x*f, a.y*f, a.z*f));
}

inline SDPoint3 operator/(const SDPoint3& a, const float f) {
	return(SDPoint3(a.x/f, a.y/f, a.z/f));
}


inline float DotProd(SDPoint3& a, SDPoint3& b) { 
	return(a.x*b.x+a.y*b.y+a.z*b.z);	
}


#endif

