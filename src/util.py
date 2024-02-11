import pandas as pd
import re
import logging
import datetime
from collections import defaultdict
# define regex for valid characters in variable names
_VALID_CHARS = r'a-zA-Z0-9\_'

# valid element types
_VALID_TYPES = [
    'protein', 'protein family', 'protein complex',
    'rna', 'mrna', 'gene', 'chemical', 'biological process'
    ]

_VAR_COL = 'Variable'
_IDX_COL = '#'

def get_model_template(optional_columns=[], reading=pd.DataFrame()):

    model_columns = [
            'Variable',
            '#',
            'Element Name',
            'Element IDs',
            'Element Type',
            'Positive',
            'Negative',
            'Scenario']

    model_columns.extend(optional_columns)

    model_df = pd.DataFrame(columns=model_columns)

    if not reading.empty:
        # add ontology terms from reading
        elements = reading[
                ['Element Name','Element ID']
                ].rename(columns={
                        'Element Name' : 'Name',
                        'Element ID' : 'ID'
                        }).drop_duplicates()
        regulators = reading[
                ['Regulator Name','Regulator ID']
                ].rename(columns={
                        'Regulator Name' : 'Name',
                        'Regulator ID' : 'ID'
                        }).drop_duplicates()
        all_elements = elements.append(regulators).drop_duplicates()
        model_df['Variable'] = all_elements['Name']
        model_df['Element Name'] = all_elements['Name']
        model_df['Element IDs'] = all_elements['ID']
        model_df['#'] = model_df.reset_index().index
        model_df['Scenario'] = 1

    model_df.fillna('', inplace=True)

    return model_df

def get_model(model_file: str) -> pd.DataFrame:
    """Load model into a DataFrame and standardize column names
    """

    global _VALID_CHARS
    global _VAR_COL
    global _IDX_COL

    index_col_name = _IDX_COL
    var_col_name = _VAR_COL
    pos_reg_col_name = 'Positive Regulation Rule'
    pos_list_col_name = 'Positive List'
    neg_reg_col_name = 'Negative Regulation Rule'
    neg_list_col_name = 'Negative List'
    reg_list_col_name = 'Regulators'
    element_name_col_name = 'Element Name'
    ids_col_name = 'Element IDs'
    type_col_name = 'Element Type'

    # Load the input file containing elements and regulators
    model_sheets = pd.ExcelFile(model_file)
    # get the model from the first sheet, will check the other sheets for truth tables later
    model = model_sheets.parse(0,na_values='NaN',keep_default_na=False,index_col=None)

    # check model format
    if 'element attributes' in [x.lower() for x in model.columns]:
        # drop two header rows and set column names to third row
        model = model.rename(columns=model.iloc[1]).drop([0,1]).set_index(index_col_name)

    # get other sheets
    # TODO: parse truth tables here? or just return other sheets separately?
    if len(model_sheets.sheet_names) > 1:
        df_other_sheets = {sheet : model_sheets.parse(sheet,na_values='NaN',keep_default_na=False) \
            for sheet in model_sheets.sheet_names[1:]}
    else:
        df_other_sheets = ''

    # format model columns
    input_col_X = [
            x.strip() for x in model.columns
            if ('variable' in x.lower())
            ]
    input_col_A = [
            x.strip() for x in model.columns
            if ('positive regulation rule' in x.lower())
            ]
    input_col_I = [
            x.strip() for x in model.columns
            if ('negative regulation rule' in x.lower())
            ]
    input_col_initial = [
            x.strip() for x in model.columns
            if ('state list' in x.lower())
            ]

    input_col_name = [
            x.strip() for x in model.columns
            if ('element name' in x.lower())
            ]
    input_col_ids = [
            x.strip() for x in model.columns
            if ('element ids' in x.lower())
            ]
    input_col_type = [
            x.strip() for x in model.columns
            if ('element type' in x.lower())
            ]

    # check for all required columns or duplicate colummns
    if (len(input_col_X) == 0
            or len(input_col_A) == 0
            or len(input_col_I) == 0
            or len(input_col_initial) == 0
            ):
        raise ValueError(
                'Missing one or more required columns in input file: '
                'Variable, Positive Regulation Rule, Negative Regulation Rule, State List'
                )
    elif (len(input_col_X) > 1
            or len(input_col_A) > 1
            or len(input_col_I) > 1
            ):
        raise ValueError('Duplicate column of: Variable, Positive Regulation Rule, Negative Regulation Rule')

    if (len(input_col_name) == 0
            or len(input_col_ids) == 0
            or len(input_col_type) == 0
            ):
        raise ValueError(
                'Missing one or more required column names: '
                'Element Name, Element IDs, Element Type'
                )
    elif (len(input_col_name) > 1
            or len(input_col_ids) > 1
            or len(input_col_type) > 1
            ):
        raise ValueError(
                'Duplicate column of: '
                'Element Name, Element IDs, Element Type'
                )

    # TODO: check for other columns here as they are needed

    # processing
    # use # column or index to preserve order of elements in the model
    if index_col_name in model.columns:
        model.set_index(index_col_name,inplace=True)

    # remove rows with missing or marked indices
    model = drop_x_indices(model)

    model = model.reset_index()
    # standardize column names
    model = model.rename(
        index=str,
        columns={
            'index': index_col_name,
            input_col_X[0]: var_col_name,
            input_col_A[0]: pos_reg_col_name,
            input_col_I[0]: neg_reg_col_name,
            input_col_name[0]: element_name_col_name,
            input_col_ids[0]: ids_col_name,
            input_col_type[0]: type_col_name
        })

    # format invalid variable names
    model = format_variable_names(model)

    # standardize element types
    model['Element Type'] = model['Element Type'].apply(get_type)

    # set variable name as the index
    model.set_index(var_col_name,inplace=True)

    # check for empty indices
    if '' in model.index:
        raise ValueError('Missing variable names')
        # model = model.drop([''])

    # parse regulation functions into lists of regulators
    model[pos_list_col_name] = model[pos_reg_col_name].apply(
            lambda x: [y.strip() for y in re.findall('['+_VALID_CHARS+']+',x)]
            )
    model[neg_list_col_name] = model[neg_reg_col_name].apply(
            lambda x: [y.strip() for y in re.findall('['+_VALID_CHARS+']+',x)]
            )
    model[reg_list_col_name] = model.apply(
            lambda x:
            set(list(x[pos_list_col_name]) + list(x[neg_list_col_name])),
            axis=1
            )

    model.fillna('',inplace=True)

    return model

def drop_x_indices(model: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with missing or X indices
    """

    if 'X' in model.index or 'x' in model.index:
        logging.info('Dropping %s rows with X indices' % str(len(model.loc[['X']])))
        model.drop(['X'],axis=0,inplace=True)
    if '' in model.index:
        logging.info('Dropping %s rows missing indices' % str(len(model.loc[['']])))
        model.drop([''],axis=0,inplace=True)

    return model


def format_variable_names(model: pd.DataFrame) -> pd.DataFrame:
    """Format model variable names to make compatible with model checking
    """

    global _VALID_CHARS
    global _VAR_COL

    # remove whitespace in variable names
    model[_VAR_COL] = model[_VAR_COL].str.strip()

    # collect invalid element names in a list so they can be removed everywhere in the model
    # find invalid characters in element names and names starting with numbers
    invalid_names = [
        x for x in model[_VAR_COL]
        if re.search(r'(^[0-9]+)',x.strip()) or re.search(r'([^'+_VALID_CHARS+']+)',x.strip())
        ]

    if len(invalid_names) > 0:
        logging.info('Formatting variable names: ')

    # remove invalid characters at the start of the variable name
    replace_names = [re.sub(r'^[^'+_VALID_CHARS+']+','',x) for x in invalid_names]
    # replace invalid characters elsewhere in variable names
    replace_names = [re.sub(r'[^'+_VALID_CHARS+']+','_',x) for x in replace_names]

    # add ELE_ at the beginning of names starting with numbers
    replace_names = [re.sub(r'(^[0-9]+)','ELE_\\1',x) for x in replace_names]

    name_pairs = zip(invalid_names,replace_names)

    for (invalid_name,replace_name) in name_pairs:
        logging.info('%s -> %s' % (invalid_name,replace_name))
        model.replace(re.escape(invalid_name),re.escape(replace_name),regex=True,inplace=True)

    return model

def get_type(input_type):
    """Standardize element types
    """

    global _VALID_TYPES

    if input_type.lower() in _VALID_TYPES:
        return input_type
    elif input_type.lower().startswith('protein'):
        return 'protein'
    elif input_type.lower().startswith('chemical'):
        return 'chemical'
    elif input_type.lower().startswith('biological'):
        return 'biological'
    else:
        return 'other'

def model_to_dict(model: pd.DataFrame):
    """Convert model table to a dictionary
    """

    # convert dataframe to dict with variable name as the index
    model_dict = model.to_dict(orient='index')

    return model_dict


def get_model_from_delphi(model_file: str) -> pd.DataFrame:

    global _IDX_COL

    ##############       adding the spreadsheet column names to a dataframe        ############
    column_names = [_IDX_COL,'Element Name', 'Element IDs', 'Element Type', 'Agent',
                    'Patient', 'Value Judgment', 'Specificity', 'Location', 'Time Scale / Frequency',
                    'Value: Activity / Amount ', 'Element NOTES', 'Variable', 'Positive',
                    'Negative','Influence Set NOTES', 'Levels', 'Spontaneous Behavior',
                    'Balancing Behavior', 'Update Group', 'Update Rate', 'Update Rank', 'Delay', 'Mechanism',
                    'Weight', 'Regulator Level', 'Evidence', 'Initial 0']
    df_model = pd.DataFrame(columns=column_names)

    ##############     Reading the json as a dict    ############
    with open(model_file) as json_file:
        data = json.load(json_file)

    json_data = pd.DataFrame.from_dict(data, orient='index').T

    ############      creating a list of the variables and adding them to the dataframe    ############
    variables_list = list()

    for var in json_data['variables'][0]:
        variables_list.append(var['name'])

    df_model['Variable'] = variables_list
    df_model[_IDX_COL] = [x+1 for x in range(len(variables_list))]

    ############    Reading the edges     ############
    positive_edges = {key: [] for key in variables_list}
    negative_edges = {key: [] for key in variables_list}
    evidence_for_edge = {key: [] for key in variables_list}

    for edge in json_data['edge_data'][0]:
        source = edge['source']
        target = edge['target']

        subj_polarities = list()
        obj_polarities = list()
        for evidence in edge['InfluenceStatements']:
            subj_polarities.append(evidence['subj_delta']['polarity'])
            obj_polarities.append(evidence['obj_delta']['polarity'])

        # if number of 1s = number of -1s, choose the first polarity
        subj_polarity = subj_polarities[0]
        obj_polarity = obj_polarities[0]

        # number of 1s != number of -1s, choose the most frequent polarity
        if subj_polarities.count(1) != subj_polarities.count(-1):
            subj_polarity = 1
            if subj_polarities.count(1) < subj_polarities.count(-1):
                subj_polarity = -1

        if obj_polarities.count(1) != obj_polarities.count(-1):
            obj_polarity = 1
            if obj_polarities.count(1) < obj_polarities.count(-1):
                obj_polarity = -1

        if subj_polarity == 1 and obj_polarity == 1:
            positive_edges[target].append(source)
        elif subj_polarity == -1 and obj_polarity == 1:
            positive_edges[target].append('!'+source)
        elif subj_polarity == 1 and obj_polarity == -1:
            negative_edges[target].append(source)
        elif subj_polarity == -1 and obj_polarity == -1:
            negative_edges[target].append('!'+source)

        evidence = edge['InfluenceStatements'][0]['evidence'][0]['text']
        evidence_for_edge[target].append(evidence)

    df_model['Positive'] = [
        ','.join(positive_edges[key]) for key in variables_list]
    df_model['Negative'] = [
        ','.join(negative_edges[key]) for key in variables_list]
    df_model['Evidence'] = [
        ','.join(evidence_for_edge[key]) for key in variables_list]
    df_model['Initial 0'] = 1

    df_model.fillna('',inplace=True)

    return df_model
