from pytomography.io.SPECT import dicom
from pytomography.priors import RelativeDifferencePrior, QuadraticPrior, LogCoshPrior, TopNAnatomyNeighbourWeight
from Logic.VtkkmrmlUtils import *

def selectPrior(prior_type, prior_beta, prior_delta, prior_gamma, files_NM, bed_idx, 
                index_peak, N_prior_anatomy_nearest_neighbours, prior_anatomy_image_file):
    if prior_type=='None':
        return None
    else:
        if prior_anatomy_image_file is not None:
            files_CT = filesFromNode(prior_anatomy_image_file)
            prior_anatomy_image = dicom.get_attenuation_map_from_CT_slices(files_CT, files_NM[bed_idx], index_peak)
            prior_weight = TopNAnatomyNeighbourWeight(prior_anatomy_image, N_neighbours=N_prior_anatomy_nearest_neighbours)
        else:
            prior_weight = None
        if prior_type=='RelativeDifferencePenalty':
            prior = RelativeDifferencePrior(beta=prior_beta, gamma=prior_gamma, weight=prior_weight)
            return prior
        elif prior_type=='Quadratic':
            prior = QuadraticPrior(beta=prior_beta, delta=prior_delta, weight=prior_weight)
            return prior
        elif prior_type=='LogCosh':
            prior = LogCoshPrior(beta=prior_beta, delta=prior_delta, weight=prior_weight)
            return prior
