import awkward as ak
import numpy as np

from pocket_coffea.workflows.base import BaseProcessorABC
from pocket_coffea.utils.configurator import Configurator
from pocket_coffea.lib.hist_manager import Axis
from pocket_coffea.lib.objects import (
    jet_correction,
    lepton_selection,
    jet_selection,
    btagging,
    get_dilepton
)


class CommBTVBaseProcessor(BaseProcessorABC):
    def __init__(self, cfg: Configurator):
        super().__init__(cfg)

        # self.proc_type = self.params["proc_type"]
        # self.isArray=self.cfg["isArray"]
        #  self.campaign["run_options]/
        print(self.params,self.cfg)
    def apply_object_preselection(self, variation):
        '''
        
        '''
        # Include the supercluster pseudorapidity variable
        electron_etaSC = self.events.Electron.eta + self.events.Electron.deltaEtaSC
        self.events["Electron"] = ak.with_field(
            self.events.Electron, electron_etaSC, "etaSC"
        )
        # Build masks for selection of muons, electrons, jets, fatjets
        self.events["MuonGood"] = lepton_selection(
            self.events, "Muon", self.params
        )
        self.events["ElectronGood"] = lepton_selection(
            self.events, "Electron", self.params
        )
        leptons = ak.with_name(
            ak.concatenate((self.events.MuonGood, self.events.ElectronGood), axis=1),
            name='PtEtaPhiMCandidate',
        )
        self.events["LeptonGood"] = leptons[ak.argsort(leptons.pt, ascending=False)]

        self.events["ll"] = get_dilepton(
            self.events.ElectronGood, self.events.MuonGood
        )

        self.events["JetGood"], self.jetGoodMask = jet_selection(
            self.events, "Jet", self.params, "LeptonGood"
        )
        print(self.params)
        # self.events["BJet_XXT"] = btagging(
            # self.events["JetGood"], self.params.bctagging[self.campaign].b.DeepFlav.XXT)
        # self.events["BJet_XT"] = btagging(
        #     self.events["JetGood"], self.params.btagging.T[self.campaign])
        # self.events["BJet_T"] = btagging(
        #     self.events["JetGood"], self.params.btagging.working_point[self.campaign])
        

    def count_objects(self, variation):
        self.events["nMuonGood"] = ak.num(self.events.MuonGood)
        self.events["nElectronGood"] = ak.num(self.events.ElectronGood)
        self.events["nLeptonGood"] = ak.num(self.events.LeptonGood)

        self.events["nJet"] = ak.num(self.events.Jet)
        self.events["nJetGood"] = ak.num(self.events.JetGood)
        # self.events["nBJetGood"] = ak.num(self.events.BJetGood)
        # self.events["nfatjet"]   = ak.num(self.events.FatJetGood)

    # Function that defines common variables employed in analyses and save them as attributes of `events`
    def define_common_variables_before_presel(self, variation):
        self.events["JetGood_pt"] = self.events.JetGood.pt
    def define_common_variables_after_presel(self, variation):

        
        
        self.events["JetGood_pt"] = self.events.JetGood.pt
        # self.events["dilep_deltaR"] = self.events.ll.deltaR

        
