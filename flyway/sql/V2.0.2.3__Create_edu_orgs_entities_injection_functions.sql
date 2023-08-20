-- Version: v2.0.2.3 // #lab-2 #intermediate-2.3
-- Description: Create functions provides injection/referencing of educational organization and related entities.


-- Create get_edu_org() function, that:
-- Provides obtaining educational organization id (references "edu_orgs"."org_id")
-- by passed names of organization, its supervisor institution, type ("edu_orgtypes")
-- and location territory id. In case when entities corresponds passed names not exists -
-- inserts new rows to corresponding tables, else takes first occurred row from existing.
-- In case when passed organization name is NULL - returns NULL.

-- -- Define get_edu_org() function
CREATE FUNCTION get_edu_org(name_       edu_orgs.org_name%TYPE,
                            supervisor_ edu_supers.super_name%TYPE,
                            type_       edu_orgtypes.type_name%TYPE,
                            location_   edu_orgs.location_terr_id%TYPE)
    RETURNS edu_orgs.org_id%TYPE
    LANGUAGE 'plpgsql'
AS $$
DECLARE
    check_org_ BOOL := true;    -- Flag indicates whether there can be existing educational organization entity

    org_id_ edu_orgs.org_id%TYPE;           -- Variable will store obtained target educational organization id
    super_id_ edu_supers.super_id%TYPE;     -- Variable will store obtained target educational supervisor id
    orgtype_id_ edu_orgtypes.type_id%TYPE;  -- Variable will store obtained target educational organization type id

BEGIN
    -- Check that input name is not NULL

    IF name_ is null THEN
        RETURN null;
    END IF;

    -- Obtain supervisor id if passed supervisor name is not NULL

    IF supervisor_ is not null THEN
        -- Try to select id from "edu_supers"
        SELECT edu_supers.super_id INTO super_id_
            FROM edu_supers WHERE edu_supers.super_name = supervisor_
                LIMIT 1;

        -- Insert new supervisor if not exists & set check_org_ flag to false
        IF NOT FOUND THEN
            INSERT INTO edu_supers (super_name) VALUES (supervisor_)
                RETURNING edu_supers.super_id INTO super_id_;
            check_org_ := false;
        END IF;
    END IF;

    -- Obtain organization type id if passed type name is not NULL

    IF type_ is not null THEN
        -- Try to select id from "edu_orgtypes"
        SELECT edu_orgtypes.type_id INTO orgtype_id_
            FROM edu_orgtypes WHERE edu_orgtypes.type_name = type_
                LIMIT 1;

        -- Insert new type if not exists & set check_org_ flag to false
        IF NOT FOUND THEN
            INSERT INTO edu_orgtypes (type_name) VALUES (type_)
                RETURNING edu_orgtypes.type_id INTO orgtype_id_;
            check_org_ := false;
        END IF;
    END IF;

    -- Obtain educational organization id

    -- -- Try to select id from "edu_orgs" if check_org_ flag is true
    IF check_org_ THEN
        SELECT edu_orgs.org_id INTO org_id_
            FROM edu_orgs
            WHERE edu_orgs.super_id = super_id_
              AND edu_orgs.orgtype_id = orgtype_id_
              AND edu_orgs.location_terr_id = location_
                LIMIT 1;
    END IF;

    -- -- Insert new organization if not exists
    IF NOT (check_org_ AND FOUND) THEN
        INSERT INTO edu_orgs (org_name, location_terr_id, orgtype_id, super_id)
            VALUES (name_, location_, orgtype_id_, super_id_)
                RETURNING edu_orgs.org_id INTO org_id_;
    END IF;

    RETURN org_id_;
END
$$;


-- -- Add 'doc'-comment to the get_edu_org() function.
COMMENT ON FUNCTION get_edu_org IS
E'Function, provides obtaining educational organization id (references "edu_orgs"."org_id")
by passed names of organization, its supervisor institution, type ("edu_orgtypes")
and location territory id. In case when entities corresponds passed names not exists -
inserts new rows to corresponding tables, else takes first occurred row from existing.
In case when passed organization name is NULL - returns NULL.';
