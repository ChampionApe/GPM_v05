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
    sheets = pd.read_excel(os.getcwd() + "/../examples/Abatement/Data/techdata_new2ID_only_simple_2Twith2overlap_simple.xlsx", sheet_name=["inputdisp", "inputprices"])
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

        if techcat_type == "inputdisp":
            #Empty potential coverages container (shares that components make up of their upper categories (energy services or emission types))
            coverage_potentials = multiindex_series(idx_level_names=["n", "nn"], series_name="coverage_potentials_ID")     
            #Empty current coverage container (shares that technology goods (U) make up of their upper categories (E or M))
            current_applications = multiindex_series(idx_level_names=["n", "nn"], series_name="current_applications_ID")
            current_coverages_split = multiindex_series(idx_level_names=["n", "nn"], series_name="current_coverages_split_ID")
        elif techcat_type == "endofpipe":
            #Empty potential coverages container (shares that components make up of their upper categories (energy services or emission types))
            coverage_potentials = multiindex_series(idx_level_names=["n", "z"], series_name="coverage_potentials_EOP")     
            #Empty current coverage container (shares that technology goods (U) make up of their upper categories (E or M))
            current_applications = multiindex_series(idx_level_names=["z", "n"], series_name="current_applications_EOP")
            current_coverages_split = multiindex_series(idx_level_names=["n", "z"], series_name="current_coverages_split_EOP")

        #Technologies
        tech_series = prefix + "_" + df["tech"].astype("str")
        techs = {str(tech):[] for tech in tech_series}
        techs_inputs = techs.copy()
        # techs_replace = techs.copy()

        unit_costs = pd.concat([tech_series, df["unit_cost"]], axis=1)

        #Inputs
        mu_type = intensity_or_share(techcat_type) #intensity or share
        input_cols = [col for col in df.columns if "input_" + mu_type + "_" in col]
        inputs = pd.Series([col[len("input_" + mu_type + "_"):] for col in input_cols])

        #Replace energy mix
        # replace_cols = [col for col in df.columns if "replace_share_" in col]

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
            # techs_replace[tech] = df[replace_cols].iloc[i, :]

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
                        current_applications[(E, tech)] = curr_coverage
                        total_curr_coverage = (df.loc[i, [e + "_coverage_curr" for e in upper_categories]]).sum()
                        
                        solo_curr_coverage = curr_coverage * (1-shares.sum())
                        current_coverages_split[(U, E)] = solo_curr_coverage
                        #add to mu (we divide by total curr_coverage to make sure that the mus from T to U sum to 1 (scale-preservance))
                        mu[(U, tech)] = solo_curr_coverage / total_curr_coverage

                        if testing:
                            j = E + "_overlap_1_potshare"
                            share = shares[j]

                        for j, share in shares.items():
                            if share > 0:
                                #identify the technologies that this potential is shared with:
                                othertechs = [prefix + "_" + othertech for othertech in str(df[E + "_overlap" + re.search("_[0-9]+_", j)[0] + "othertechs"][i]).split(",")]
                                # print(othertechs)
                                #Check if this component has been dealt with earlier and so should not be constructed again
                                if i > np.min([tech_series[tech_series == othertech].index[0] for othertech in othertechs]):
                                    continue
                                else:
                                    #Construct new component, technology goods (for current tech as well as the ones it overlaps with)
                                    U = next_U(techs[tech], tech)
                                    techs[tech].append(U)

                                    overlap_curr_coverage = share * curr_coverage

                                    #Current coverage tells us the value of U/E, which we store later calibration
                                    current_coverages_split[(U, E)] = overlap_curr_coverage

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
                                        othertech = othertechs[0]

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
                                        overlap_cols = [col for col in list(row.columns[(row.astype(str) == overlapping_techs).all()]) if col.startswith(E)]
                                        if len(overlap_cols) != 1:
                                            raise Exception("Must only find one column with these technologies overlapping, in this E")
                                        othertech_curr_potential = row[E + "_coverage_curr"].values[0] * row.loc[:, overlap_cols[0].replace("othertechs", "potshare")].values[0]
                                        current_coverages_split[(U, E)] = othertech_curr_potential

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

            mu2 = mu.reset_index()
            mu2 = 1 - mu2.loc[mu2["nn"].isin(upper_categories.keys()), :].groupby("nn").sum()


            # baseline_C_inputs["C_" + E + "_base"] = ["C_" + E + "_base_" + inp for inp in inputs] + ["C_" + E + "_base_K"]

            # baseline_U_inputs = {}
            basetechs = {}
            for E in upper_categories:
                basetechs["basetech_" + E] = []
                #baseline technology goods under each non-baseline component
                for c in upper_categories[E]:
                    U0 = "U0_" + prefix + "_" + c
                    components[c].append(U0)
                    basetechs["basetech_" + E].append(U0)
                #Then add baseline component and its baseline tech good
                upper_categories[E].append("C0_" + E)
                components["C0_" + E] = ["U0_" + prefix + "_" + "C0_" + E]
                mu[("C0_" + E, E)] = mu2.loc[E, "mu"]
                coverage_potentials[("C0_" + E, E)] = mu2.loc[E, "mu"] 
                basetechs["basetech_" + E].append("U0_" + prefix + "_" + "C0_" + E)

            # if testing:
            #     c = list(components.keys())[1]

            basetech_inputs = {}
            if testing:
                basetech = list(basetechs.keys())[0]

            for basetech in basetechs:
                basetech_inputs[basetech] = [basetech + "_" + inp for inp in list(inputs) + ["K"]]
                [Q2P.append((basetech + "_" + inp, inp)) for inp in list(inputs) + ["K"]]


        Q2P = pd.MultiIndex.from_tuples(Q2P, names=["n", "nn"])

        
        output[prefix] = {"techs_inputs":techs_inputs, "techs":techs, "components":components, "upper_categories":upper_categories, 
                            "mu":mu, "Q2P":Q2P, "unit_costs":unit_costs, "current_applications_" + prefix:current_applications, 
                            "current_coverages_split_" + prefix:current_coverages_split, "coverage_potentials_" + prefix:coverage_potentials}

        output["PwT"] = inputprices.set_index("input")["price"]
        output["PwT"].name = "PwT"
        output["PwT"].index.name = "n"

        #Add baseline components if this is input-displacing technologies
        if techcat_type == "inputdisp":
            output[prefix]["basetechs"] = basetechs
            output[prefix]["basetech_inputs"] = basetech_inputs
            # output[prefix]["baseline_U_inputs"] = baseline_U_inputs


    return output




# %%

# %%

# %%
