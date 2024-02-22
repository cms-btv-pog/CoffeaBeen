from pocket_coffea.utils.configurator import Configurator
from pocket_coffea.lib.cut_definition import Cut
from pocket_coffea.lib.cut_functions import get_nObj_min, get_HLTsel,get_nObj_eq
from pocket_coffea.parameters.cuts import passthrough
from pocket_coffea.parameters.histograms import *
import CommBTVbase
from CommBTVbase import CommBTVBaseProcessor

import CommonSelector
from CommonSelector import *

import cloudpickle
cloudpickle.register_pickle_by_value(CommBTVbase)
cloudpickle.register_pickle_by_value(CommonSelector)

import os
localdir = os.getcwd()
# Loading default parameters
from pocket_coffea.parameters import defaults
default_parameters = defaults.get_default_parameters()
defaults.register_configuration_dir("config_dir", localdir+"/params")

parameters = defaults.merge_parameters_from_files(default_parameters,
                                                  f"{localdir}/params/object_preselection.yml",
                                                  f"{localdir}/params/triggers.yml",
                                                  f"{localdir}/params/bctagging.yml",
                                                  update=True)

files_2022 = [
    f"{localdir}/datasets/Run3_2022_WtoLNu4Jets.json",
    f"{localdir}/datasets/Run3_2022_TTToLNu2Q.json",
    f"{localdir}/datasets/Run3_2022_TTTo2L2Nu.json",
    f"{localdir}/datasets/Run3_2022_TTTo4Q.json",
]

# parameters["proc_type"] = "WLNu"
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

    skim = [get_HLTsel(primaryDatasets=["MuonEG"]),
            get_nObj_min(1, 20., "Jet"),
            ], 

    #preselections = [onelep_plus_met],
    # preselections = [lep_met_2jets],
    preselections = [passthrough],
    categories = {
        "ee":[get_nObj_eq(0, coll="MuonGood"),get_nObj_eq(2, coll="ElectronGood")],
        "mumu":[get_nObj_eq(2, coll="MuonGood"),get_nObj_eq(0, coll="ElectronGood")],
        "emu":[get_nObj_eq(1, coll="MuonGood"),get_nObj_eq(1, coll="ElectronGood")]
    },
   

    weights = {
        "common": {
            "inclusive": ["genWeight","lumi","XS",
                        #   "pileup",
                        #   "sf_mu_id","sf_mu_iso",
                        #   "sf_ele_reco","sf_ele_id",
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
                    # "pileup",
                    # "sf_mu_id", "sf_mu_iso",
                    # "sf_ele_reco", "sf_ele_id",
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
        # **count_hist(name="nBJets", coll="BJetGood",bins=8, start=0, stop=8),
        **jet_hists(coll="JetGood", pos=0),
        # **jet_hists(coll="JetGood", pos=1),

       

        "nJet": HistConf( [Axis(field="nJet", bins=15, start=0, stop=15, label=r"nJet direct from NanoAOD")] ),

        
        
        "MET_pt": HistConf( [Axis(coll="MET", field="pt", bins=50, start=0, stop=200, label=r"MET $p_T$ [GeV]")] ),
        "MET_phi": HistConf( [Axis(coll="MET", field="phi", bins=64, start=-math.pi, stop=math.pi, label=r"MET $phi$")] ),

    }
)


run_options = {
    "executor"       : "futures",
    "env"            : "conda",
    "workers"        : 1,
    "scaleout"       : 5,
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
    