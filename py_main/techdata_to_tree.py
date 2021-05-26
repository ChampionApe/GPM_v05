""" This script loads a technology catalog, which must have a particular form, 
and constructs the nesting tree that it implies."""

#%% Packages


import os
import re
import pandas as pd
import numpy as np
from pandas.core.indexes import base
# import DataBase



#%% Load catalog
testing = False
if testing:
    sheets = pd.read_excel(os.getcwd() + "/../examples/Abatement/Data/techdata_new.xlsx", sheet_name=["inputdisp", "inputprices"])
    dict_with_techcats = sheets
    #inputdisp = sheets["inputdisp"]
    #inputprices = sheets["inputprices"]
    #endofpipe = sheets["endofpipe"]

# %% Functions to diagnose catalogs (input-displacing and end-of-pipe)

def diagnose_inputdisp(inputdisp):
    print("diagnosing")

def diagnose_endofpipe(endofpipe):
    print("diagnosing")


#%% Functions to load catalogs. This assumes that they have the correct structure (diagnose-functions should check that)

def next_U(U_list, tech):

    assert isinstance(U_list, list)

    if len(U_list) == 0:
        U = "U_" + str(tech) + "_1"
    elif len(U_list) > 0:
        U = "U_" + str(tech) + "_" + str(int(U_list[len(U_list) - 1].split("_")[-1]) + 1)

    return U

def next_C(C_list, E):

    assert isinstance(C_list, list)

    if len(C_list) == 0:
        C = "C_" + str(E) + "_1"
    elif len(C_list) > 0:
        C = "C_" + str(E) + "_" + str(int(C_list[len(C_list) - 1].split("_")[-1]) + 1)

    return C

def multiindex_series(idx_level_names, idx_name=None, series_name=None):
    if idx_name is None and series_name is not None:
        idx_name = series_name
    elif idx_name is not None and series_name is None:
        series_name = idx_name
    elif idx_name is None and series_name is None:
        raise Exception("Supply either index name or series name")
    idx = pd.MultiIndex(levels=[[]]*len(idx_level_names), codes=[[]]*len(idx_level_names), names=idx_level_names)
    ser = pd.Series(index=idx, dtype=float)
    ser.rename(series_name, inplace=True)
    #ser.index.name = idx_name
    return ser




#Index entries should always be of the form ["branch", "node"]. This means it does not necessarily follow the verticual order of the tree (switches with output/input)

def get_prefix(techcat_type):
    if techcat_type == "inputdisp":
        prefix = "ID"
    elif techcat_type == "endofpipe":
        prefix = "EOP"
    return prefix

def intensity_or_share(techcat_type):
    """ inputs must be named input_int_[NAME] for inputdisp and with 'share' replacing 'int' for end of pipe"""

    if techcat_type == "inputdisp":
        mu_type = "int"
    elif techcat_type == "endofpipe":
        mu_type = "share"
    return mu_type
    
def find_key_from_value(d, value):
    assert isinstance(d, dict)
    out = []
    for (k, v) in d.items():
        if value in v:
            out.append(k)
    if len(out) == 1:
        return out[0]
    else:
        raise Exception("Value exists in multiple keys")


#%%



def load_techcats(dict_with_techcats):
    #The final output container
    output = {}
    inputprices = dict_with_techcats["inputprices"]


    # testing=False
    if testing:
        techcat_type = "inputdisp"

    for techcat_type in dict_with_techcats:
        if techcat_type not in ["inputdisp", "endofpipe"]:
            continue
        df = dict_with_techcats[techcat_type]
        prefix = get_prefix(techcat_type)

        output[prefix] = {}

        #Empty mu container
        mu = multiindex_series(idx_level_names=["n", "nn"], series_name="mu")

        #Empty potential coverages container (shares that components make up of their upper categories (energy services or emission types))
        coverage_potentials = multiindex_series(idx_level_names=["n", "nn"], series_name="coverage_potentials")
        #Empty current coverage container (shares that technology goods (U) make up of their upper categories (E or M))
        current_coverages = multiindex_series(idx_level_names=["n", "nn"], series_name="current_coverages")


        #Technologies
        tech_series = prefix + "_" + df["tech"].astype("str")
        techs = {str(tech):[] for tech in tech_series}
        techs_inputs = techs.copy()
        techs_replace = techs.copy()

        unit_costs = pd.concat([tech_series, df["unit_cost"]], axis=1)

        #Inputs
        mu_type = intensity_or_share(techcat_type) #intensity or share
        input_cols = [col for col in df.columns if "input_" + mu_type + "_" in col]
        inputs = pd.Series([col[len("input_" + mu_type + "_"):] for col in input_cols])

        #Replace energy mix
        replace_cols = [col for col in df.columns if "replace_share_" in col]

        #Energy services / emission types
        upper_categories = {col[0:len(col)-len("_coverage_pot")]:[] for col in df.columns if "_coverage_pot" in col}
        
        #Number of potential overlaps (simply deduces it from xlsx structure)
        n_overlaps = len([col for col in df.columns if "_overlap_" in col])/ (len(upper_categories) * 2)

        #Object for making a mapping that tells us that multiple quantities must have the same price.
        Q2P = []

        #Components object
        components = {}

        # testing=False
        if testing:
            i = 0
            tech = tech_series[0]

        for i, tech in enumerate(tech_series):
            # print(i)
            # print(tech)

            #Relevant inputs for technology
            tech_inputs = list(inputs[list(np.where(df[input_cols].iloc[i, :] > 0)[0])])
            techs_inputs[tech] = [tech + "_" + inp for inp in tech_inputs] + [tech + "_K"]
            # if df[replace_cols].iloc[i, :].isna().all():
            #     techs_replace[tech] = np.nan
            # else:
            techs_replace[tech] = df[replace_cols].iloc[i, :]

            energy_costs = 0

            if testing:
                i_input = "electricity"

            for i_input in tech_inputs:
            # Add to mu (nest combining non-capital inputs and capital into tau). 
                mu[(tech + "_" + i_input, tech)] = df.loc[i, "input_" + mu_type + "_" + i_input]
                #Calculate each energy input's contribution to the unit cost and add it to energy_costs
                energy_costs += inputprices.set_index("input").loc[i_input, "price"] * df.loc[i, "input_" + mu_type + "_" + i_input]

            #Capital constitutes the remainder of the costs between the stated unit cost and the costs related to energy:
            mu[(tech + "_K", tech)] = (unit_costs.loc[i, "unit_cost"] - energy_costs)/inputprices.set_index("input").loc["K", "price"] 

            if mu[(tech + "_K", tech)] < 0: 
                print("Negative share parameter for capital: Stated unit costs inconsistent with energy prices and/or input intensities/shares")
                print("Technology was: " + tech)
                raise Exception("negative share parameter")



            #Add to Q2P
            [Q2P.append((tech + "_" + inp, inp)) for inp in tech_inputs]
            Q2P.append((tech + "_K", "K"))

            if testing:
                E = list(upper_categories.keys())[0]

            for E in upper_categories:
            
                potential = df.loc[i, E + "_coverage_pot"]
                if potential > 0:

                    shares = df[[E + "_overlap_" + str(n_overlap) + "_potshare" for n_overlap in list(range(1, int(n_overlaps) + 1))]].iloc[i, :]
                    
                    if (all(shares.isna()) or shares.sum() < 1):

                        C = next_C(upper_categories[E], E)
                        upper_categories[E].append(C)
                        
                        #Add to mu object. The non-overlapping part of potential (not for EOP because Cs are the output) 
                        
                        solo_potential = potential * (1 - shares.sum())
                        coverage_potentials[(C, E)] = solo_potential
                        if techcat_type == "inputdisp":
                            mu[(C, E)] = solo_potential

                        #Create technology good
                        U = next_U(techs[tech], tech)
                        components[C] = [U]
                        techs[tech].append(U)

                        #Add current coverage to mu, as the share parameter in the output nest from T to U (technologies to their technology goods)
                        curr_coverage = df.loc[i, E + "_coverage_curr"]
                        total_curr_coverage = (df.loc[i, [e + "_coverage_curr" for e in upper_categories]]).sum()
                        
                        solo_curr_coverage = curr_coverage * (1-shares.sum())
                        current_coverages[(U, E)] = solo_curr_coverage
                        #add to mu (we divide by total curr_coverage to make sure that the mus from T to U sum to 1 (scale-preservance))
                        mu[(U, tech)] = solo_curr_coverage / total_curr_coverage

                        if testing:
                            j = "EL_overlap_1_potshare"
                            share = 0.25

                        for j, share in shares.items():
                            if share > 0:
                                #identify the technologies that this potential is shared with:
                                othertechs = [prefix + "_" + othertech for othertech in str(df[E + "_overlap" + re.search("_[0-9]+_", j)[0] + "othertechs"][i]).split(",")]
                                #Check if this component has been dealt with earlier and so should not be constructed again
                                if i > np.min([tech_series[tech_series == othertech].index[0] for othertech in othertechs]):
                                    continue
                                else:
                                    #Construct new component, technology goods (for current tech as well as the ones it overlaps with)
                                    U = next_U(techs[tech], tech)
                                    techs[tech].append(U)

                                    overlap_curr_coverage = share * curr_coverage

                                    #Current coverage tells us the value of U/E, which we store later calibration
                                    current_coverages[(U, E)] = overlap_curr_coverage

                                    #Add to mu (again, we divide by total curr_coverage to ensure the mus sum to 1)
                                    mu[(U, tech)] = overlap_curr_coverage / total_curr_coverage

                                    #Component
                                    C = next_C(upper_categories[E], E)
                                    upper_categories[E].append(C)
                                    
                                    #The potential reflects C/E:
                                    overlap_coverage_potential = potential * share
                                    coverage_potentials[(C, E)] = overlap_coverage_potential

                                    #Add to mu if input-displacing, where components are actually combined into E (in EOP the component themselves are the outputs)
                                    if techcat_type == "inputdisp":
                                        mu[(C, E)] = overlap_coverage_potential

                                    #initialize list of technology goods under this component
                                    components[C] = [U]

                                    if testing:
                                        othertech = "ID_2"

                                    for othertech in othertechs:
                                        U = next_U(techs[othertech], othertech)
                                        techs[othertech].append(U)
                                        components[C].append(U)

                                        #Find the share that this overlap constitutes for othertech
                                        #First reconstruct the list of overlapping techs as it will appear in othertech's line in the catalog
                                        overlapping_techs = ",".join([t for t in [tech.split("_", 1)[1]] + [t.split("_", 1)[1] for t in othertechs] if t != othertech.split("_", 1)[1]])
                                        #row contains the row corresponding to othertech in the catalog
                                        row = df[df.loc[:, "tech"].astype(str) == othertech.split("_", 1)[1]]
                                        #Find the exact field where this data is stored, and retrieve the corresponding overlap share:
                                        #Calculate the current coverage (of this overlapping part) as a share of the technology's total current coverage.
                                        othertech_curr_potential = row[E + "_coverage_curr"].values[0] * row.loc[:, list(row.columns[(row.astype(str) == overlapping_techs).all()])[0].replace("othertechs", "potshare")].values[0]
                                        current_coverages[(U, E)] = othertech_curr_potential

                                        mu[(U, othertech)] = (othertech_curr_potential / row[[e + "_coverage_curr" for e in upper_categories]].sum(axis=1)).values[0]

        mu2 = mu.reset_index()
        mu2 = mu2.loc[mu2["n"].str.startswith(("U")), :]

        for t in mu2.nn.unique():
            if t[:2] == "ID":
                if round(mu2[mu2.loc[:, "nn"] == t]["mu"].sum(), 2) != 1:
                    print(mu2[mu2.loc[:, "nn"] == t]["mu"])
                    raise Exception("mus from tau to Us don't sum to one. They must (scale preserving). The problem is for " + t + ".")

        #There are no baseline components nor baseline technology goods in the end of pipe sector.
        if techcat_type == "inputdisp":
            #Add baseline elements to components, and inputs to baseline technology goods (U)

            baseline_U_inputs = {}
            IO_tech = {}
            IO_tech["IO_tech"] = []
            if testing:
                c = list(components.keys())[1]
            for c in components:
                base_U = "U_" + prefix + "_" + c + "_base"


                #Check whether the underlying technologies have specified the fuels that they replace.
                c_techs = [find_key_from_value(techs, U) for U in components[c]]
                if testing:
                    c_t = c_techs[0]
                
                replace_vectors_weight = 0
                replace_vectors = pd.Series(index=replace_cols, dtype=float)
                for c_t in c_techs:
                    if not techs_replace[c_t].isna().all():
                        replace_vectors_weight += 1
                if replace_vectors_weight == 0:
                    #Add the baseline_Us without replacement vectors to the output of the overall IO baseline tech
                    IO_tech["IO_tech"].append(base_U)
                else:
                    replace_vectors_weight = 1/replace_vectors_weight 
                    for c_t in c_techs:
                        if techs_replace[c_t].isna().all():
                            continue
                        else:
                            replace_vectors = pd.concat([replace_vectors, replace_vectors_weight*techs_replace[c_t]], axis=1).sum(axis=1)
                    assert replace_vectors.sum() == 1
                    replace_vectors = replace_vectors[replace_vectors > 0]
                    baseline_U_inputs[base_U] = []
                    if testing:
                        inp = replace_vectors.index[0]
                    for inp in replace_vectors.index:
                        baseline_U_inputs[base_U] += [base_U + "_" + inp.split("replace_share_")[1]]
                        mu[(base_U + "_" + inp.split("replace_share_")[1], base_U)] = replace_vectors[inp]
                            
                components[c].append(base_U)


                #Add the latter to Q2P as well:
                [Q2P.append(("U_" + prefix + "_" + c + "_base_" + inp, inp)) for inp in inputs]
                Q2P.append(("U_" + prefix + "_" + c + "_base_K", "K"))

        


            #Calculate mu-parameters for baseline components to be used below (they sum to 1 under E by construction):
            mu2 = mu.reset_index()
            mu2 = 1 - mu2.loc[mu2["nn"].isin(upper_categories.keys()), :].groupby("nn").sum()
                
            for E in upper_categories:
                upper_categories[E].append("C_" + E + "_base")
                mu[("C_" + E + "_base", E)] = mu2.loc[E, "mu"]
                # baseline_C_inputs["C_" + E + "_base"] = ["C_" + E + "_base_" + inp for inp in inputs] + ["C_" + E + "_base_K"]
                IO_tech["IO_tech"].append("C_" + E + "_base")
                
                #Add to Q2P
                # [Q2P.append(("C_" + E + "_base_" + inp, inp)) for inp in inputs]
                # Q2P.append(("C_" + E + "_base_K", "K"))


        if techcat_type == "inputdisp":
            IO_tech_inputs = {"IO_tech":["IO_tech_" + inp for inp in inputs]}
            [Q2P.append(("IO_tech_" + inp, inp)) for inp in inputs]
            Q2P.append(("IO_tech_K", "K"))

        Q2P = pd.MultiIndex.from_tuples(Q2P, names=["n", "nn"])


        output[prefix] = {"techs_inputs":techs_inputs, "techs":techs, "components":components, "upper_categories":upper_categories, 
                            "mu":mu, "Q2P":Q2P, "unit_costs":unit_costs, "current_coverages":current_coverages, "coverage_potentials":coverage_potentials}

        output["inputprices"] = inputprices.set_index("input")["price"]

        #Add baseline components if this is input-displacing technologies
        if techcat_type == "inputdisp":
            output[prefix]["IO_tech"] = IO_tech
            output[prefix]["IO_tech_inputs"] = IO_tech_inputs
            output[prefix]["baseline_U_inputs"] = baseline_U_inputs


    return output



#%% 

# def load_endofpipe(endofpipe):
#     tech_series = "EOP_" + endofpipe["tech"].astype(str)
#     techs = {str(tech):[] for tech in tech_series}
#     techs_inputs = techs.copy()

#     #Bottom (inputs) of the tree are easily retrieved
#     input_cols = [col for col in endofpipe.columns if "input_share_" in col]
#     inputs = pd.Series([col[len("input_share_"):] for col in input_cols])

#     #Emission types
#     emission_types = {col[0:len(col)-len("_coverage_pot")]:[] for col in endofpipe.columns if "_coverage_pot" in col}
#     #Number of potential overlaps
#     n_overlaps = len([col for col in endofpipe.columns if "_overlap_" in col])/ (len(emission_types) * 2)

#     Q2P = []
#     components = {}
    
#     if testing:
#         i = 0
#         tech = tech_series[0]


#     for i, tech in enumerate(tech_series):
#         tech_inputs = list(inputs[list(np.where(endofpipe[input_cols].iloc[i, :] > 0)[0])])
#         #if len(tech_inputs) > 0:
#         techs_inputs[tech] = [tech + "_" + inp for inp in tech_inputs] + [tech + "_K"]
        
#         #Add to Q2P
#         [Q2P.append((tech + "_" + inp, inp)) for inp in tech_inputs]
#         Q2P.append((tech + "_K", "K"))

#         if testing:
#             M = list(emission_types.keys())[1]
#         for M in emission_types:
                
#             shares = endofpipe[[M + "_overlap_" + str(n_overlap) + "_potshare" for n_overlap in list(range(1, int(n_overlaps) + 1))]].iloc[i, :]

#             if (all(shares.isna()) or shares.sum() < 1) and (endofpipe.loc[i, M + "_coverage_pot"] > 0):
#                 C = next_C(emission_types[M], M)
                
#                 emission_types[M].append(C)
#                 # append(E + "_comp_" + str(C_num))
                
#                 #Create technology good
#                 U = next_U(techs[tech], tech)
#                 components[C] = [U]
#                 techs[tech].append(U)

#             if testing:
#                 j = "SO2_overlap_1_potshare"
#                 share = 0.25
            
            
#             for j, share in shares.items():
#                 #n_overlap += 1
#                 if share > 0:
                    
#                     #identify the technologies that this potential is shared with:
#                     othertechs = ["EOP_" + othertech for othertech in str(endofpipe[M + "_overlap" + re.search("_[0-9]+_", j)[0] + "othertechs"][i]).split(",")]
#                     #Check if this component has been dealt with earlier and so should not be constructed again
#                     if i > np.min([tech_series[tech_series == othertech].index[0] for othertech in othertechs]):
#                         continue
#                     else:
#                         #Construct new component, technology goods (for current tech as well as the ones it overlaps with)

#                         #Technology good for current tech
#                         U = next_U(techs[tech], tech)
#                         techs[tech].append(U)
#                         #techs[tech].append("U_" + str(tech) + "_" + str("U_num"))

#                         #Component
#                         C = next_C(emission_types[M], M)
#                         emission_types[M].append(C)
#                         components[C] = [U]
                        
#                         #Technology goods for other techs
#                         for othertech in othertechs:
#                             U = next_U(techs[othertech], othertech)
#                             techs[othertech].append(U)
#                             components[C].append(U)

#     #Add baseline elements to components, and inputs to baseline technology goods (U)
#     baseline_U_inputs = {}
#     for c in components:
#         # E = c.split("_")[0]
#         components[c].append("U_EOP_" + c + "_base")
#         baseline_U_inputs["U_EOP_" + c + "_base"] = ["U_EOP_" + c + "_base_" + inp for inp in inputs] + ["U_EOP_" + c + "_base_K"]
#         #Add the latter to Q2P as well:
#         [Q2P.append(("U_EOP_" + c + "_base_" + inp, inp)) for inp in inputs]
#         Q2P.append(("U_EOP_" + c + "_base_K", "K"))

#     Q2P = pd.MultiIndex.from_tuples(Q2P, names=["n", "nn"])

#     return {"techs_inputs":techs_inputs, "techs":techs, "components":components, "emission_types":emission_types, "Q2P":Q2P, "baseline_U_inputs":baseline_U_inputs}

# #%%
# def load_inputdisp(inputdisp):
#     """Loads the input-displacing catalog and constructs a nesting tree from it"""
#     #Empty mu container:
#     mu = multitindex_series(idx_level_names=["n", "nn"], series_name="mu")

#     print("Loading input-displacing technology catalog.")

#     tech_series = "ID_" + inputdisp["tech"].astype(str)
#     techs = {str(tech):[] for tech in tech_series}
#     techs_inputs = techs.copy()


#     #Bottom (inputs) and top (services) of the tree are easily retrieved
#     input_cols = [col for col in inputdisp.columns if "input_int_" in col]
#     inputs = pd.Series([col[len("input_int_"):] for col in input_cols])

#     #energy_services = [col[0:len(col)-len("_coverage_pot")] for col in inputdisp.columns if "_coverage_pot" in col]
#     energy_services = {col[0:len(col)-len("_coverage_pot")]:[] for col in inputdisp.columns if "_coverage_pot" in col}
#     #baseline_C_potentials = {e:1 for e in energy_services}

#     #The number of potential overlaps per technology. (simply counts how many column-pairs with overlap information that are present)
#     #Divides by 2 because there are pairs. Divides by the number of energy services because the number n_overlaps is duplicated for each, 
#     #using a prefix that refers to the name of the energy service.
#     n_overlaps = len([col for col in inputdisp.columns if "_overlap_" in col])/ (len(energy_services) * 2)

#     #delete:
#     #np.max([int(col[len(energy_services[0] + "_overlap_"):len(col)-len("_potshare")]) \
#     #                     for col in inputdisp.columns if all([s in col for s in [energy_services[0] + "_overlap_", "_potshare"]])])

#     #A map reflecting that energy inputs, say oil, can be used by multiple technologies while in essence it's the same oil. So there are multiple
#     #quantities of oil, but they must all have the same price! We collect this correspondence from "different" oil quantities back to simply "oil"
#     #in the list Q2P, as tuples, which can than later be converted into a multiindex

#     Q2P = []

#     #%%

#     #Go through each technology, and create components. Each technology gets a component for each time it has a unique part of its potential
#     #that it shares with another technology. If the sum of shared parts is less than 100 percent, it will get a final component where it does
#     #not compete with other technologies (and only a baseline technology, which is added later)

    
#     if testing:
#         i = 0
#         tech = tech_series[0]

#     #initialize
#     components = {}

#     for i, tech in enumerate(tech_series):
#         # print(i)
#         # print(tech)

#         tech_inputs = list(inputs[list(np.where(inputdisp[input_cols].iloc[i, :] > 0)[0])])
        
#         techs_inputs[tech] = [tech + "_" + inp for inp in tech_inputs] + [tech + "_K"]
#         for i_input in tech_inputs:
#             # Add to mu (nest combining non-capital inputs and capital into tau). 
#             # We do not include capital here, because the unit cost is not sufficient information 
#             mu[(tech + "_" + i_input, tech)] = inputdisp.loc[i, "input_int_" + i_input]

#         #Add to Q2P
#         [Q2P.append((tech + "_" + inp, inp)) for inp in tech_inputs]
#         Q2P.append((tech + "_K", "K"))

#         if testing:
#             E = list(energy_services.keys())[0]

#         for E in energy_services:
            
#             potential = inputdisp.loc[i, E + "_coverage_pot"]
#             if potential > 0:

#                 shares = inputdisp[[E + "_overlap_" + str(n_overlap) + "_potshare" for n_overlap in list(range(1, int(n_overlaps) + 1))]].iloc[i, :]
                
#                 if shares.sum() < 1:
                    
#                     C = next_C(energy_services[E], E)
#                     energy_services[E].append(C)
                    
#                     #Add to mu object. The non-overlapping part of potential. 
#                     mu[(C, E)] = potential * (1 - shares.sum())
#                     #baseline_C_potentials[E] -= potential * (1 - shares.sum())
                    
#                     #Create technology good
#                     U = next_U(techs[tech], tech)
#                     components[C] = [U]
#                     techs[tech].append(U)

#                     #Add current coverage to mu, as the share parameter in the output nest from T to U (technologies to their technology goods)
#                     curr_coverage = inputdisp.loc[i, E + "_coverage_curr"]
                    
#                     #Should make sure that all potentials have a non-zero current coverage (corner solutions avoided.)
#                     #if curr_coverage == 0:
#                         #if zero current coverage, set it to 1 percent to avoid corner solutions.
#                         #curr_coverage = 0.01
                    
#                     #The share of current coverage not overlapping with anything
#                     total_curr_coverage = (inputdisp.loc[i, [e + "_coverage_curr" for e in energy_services]]).sum()
#                     mu[(U, tech)] = (1- shares.sum()) * curr_coverage / total_curr_coverage


#                 #n_overlap = 0
#                 if testing:
#                     j = E + "_overlap_2_potshare"
#                     share = 0.25
#                 for j, share in shares.items():
#                     #n_overlap += 1
#                     if share > 0:
                        
#                         #identify the technologies that this potential is shared with:
#                         othertechs = ["ID_" + othertech for othertech in str(inputdisp[E + "_overlap" + re.search("_[0-9]+_", j)[0] + "othertechs"][i]).split(",")]
#                         #Check if this component has been dealt with earlier and so should not be constructed again
#                         if i > np.min([tech_series[tech_series == othertech].index[0] for othertech in othertechs]):
#                             continue
#                         else:
#                             #Construct new component, technology goods (for current tech as well as the ones it overlaps with)

#                             #Technology good for current tech
#                             U = next_U(techs[tech], tech)
#                             techs[tech].append(U)
#                             #Add to mu
#                             mu[(U, tech)] = share * curr_coverage / total_curr_coverage

#                             #Component
#                             C = next_C(energy_services[E], E)
#                             energy_services[E].append(C)
#                             #Add to mu
#                             mu[(C, E)] = potential * share

#                             #initialize list of technology goods under this component
#                             components[C] = [U]
                            
#                             #Technology goods for other techs
#                             if testing:
#                                 othertech = "ID_2"
#                             for othertech in othertechs:
#                                 U = next_U(techs[othertech], othertech)
#                                 techs[othertech].append(U)
                                
#                                 #Find the share that this overlap constitutes for othertech
#                                 #First find the overlapping
#                                 overlapping_techs = ",".join([t for t in [tech.split("_", 1)[1]] + [t.split("_", 1)[1] for t in othertechs] if t != othertech.split("_", 1)[1]])
#                                 row = inputdisp[inputdisp.loc[:, "tech"].astype(str) == othertech.split("_", 1)[1]]
#                                 #Find the exact field where this data is stored, and retrieve the corresponding overlap share:
#                                 #Calculate the current coverage (of this overlapping part) as a share of the technology's total current coverage.
#                                 try:
#                                     mu[(U, othertech)] = (row.loc[:, list(row.columns[(row.astype(str) == overlapping_techs).all()])[0].replace("othertechs", "potshare")].values[0] \
#                                                          * row[E + "_coverage_curr"] / row[[e + "_coverage_curr" for e in energy_services]].sum(axis=1)).values[0]
#                                 except:
#                                     raise Exception("STOP!")
#                                 #row[[E + "_overlap_" + str(n_overlap) + "_othertechs" for n_overlap in range(1, int(n_overlaps) + 1)]]

#                                 components[C].append(U)

#     mu2 = mu.reset_index()
#     mu2 = mu2.loc[mu2["n"].str.startswith(("U")), :]

#     for t in mu2.nn.unique():
#         if t[:2] == "ID":
#             if mu2[mu2.loc[:, "nn"] == t]["mu"].sum() != 1:
#                 raise Exception("mus from tau to Us don't sum to one. They must (scale preserving). The problem is for " + t + ".")

#     #Calculate mu-parameters for baseline components to be used below (they sum to 1 under E by construction):
#     mu2 = mu.reset_index()
#     mu2 = 1 - mu2.loc[mu2["nn"].isin(energy_services.keys()), :].groupby("nn").sum()

#     baseline_U_inputs = {}
#     #Add baseline elements to energy_services and components.
#     for c in components:
#         # E = c.split("_")[0]
#         components[c].append("U_ID_" + c + "_base")
#         baseline_U_inputs["U_ID_" + c + "_base"] = ["U_ID_" + c + "_base_" + inp for inp in inputs] + ["U_ID_" + c + "_base_K"]
#         #Add the latter to Q2P as well:
#         [Q2P.append(("U_ID_" + c + "_base_" + inp, inp)) for inp in inputs]
#         Q2P.append(("U_ID_" + c + "_base_K", "K"))

#     baseline_C_inputs = {}
#     for e in energy_services:
#         energy_services[e].append("C_" + e + "_base")
#         mu[("C_" + e + "_base", e)] = mu2.loc[e, "mu"]
#         baseline_C_inputs["C_" + e + "_base"] = ["C_" + e + "_base_" + inp for inp in inputs] + ["C_" + e + "_base_K"]
#         #Add to Q2P
#         [Q2P.append(("C_" + e + "_base_" + inp, inp)) for inp in inputs]
#         Q2P.append(("C_" + e + "_base_K", "K"))



#     Q2P = pd.MultiIndex.from_tuples(Q2P, names=["n", "nn"])

#     return {"techs_inputs":techs_inputs, "techs":techs, "components":components, "upper_categories":energy_services, 
#             "Q2P":Q2P, "mu":mu, "baseline_C_inputs":baseline_C_inputs, "baseline_U_inputs":baseline_U_inputs}

# # %%

# # o = load_inputdisp(inputdisp)
# # o2 = load_techcats(sheets)
# # o2["ID"]