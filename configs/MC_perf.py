from pocket_coffea.utils.configurator import Configurator
from pocket_coffea.lib.cut_definition import Cut
from pocket_coffea.lib.cut_functions import get_nObj_min, get_HLTsel
from pocket_coffea.parameters.cuts import passthrough
from pocket_coffea.parameters.histograms import *
import workflow
from workflow import CommBTVBaseProcessor

import CommonSelectors
from CommonSelectors import *

import cloudpickle
cloudpickle.register_pickle_by_value(workflow)
cloudpickle.register_pickle_by_value(CommonSelectors)

import os
localdir = os.path.dirname(os.path.abspath(__file__))

# Loading default parameters
from pocket_coffea.parameters import defaults
default_parameters = defaults.get_default_parameters()
defaults.register_configuration_dir("config_dir", localdir+"/params")

parameters = defaults.merge_parameters_from_files(default_parameters,
                                                  f"{localdir}/params/object_preselection.yaml",
                                                  f"{localdir}/params/triggers.yaml",
                                                  f"{localdir}/params/ctagging.yaml",
                                                  update=True)

files_2022 = [
    f"{localdir}/datasets/Run3_2022_WtoLNu4Jets.json",
]

parameters["proc_type"] = "WLNu"
cfg = Configurator(
    parameters = parameters,
    datasets = {
        "jsons": files_2022,
        #"jsons": files_2018,

        # "filter" : {
        #     "samples": [
        #         "DATA_SingleMuon",
        #         "DATA_SingleElectron", # For 2017
        #         "DATA_EGamma",          # For 2018
        #         "WW", "WZ", "ZZ", "QCD",
        #         "DYJetsToLL_FxFx",
        #         "WJetsToLNu_FxFx",
        #         "TTToSemiLeptonic", "TTTo2L2Nu",
        #     ],
        #     "samples_exclude" : [],
        #     #"year": ['2016_PreVFP', '2016_PostVFP']
        #     "year": ['2016_PreVFP', '2016_PostVFP', '2017', '2018']
        # },
    },

    workflow = CommBTVBaseProcessor,

    skim = [get_HLTsel(primaryDatasets=["SingleMuon","SingleEle"]),
            get_nObj_min(3, 20., "Jet")], # in default jet collection there are leptons. So we ask for 1lep+2jets=3Jet objects

    #preselections = [onelep_plus_met],
    preselections = [lep_met_2jets],
    categories = {
        "baseline_1L2j": [passthrough],
        "presel_Wlnu_2j": [wlnu_plus_2j],
        "SR_Wlnu_2j_cj":  [wlnu_plus_2j,ctag_j1],
        "SR_Wmunu_2j_cj": [wmunu_plus_2j,ctag_j1],
        "SR_Welnu_2j_cj": [welnu_plus_2j,ctag_j1],
    },

    weights = {
        "common": {
            "inclusive": ["genWeight","lumi","XS",
                          "pileup",
                          "sf_mu_id","sf_mu_iso",
                          "sf_ele_reco","sf_ele_id",
                          ],
            "bycategory" : {
            }
        },
        "bysample": {
        }
    },

    variations = {
        "weights": {
            "common": {
                "inclusive": [
                    "pileup",
                    "sf_mu_id", "sf_mu_iso",
                    "sf_ele_reco", "sf_ele_id",
                ],
                "bycategory" : {
                }
            },
        "bysample": {
        }
        },
    },


    variables = {
        **lepton_hists(coll="LeptonGood", pos=0),
        **count_hist(name="nElectronGood", coll="ElectronGood",bins=5, start=0, stop=5),
        **count_hist(name="nMuonGood", coll="MuonGood",bins=5, start=0, stop=5),
        **count_hist(name="nJets", coll="JetGood",bins=8, start=0, stop=8),
        **count_hist(name="nBJets", coll="BJetGood",bins=8, start=0, stop=8),
        **jet_hists(coll="JetGood", pos=0),
        **jet_hists(coll="JetGood", pos=1),

       

        "nJet": HistConf( [Axis(field="nJet", bins=15, start=0, stop=15, label=r"nJet direct from NanoAOD")] ),

        "dilep_nom_pt" : HistConf( [Axis(coll="dilep", field="pt", bins=100, start=0, stop=400, label=r"$p_T{\\ell\\ell}$ [GeV]")] ),
        
        
        "MET_pt": HistConf( [Axis(coll="MET", field="pt", bins=50, start=0, stop=200, label=r"MET $p_T$ [GeV]")] ),
        "MET_phi": HistConf( [Axis(coll="MET", field="phi", bins=64, start=-math.pi, stop=math.pi, label=r"MET $phi$")] ),

    }
)


run_options = {
    "executor"       : "parsl/condor",
    "env"            : "conda",
    "workers"        : 1,
    "scaleout"       : 10,
    "walltime"       : "00:60:00",
    "mem_per_worker" : 2, # For Parsl
    #"mem_per_worker" : "2GB", # For Dask
    "exclusive"      : False,
    "skipbadfiles"   : False,
    "chunk"          : 500000,
    "retries"        : 20,
    "treereduction"  : 20,
    "adapt"          : False,
    "requirements": (
            '( Machine != "lx3a44.physik.rwth-aachen.de")'
        ),

    }