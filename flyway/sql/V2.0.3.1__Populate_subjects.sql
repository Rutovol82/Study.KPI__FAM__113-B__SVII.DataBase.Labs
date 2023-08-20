-- Version: v2.0.3.1 // #lab-2 #intermediate-3.1
-- Description: Populate table "subjects" table with subjects codes & names.


-- Populate "subjects" table

INSERT INTO subjects (subject_code, subject_name)
    VALUES
        -- Ukrainian language
        (
            'ukr_lang',
            (
                SELECT test$ukr_lang$subject$name FROM zno_odata_records
                WHERE test$ukr_lang$subject$name is not null LIMIT 1
            )
        ),
        -- Ukrainian language and literature
        (
            'ukr_lang_lit',
            (
                SELECT test$ukr_lang_lit$subject$name FROM zno_odata_records
                WHERE test$ukr_lang_lit$subject$name is not null LIMIT 1
            )
        ),
        -- Ukrainian history
        (
            'ukr_history',
            (
                SELECT test$ukr_history$subject$name FROM zno_odata_records
                WHERE test$ukr_history$subject$name is not null LIMIT 1
            )
        ),
        -- Mathematics
        (
            'math',
            (
                SELECT test$math$subject$name FROM zno_odata_records
                WHERE test$math$subject$name is not null LIMIT 1
            )
        ),
        -- Mathematics (standard level)
        (
            'math_std',
            (
                SELECT test$math_std$subject$name FROM zno_odata_records
                WHERE test$math_std$subject$name is not null LIMIT 1
            )
        ),
        -- Physics
        (
            'physics',
            (
                SELECT test$physics$subject$name FROM zno_odata_records
                WHERE test$physics$subject$name is not null LIMIT 1
            )
        ),
        -- Chemistry
        (
            'chemistry',
            (
                SELECT test$chemistry$subject$name FROM zno_odata_records
                WHERE test$chemistry$subject$name is not null LIMIT 1
            )
        ),
        -- Biology
        (
            'biology',
            (
                SELECT test$biology$subject$name FROM zno_odata_records
                WHERE test$biology$subject$name is not null LIMIT 1
            )
        ),
        -- Geography
        (
            'geography',
            (
                SELECT test$geography$subject$name FROM zno_odata_records
                WHERE test$geography$subject$name is not null LIMIT 1
            )
        ),
        -- English language
        (
            'eng_lang',
            (
                SELECT test$eng_lang$subject$name FROM zno_odata_records
                WHERE test$eng_lang$subject$name is not null LIMIT 1
            )
        ),
        -- France language
        (
            'fra_lang',
            (
                SELECT test$fra_lang$subject$name FROM zno_odata_records
                WHERE test$fra_lang$subject$name is not null LIMIT 1
            )
        ),
        -- Deutch language
        (
            'deu_lang',
            (
                SELECT test$deu_lang$subject$name FROM zno_odata_records
                WHERE test$deu_lang$subject$name is not null LIMIT 1
            )
        ),
        -- Spanish language
        (
            'spa_lang',
            (
                SELECT test$spa_lang$subject$name FROM zno_odata_records
                WHERE test$spa_lang$subject$name is not null LIMIT 1
            )
        );
