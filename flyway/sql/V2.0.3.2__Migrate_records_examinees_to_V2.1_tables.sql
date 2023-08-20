-- Version: v2.0.3.2 // #lab-2 #intermediate-3.2
-- Description: Migrate records, examinees data and related instances (except "test_passes" branch)
            --  from "zno_odata_records" to previously created tables of #lab-2 #primary schema.


-- Perform complex insertion using previously defined injection/referencing functions
-- on top of the "records" table population

INSERT INTO records (record_id, record_year, examinee_id)
    SELECT
        zno_odata_records.id,
        zno_odata_records.year,
        new_examinee(
            sex_ := zno_odata_records.examinee$sex,
            birth_year_ := zno_odata_records.examinee$birth_year,
            residence_ := get_location(
                region_ := zno_odata_records.examinee$residence$region,
                area_ := zno_odata_records.examinee$residence$area,
                territory_ := zno_odata_records.examinee$residence$territory
            ),
            residence_terrtype_ := zno_odata_records.examinee$residence_tertype,
            edu_profile_ := get_edu_profile(
                name_ := zno_odata_records.examinee$edu$class$profile
            ),
            edu_lang_ := get_edu_lang(
                name_ := zno_odata_records.examinee$edu$class$lang
            ),
            edu_org_ := get_edu_org(
                name_ := zno_odata_records.examinee$edu$org$name,
                supervisor_ := zno_odata_records.examinee$edu$org$supervisor,
                type_ := zno_odata_records.examinee$edu$org$type,
                location_ := get_location(
                    region_ := zno_odata_records.examinee$edu$org$loc$region,
                    area_ := zno_odata_records.examinee$edu$org$loc$area,
                    territory_ := zno_odata_records.examinee$edu$org$loc$territory
                )
            ),
            edu_status_ := zno_odata_records.examinee$edu$status
        )
    FROM zno_odata_records
