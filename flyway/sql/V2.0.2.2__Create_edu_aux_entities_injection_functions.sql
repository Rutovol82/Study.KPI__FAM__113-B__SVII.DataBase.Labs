-- Version: v2.0.2.2 // #lab-2 #intermediate-2.2
-- Description: Create functions provides injection/referencing of auxiliary educational entities.


-- Create get_edu_lang() function, that:
-- Provides obtaining educational language id (references "edu_langs"."lang_id")
-- by passed language name. In case when language entity corresponds passed name not exists -
-- inserts new row to "edu_langs" table, else takes first occurred row from existing.
-- In case when passed language name is NULL - returns NULL.

-- -- Define get_edu_lang() function
CREATE FUNCTION get_edu_lang(name_ edu_langs.lang_name%TYPE)
    RETURNS edu_langs.lang_id%TYPE
    LANGUAGE 'plpgsql'
AS $$
DECLARE id_ edu_langs.lang_id%TYPE;     -- Variable will store obtained language id
BEGIN
    -- Check that input language name is not NULL
    IF name_ is null THEN
        RETURN null;
    END IF;

    -- Try to select id from "edu_langs"
    SELECT edu_langs.lang_id INTO id_
        FROM edu_langs WHERE edu_langs.lang_name = name_
            LIMIT 1;

    -- Insert new language if not exists
    IF NOT FOUND THEN
        INSERT INTO edu_langs (lang_name) VALUES (name_)
            RETURNING edu_langs.lang_id INTO id_;
    END IF;

    RETURN id_;
END
$$;


-- -- Add 'doc'-comment to the get_edu_lang() function.
COMMENT ON FUNCTION get_edu_lang IS
E'Function, provides obtaining educational language id (references "edu_langs"."lang_id")
by passed language name. In case when language entity corresponds passed name not exists -
inserts new row to "edu_langs" table, else takes first occurred row from existing.
In case when passed language name is NULL - returns NULL.';


-- Create get_edu_profile() function, that:
-- Provides obtaining educational profile id (references "edu_profiles"."profile_id")
-- by passed profile name. In case when profile entity corresponds passed name not exists -
-- inserts new row to "edu_profiles" table, else takes first occurred row from existing.
-- In case when passed profile name is NULL - returns NULL.

-- -- Define get_edu_profile() function
CREATE FUNCTION get_edu_profile(name_ edu_profiles.profile_name%TYPE)
    RETURNS edu_profiles.profile_id%TYPE
    LANGUAGE 'plpgsql'
AS $$
DECLARE id_ edu_profiles.profile_id%TYPE;   -- Variable will store obtained profile id
BEGIN
    -- Check that input profile name is not NULL
    IF name_ is null THEN
        RETURN null;
    END IF;

    -- Try to select id from "edu_profiles"
    SELECT edu_profiles.profile_id INTO id_
        FROM edu_profiles WHERE edu_profiles.profile_name = name_
            LIMIT 1;

    -- Insert new profile if not exists
    IF NOT FOUND THEN
        INSERT INTO edu_profiles (profile_name) VALUES (name_)
            RETURNING edu_profiles.profile_id INTO id_;
    END IF;

    RETURN id_;
END
$$;


-- -- Add 'doc'-comment to the get_edu_profile() function.
COMMENT ON FUNCTION get_edu_profile IS
E'Function, provides obtaining educational profile id (references "edu_profiles"."profile_id")
by passed profile name. In case when profile entity corresponds passed name not exists -
inserts new row to "edu_profiles" table, else takes first occurred row from existing.
In case when passed profile name is NULL - returns NULL.';
