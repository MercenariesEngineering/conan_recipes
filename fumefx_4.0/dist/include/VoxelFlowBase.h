//-----------------------------------------------------------------------------------------
//
//			This file is copyright 2006-2013 by Sitni Sati d.o.o., Zagreb, Croatia
//		Unathorized viewing, usage, copying and reproduction is strictly prohibited
//			Redistribution of header files is not allowed under any circumstances.
//	Redistribution of library (dll) files is allowed only by written permission from Sitni Sati d.o.o.
//
//									www.afterworks.com
//-----------------------------------------------------------------------------------------

#include "vfTypes.h"
#include "float.h"
#include "SDPoint3.h"
#include "SDMath.h"
#include "SDColor.h"
#include "FXShadeData.h"

#include "stddefs.h"

#include <vector>

#ifndef VOXELFLOWBASE
#define VOXELFLOWBASE


#ifdef _MSC_VER
 #ifdef  BUILD_SD
	#define VFExport VFDLLEXPORT
 #else
	#define VFExport VFDLLLOCAL
 #endif
#else
	#define VFExport __attribute__ ((visibility("default")))
#endif

// What channels to use in simulation?
// ---------------------------------------------------------------------------------- //
const int SIM_USENONE	= 1<<0; ///<
const int SIM_USEFUEL	= 1<<1; ///< Simulate\load\save fuel
const int SIM_USETEMP	= 1<<2; ///< Simulate\load\save temperature
const int SIM_USEDENS	= 1<<3; ///< Simulate\load\save smoke
const int SIM_USETEXT	= 1<<4; ///< Simulate\load\save Fluid Mapping
const int SIM_USEVEL	= 1<<5; ///< Simulate\load\save velocities
const int SIM_USEFLAGS	= 1<<6; ///< Simulate\load\save voxel flags
const int SIM_USECOLOR	= 1<<7; ///< Simulate\load\save color

const int SIM_USEWT		= 1<<8; ///< Used just for Saving WT data - hfEnergy
const int SIM_TOTALCHANS = 8;

// Load sim / output error codes
// ---------------------------------------------------------------------------------- //
const int LOAD_OK				= 1<<0;	///< Loading ok
const int LOAD_USERCANCEL		= 1<<1; ///< Loading canceled
const int LOAD_FILEOPENERROR	= 1<<2;
const int LOAD_FILELOADERROR	= 1<<3;
const int LOAD_RAMERR			= 0;	//memory allocation error


class FXShadeData;
//!! for now
#ifndef miFALSE
	struct miColor{ float r, g, b, a; };
#endif

class shdParams_Standard {

public:

	int		renderReq;
	float	stepSizeSmoke;
	float	stepSizeFire;
	float	jittering;

//falloff map params
	int		falloff_Type;
	float	falloff_Strength;
	BOOL	falloff_useMap;

//separateAlpha
	BOOL	separateAlpha;

//fire
	BOOL	doFire;
	float   fireBrightness;
	float   fireOpacity;
	float	firefGImult;
	float	fireAlpha;

	BOOL	fireOpacMapUse;
	int		fireOpacMapCoords;
	float	fireOpacMapStren;

	int		fireColorSource; //0 - from gradient, 1 - from grid
	int		n_fireCol;	// number of color gradient samples
	miColor *fireColTable; //array of color for fire

	int		n_fireOpac;	// number of Bezier curve samples
	float   *fireOpacTable; //array of float for fire

//smoke
	BOOL	doSmoke;
	float	smokeMinDens;
	float	smokeMaxDens;
	SDColor	smokeAmbientCol;
	float   smokeOpacity; //aka denisty
	float   visFalloff;
	float   shadowFalloff;
	float	smokeGImult;
	BOOL	smokeCastShadows;
	BOOL	smokeRcvShadows;

	BOOL	smokeOpacMapUse;
	int		smokeOpacMapCoords;
	float	smokeOpacMapStren;

	int		smokeColorSource; //0 - from gradient, 1 - from grid
	int		n_smokeCol;	// number of samples
	miColor *smokeColTable; //array of color for smoke

	int		n_smokeOpac;	// number of samples
	float   *smokeOpacTable; //array of float for smoke

//fuel
	BOOL	doFuel;
	int		fuelColorSource; //0 - from gradient, 1 - from grid
	SDColor	fuelColor;
	float	fuelOpacity;
	float	fuelvisFalloff;
	float	fuelfGImult;
	BOOL	fuelCastShadows;
	BOOL	fuelRcvShadows;

//shadows
	float	shadowstepSize;
	float	shadowJittering;

//illumination map
	BOOL	im_doIlluminationMap;
	float	im_mapMultipler;
	BOOL	im_doDraftMap;
	float	im_colorThresh;
	BOOL	ms_doMultipleScattering;
	int		ms_maxDepth;
	float	ms_fireStrength;
	float	ms_smokeStrength;
	float	ms_falloff;
};


#ifndef WIN32
#define FFX_SRV_FIL_MR "/tmp/ffx_srv_file_mr"
#define FFX_CLI_FIL_MR "/tmp/ffx_cli_file_mr"
#endif


/*!
 FumeFX will pass this to SmokeDynamics for saving / loading
 NOT USED AT THE MOMENT !
*/

const int DATA_IN2=0x200;

class FumeFXSaveToFileData
{
	
public:
		SDMatrix3 tm; ///< FumeFX transformation matrix (object to world space).

		int type;	  /*!<   Retrieves the unit type in effect. This may be one of the following values:

							Supported unit types (3ds max defines):
							UNITS_INCHES
							UNITS_FEET
							UNITS_MILES
							UNITS_MILLIMETERS
							UNITS_CENTIMETERS
							UNITS_METERS
							UNITS_KILOMETERS
						*/

		float scale; /*!<	The master scale setting. This is the value the user entered in the
							1 Unit = XXX field of the 3ds max General Page in the Preference Settings dialog box.
					*/

		FumeFXSaveToFileData() { type=-1; scale=0.0f; }
};

// Structure for holding .fxd and .fdc data.
// Used internally
// ---------------------------------------------------------------------------------- //
struct SimulationHeader {
	//int _simFileVer;
	int frame;
	bool adaptive;
	float dx,lxmax,lymax,lzmax,lx,ly,lz;
	int nx,ny,nz,nx0,ny0,nz0,nxmax,nymax,nzmax;
	int loadedOutputVars;
};

//This class is an interface between VoxelFlow and texture map evaluation
class vfMapSampler {

public:

	int nMaps;
	SDPoint3 mapPt; // Sample point

	virtual BOOL isMapPresent(int i)=0;
	virtual SDColor Sample(int mapNum, SDPoint3 pos, BOOL needConvert)=0;
};

//This class is an interface between VoxelFlow and app defined lights
class vfLightSampler {

public:

	int nLights;
	virtual BOOL Illuminate(SDPoint3 lgtPt, int lightNum, SDColor &col, BOOL needShadows)=0;

};

class vfShader {

public:

	int renderReq;
	virtual BYTE IllumRequired(FXShadeData *input)=0;
	virtual void FastShade(FXShadeData &input, FXFastShadeData &data)=0;
};

//Render NSimBridge
class renderNSimBridge {

	float width,length,height;

public:

	int interpAxis;
	BOOL inverted;
	SDBox wbbox;

	void Init();

VFExport	float NSimBlendFactor(SDPoint3 wpt);

};

class VoxelFlowBase {

public:

// Dimensions - do not attempt to write to these vars !!
// ---------------------------------------------------------------------------------- //

	float	dx,idx;							// in generic units: voxel size and inverse (1/dx)

	// lx0	- beginning of adaptive zone (generic units)
	// lx	- dimension of adaptive zone (generic units)
	// lxmax - dimension of whole container (generic units)
	// lxmax >= lx0 + lx
	float	lx0, lx, lxmax;					///< Dimensions of adaptive grid in GENERIC UNITS
	float	ly0, ly, lymax;					///< Dimensions of adaptive grid in GENERIC UNITS
	float	lz0, lz, lzmax;					///< Dimensions of adaptive grid in GENERIC UNITS
	float	midx, midy, midz;				///< midx = lmax/2

	// nx0 - beginning of adaptive zone
	// nx - dimension of adaptive zone
	// nxmax - dimension of whole container
	// nxmax >= nx0 + nx
	int		nx0, nx, nxmax;					///< Dimensions of adaptive grid in VOXELS
	int		ny0, ny, nymax;					///< Dimensions of adaptive grid in VOXELS
	int		nz0, nz, nzmax;					///< Dimensions of adaptive grid in VOXELS
	int		nyz;							///< nyz=ny*nz
	unsigned int cells;						///< Current (total) number of voxels (nx*ny*nz)

	std::vector<renderNSimBridge*> rNSB;	///< NsimBridges for rendering. has only bbox and few flags

	float   phasetime,phasea, phaseb;			// Texture a and b phases, phasetime=itegral of time phase
												// Calculated internally
//IO
	int		loadedOutputVars;	///< After loading (output, sim or just header), you can check which channels are available in the output file

	///
	/// Saves output. can be called when the simulation step has finished.
	/// channels to export are determined from callback function ExportChannel
	/// SaveField _fieldID = the field ID that will be saved.
	/// FumeFXIO lib supports operation only on spare_field
	enum SaveField { sim_field=1, spare_field };
	VFExport virtual __int64 SaveOutput(TCHAR const fileName[MAX_PATH], int expChannels, FumeFXSaveToFileData &ffxdata, SaveField _fieldID = sim_field)=0;

	///
	/// Reset and Allocate and Initialize the grid with a loaded output.
	/// shaderReqs: shader requrements - channels that are needed for rendering;
	/// ffxChanReqs: channel requirements - all needed channels. shaderreqs must be a ssubset of chan. reqs.
	///
	VFExport virtual int LoadOutput	(TCHAR const fileName[MAX_PATH], FumeFXSaveToFileData &ffxdata, int shaderReqs, int ffxChanReqs, BOOL asSnapshot = FALSE)=0;

	///
	/// You can create grid of your dimensions. Before this call, you need to setup nx0, ny0, nz0, lx0, ly0,lz0
	///
	VFExport virtual void InitForOutput(int nxa, int nya, int nza, float lxa, float lya, float lza,float spacing,int outputVars)=0;

	///
	/// For reading grid dimensions, doesn't change the state of the smoke grid.
	///
	VFExport virtual int LoadSimHeader(TCHAR const fileName[MAX_PATH], FumeFXSaveToFileData &ffxdata, int &frame, BOOL &_adaptive,float &_dx, float &_lxmax, float &_lymax, float &_lzmax )=0;

	///
	/// Load simulation header (.fxd file) values directly into the grid. Used internally !
	///
	VFExport virtual int LoadHeader	(TCHAR * fname)=0;

	///
	/// Load simulation header(.fxd file) values into the SimulationHeader &sh.
	///
	VFExport virtual int LoadHeader	(TCHAR * fname, SimulationHeader &sh)=0;

	///
	/// Free all memory.
	///
	VFExport virtual void	Reset()=0;

	///
	/// Intersects the grid.  ray must be in local coordinates
	///
	VFExport virtual bool Intersect(float viewPoint[3], float direction[3], float &first, float &last)=0;


// Field access methods - by index
// pos (index) is calcualed as ((xcoord * ny + ycoord)*nz + zcoord), coords in voxels
// fields 2 are used for loading output (display, space warps)
// ---------------------------------------------------------------------------------- //
	VFExport virtual WORD GetF(int pos)=0;

	VFExport virtual float GetRo2(int pos)=0;
	VFExport virtual float GetFuel2(int pos)=0;
	VFExport virtual float GetTemp2(int pos)=0;
	VFExport virtual void GetColor2(int pos, SDColor &col)=0;
	VFExport virtual void GetVel2(int pos, float &vx, float &vy, float &vz)=0;
	VFExport virtual void GetVel2(int pos, SDPoint3 &point)=0;
	VFExport virtual void GetXYZ2(int pos, float &tx, float &ty, float &tz)=0;
	VFExport virtual void GetXYZ2(int pos, SDPoint3 &point)=0;

	VFExport virtual void SetRo2(int pos, float value)=0;
	VFExport virtual void SetFuel2(int pos, float value)=0;
	VFExport virtual void SetTemp2(int pos, float value)=0;
	VFExport virtual void SetColor2(int pos, SDColor &col)=0;
	VFExport virtual void SetVel2(int pos, float vx, float vy, float vz)=0;
	VFExport virtual void SetVel2(int pos, SDPoint3 &point)=0;
	VFExport virtual void SetXYZ2(int pos, float tx, float ty, float tz)=0;
	VFExport virtual void SetXYZ2(int pos, SDPoint3 &point)=0;


// Field get methods - by local coordinate - for RENDERING and SW's
// ---------------------------------------------------------------------------------- //
	VFExport virtual SDColor GetIMColor(float point[3], float *colR, float *colG, float *colB)=0;
	VFExport virtual SDPoint3 GetTexCoords(float point[3])=0;//,SDPoint3 &vel, BYTE &_f)
	VFExport virtual BOOL GetVel(float point[3], SDPoint3 &vel)=0;
	VFExport virtual BOOL GetVelRoFast(float point[3],SDPoint3 &vel, float &ro)=0;
	VFExport virtual BOOL GetRo(float point[3], float &ro)=0;
	VFExport virtual BOOL GetTemp(float point[3], float &Temp)=0;
	///
	/// This function will get the value of the voxel without interpolation
	///
	VFExport virtual BOOL GetValueFast(float point[3], int shadReq, FXShadeData &output)=0;
	//shdReq - shading requirements,
	//sdata - output
	VFExport virtual BOOL GetValueField(float point[3], float *field, float &val)=0;
	VFExport virtual BOOL GetValue(float point[3], int shdaReq, FXShadeData &output)=0;

	// is_pos - if true then val is a pointer to a voxel index. If false, then val points to an
	// array of i,j,k integer coords.
	VFExport virtual BOOL GetValueVoxel(int * val, bool is_pos, int shadReq, FXShadeData &output)=0;

	VFExport virtual BOOL GetValueForPreview(float point[3],float &fire, float &ro)=0;

//Used internally
	VFExport virtual void CalcFalloff(shdParams_Standard *params, SDPoint3 lpe, float &thisedFallStren)=0;

//Shading
	VFExport virtual BOOL ShadeStandard(SDPoint3 lPt, shdParams_Standard *params, const FXShadeData &fxSD, vfLightSampler* lSamp, vfMapSampler *mSamp, SDColor &col, SDColor &trn, float &alpha, int &mediaType)=0;

// Illumination Map vars and methods
	BOOL IMCreationinProgress, isIllumMapLoaded;
	bool doDraftMap;
	float IlluminationMapMultipler;
	float colorThresh; // color threshold for draft IM
// Multiple scattering vars
	bool DoMultipleScattering;
	float FireGIStren, SmokeGIStren, MSGIFalloff;
	int MSAccuracy;

	bool noRAMforIM,noRAMforMS; //signal outOF RAM for a single frame
	bool didIllumMap;//if IM was built

	// int numThreads - number of threads to spawn during IM creation. Some renderers might not
	//					support thread creation outside of their core (like mental ray).
	//					If set to -1, all procs will be used
	// vfShader *theShader - pointer to a shader
	// vfLightSampler *lSamp - pointer to vfLightSampler interface.
	// char *_pathIM -	full name and path of the illumination map cache file for the current frame.
	//					If caching in FumeFX is disabled, pass NULL to PrepareIM()
	VFExport virtual BOOL PrepareIM(vfShader *theShader, const char *_pathIM=NULL)=0;
	VFExport virtual BOOL CreateIlluminationMap(int threadNum, int totalThreads, vfShader *theShader, vfLightSampler *lSamp)=0;
	VFExport virtual void FinishIMandMS(vfShader *theShader, vfLightSampler *lSamp)=0;

	VFExport virtual SDColor GetIMColor(float point[3])=0;



};


// Creation
// ---------------------------------------------------------------------------------- //

VFExport		VoxelFlowBase* CreateVoxelFlow();
VFExport		void DeleteVoxelFlow(VoxelFlowBase* smoke);

// File utils
// fname: resulting file name is stored here
// basename: name of the file, without extension
// frame: frame number
// flag: do not use
// ---------------------------------------------------------------------------------- //

//for .fxd / .f3d
VFExport bool vfMakeOutputName(TCHAR* fname, const TCHAR* basename, int frame);

//for .fim
VFExport bool vfMakeIllumMapName(TCHAR* fname, const TCHAR* basename, int frame);

//for .fdc
VFExport bool vfMakeSnapshotName(TCHAR* fname, const TCHAR* basename, int frame);

//for .png
VFExport bool vfMakePNGName(TCHAR* fname, const TCHAR* basename, int frame);

#endif
