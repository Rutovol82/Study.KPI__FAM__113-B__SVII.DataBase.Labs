-- Version: v2.0.2.4 // #lab-2 #intermediate-2.4
-- Description: Create functions provides injection/referencing of testing points entities.


-- Create get_test_point() function, that:
-- Provides obtaining educational testing point id (references "test_points"."point_id")
-- by passed point name and location territory id. In case when language entity corresponds passed name not exists -
-- inserts new row to "test_points" table, else takes first occurred row from existing.
-- In case when one or more passed names are NULL - returns NULL.

-- -- Define get_test_point() function
CREATE FUNCTION get_test_point(name_      test_points.point_name%TYPE,
                               location_  test_points.location_terr_id%TYPE)
    RETURNS test_points.point_id%TYPE
    LANGUAGE 'plpgsql'
AS $$
DECLARE id_ test_points.point_id%TYPE;     -- Variable will store obtained profile id
BEGIN
    -- Check that input point name is not NULL
    IF name_ is null THEN
        RETURN null;
    END IF;

    -- Try to select id from "test_points"
    SELECT point_id INTO id_
        FROM test_points WHERE test_points.point_name = name_ AND test_points.location_terr_id = location_
            LIMIT 1;

    -- Insert new test point if not exists
    IF NOT FOUND THEN
        INSERT INTO test_points (point_name, location_terr_id) VALUES (name_, location_)
            RETURNING test_points.point_id INTO id_;
    END IF;

    RETURN id_;
END
$$;


-- -- Add 'doc'-comment to the get_test_point() function.
COMMENT ON FUNCTION get_test_point IS
E'Function, provides obtaining educational testing point id (references "test_points"."point_id")
by passed point name and location territory id. In case when language entity corresponds passed name not exists -
inserts new row to "test_points" table, else takes first occurred row from existing.
In case when one or more passed names are NULL - returns NULL.';
