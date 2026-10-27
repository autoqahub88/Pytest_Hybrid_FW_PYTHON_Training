import configparser
from pathlib import Path
import pandas as pd
import inspect
import datetime
from datetime import datetime
from utilites import logger as log

logger = log.setup_logger("file_handling")

def read_ini_file(section_name,key_name):
    """
    ***************************************************************************************************
    Author        : B. Nagaraju
    Creation Date : Oct 2026
    Purpose       : This function help us to read the data from the ini file based on section_name and key_name
    Input helps
    section_name : Users
    key_name = success_mg
    ***************************************************************************************************
    """
    current_function_name = get_function_name()
    try:
        config = configparser.ConfigParser()
        file_path = Path(__file__).resolve().parents[1] / "configuration/global_msg.ini"
        config.read(file_path)
        key_data = config[section_name][key_name]
        logger.info(f"Function-'{current_function_name}'- successfully retrieved the data from ini file"
                    f" for the section '{section_name}' and key '{key_name}' and key data is '{key_data}' ")
        return key_data
    except Exception as exe:
        error_msg = (f"Function-'{current_function_name}'- Failed to retrieve the data from the ini file "
                         f" for the section '{section_name}' and key_name is '{key_name}'.Reason: {exe}")
        logger.exception(error_msg)
        raise RuntimeError(error_msg) from exe

def read_test_data(sheet_name,test_case_name):
    """
    ************************************************************
    Author: Nagaraju B
    Creation Date: Oct 2026
    Purpose: This function helps to select an item.
    Input help
    sheet_name : Users
    test_case_name: test_create_user_with_manadatory_fields
    **************************************************************
    """
    current_function_name = get_function_name()
    try:
        file_path = Path(__file__).resolve().parents[1] / "testdata/TestData_ActTime.xlsx"
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        filtered_df = df[df["Test_Case_Name"] == test_case_name]
        if filtered_df.empty:
            raise ValueError(f"Test case '{test_case_name}' not found")

        test_data = filtered_df.iloc[0].to_dict()
        test_data = {k:("nothing" if pd.isna(v) else v) for k,v in test_data.items()}
        logger.info(f"Function- '{current_function_name}'- successfully retrieved the data for the test case"
                    f" '{test_case_name}'- and testdata is '{test_data}' ")
        return test_data

    except Exception as exe:
        error_msg = (f"Function-'{current_function_name}'- Failed to retrieve the test data for the test case"
                         f" '{test_case_name}' .Reason: {exe}")
        logger.exception(error_msg)
        raise RuntimeError(error_msg) from exe

def get_function_name():
    return inspect.stack()[1].function

def get_timestamp():
    return "_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
