#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class MFVSkimmedTracks : public edm::EDFilter {
public:
  explicit MFVSkimmedTracks(const edm::ParameterSet&);
private:
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const edm::EDGetTokenT<pat::PackedCandidateCollection> packed_candidates_token;
  const edm::EDGetTokenT<std::vector<size_t>> packed_candidates_indices_token;

  const double min_pt;
  const double min_dxybs;
  const double min_nsigmadxybs;
  const bool input_is_miniaod;
  const bool cut;
  const bool debug;
};

MFVSkimmedTracks::MFVSkimmedTracks(const edm::ParameterSet& cfg)
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    beamspot_token(consumes<reco::BeamSpot>(edm::InputTag("offlineBeamSpot"))),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    packed_candidates_token(consumes<pat::PackedCandidateCollection>(cfg.getParameter<edm::InputTag>("packed_candidates_src"))),
    packed_candidates_indices_token(consumes<std::vector<size_t>>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    min_pt(cfg.getParameter<double>("min_pt")),
    min_dxybs(cfg.getParameter<double>("min_dxybs")),
    min_nsigmadxybs(cfg.getParameter<double>("min_nsigmadxybs")),
    input_is_miniaod(cfg.getParameter<bool>("input_is_miniaod")),
    cut(cfg.getParameter<bool>("cut")),
    debug(cfg.getUntrackedParameter<bool>("debug", false))
{
  produces<reco::TrackCollection>();
  produces<std::vector<int>>(); // which PV if any, -1 if none
}

bool MFVSkimmedTracks::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  edm::Handle<reco::BeamSpot> beamspot;
  if (min_dxybs > 0 || min_nsigmadxybs > 0)
    event.getByToken(beamspot_token, beamspot);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertices_token, primary_vertices);

  edm::Handle<pat::PackedCandidateCollection> packed_candidates;
  edm::Handle<std::vector<size_t>> packed_candidates_indices;
  if (input_is_miniaod) {
    event.getByToken(packed_candidates_token, packed_candidates);
    event.getByToken(packed_candidates_indices_token, packed_candidates_indices);
    assert(packed_candidates_indices->size() == tracks->size());
  }

  if (debug) std::cout << "MFVSkimmedTracks::filter: run " << event.id().run() << " lumi " << event.luminosityBlock() << " event " << event.id().event() << " has " << tracks->size() << " input tracks, " << primary_vertices->size() << " primary vertices\n";

  std::map<reco::TrackRef, std::vector<int>> tracks_in_pvs;
  if (!input_is_miniaod)
    for (size_t i = 0, ie = primary_vertices->size(); i < ie; ++i) {
      const reco::Vertex& pv = (*primary_vertices)[i];
      for (auto it = pv.tracks_begin(), ite = pv.tracks_end(); it != ite; ++it)
        tracks_in_pvs[it->castTo<reco::TrackRef>()].push_back(i);
    }
  
  std::unique_ptr<reco::TrackCollection> output_tracks(new reco::TrackCollection);
  std::unique_ptr<std::vector<int>> output_pvindex(new std::vector<int>);

  int itk = -1;
  for (const reco::Track& tk : *tracks) {
    ++itk;
    const double pt = tk.pt();
    const bool min_r = tk.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,1);
    const int npxlayers = tk.hitPattern().pixelLayersWithMeasurement();
    const int nstlayers = tk.hitPattern().stripLayersWithMeasurement();

    bool pass = pt > min_pt && min_r && npxlayers >= 2 && nstlayers >= 6;

    if (debug) std::cout << "track #" << itk << " pt " << pt << " eta " << tk.eta() << " min_r " << min_r << " npxlayers " << npxlayers << " nstlayers " << nstlayers << " pass so far? " << pass;

    if (pass && (min_dxybs > 0 || min_nsigmadxybs > 0)) {
      const double dxybs = tk.dxy(*beamspot);
      const double dxyerr = tk.dxyError();
      const double nsigmadxybs = dxybs / dxyerr;
      if (fabs(dxybs) < min_dxybs || fabs(nsigmadxybs) < min_nsigmadxybs)
        pass = false;
      if (debug) std::cout << " dxybs " << dxybs << " dxyerr " << dxyerr << " sigmadxybs " << nsigmadxybs;
    }

    if (pass) {
      output_tracks->push_back(tk);

      if (input_is_miniaod) {
        const size_t ipc = (*packed_candidates_indices)[itk];
        const pat::PackedCandidate& pc = (*packed_candidates)[ipc];
        output_pvindex->push_back(pc.vertexRef().key());
      }
      else {
        reco::TrackRef ref(tracks, itk);
        const std::vector<int>& pv_for_track = tracks_in_pvs[ref];
        if (pv_for_track.size() > 1)
          throw cms::Exception("BadAssumption", "multiple PV for a track");
        output_pvindex->push_back(pv_for_track.size() ? pv_for_track[0] : -1);
      }

      if (debug) std::cout << " selected! now " << output_tracks->size() << " output tracks";
    }

    if (debug) std::cout << std::endl;
  }

  const size_t n_out = output_tracks->size();
  event.put(std::move(output_tracks));
  event.put(std::move(output_pvindex));

  return !cut || n_out;
}

DEFINE_FWK_MODULE(MFVSkimmedTracks);
