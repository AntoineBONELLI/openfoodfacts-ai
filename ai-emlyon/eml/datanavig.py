#----------------------------IMPORTS----------------------------

import pandas as pd
import numpy as np

#----------------------------FUNCTIONS----------------------------

#Drop cols based on a treshold, as int (abs count) or float (proportion)
def drop_cols (df, tresh=0.5, inplace=True, print_cols=True):
    """ 
    Drop all columns with the count of non-null values less than the treshold specified.
    Return a dictionnary with keys equal to the names of dropped columns, 
    and values equal to the type of dropped columns.
    
    Parameters
    ----------
    df : Pandas DataFrame
    tresh : Int or float, default 0.5
        The specified treshold.
        - if float:
            Compute an int treshold proportional to len(df).
            For example, 0.5 will return a value equal to 50% of len(df).
        - if integer:
            Use the number specified
    inplace : Boolean, default == True
        Apply changes inplace or not.
    print_cols : Boolean, default == True
        Print a progress with dropped columns names and dtypes.
        Format : "Column removed : {col} --- dtype : {coltype}"

    Return
    ------
    Return a dictionnary with keys equal to the names of dropped columns, 
    and values equal to the type of dropped columns.
    Example:
    {'energy_100g' : float, 'stores' : object}

    """
    cols_dropped = {}
    cols = df.columns.to_list()
    if isinstance(tresh, float): #if tresh is float
        treshold = int(len(df) * tresh) 
    else: #if tresh is int
        treshold = tresh
    for col in cols : #loop over columns
        coltype = str(df[col].dtype) #save col dtype
        col_count = df[col].count() #save col count (non-null values)
        if col_count < treshold :
            df.drop([col], axis=1, inplace=inplace) #drop the col
            to_update = {col:[coltype, col_count]} 
            cols_dropped.update(to_update) #append the dict
            if print_cols: #if print_cols is True
                print(f"Column removed : {col} --- dtype : {coltype}")
    return cols_dropped

#Drop cols in the off_cols_dict
def remove_cols_dict(cols_dict, cols_to_drop):
    if isinstance(cols_to_drop, dict):
        cols_to_drop = [col for col in cols_to_drop.keys()] #extract columns names in a list
    for group in cols_dict.keys(): #loop over the cols dict
        cols_dict[group] = [col for col in cols_dict[group] if col not in cols_to_drop] #keep only cols names not in cols_to_drop

#----------------------------DATA----------------------------

ppns2_list = ['appetizers',
 'artificially sweetened beverages',
 'biscuits and cakes',
 'bread',
 'breakfast cereals',
 'cereals',
 'cheese',
 'chocolate products',
 'dairy desserts',
 'dressings and sauces',
 'dried fruits',
 'eggs',
 'fats',
 'fish and seafood',
 'fruit juices',
 'fruit nectars',
 'fruits',
 'ice cream',
 'legumes',
 'meat',
 'milk and yogurt',
 'nuts',
 'offals',
 'one dish meals',
 'pastries',
 'pizza pies and quiche',
 'plant based milk substitutes',
 'potatoes',
 'processed meat',
 'salty and fatty products',
 'sandwiches',
 'soups',
 'sweetened beverages',
 'sweets',
 'teas and herbal teas and coffees',
 'unsweetened beverages',
 'vegetables',
 'waters and flavored waters']

off_columns_dict = {'robotoff':['robotoff_countries', 'robotoff_brands', 'robotoff_value_tag',
'robotoff_data.lang', 'robotoff_data.model', 'robotoff_data.confidence'],
'meta':['code',
 'url',
 'creator',
 'created_t',
 'created_datetime',
 'last_modified_t',
 'last_modified_datetime',
 'emb_codes',
 'emb_codes_tags',
 'states',
 'states_tags',
 'states_en'],
 'image':['image_url',
 'image_small_url',
 'image_ingredients_url',
 'image_ingredients_small_url',
 'image_nutrition_url',
 'image_nutrition_small_url'],
 'infopdt':[ 'product_name',
 'abbreviated_product_name',
 'generic_name',
 'quantity',
 'packaging',
 'packaging_tags',
 'packaging_text',
 'brands',
 'brands_tags',
 'stores',
 'serving_size',
 'serving_quantity',
 'nutriscore_score',
 'nutriscore_grade',
 'nova_group',
 'brand_owner'],
 'ingredients':[ 'labels',
 'labels_tags',
 'labels_en',
 'ingredients_text',
 'allergens',
 'traces',
 'traces_tags',
 'traces_en',
 'additives_n',
 'additives_tags',
 'additives_en',
 'ingredients_from_palm_oil_n',
 'ingredients_from_palm_oil_tags',
 'ingredients_that_may_be_from_palm_oil_n',
 'ingredients_that_may_be_from_palm_oil_tags',
 'nutriscore_score',
 'nutriscore_grade',
 'nova_group'],
 'cats':[ 'main_category',
 'main_category_en',
 'pnns_groups_1',
 'pnns_groups_2',
 'categories',
 'categories_tags',
 'categories_en'],
 'geo':['origins',
 'origins_tags',
 'origins_en',
 'manufacturing_places',
 'manufacturing_places_tags',
 'cities_tags',
 'countries',
 'countries_tags',
 'countries_en',
 'first_packaging_code_geo'],
 'empty':['cities',
 'allergens_en',
 'no_nutriments',
 'ingredients_from_palm_oil',
 'ingredients_that_may_be_from_palm_oil'],
 'dummy':['pnns_groups_1',
 'pnns_groups_2',
 'nutriscore_grade'],
 'tags':['categories_tags',
 'manufacturing_places_tags',
 'labels_tags',
 'emb_codes_tags',
 'cities_tags',
 'countries_tags'],
 '100g':['energy-kj_100g',
 'energy-kcal_100g',
 'energy_100g',
 'energy-from-fat_100g',
 'fat_100g',
 'saturated-fat_100g',
 '-butyric-acid_100g',
 '-caproic-acid_100g',
 '-caprylic-acid_100g',
 '-capric-acid_100g',
 '-lauric-acid_100g',
 '-myristic-acid_100g',
 '-palmitic-acid_100g',
 '-stearic-acid_100g',
 '-arachidic-acid_100g',
 '-behenic-acid_100g',
 '-lignoceric-acid_100g',
 '-cerotic-acid_100g',
 '-montanic-acid_100g',
 '-melissic-acid_100g',
 'monounsaturated-fat_100g',
 'polyunsaturated-fat_100g',
 'omega-3-fat_100g',
 '-alpha-linolenic-acid_100g',
 '-eicosapentaenoic-acid_100g',
 '-docosahexaenoic-acid_100g',
 'omega-6-fat_100g',
 '-linoleic-acid_100g',
 '-arachidonic-acid_100g',
 '-gamma-linolenic-acid_100g',
 '-dihomo-gamma-linolenic-acid_100g',
 'omega-9-fat_100g',
 '-oleic-acid_100g',
 '-elaidic-acid_100g',
 '-gondoic-acid_100g',
 '-mead-acid_100g',
 '-erucic-acid_100g',
 '-nervonic-acid_100g',
 'trans-fat_100g',
 'cholesterol_100g',
 'carbohydrates_100g',
 'sugars_100g',
 '-sucrose_100g',
 '-glucose_100g',
 '-fructose_100g',
 '-lactose_100g',
 '-maltose_100g',
 '-maltodextrins_100g',
 'starch_100g',
 'polyols_100g',
 'fiber_100g',
 '-soluble-fiber_100g',
 '-insoluble-fiber_100g',
 'proteins_100g',
 'casein_100g',
 'serum-proteins_100g',
 'nucleotides_100g',
 'salt_100g',
 'sodium_100g',
 'alcohol_100g',
 'vitamin-a_100g',
 'beta-carotene_100g',
 'vitamin-d_100g',
 'vitamin-e_100g',
 'vitamin-k_100g',
 'vitamin-c_100g',
 'vitamin-b1_100g',
 'vitamin-b2_100g',
 'vitamin-pp_100g',
 'vitamin-b6_100g',
 'vitamin-b9_100g',
 'folates_100g',
 'vitamin-b12_100g',
 'biotin_100g',
 'pantothenic-acid_100g',
 'silica_100g',
 'bicarbonate_100g',
 'potassium_100g',
 'chloride_100g',
 'calcium_100g',
 'phosphorus_100g',
 'iron_100g',
 'magnesium_100g',
 'zinc_100g',
 'copper_100g',
 'manganese_100g',
 'fluoride_100g',
 'selenium_100g',
 'chromium_100g',
 'molybdenum_100g',
 'iodine_100g',
 'caffeine_100g',
 'taurine_100g',
 'ph_100g',
 'fruits-vegetables-nuts_100g',
 'fruits-vegetables-nuts-dried_100g',
 'fruits-vegetables-nuts-estimate_100g',
 'collagen-meat-protein-ratio_100g',
 'cocoa_100g',
 'chlorophyl_100g',
 'carbon-footprint_100g',
 'carbon-footprint-from-meat-or-fish_100g',
 'nutrition-score-fr_100g',
 'nutrition-score-uk_100g',
 'glycemic-index_100g',
 'water-hardness_100g',
 'choline_100g',
 'phylloquinone_100g',
 'beta-glucan_100g',
 'inositol_100g',
 'carnitine_100g'],
 'numeric':['serving_quantity',
'additives_n',
'ingredients_from_palm_oil_n',
'ingredients_that_may_be_from_palm_oil_n',
'nutriscore_score',
'nova_group',
'energy-kj_100g',
 'energy-kcal_100g',
 'energy_100g',
 'energy-from-fat_100g',
 'fat_100g',
 'saturated-fat_100g',
 '-butyric-acid_100g',
 '-caproic-acid_100g',
 '-caprylic-acid_100g',
 '-capric-acid_100g',
 '-lauric-acid_100g',
 '-myristic-acid_100g',
 '-palmitic-acid_100g',
 '-stearic-acid_100g',
 '-arachidic-acid_100g',
 '-behenic-acid_100g',
 '-lignoceric-acid_100g',
 '-cerotic-acid_100g',
 '-montanic-acid_100g',
 '-melissic-acid_100g',
 'monounsaturated-fat_100g',
 'polyunsaturated-fat_100g',
 'omega-3-fat_100g',
 '-alpha-linolenic-acid_100g',
 '-eicosapentaenoic-acid_100g',
 '-docosahexaenoic-acid_100g',
 'omega-6-fat_100g',
 '-linoleic-acid_100g',
 '-arachidonic-acid_100g',
 '-gamma-linolenic-acid_100g',
 '-dihomo-gamma-linolenic-acid_100g',
 'omega-9-fat_100g',
 '-oleic-acid_100g',
 '-elaidic-acid_100g',
 '-gondoic-acid_100g',
 '-mead-acid_100g',
 '-erucic-acid_100g',
 '-nervonic-acid_100g',
 'trans-fat_100g',
 'cholesterol_100g',
 'carbohydrates_100g',
 'sugars_100g',
 '-sucrose_100g',
 '-glucose_100g',
 '-fructose_100g',
 '-lactose_100g',
 '-maltose_100g',
 '-maltodextrins_100g',
 'starch_100g',
 'polyols_100g',
 'fiber_100g',
 '-soluble-fiber_100g',
 '-insoluble-fiber_100g',
 'proteins_100g',
 'casein_100g',
 'serum-proteins_100g',
 'nucleotides_100g',
 'salt_100g',
 'sodium_100g',
 'alcohol_100g',
 'vitamin-a_100g',
 'beta-carotene_100g',
 'vitamin-d_100g',
 'vitamin-e_100g',
 'vitamin-k_100g',
 'vitamin-c_100g',
 'vitamin-b1_100g',
 'vitamin-b2_100g',
 'vitamin-pp_100g',
 'vitamin-b6_100g',
 'vitamin-b9_100g',
 'folates_100g',
 'vitamin-b12_100g',
 'biotin_100g',
 'pantothenic-acid_100g',
 'silica_100g',
 'bicarbonate_100g',
 'potassium_100g',
 'chloride_100g',
 'calcium_100g',
 'phosphorus_100g',
 'iron_100g',
 'magnesium_100g',
 'zinc_100g',
 'copper_100g',
 'manganese_100g',
 'fluoride_100g',
 'selenium_100g',
 'chromium_100g',
 'molybdenum_100g',
 'iodine_100g',
 'caffeine_100g',
 'taurine_100g',
 'ph_100g',
 'fruits-vegetables-nuts_100g',
 'fruits-vegetables-nuts-dried_100g',
 'fruits-vegetables-nuts-estimate_100g',
 'collagen-meat-protein-ratio_100g',
 'cocoa_100g',
 'chlorophyl_100g',
 'carbon-footprint_100g',
 'carbon-footprint-from-meat-or-fish_100g',
 'nutrition-score-fr_100g',
 'nutrition-score-uk_100g',
 'glycemic-index_100g',
 'water-hardness_100g',
 'choline_100g',
 'phylloquinone_100g',
 'beta-glucan_100g',
 'inositol_100g',
 'carnitine_100g']
 }