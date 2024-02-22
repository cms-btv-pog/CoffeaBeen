import awkward as ak
from pocket_coffea.lib.cut_definition import Cut

def softmu_mask(events, campaign):
    softmumask = (
        (events.Muon.pt < 25)
        & (abs(events.Muon.eta) < 2.4)
        & (events.Muon.tightId > 0.5)
        & (events.Muon.pfRelIso04_all > 0.2)
        & (events.Muon.jetIdx != -1)
    )

    return softmumask


def mu_idiso(events, campaign):
    mumask = (
        (abs(events.Muon.eta) < 2.4)
        & (events.Muon.tightId > 0.5)
        & (events.Muon.pfRelIso04_all <= 0.15)
    )
    return mumask


def softmu(events, campaign):
    mumask = (
        (abs(events.Muon.eta) < 2.4)
        & (events.Muon.tightId > 0.5)
        & (events.Muon.pfRelIso04_all < 0.12)
    )
    return mumask


def multijet_mask(events):
    multijetmask = (
        (abs(events.Jet.eta) < 2.4) & (events.Jet.pt > 180) & (events.Jet.jetId >= 5)
    )
    return ak.where(ak.is_none(multijetmask), False, mask)
def DilepOneJet(events,params, **kwargs):
    nj = (events.nJetGood >= params["nj"])
    nlep = (events.LeptonGood >= params["nlep"])
    mask = nj & nlep
    return ak.where(ak.is_none(mask), False, mask)

    

ttbar_preselection= Cut(
    name="ttbar_preselection",
    function=DilepOneJet,
    params={
        "nj" : 1,
        "nlep" : 2
    },
)