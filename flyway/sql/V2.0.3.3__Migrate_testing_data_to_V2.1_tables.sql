-- Version: v2.0.3.3 // #lab-2 #intermediate-3.3
-- Description: Migrate testing data from "zno_odata_records" to previously created tables of #lab-2 #primary schema.


-- Perform complex insertions using previously defined injection/referencing functions
-- on top of the "test_passes" table population by subjects


-- -- Ukrainian language and literature
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'ukr_lang_lit')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             adapt_scale,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$ukr_lang_lit$status,
            get_test_point(
                name_ := zno_odata_records.test$ukr_lang_lit$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$ukr_lang_lit$point$loc$region,
                    area_ := zno_odata_records.test$ukr_lang_lit$point$loc$area,
                    territory_ := zno_odata_records.test$ukr_lang_lit$point$loc$territory
                )
            ),
            zno_odata_records.test$ukr_lang_lit$adapt_scale,
            zno_odata_records.test$ukr_lang_lit$score,
            zno_odata_records.test$ukr_lang_lit$score_12,
            zno_odata_records.test$ukr_lang_lit$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$ukr_lang_lit$subject$name IS NOT NULL;


-- -- Ukrainian language
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'ukr_lang'),
     ukr_lang_lit_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'ukr_lang_lit')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status, super_pass_id,
                             test_point_id,
                             adapt_scale,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$ukr_lang$status,
            CASE
                WHEN zno_odata_records.test$ukr_lang$sub_test$ukr_lang_lit
                THEN
                (
                    SELECT test_passes.pass_id FROM test_passes
                        WHERE test_passes.record_id = zno_odata_records.id
                          AND subject_id = (SELECT id FROM ukr_lang_lit_subject_)
                )
            END,
            get_test_point(
                name_ := zno_odata_records.test$ukr_lang$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$ukr_lang$point$loc$region,
                    area_ := zno_odata_records.test$ukr_lang$point$loc$area,
                    territory_ := zno_odata_records.test$ukr_lang$point$loc$territory
                )
            ),
            zno_odata_records.test$ukr_lang$adapt_scale,
            zno_odata_records.test$ukr_lang$score,
            zno_odata_records.test$ukr_lang$score_12,
            zno_odata_records.test$ukr_lang$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$ukr_lang$subject$name IS NOT NULL;


-- -- Ukrainian history
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'ukr_history')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             test_lang_id,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$ukr_history$status,
            get_test_point(
                name_ := zno_odata_records.test$ukr_history$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$ukr_history$point$loc$region,
                    area_ := zno_odata_records.test$ukr_history$point$loc$area,
                    territory_ := zno_odata_records.test$ukr_history$point$loc$territory
                )
            ),
            get_edu_lang(
                name_ := zno_odata_records.test$ukr_history$lang
            ),
            zno_odata_records.test$ukr_history$score,
            zno_odata_records.test$ukr_history$score_12,
            zno_odata_records.test$ukr_history$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$ukr_history$subject$name IS NOT NULL;


-- -- Mathematics
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'math')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             test_lang_id, dpa_level,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$math$status,
            get_test_point(
                name_ := zno_odata_records.test$math$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$math$point$loc$region,
                    area_ := zno_odata_records.test$math$point$loc$area,
                    territory_ := zno_odata_records.test$math$point$loc$territory
                )
            ),
            get_edu_lang(
                name_ := zno_odata_records.test$math$lang
            ),
            zno_odata_records.test$math$dpa_level,
            zno_odata_records.test$math$score,
            zno_odata_records.test$math$score_12,
            zno_odata_records.test$math$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$math$subject$name IS NOT NULL;


-- -- Mathematics (standard level)
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'math_std')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             test_lang_id,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$math_std$status,
            get_test_point(
                name_ := zno_odata_records.test$math_std$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$math_std$point$loc$region,
                    area_ := zno_odata_records.test$math_std$point$loc$area,
                    territory_ := zno_odata_records.test$math_std$point$loc$territory
                )
            ),
            get_edu_lang(
                name_ := zno_odata_records.test$math_std$lang
            ),
            zno_odata_records.test$math_std$score,
            zno_odata_records.test$math_std$score_12,
            zno_odata_records.test$math_std$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$math_std$subject$name IS NOT NULL;


-- -- Physics
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'physics')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             test_lang_id,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$physics$status,
            get_test_point(
                name_ := zno_odata_records.test$physics$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$physics$point$loc$region,
                    area_ := zno_odata_records.test$physics$point$loc$area,
                    territory_ := zno_odata_records.test$physics$point$loc$territory
                )
            ),
            get_edu_lang(
                name_ := zno_odata_records.test$physics$lang
            ),
            zno_odata_records.test$physics$score,
            zno_odata_records.test$physics$score_12,
            zno_odata_records.test$physics$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$physics$subject$name IS NOT NULL;


-- -- Chemistry
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'chemistry')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             test_lang_id,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$chemistry$status,
            get_test_point(
                name_ := zno_odata_records.test$chemistry$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$chemistry$point$loc$region,
                    area_ := zno_odata_records.test$chemistry$point$loc$area,
                    territory_ := zno_odata_records.test$chemistry$point$loc$territory
                )
            ),
            get_edu_lang(
                name_ := zno_odata_records.test$chemistry$lang
            ),
            zno_odata_records.test$chemistry$score,
            zno_odata_records.test$chemistry$score_12,
            zno_odata_records.test$chemistry$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$chemistry$subject$name IS NOT NULL;


-- -- Biology
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'biology')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             test_lang_id,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$biology$status,
            get_test_point(
                name_ := zno_odata_records.test$biology$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$biology$point$loc$region,
                    area_ := zno_odata_records.test$biology$point$loc$area,
                    territory_ := zno_odata_records.test$biology$point$loc$territory
                )
            ),
            get_edu_lang(
                name_ := zno_odata_records.test$biology$lang
            ),
            zno_odata_records.test$biology$score,
            zno_odata_records.test$biology$score_12,
            zno_odata_records.test$biology$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$biology$subject$name IS NOT NULL;


-- -- Geography
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'geography')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             test_lang_id,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$geography$status,
            get_test_point(
                name_ := zno_odata_records.test$geography$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$geography$point$loc$region,
                    area_ := zno_odata_records.test$geography$point$loc$area,
                    territory_ := zno_odata_records.test$geography$point$loc$territory
                )
            ),
            get_edu_lang(
                name_ := zno_odata_records.test$geography$lang
            ),
            zno_odata_records.test$geography$score,
            zno_odata_records.test$geography$score_12,
            zno_odata_records.test$geography$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$geography$subject$name IS NOT NULL;


-- -- English language
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'eng_lang')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             dpa_level,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$eng_lang$status,
            get_test_point(
                name_ := zno_odata_records.test$eng_lang$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$eng_lang$point$loc$region,
                    area_ := zno_odata_records.test$eng_lang$point$loc$area,
                    territory_ := zno_odata_records.test$eng_lang$point$loc$territory
                )
            ),
            zno_odata_records.test$eng_lang$dpa_level,
            zno_odata_records.test$eng_lang$score,
            zno_odata_records.test$eng_lang$score_12,
            zno_odata_records.test$eng_lang$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$eng_lang$subject$name IS NOT NULL;


-- -- France language
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'fra_lang')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             dpa_level,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$fra_lang$status,
            get_test_point(
                name_ := zno_odata_records.test$fra_lang$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$fra_lang$point$loc$region,
                    area_ := zno_odata_records.test$fra_lang$point$loc$area,
                    territory_ := zno_odata_records.test$fra_lang$point$loc$territory
                )
            ),
            zno_odata_records.test$fra_lang$dpa_level,
            zno_odata_records.test$fra_lang$score,
            zno_odata_records.test$fra_lang$score_12,
            zno_odata_records.test$fra_lang$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$fra_lang$subject$name IS NOT NULL;


-- -- Deutsch language
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'deu_lang')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             dpa_level,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$deu_lang$status,
            get_test_point(
                name_ := zno_odata_records.test$deu_lang$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$deu_lang$point$loc$region,
                    area_ := zno_odata_records.test$deu_lang$point$loc$area,
                    territory_ := zno_odata_records.test$deu_lang$point$loc$territory
                )
            ),
            zno_odata_records.test$deu_lang$dpa_level,
            zno_odata_records.test$deu_lang$score,
            zno_odata_records.test$deu_lang$score_12,
            zno_odata_records.test$deu_lang$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$deu_lang$subject$name IS NOT NULL;


-- -- Spanish language
WITH current_subject_ AS (SELECT subject_id AS id FROM subjects WHERE subject_code = 'spa_lang')
    INSERT INTO test_passes (record_id, subject_id,
                             test_status,
                             test_point_id,
                             dpa_level,
                             score, score_12, score_100)
        SELECT
            zno_odata_records.id,
            (SELECT id FROM current_subject_),
            zno_odata_records.test$spa_lang$status,
            get_test_point(
                name_ := zno_odata_records.test$spa_lang$point$name,
                location_ := get_location(
                    region_ := zno_odata_records.test$spa_lang$point$loc$region,
                    area_ := zno_odata_records.test$spa_lang$point$loc$area,
                    territory_ := zno_odata_records.test$spa_lang$point$loc$territory
                )
            ),
            zno_odata_records.test$spa_lang$dpa_level,
            zno_odata_records.test$spa_lang$score,
            zno_odata_records.test$spa_lang$score_12,
            zno_odata_records.test$spa_lang$score_100
        FROM zno_odata_records
        WHERE zno_odata_records.test$spa_lang$subject$name IS NOT NULL;
