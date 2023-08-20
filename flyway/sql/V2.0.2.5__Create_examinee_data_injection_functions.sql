-- Version: v2.0.2.5 // #lab-2 #intermediate-2.5
-- Description: Create functions provides injection of examinee data entities.


-- Create new_examinee() function, that:
-- Provides properly injection of new examinee data instance to the "examinees_data" table
-- and returns examinee id (references "test_points"."point_id").
-- In case when all passed values are NULL - returns NULL without new row insertion.

-- -- Define new_examinee() function
CREATE FUNCTION new_examinee(sex_                   examinees_data.sex%TYPE,
                             birth_year_            examinees_data.birth_year%TYPE,
                             residence_             examinees_data.residence_terr_id%TYPE,
                             residence_terrtype_    examinees_data.residence_terrtype%TYPE,
                             edu_profile_           examinees_data.edu_profile_id%TYPE,
                             edu_lang_              examinees_data.edu_lang_id%TYPE,
                             edu_org_               examinees_data.edu_org_id%TYPE,
                             edu_status_            examinees_data.edu_status%TYPE)
    RETURNS examinees_data.examinee_id%TYPE
    LANGUAGE 'plpgsql'
AS $$
DECLARE id_ test_points.point_id%TYPE;  -- Variable will store returned examinee id
BEGIN
    -- Check that input contains not NULL values
    IF sex_ is null AND birth_year_ is null AND residence_ is null AND residence_terrtype_ is null AND
       edu_profile_ is null AND edu_lang_ is null AND edu_org_ is null AND edu_status_ is null
    THEN
        RETURN null;
    END IF;

    -- Insert new examinee
    INSERT INTO
        examinees_data (sex, birth_year, residence_terr_id, residence_terrtype,
                        edu_profile_id, edu_lang_id, edu_org_id, edu_status)
    VALUES
        (sex_, birth_year_, residence_, residence_terrtype_,
         edu_profile_, edu_lang_, edu_org_, edu_status_)
    RETURNING examinees_data.examinee_id INTO id_;

    RETURN id_;
END
$$;


-- -- Add 'doc'-comment to the get_test_point() function.
COMMENT ON FUNCTION get_test_point IS
E'Function, provides properly injection of new examinee data instance to the "examinees_data" table
and returns examinee id (references "test_points"."point_id").
In case when all passed values are NULL - returns NULL without new row insertion.';
