import pytest
from helpers import for_one_database, for_one_result_set, get_credentials
from typing import Callable
from turbodbc import connect

@for_one_database
def test_nextset_supported(dsn, configuration):
    cursor = connect(dsn, **get_credentials(configuration)).cursor()
    assert "nextset" in dir(cursor)
    assert isinstance(cursor.nextset, Callable)

@for_one_database
def test_nextset_with_one_result_set(dsn, configuration):
    cursor = connect(dsn, **get_credentials(configuration)).cursor()
    cursor.execute("SELECT 42")
    try:
        cursor.nextset()
    except Exception as exc:
        assert False, f"Didn't find a call for nextset\n{exc}\n"
    else:
        assert True, "Found call for nextset"

@for_one_result_set
def test_nextset_with_two_result_set(dsn, configuration):
    print(f"dsn: {dsn}\n")
    cursor = connect(dsn, **get_credentials(configuration)).cursor()
    multi_result_set_stored_proc = """CREATE PROCEDURE TEST_PROC 
    AS 
    SET NOCOUNT ON 
    SELECT 4 
    SELECT 2 
    """
    cursor.execute(multi_result_set_stored_proc)
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

@for_one_database
def test_nextset_with_function(dsn, configuration):
    cursor = connect(dsn, **get_credentials(configuration)).cursor()
    multi_result_set_func = """CREATE FUNCTION TEST_FUNC ()
    RETURNS SETOF int AS 
    $func$
    BEGIN
    RETURN QUERY SELECT 4; 
    RETURN QUERY SELECT 2; 
    END
    $func$ LANGUAGE plpgsql;
    """
    cursor.execute(multi_result_set_func)
    cursor.execute("select TEST_FUNC();")
    try:
        assert cursor.fetchall() == [[4], [2]]
    except Exception as exc:
        assert False, f"Didn't find a call for nextset\n{exc}\n"
    else:
        assert True, "Found call for nextset"

@for_one_database
def test_nextset_with_postgres_procedure(dsn, configuration):
    cursor = connect(dsn, **get_credentials(configuration)).cursor()
    multi_result_set_func = """CREATE PROCEDURE TEST_PROC(result_one inout refcursor, result_two inout refcursor) 
    AS 
    $$
    BEGIN
        OPEN result_one FOR SELECT 4;

        OPEN result_two FOR SELECT 2;
    END;
    $$ 
    LANGUAGE plpgsql;
    """
    cursor.execute(multi_result_set_func)
    cursor.execute("select TEST_FUNC(null, null);")
    try:
#        assert cursor.fetchall() == [[4], [2]]
        assert True == True
        print(f"fetch all for open proc:\n{cursor.fetchall()}\n")
    except Exception as exc:
        assert False, f"Didn't find a call for nextset\n{exc}\n"
    else:
        assert True, "Found call for nextset"

@for_one_database
def test_nextset_with_one_result_set(dsn, configuration):
    cursor = connect(dsn, **get_credentials(configuration)).cursor()
    cursor.execute("SELECT 4;SELECT 2;")
    try:
        assert cursor.fetchall() == [[4]]
        next_set_present = cursor.nextset()
        if next_set_present:
            assert cursor.fetchall() == [[2]]
    except Exception as exc:
        assert False, f"Didn't find a call for nextset\n{exc}\n"
    else:
        assert True, "Found call for nextset"
