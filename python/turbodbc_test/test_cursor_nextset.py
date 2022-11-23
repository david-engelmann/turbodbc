import pytest
from helpers import for_one_database, for_one_result_set, get_credentials
from typing import Callable
from turbodbc import connect

@for_one_database
def test_nextset_supported(dsn, configuration):
    cursor = connect(dsn, **get_credentials(configuration)).cursor()
    assert "nextset" in dir(cursor)
    assert isinstance(cursor.nextset, Callable)

@for_one_result_set
def test_nextset_with_one_result_set(dsn, configuration):
    cursor = connect(dsn, **get_credentials(configuration)).cursor()
    print(f"options:\n{configuration}\ncursor:\n{dir(cursor)}\n")
    cursor.execute("SELECT 42")
    try:
        cursor.nextset()
    except Exception as exc:
        assert False, f"Didn't find a call for nextset\n{exc}\n"
    else:
        assert True, "Found call for nextset"

@for_one_result_set
def test_nextset_with_two_result_set(dsn, configuration):
    cursor = connect(dsn, **get_credentials(configuration)).cursor()
    stored_proc = """CREATE PROCEDURE TEST_PROC 
    AS 
    BEGIN 
    SET NOCOUNT ON 
    SELECT 4 
    SELECT 2 
    END"""
    cursor.execute(stored_proc)
    cursor.execute("EXEC TEST_PROC;")
    try:
        assert cursor.fetchall() == [[4]]
        next_set_present = cursor.nextset()
        if next_set_present:
            assert cursor.fetchall() == [[2]]
    except Exception as exc:
        assert False, f"Didn't find a call for nextset\n{exc}\n"
    else:
        assert True, "Found call for nextset"

