#ifndef JMTucker_Tools_Geometry_h
#define JMTucker_Tools_Geometry_h

namespace jmt {
  namespace Geometry {
    bool inside_beampipe(bool is_mc, double x, double y);
    bool inside_beampipe(double x, double y);
  }
}

#endif
