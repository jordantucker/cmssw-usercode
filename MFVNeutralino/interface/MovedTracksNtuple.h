#ifndef JMTucker_MFVNeutralino_interface_MovedTracksNtuple_h
#define JMTucker_MFVNeutralino_interface_MovedTracksNtuple_h

#include <vector>
#include "TLorentzVector.h"

class TTree;
class TVector3;

namespace mfv {
  struct MovedTracksNtuple {
    typedef unsigned char uchar;
    typedef unsigned short ushort;

    unsigned run;
    unsigned lumi;
    unsigned long long event;

    float weight;

    bool gen_valid;
    float gen_lsp_pt[2];
    float gen_lsp_eta[2];
    float gen_lsp_phi[2];
    float gen_lsp_mass[2];
    float gen_lsp_decay[2*3];
    uchar gen_decay_type[2];

    uchar pass_hlt;
    float bsx;
    float bsy;
    float bsz;
    float bsdxdz;
    float bsdydz;
    float bsx_at_z(float z) const { return bsx + bsdxdz * (z - bsz); }
    float bsy_at_z(float z) const { return bsy + bsdydz * (z - bsz); }
    uchar npu;
    uchar npv;
    float pvx;
    float pvy;
    float pvz;
    ushort pvntracks;
    float pvsumpt2;
    float jetht;
    ushort ntracks;
    uchar nseltracks;
    std::vector<float> alljets_pt;
    std::vector<float> alljets_eta;
    std::vector<float> alljets_phi;
    std::vector<float> alljets_energy;
    std::vector<float> alljets_bdisc;
    std::vector<uchar> alljets_hadronflavor;
    size_t nalljets() const { return p_alljets_pt ? p_alljets_pt->size() : alljets_pt.size(); }

    uchar npreseljets;
    uchar npreselbjets;
    uchar nlightjets;
    std::vector<float> jets_pt; // these are the moved jets
    std::vector<float> jets_eta;
    std::vector<float> jets_phi;
    std::vector<float> jets_energy;
    std::vector<uchar> jets_ntracks;
    uchar njets() const { return p_jets_pt ? uchar(p_jets_pt->size()) : uchar(jets_pt.size()); }
    uchar nbjets() const { return njets() - nlightjets; }

    TLorentzVector alljets_p4(size_t i) const {
      TLorentzVector p;
      if (p_alljets_pt)
        p.SetPtEtaPhiE((*p_alljets_pt)[i], (*p_alljets_eta)[i], (*p_alljets_phi)[i], (*p_alljets_energy)[i]);
      else
        p.SetPtEtaPhiE(alljets_pt[i], alljets_eta[i], alljets_phi[i], alljets_energy[i]);
      return p;
    }

    TLorentzVector jets_p4(size_t i) const {
      TLorentzVector p;
      if (p_jets_pt)
        p.SetPtEtaPhiE((*p_jets_pt)[i], (*p_jets_eta)[i], (*p_jets_phi)[i], (*p_jets_energy)[i]);
      else
        p.SetPtEtaPhiE(jets_pt[i], jets_eta[i], jets_phi[i], jets_energy[i]);
      return p;
    }

    float move_x;
    float move_y;
    float move_z;
    TVector3 move_vector() const;
    double move_tau() const;

    std::vector<float> vtxs_x;
    std::vector<float> vtxs_y;
    std::vector<float> vtxs_z;
    std::vector<float> vtxs_pt; // this and next three are from tracksplusjets momentum
    std::vector<float> vtxs_theta;
    std::vector<float> vtxs_phi;
    std::vector<float> vtxs_mass;
    std::vector<float> vtxs_tkonlymass;
    std::vector<uchar> vtxs_ntracks;
    std::vector<float> vtxs_anglemin; // tracks' angles are between momentum and the move vector
    std::vector<float> vtxs_anglemax;
    std::vector<float> vtxs_bs2derr;

    MovedTracksNtuple();
    void clear();
    void write_to_tree(TTree* tree);
    void read_from_tree(TTree* tree);

    // ugh
    std::vector<float>* p_alljets_pt;
    std::vector<float>* p_alljets_eta;
    std::vector<float>* p_alljets_phi;
    std::vector<float>* p_alljets_energy;
    std::vector<float>* p_alljets_bdisc;
    std::vector<uchar>* p_alljets_hadronflavor;
    std::vector<float>* p_jets_pt;
    std::vector<float>* p_jets_eta;
    std::vector<float>* p_jets_phi;
    std::vector<float>* p_jets_energy;
    std::vector<uchar>* p_jets_ntracks;
    std::vector<float>* p_vtxs_x;
    std::vector<float>* p_vtxs_y;
    std::vector<float>* p_vtxs_z;
    std::vector<float>* p_vtxs_pt;
    std::vector<float>* p_vtxs_theta;
    std::vector<float>* p_vtxs_phi;
    std::vector<float>* p_vtxs_mass;
    std::vector<float>* p_vtxs_tkonlymass;
    std::vector<uchar>* p_vtxs_ntracks;
    std::vector<float>* p_vtxs_anglemin;
    std::vector<float>* p_vtxs_anglemax;
    std::vector<float>* p_vtxs_bs2derr;
  };
}

#endif
