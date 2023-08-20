-- Version: v1.1 // #lab-1 #primary
-- Description: Create solid table corresponds OpenData files structure


-- Create data table

CREATE TABLE zno_odata_records
(
    -- Record id ('OutID')
    id                                              CHAR(36)        NOT NULL        PRIMARY KEY,

    -- Record year
    year                                            SMALLINT        NOT NULL,

    -- Examinee data

    -- -- Basic info
    examinee$sex                                    sex             NULL,
    examinee$birth_year                             SMALLINT        NULL,

    -- -- Residence info
    examinee$residence$region                       VARCHAR         NULL,
    examinee$residence$area                         VARCHAR         NULL,
    examinee$residence$territory                    VARCHAR         NULL,

    -- -- Additional residence info
    examinee$residence_tertype                      terrtype        NULL,

    -- -- Educational info
    examinee$edu$status                             edu_status      NULL,
    -- -- -- Class info
    examinee$edu$class$lang                         VARCHAR         NULL,
    examinee$edu$class$profile                      VARCHAR         NULL,
    -- -- -- Educational organization info
    examinee$edu$org$name                           VARCHAR         NULL,
    examinee$edu$org$type                           VARCHAR         NULL,
    examinee$edu$org$supervisor                     VARCHAR         NULL,
    -- -- -- -- Educational organization location info
    examinee$edu$org$loc$region                     VARCHAR         NULL,
    examinee$edu$org$loc$area                       VARCHAR         NULL,
    examinee$edu$org$loc$territory                  VARCHAR         NULL,


    -- Tests results

    -- -- Ukrainian language
    -- -- -- Subject info
    test$ukr_lang$subject$name                      VARCHAR         NULL,
    -- -- -- Testing info
    test$ukr_lang$point$name                        VARCHAR         NULL,
    test$ukr_lang$point$loc$region                  VARCHAR         NULL,
    test$ukr_lang$point$loc$area                    VARCHAR         NULL,
    test$ukr_lang$point$loc$territory               VARCHAR         NULL,
    -- -- -- Individual details
    test$ukr_lang$adapt_scale                       SMALLINT        NULL,
    -- -- -- Test results
    test$ukr_lang$status                            test_status     NULL,
    test$ukr_lang$sub_test$ukr_lang_lit             BOOLEAN         NULL,
    -- -- -- -- Test scores
    test$ukr_lang$score                             SMALLINT        NULL,
    test$ukr_lang$score_12                          SMALLINT        NULL,
    test$ukr_lang$score_100                         DECIMAL(4, 1)   NULL,

    -- -- Ukrainian language and literature
    -- -- -- Subject info
    test$ukr_lang_lit$subject$name                  VARCHAR         NULL,
    -- -- -- Testing info
    test$ukr_lang_lit$point$name                    VARCHAR         NULL,
    test$ukr_lang_lit$point$loc$region              VARCHAR         NULL,
    test$ukr_lang_lit$point$loc$area                VARCHAR         NULL,
    test$ukr_lang_lit$point$loc$territory           VARCHAR         NULL,
    -- -- -- Individual details
    test$ukr_lang_lit$adapt_scale                   SMALLINT        NULL,
    -- -- -- Test results
    test$ukr_lang_lit$status                        test_status     NULL,
    -- -- -- -- Test scores
    test$ukr_lang_lit$score                         SMALLINT        NULL,
    test$ukr_lang_lit$score_12                      SMALLINT        NULL,
    test$ukr_lang_lit$score_100                     DECIMAL(4, 1)   NULL,

    -- -- Ukrainian history
    -- -- -- Subject info
    test$ukr_history$subject$name                   VARCHAR         NULL,
    -- -- -- Testing info
    test$ukr_history$point$name                     VARCHAR         NULL,
    test$ukr_history$point$loc$region               VARCHAR         NULL,
    test$ukr_history$point$loc$area                 VARCHAR         NULL,
    test$ukr_history$point$loc$territory            VARCHAR         NULL,
    -- -- -- Individual details
    test$ukr_history$lang                           VARCHAR         NULL,
    -- -- -- Test results
    test$ukr_history$status                         test_status     NULL,
    -- -- -- -- Test scores
    test$ukr_history$score                          SMALLINT        NULL,
    test$ukr_history$score_12                       SMALLINT        NULL,
    test$ukr_history$score_100                      DECIMAL(4, 1)   NULL,

    -- -- Mathematics
    -- -- -- Subject info
    test$math$subject$name                          VARCHAR         NULL,
    -- -- -- Testing info
    test$math$point$name                            VARCHAR         NULL,
    test$math$point$loc$region                      VARCHAR         NULL,
    test$math$point$loc$area                        VARCHAR         NULL,
    test$math$point$loc$territory                   VARCHAR         NULL,
    -- -- -- Individual details
    test$math$dpa_level                             dpa_level       NULL,
    test$math$lang                                  VARCHAR         NULL,
    -- -- -- Test results
    test$math$status                                test_status     NULL,
    -- -- -- -- Test scores
    test$math$score                                 SMALLINT        NULL,
    test$math$score_12                              SMALLINT        NULL,
    test$math$score_100                             DECIMAL(4, 1)   NULL,

    -- -- Mathematics (standard level)
    -- -- -- Subject info
    test$math_std$subject$name                      VARCHAR         NULL,
    -- -- -- Testing info
    test$math_std$point$name                        VARCHAR         NULL,
    test$math_std$point$loc$region                  VARCHAR         NULL,
    test$math_std$point$loc$area                    VARCHAR         NULL,
    test$math_std$point$loc$territory               VARCHAR         NULL,
    -- -- -- Individual details
    test$math_std$lang                              VARCHAR         NULL,
    -- -- -- Test results
    test$math_std$status                            test_status     NULL,
    -- -- -- -- Test scores
    test$math_std$score                             SMALLINT        NULL,
    test$math_std$score_12                          SMALLINT        NULL,
    test$math_std$score_100                         DECIMAL(4, 1)   NULL,

    -- -- Physics
    -- -- -- Subject info
    test$physics$subject$name                       VARCHAR         NULL,
    -- -- -- Testing info
    test$physics$point$name                         VARCHAR         NULL,
    test$physics$point$loc$region                   VARCHAR         NULL,
    test$physics$point$loc$area                     VARCHAR         NULL,
    test$physics$point$loc$territory                VARCHAR         NULL,
    -- -- -- Individual details
    test$physics$lang                               VARCHAR         NULL,
    -- -- -- Test results
    test$physics$status                             test_status     NULL,
    -- -- -- -- Test scores
    test$physics$score                              SMALLINT        NULL,
    test$physics$score_12                           SMALLINT        NULL,
    test$physics$score_100                          DECIMAL(4, 1)   NULL,

    -- -- Chemistry
    -- -- -- Subject info
    test$chemistry$subject$name                     VARCHAR         NULL,
    -- -- -- Testing info
    test$chemistry$point$name                       VARCHAR         NULL,
    test$chemistry$point$loc$region                 VARCHAR         NULL,
    test$chemistry$point$loc$area                   VARCHAR         NULL,
    test$chemistry$point$loc$territory              VARCHAR         NULL,
    -- -- -- Individual details
    test$chemistry$lang                             VARCHAR         NULL,
    -- -- -- Test results
    test$chemistry$status                           test_status     NULL,
    -- -- -- -- Test scores
    test$chemistry$score                            SMALLINT        NULL,
    test$chemistry$score_12                         SMALLINT        NULL,
    test$chemistry$score_100                        DECIMAL(4, 1)   NULL,

    -- -- Biology
    -- -- -- Subject info
    test$biology$subject$name                       VARCHAR         NULL,
    -- -- -- Testing info
    test$biology$point$name                         VARCHAR         NULL,
    test$biology$point$loc$region                   VARCHAR         NULL,
    test$biology$point$loc$area                     VARCHAR         NULL,
    test$biology$point$loc$territory                VARCHAR         NULL,
    -- -- -- Individual details
    test$biology$lang                               VARCHAR         NULL,
    -- -- -- Test results
    test$biology$status                             test_status     NULL,
    -- -- -- -- Test scores
    test$biology$score                              SMALLINT        NULL,
    test$biology$score_12                           SMALLINT        NULL,
    test$biology$score_100                          DECIMAL(4, 1)   NULL,

    -- -- Geography
    -- -- -- Subject info
    test$geography$subject$name                     VARCHAR         NULL,
    -- -- -- Testing info
    test$geography$point$name                       VARCHAR         NULL,
    test$geography$point$loc$region                 VARCHAR         NULL,
    test$geography$point$loc$area                   VARCHAR         NULL,
    test$geography$point$loc$territory              VARCHAR         NULL,
    -- -- -- Individual details
    test$geography$lang                             VARCHAR         NULL,
    -- -- -- Test results
    test$geography$status                           test_status     NULL,
    -- -- -- -- Test scores
    test$geography$score                            SMALLINT        NULL,
    test$geography$score_12                         SMALLINT        NULL,
    test$geography$score_100                        DECIMAL(4, 1)   NULL,

    -- -- English language
    -- -- -- Subject info
    test$eng_lang$subject$name                      VARCHAR         NULL,
    -- -- -- Testing info
    test$eng_lang$point$name                        VARCHAR         NULL,
    test$eng_lang$point$loc$region                  VARCHAR         NULL,
    test$eng_lang$point$loc$area                    VARCHAR         NULL,
    test$eng_lang$point$loc$territory               VARCHAR         NULL,
    -- -- -- Individual details
    test$eng_lang$dpa_level                         dpa_level       NULL,
    -- -- -- Test results
    test$eng_lang$status                            test_status     NULL,
    -- -- -- -- Test scores
    test$eng_lang$score                             SMALLINT        NULL,
    test$eng_lang$score_12                          SMALLINT        NULL,
    test$eng_lang$score_100                         DECIMAL(4, 1)   NULL,

    -- -- France language
    -- -- -- Subject info
    test$fra_lang$subject$name                      VARCHAR         NULL,
    -- -- -- Testing info
    test$fra_lang$point$name                        VARCHAR         NULL,
    test$fra_lang$point$loc$region                  VARCHAR         NULL,
    test$fra_lang$point$loc$area                    VARCHAR         NULL,
    test$fra_lang$point$loc$territory               VARCHAR         NULL,
    -- -- -- Individual details
    test$fra_lang$dpa_level                         dpa_level       NULL,
    -- -- -- Test results
    test$fra_lang$status                            test_status     NULL,
    -- -- -- -- Test scores
    test$fra_lang$score                             SMALLINT        NULL,
    test$fra_lang$score_12                          SMALLINT        NULL,
    test$fra_lang$score_100                         DECIMAL(4, 1)   NULL,

    -- -- Deutsch language
    -- -- -- Subject info
    test$deu_lang$subject$name                      VARCHAR         NULL,
    -- -- -- Testing info
    test$deu_lang$point$name                        VARCHAR         NULL,
    test$deu_lang$point$loc$region                  VARCHAR         NULL,
    test$deu_lang$point$loc$area                    VARCHAR         NULL,
    test$deu_lang$point$loc$territory               VARCHAR         NULL,
    -- -- -- Individual details
    test$deu_lang$dpa_level                         dpa_level       NULL,
    -- -- -- Test results
    test$deu_lang$status                            test_status     NULL,
    -- -- -- -- Test scores
    test$deu_lang$score                             SMALLINT        NULL,
    test$deu_lang$score_12                          SMALLINT        NULL,
    test$deu_lang$score_100                         DECIMAL(4, 1)   NULL,

    -- -- Spanish language
    -- -- -- Subject info
    test$spa_lang$subject$name                      VARCHAR         NULL,
    -- -- -- Testing info
    test$spa_lang$point$name                        VARCHAR         NULL,
    test$spa_lang$point$loc$region                  VARCHAR         NULL,
    test$spa_lang$point$loc$area                    VARCHAR         NULL,
    test$spa_lang$point$loc$territory               VARCHAR         NULL,
    -- -- -- Individual details
    test$spa_lang$dpa_level                         dpa_level       NULL,
    -- -- -- Test results
    test$spa_lang$status                            test_status     NULL,
    -- -- -- -- Test scores
    test$spa_lang$score                             SMALLINT        NULL,
    test$spa_lang$score_12                          SMALLINT        NULL,
    test$spa_lang$score_100                         DECIMAL(4, 1)   NULL
);
