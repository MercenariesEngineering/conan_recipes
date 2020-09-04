//-----------------------------------------------------------------------------------------
//
//			This file is copyright 2006-2013 by Sitni Sati d.o.o., Zagreb, Croatia
//		Unathorized viewving, usage, copying and reproduction is strictly prohibited
//
//									www.afterworks.com
//-----------------------------------------------------------------------------------------

#ifndef SD_COLOR
#define SD_COLOR


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

class SDColor {
	public:
	float r,g,b;
	SDColor() {r = g = b = 0; };
	SDColor(float r, float g, float b) { this->r = r; this->g = g; this->b = b; };
//	BOOL operator==(SDColor &c) { return ((r == c.r) && (g == c.g) && (b == c.b)); };
	
	void ClampMax() { r = r>1.0f ? 1.0f : r;  g = g>1.0f ? 1.0f : g; b = b>1.0f ? 1.0f : b; }
	void ClampMinMax() { r = (r>1.0f) ? 1.0f : (r<0.0f) ? 0.0f : r; g = (g>1.0f) ? 1.0f : (g<0.0f) ? 0.0f : g; b = (b>1.0f) ? 1.0f : (b<0.0f) ? 0.0f : b; }

	
	inline SDColor operator+(const SDColor&) const;
	inline SDColor operator-(const SDColor&) const;
	inline SDColor operator*(const SDColor&) const;	

	inline SDColor& operator+=(const SDColor&);
	inline SDColor& operator*=(const float); 
	inline SDColor& operator*=(const SDColor&);	// element-by-element multiply.

	SmokeExport static const SDColor White;
	SmokeExport static const SDColor Black;
	SmokeExport static const SDColor Red;
	SmokeExport static const SDColor Green;
	SmokeExport static const SDColor Blue;
};

inline float Intens(const SDColor &col) {  return (col.r+col.g+col.b)/3.0f; }


inline SDColor SDColor::operator+(const SDColor& c) const{
	return (SDColor(r+c.r,g+c.g,b+c.b));
}


inline SDColor SDColor::operator-(const SDColor& c) const{
	return (SDColor(r-c.r,g-c.g,b-c.b));
}

inline SDColor SDColor::operator*(const SDColor& c) const{
	return (SDColor(r*c.r,g*c.g,b*c.b));
}


inline SDColor& SDColor::operator+=(const SDColor& a) {
	r += a.r;	g += a.g;	b += a.b;
	return *this;
}

inline SDColor& SDColor::operator*=(const float f) {
	r *= f;   g *= f;	b *= f;
	return *this;
}

inline SDColor& SDColor::operator*=(const SDColor& a) { 
	r *= a.r;	g *= a.g;	b *= a.b;	
	return *this; 
}


inline SDColor operator*( float f, const SDColor& a) {
	return(SDColor(a.r*f, a.g*f, a.b*f));
}

inline SDColor operator*( const SDColor& a, const float f) {
	return (SDColor(a.r*f, a.g*f, a.b*f));
}

inline float FLength(const SDColor& v) { return sqrtf(v.r*v.r + v.g*v.g + v.b*v.b); }



#endif
