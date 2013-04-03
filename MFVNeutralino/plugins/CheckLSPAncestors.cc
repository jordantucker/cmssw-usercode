#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/MFVNeutralino/interface/MCInteractionMFV3j.h"
#include "JMTucker/Tools/interface/GenUtilities.h"
#include "JMTucker/Tools/interface/Utilities.h"

class CheckLSPAncestors : public edm::EDAnalyzer {
 public:
  explicit CheckLSPAncestors(const edm::ParameterSet&) {}
  void analyze(const edm::Event&, const edm::EventSetup&);
};

void CheckLSPAncestors::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<reco::GenParticleCollection> gen_particles;
  event.getByLabel("genParticles", gen_particles);

  MCInteractionMFV3j mci;
  mci.Init(*gen_particles);
  die_if_not(mci.Valid(), "MCInteractionMFV3j failed to init");

  // lsps_init are those before all the ISR generated by pythia8.
  std::vector<const reco::Candidate*> lsps_init;
  for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    if (abs(gen.status()) == 22 && gen.pdgId() == 1000021)
      lsps_init.push_back(&gen);
  }
  die_if_not(lsps_init.size() == 2, "did not find two initial copies of the LSPs");

  printf("codes_%u_%u = {\n", event.id().run(), event.id().event());
  for (int i = 0, ie = int(gen_particles->size()); i < ie; ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    int code = 0;
    if (is_ancestor_of(&gen, mci.lsps[0]))
      code += 1;
    if (is_ancestor_of(&gen, mci.lsps[1]))
      code += 2;
    if (code == 0 && (is_ancestor_of(&gen, lsps_init[0]) || is_ancestor_of(&gen, lsps_init[1])))
      code += 4;
    printf("  %i: %i,\n", i, code);
  }
  printf("}\n");
}

DEFINE_FWK_MODULE(CheckLSPAncestors);
