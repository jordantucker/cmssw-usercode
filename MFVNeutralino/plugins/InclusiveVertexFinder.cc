#include <memory>

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

#include "RecoVertex/ConfigurableVertexReco/interface/ConfigurableVertexReconstructor.h"
#include "TrackingTools/PatternTools/interface/TwoTrackMinimumDistance.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
//#include "RecoVertex/AdaptiveVertexFinder/interface/TracksClusteringFromDisplacedSeed.h"
#include "JMTucker/MFVNeutralino/plugins/TracksClusteringFromDisplacedSeed.h"

#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexUpdator.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexTrackCompatibilityEstimator.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexSmoother.h"
#include "RecoVertex/MultiVertexFit/interface/MultiVertexFitter.h"

//#define VTXDEBUG 1

class MFVInclusiveVertexFinder : public edm::EDProducer {
    public:
	MFVInclusiveVertexFinder(const edm::ParameterSet &params);

	virtual void produce(edm::Event &event, const edm::EventSetup &es);

    private:
	bool trackFilter(const reco::TrackRef &track) const;
        std::pair<std::vector<reco::TransientTrack>,GlobalPoint> nearTracks(const reco::TransientTrack &seed, const std::vector<reco::TransientTrack> & tracks, const reco::Vertex & primaryVertex) const;

	edm::InputTag				beamSpotCollection;
	edm::InputTag				primaryVertexCollection;
	edm::InputTag				trackCollection;
	unsigned int				minHits;
	unsigned int				maxNTracks;
	double					maxLIP;
        double 					minPt;
        double 					vertexMinAngleCosine;
        double 					vertexMinDLen2DSig;
        double 					vertexMinDLenSig;

	std::auto_ptr<VertexReconstructor>	vtxReco;
	std::auto_ptr<MFVTracksClusteringFromDisplacedSeed>	clusterizer;

  const bool reweight_mfv;
  TH1F* h_npv;
  TH1F* h_ntracks;
  TH1F* h_trackhits;
  TH1F* h_trackpt;
  TH1F* h_trackdz;
  TH1F* h_trackfilteredhits;
  TH1F* h_trackfilteredpt;
  TH1F* h_trackfiltereddz;
  TH1F* h_nseltracks;
  TH1F* h_nclusters;
  TH1F* h_ntrackspercluster;
  TH1F* h_clusterseedtrackpt;
  TH1F* h_clusterseedtrackdxy;
  TH1F* h_clusterseedpointrho;
  TH1F* h_nverticespercluster;
  TH1F* h_singlefitspercluster;
  TH1F* h_nvertex;
  TH1F* h_vertexdisttopv;
  TH1F* h_vertexdist2topv;
  TH1F* h_vertexdisttopverr;
  TH1F* h_vertexdist2topverr;
  TH1F* h_vertexdisttopvsig;
  TH1F* h_vertexdist2topvsig;
  TH1F* h_vertexchi2;
  TH1F* h_vertexndof;
  TH1F* h_vertexrho;
  TH1F* h_ntrackspervertex;
  TH1F* h_vertextrackweight;
  TH1F* h_vertexpvsvcostheta;
  TH1F* h_nselectedvertex;
  TH1F* h_selectedvertexdisttopv;
  TH1F* h_selectedvertexdist2topv;
  TH1F* h_selectedvertexdisttopverr;
  TH1F* h_selectedvertexdist2topverr;
  TH1F* h_selectedvertexdisttopvsig;
  TH1F* h_selectedvertexdist2topvsig;
  TH1F* h_selectedvertexchi2;
  TH1F* h_selectedvertexndof;
  TH1F* h_selectedvertexrho;
  TH1F* h_selectedntrackspervertex;
  TH1F* h_selectedvertextrackweight;
  TH1F* h_selectedvertexpvsvcostheta;
};

MFVInclusiveVertexFinder::MFVInclusiveVertexFinder(const edm::ParameterSet &params) :
	beamSpotCollection(params.getParameter<edm::InputTag>("beamSpot")),
	primaryVertexCollection(params.getParameter<edm::InputTag>("primaryVertices")),
	trackCollection(params.getParameter<edm::InputTag>("tracks")),
	minHits(params.getParameter<unsigned int>("minHits")),
	maxNTracks(params.getParameter<unsigned int>("maxNTracks")),
       	maxLIP(params.getParameter<double>("maximumLongitudinalImpactParameter")),
 	minPt(params.getParameter<double>("minPt")), //0.8
        vertexMinAngleCosine(params.getParameter<double>("vertexMinAngleCosine")), //0.98
        vertexMinDLen2DSig(params.getParameter<double>("vertexMinDLen2DSig")), //2.5
        vertexMinDLenSig(params.getParameter<double>("vertexMinDLenSig")), //0.5
	vtxReco(new ConfigurableVertexReconstructor(params.getParameter<edm::ParameterSet>("vertexReco"))),
        clusterizer(new MFVTracksClusteringFromDisplacedSeed(params.getParameter<edm::ParameterSet>("clusterizer"))),
        reweight_mfv(params.getUntrackedParameter<bool>("reweight_mfv", false))
{
	produces<reco::VertexCollection>();
	//produces<reco::VertexCollection>("multi");

  edm::Service<TFileService> fs;
  TH1::SetDefaultSumw2();
  h_npv = fs->make<TH1F>("h_npv", ";npv;events", 100, 0, 100);
  h_ntracks = fs->make<TH1F>("h_ntracks", ";ntracks;events/30", 50, 0, 1500);
  h_trackhits = fs->make<TH1F>("h_trackhits", ";nhits/track;tracks", 50, 0, 50);
  h_trackpt = fs->make<TH1F>("h_trackpt", ";track pt;tracks/5 GeV", 100, 0, 500);
  h_trackdz = fs->make<TH1F>("h_trackdz", ";track dz(pv);tracks/2 cm", 150, -150, 150);
  h_trackfilteredhits = fs->make<TH1F>("h_trackfilteredhits", "selected tracks;nhits/track;tracks", 50, 0, 50);
  h_trackfilteredpt   = fs->make<TH1F>("h_trackfilteredpt", "selected tracks;nhits;tracks/5 GeV", 100, 0, 500);
  h_trackfiltereddz   = fs->make<TH1F>("h_trackfiltereddz", "selcted tracks;track dz(pv)", 50, -0.5, 0.5);

  h_nseltracks = fs->make<TH1F>("h_nseltracks", "", 500, 0, 500);
  h_nclusters = fs->make<TH1F>("h_nclusters", "", 500, 0, 500);
  h_ntrackspercluster = fs->make<TH1F>("h_ntrackspercluster", "", 100, 0, 100);
  h_clusterseedtrackpt = fs->make<TH1F>("h_clusterseedtrackpt", "", 100, 0, 500);
  h_clusterseedtrackdxy = fs->make<TH1F>("h_clusterseedtrackdxy", "", 200, 0, 100);
  h_clusterseedpointrho = fs->make<TH1F>("h_clusterseedpointrho", "", 200, 0, 100);
  h_nverticespercluster = fs->make<TH1F>("h_nverticespercluster", "", 20, 0, 20);
  h_singlefitspercluster = fs->make<TH1F>("h_singlefitspercluster", "", 2, 0, 2);

  h_nvertex = fs->make<TH1F>("h_nvertex", "", 100, 0, 100);
  h_vertexdisttopv = fs->make<TH1F>("h_vertexdisttopv", "", 200, 0, 200);
  h_vertexdist2topv = fs->make<TH1F>("h_vertexdist2topv", "", 200, 0, 200);
  h_vertexdisttopverr = fs->make<TH1F>("h_vertexdisttopverr", "", 200, 0, 200);
  h_vertexdist2topverr = fs->make<TH1F>("h_vertexdist2topverr", "", 200, 0, 200);
  h_vertexdisttopvsig = fs->make<TH1F>("h_vertexdisttopvsig", "", 200, 0, 200);
  h_vertexdist2topvsig = fs->make<TH1F>("h_vertexdist2topvsig", "", 200, 0, 200);
  h_vertexchi2 = fs->make<TH1F>("h_vertexchi2", "", 100, 0, 20);
  h_vertexndof = fs->make<TH1F>("h_vertexndof", "", 80, 0, 80);
  h_vertexrho = fs->make<TH1F>("h_vertexrho", "", 200, 0, 200);
  h_ntrackspervertex = fs->make<TH1F>("h_ntrackspervertex", "", 50, 0, 50);
  h_vertextrackweight = fs->make<TH1F>("h_vertextrackweight", "", 50, 0, 1);
  h_vertexpvsvcostheta = fs->make<TH1F>("h_vertexpvsvcostheta", "", 200, -1, 1);

  h_nselectedvertex = fs->make<TH1F>("h_nselectedvertex", "", 100, 0, 100);
  h_selectedvertexdisttopv = fs->make<TH1F>("h_selectedvertexdisttopv", "", 200, 0, 200);
  h_selectedvertexdist2topv = fs->make<TH1F>("h_selectedvertexdist2topv", "", 200, 0, 200);
  h_selectedvertexdisttopverr = fs->make<TH1F>("h_selectedvertexdisttopverr", "", 200, 0, 200);
  h_selectedvertexdist2topverr = fs->make<TH1F>("h_selectedvertexdist2topverr", "", 200, 0, 200);
  h_selectedvertexdisttopvsig = fs->make<TH1F>("h_selectedvertexdisttopvsig", "", 200, 0, 200);
  h_selectedvertexdist2topvsig = fs->make<TH1F>("h_selectedvertexdist2topvsig", "", 200, 0, 200);
  h_selectedvertexchi2 = fs->make<TH1F>("h_selectedvertexchi2", "", 100, 0, 20);
  h_selectedvertexndof = fs->make<TH1F>("h_selectedvertexndof", "", 80, 0, 80);
  h_selectedvertexrho = fs->make<TH1F>("h_selectedvertexrho", "", 200, 0, 200);
  h_selectedntrackspervertex = fs->make<TH1F>("h_selectedntrackspervertex", "", 50, 0, 50);
  h_selectedvertextrackweight = fs->make<TH1F>("h_selectedvertextrackweight", "", 50, 0, 1);
  h_selectedvertexpvsvcostheta = fs->make<TH1F>("h_selectedvertexpvsvcostheta", "", 200, -1, 1);
}

bool MFVInclusiveVertexFinder::trackFilter(const reco::TrackRef &track) const
{
	if (track->hitPattern().numberOfValidHits() < (int)minHits)
//	if (track->hitPattern().trackerLayersWithMeasurement() < (int)minHits)
		return false;
	if (track->pt() < minPt )
		return false;
 
	return true;
}

void MFVInclusiveVertexFinder::produce(edm::Event &event, const edm::EventSetup &es)
{
	using namespace reco;

  double sigmacut = 3.0;
  double Tini = 256.;
  double ratio = 0.25;
  VertexDistance3D vdist;
  VertexDistanceXY vdist2d;
  MultiVertexFitter theMultiVertexFitter;
  AdaptiveVertexFitter theAdaptiveFitter(
                                            GeometricAnnealing(sigmacut, Tini, ratio),
                                            DefaultLinearizationPointFinder(),
                                            KalmanVertexUpdator<5>(),
                                            KalmanVertexTrackCompatibilityEstimator<5>(),
                                            KalmanVertexSmoother() );


	edm::Handle<BeamSpot> beamSpot;
	event.getByLabel(beamSpotCollection, beamSpot);

	edm::Handle<VertexCollection> primaryVertices;
	event.getByLabel(primaryVertexCollection, primaryVertices);

	const double npv_weights[100] = { 0.000000, 0.000000, 0.067249, 0.044833, 0.050810, 0.063293, 0.080533, 0.148446, 0.144329, 0.109138, 0.060456, 0.045131, 0.029133, 0.019916, 0.014338, 0.010808, 0.008680, 0.006432, 0.006350, 0.004934, 0.004402, 0.003949, 0.003134, 0.002880, 0.003237, 0.002499, 0.002638, 0.002997, 0.003357, 0.003736, 0.002880, 0.002368, 0.003047, 0.002099, 0.002397, 0.002625, 0.004110, 0.005604, 0.004483, 0.003321, 0.004483, 0.007472, 0.000000, 0.007472, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000 };
	const size_t npv = primaryVertices->size();
	const double npv_weight = reweight_mfv ? (npv < 100 ? npv_weights[npv] : 0) : 1;
	clusterizer->npv_weight = npv_weight;

	h_npv->Fill(primaryVertices->size(), npv_weight);

	edm::Handle<TrackCollection> tracks;
	event.getByLabel(trackCollection, tracks);

	edm::ESHandle<TransientTrackBuilder> trackBuilder;
	es.get<TransientTrackRecord>().get("TransientTrackBuilder",
	                                   trackBuilder);


        std::auto_ptr<VertexCollection> recoVertices(new VertexCollection);
        if(primaryVertices->size()!=0) {
     
	const reco::Vertex &pv = (*primaryVertices)[0];
        
	std::vector<TransientTrack> tts;
        //Fill transient track vector 
	h_ntracks->Fill(tracks->size(), npv_weight);
	for(TrackCollection::const_iterator track = tracks->begin();
	    track != tracks->end(); ++track) {
		TrackRef ref(tracks, track - tracks->begin());
		h_trackhits->Fill(track->hitPattern().numberOfValidHits(), npv_weight);
		h_trackpt->Fill(track->pt(), npv_weight);
		h_trackdz->Fill(ref->dz(pv.position()), npv_weight);
		if (!trackFilter(ref))
			continue;
                if( std::abs(ref->dz(pv.position())) > maxLIP)
			continue;
		h_trackfilteredhits->Fill(track->hitPattern().numberOfValidHits(), npv_weight);
		h_trackfilteredpt->Fill(track->pt(), npv_weight);
		h_trackfiltereddz->Fill(ref->dz(pv.position()), npv_weight);
		TransientTrack tt = trackBuilder->build(ref);
		tt.setBeamSpot(*beamSpot);
		tts.push_back(tt);
	}
        std::vector<MFVTracksClusteringFromDisplacedSeed::Cluster> clusters = clusterizer->clusters(pv,tts);

	h_nseltracks->Fill(tts.size(), npv_weight);
	h_nclusters->Fill(clusters.size(), npv_weight);

        //Create BS object from PV to feed in the AVR
	BeamSpot::CovarianceMatrix cov;
	for(unsigned int i = 0; i < 7; i++) {
		for(unsigned int j = 0; j < 7; j++) {
			if (i < 3 && j < 3)
				cov(i, j) = pv.covariance(i, j);
			else
				cov(i, j) = 0.0;
		}
	}
	BeamSpot bs(pv.position(), 0.0, 0.0, 0.0, 0.0, cov, BeamSpot::Unknown);


        int i=0;
#ifdef VTXDEBUG

	std::cout <<  "CLUSTERS " << clusters.size() << std::endl; 
#endif

	for(std::vector<MFVTracksClusteringFromDisplacedSeed::Cluster>::iterator cluster = clusters.begin();
	    cluster != clusters.end(); ++cluster,++i)
        {
	        h_ntrackspercluster->Fill(cluster->tracks.size(), npv_weight);

                if(cluster->tracks.size() == 0 || cluster->tracks.size() > maxNTracks ) 
		     continue;

		h_clusterseedtrackpt->Fill(cluster->seedingTrack.track().pt(), npv_weight);
		h_clusterseedtrackdxy->Fill(cluster->seedingTrack.stateAtBeamLine().transverseImpactParameter().value(), npv_weight);
		h_clusterseedpointrho->Fill(cluster->seedPoint.perp(), npv_weight);
        
 	        cluster->tracks.push_back(cluster->seedingTrack); //add the seed to the list of tracks to fit
	 	std::vector<TransientVertex> vertices;
		vertices = vtxReco->vertices(cluster->tracks, bs);  // attempt with config given reconstructor
		h_nverticespercluster->Fill(vertices.size(), npv_weight);
                TransientVertex singleFitVertex;
                singleFitVertex = theAdaptiveFitter.vertex(cluster->tracks,cluster->seedPoint); //attempt with direct fitting
                if(singleFitVertex.isValid())
                          vertices.push_back(singleFitVertex);
		h_singlefitspercluster->Fill(singleFitVertex.isValid(), npv_weight);
		for(std::vector<TransientVertex>::const_iterator v = vertices.begin();
		    v != vertices.end(); ++v) {
//			if(v->degreesOfFreedom() > 0.2)
                        {
                         Measurement1D dlen= vdist.distance(pv,*v);
                         Measurement1D dlen2= vdist2d.distance(pv,*v);
			 reco::Vertex vv(*v);
#ifdef VTXDEBUG
                       std::cout << "V chi2/n: " << v->normalisedChiSquared() << " ndof: " <<v->degreesOfFreedom() ;
                         std::cout << " dlen: " << dlen.value() << " error: " << dlen.error() << " signif: " << dlen.significance();
                         std::cout << " dlen2: " << dlen2.value() << " error2: " << dlen2.error() << " signif2: " << dlen2.significance();
                         std::cout << " pos: " << vv.position() << " error: " <<vv.xError() << " " << vv.yError() << " " << vv.zError() << std::endl;
#endif
                         GlobalVector dir;  
			 std::vector<reco::TransientTrack> ts = v->originalTracks();
			 h_vertexdisttopv->Fill(dlen.value(), npv_weight);
			 h_vertexdist2topv->Fill(dlen2.value(), npv_weight);
			 h_vertexdisttopverr->Fill(dlen.error(), npv_weight);
			 h_vertexdist2topverr->Fill(dlen2.error(), npv_weight);
			 h_vertexdisttopvsig->Fill(dlen.significance(), npv_weight);
			 h_vertexdist2topvsig->Fill(dlen2.significance(), npv_weight);
			 h_vertexchi2->Fill(v->normalisedChiSquared(), npv_weight);
			 h_vertexndof->Fill(v->degreesOfFreedom(), npv_weight);
			 h_vertexrho->Fill(v->position().perp(), npv_weight);
			 h_ntrackspervertex->Fill(ts.size(), npv_weight);
                        for(std::vector<reco::TransientTrack>::const_iterator i = ts.begin();
                            i != ts.end(); ++i) {
                                reco::TrackRef t = i->trackBaseRef().castTo<reco::TrackRef>();
                                float w = v->trackWeight(*i);
                                if (w > 0.5) dir+=i->impactPointState().globalDirection();
#ifdef VTXDEBUG
                                std::cout << "\t[" << (*t).pt() << ": "
                                          << (*t).eta() << ", "
                                          << (*t).phi() << "], "
                                          << w << std::endl;
#endif
				h_vertextrackweight->Fill(w, npv_weight);
                        }
		       GlobalPoint ppv(pv.position().x(),pv.position().y(),pv.position().z());
		       GlobalPoint sv((*v).position().x(),(*v).position().y(),(*v).position().z());
                       float vscal = dir.unit().dot((sv-ppv).unit()) ;
//                        std::cout << "Vscal: " <<  vscal << std::endl;
		       h_vertexpvsvcostheta->Fill(vscal, npv_weight);
		       if(dlen.significance() > vertexMinDLenSig  && v->normalisedChiSquared() < 10 && dlen2.significance() > vertexMinDLen2DSig)
			 h_selectedvertexpvsvcostheta->Fill(vscal, npv_weight);
                       if(dlen.significance() > vertexMinDLenSig  && vscal > vertexMinAngleCosine &&  v->normalisedChiSquared() < 10 && dlen2.significance() > vertexMinDLen2DSig)
	            	  {	 
			        h_selectedvertexdisttopv->Fill(dlen.value(), npv_weight);
				h_selectedvertexdist2topv->Fill(dlen2.value(), npv_weight);
				h_selectedvertexdisttopverr->Fill(dlen.error(), npv_weight);
				h_selectedvertexdist2topverr->Fill(dlen2.error(), npv_weight);
				h_selectedvertexdisttopvsig->Fill(dlen.significance(), npv_weight);
				h_selectedvertexdist2topvsig->Fill(dlen2.significance(), npv_weight);
				h_selectedvertexchi2->Fill(v->normalisedChiSquared(), npv_weight);
				h_selectedvertexndof->Fill(v->degreesOfFreedom(), npv_weight);
				h_selectedvertexrho->Fill(v->position().perp(), npv_weight);
				h_selectedntrackspervertex->Fill(ts.size(), npv_weight);
				//h_selectedvertexpvsvcostheta->Fill(vscal, npv_weight);
				recoVertices->push_back(*v);
#ifdef VTXDEBUG

	                        std::cout << "ADDED" << std::endl;
#endif

                         }
		       h_nselectedvertex->Fill(recoVertices->size());
                      }
                   }
        }
#ifdef VTXDEBUG

        std::cout <<  "Final put  " << recoVertices->size() << std::endl;
#endif  
        }
 
	event.put(recoVertices);

}

DEFINE_FWK_MODULE(MFVInclusiveVertexFinder);
