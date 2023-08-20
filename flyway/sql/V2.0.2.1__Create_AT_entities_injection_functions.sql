-- Version: v2.0.2.1 // #lab-2 #intermediate-2.1
-- Description: Create functions provides injection/referencing of Administrative-Territorial division entities.


-- Create get_location() function, that:
-- Provides obtaining territory id (references "territories"."terr_id")
-- by passed names of region, area & territory. In case when entities corresponds passed names not exists -
-- inserts new rows to corresponding tables, else takes first occurred row from existing.
-- In case when one or more passed names are NULL - returns NULL.

-- -- Define get_location() function
CREATE FUNCTION get_location(region_    regions.region_name%TYPE,
                             area_      areas.area_name%TYPE,
                             territory_ territories.terr_name%TYPE)
    RETURNS territories.terr_id%TYPE
    LANGUAGE 'plpgsql'
AS $$
DECLARE
    break_ BOOL := false;   -- Flag indicates if entities sequence is already broken

    region_id_ regions.region_id%TYPE;  -- Variable will store obtained target region id
    area_id_ areas.area_id%TYPE;        -- Variable will store obtained target area id
    terr_id_ territories.terr_id%TYPE;  -- Variable will store obtained target territory id

BEGIN
    -- Check that input location components are not NULL

    IF region_ is null OR area_ is null OR territory_ is null THEN
        RETURN null;
    END IF;

    -- Obtain region id

    -- -- Try to select id from "regions"
    SELECT regions.region_id INTO region_id_
        FROM regions WHERE regions.region_name = region_
            LIMIT 1;

    -- -- Insert new region if not exists & break sequence
    IF NOT FOUND THEN
        INSERT INTO regions (region_name) VALUES (region_)
            RETURNING regions.region_id INTO region_id_;
        break_ := true;
    END IF;

    -- Obtain area id

    -- -- Try to select id from "areas" if entities sequence is not broken
    IF NOT break_ THEN
        SELECT areas.area_id INTO area_id_
            FROM areas WHERE areas.region_id = region_id_ AND areas.area_name = area_
                LIMIT 1;
    END IF;

    -- -- Insert new area if not exists & break entity sequence
    IF break_ OR NOT FOUND THEN
        INSERT INTO areas (region_id, area_name) VALUES (region_id_, area_)
            RETURNING areas.area_id INTO area_id_;
        break_ := true;
    END IF;

    -- Obtain territory id

    -- -- Try to select id from "territories" if entities sequence is not broken
    IF NOT break_ THEN
        SELECT territories.terr_id INTO terr_id_
            FROM territories WHERE territories.area_id = area_id_ AND territories.terr_name = territory_
                LIMIT 1;
    END IF;

    -- -- Insert new territory if not exists
    IF break_ OR NOT FOUND THEN
        INSERT INTO territories (area_id, terr_name) VALUES (area_id_, territory_)
            RETURNING territories.terr_id INTO terr_id_;
    END IF;

    RETURN terr_id_;
END
$$;


-- -- Add 'doc'-comment to the get_location() function.
COMMENT ON FUNCTION get_location IS
E'Function, provides obtaining territory id (references "territories"."terr_id")
by passed names of region, area & territory. In case when entities corresponds passed names not exists -
inserts new rows to corresponding tables, else takes first occurred row from existing.
In case when one or more passed names are NULL - returns NULL.';
