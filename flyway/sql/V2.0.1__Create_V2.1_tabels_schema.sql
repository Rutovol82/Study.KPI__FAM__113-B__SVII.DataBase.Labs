-- Version: v2.0.1 // #lab-2 #intermediate-1
-- Description: Create final tables schema for the future #lab-2 #primary


-- Create tables for third-party entities

-- -- Create tables for Administrative-Territorial division entities

-- -- -- Region entity table
CREATE TABLE regions
(
    region_id               INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    region_name             VARCHAR         NOT NULL
);

-- -- -- Area entity table
CREATE TABLE areas
(
    area_id                 INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    region_id               INT             NOT NULL                        REFERENCES regions(region_id),
    area_name               VARCHAR         NOT NULL
);

-- -- -- Territory entity table
CREATE TABLE territories
(
    terr_id                 INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    area_id                 INT             NOT NULL                        REFERENCES areas(area_id),
    terr_name               VARCHAR         NOT NULL
);


-- -- Create tables educational information secondary entities

-- -- -- Educational language entity table
CREATE TABLE edu_langs
(
    lang_id                 INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    lang_name               VARCHAR         NOT NULL
);

-- -- -- Educations profile entity table
CREATE TABLE edu_profiles
(
    profile_id              INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    profile_name            VARCHAR         NOT NULL
);


-- -- Create tables for educational organizations info entities

-- -- -- Educational organization type entity table
CREATE TABLE edu_orgtypes
(
    type_id                 INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    type_name               VARCHAR         NOT NULL
);

-- -- -- Educational organization supervisor ('parent') entity table
CREATE TABLE edu_supers
(
    super_id                INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    super_name              VARCHAR         NOT NULL
);

-- -- -- Educational organization entity table
CREATE TABLE edu_orgs
(
    org_id                  INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    org_name                VARCHAR         NOT NULL,
    location_terr_id        INT             NULL                            REFERENCES territories(terr_id),
    orgtype_id              INT             NULL                            REFERENCES edu_orgtypes(type_id),
    super_id                INT             NULL                            REFERENCES edu_supers(super_id)
);


-- -- Create tables for testing point info entities

-- -- -- Testing point entity table
CREATE TABLE test_points
(
    point_id                INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    point_name              VARCHAR         NOT NULL,
    location_terr_id        INT             NULL                            REFERENCES territories(terr_id)
);


-- Create tables for primary entities

-- -- Create tables for record & examinee data entities

-- -- -- Examinee data entity
CREATE TABLE examinees_data
(
    examinee_id             INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    sex                     sex             NULL,
    birth_year              SMALLINT        NULL,

    residence_terr_id       INT             NULL                            REFERENCES territories(terr_id),
    residence_terrtype      terrtype        NULL,

    edu_profile_id          INT             NULL                            REFERENCES edu_profiles(profile_id),
    edu_lang_id             INT             NULL                            REFERENCES edu_langs(lang_id),

    edu_org_id              INT             NULL                            REFERENCES edu_orgs(org_id),
    edu_status              edu_status      NULL
);

-- -- -- OpenData record entity table
CREATE TABLE records
(
    record_id               CHAR(36)        NOT NULL                        PRIMARY KEY,
    --
    record_year             SMALLINT        NOT NULL,
    examinee_id             INT             NULL                            REFERENCES examinees_data(examinee_id)
);


-- -- Create tables for subject & test pass entities

-- -- -- Subject entity table
CREATE TABLE subjects
(
    subject_id              INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    subject_code            VARCHAR(64)     NOT NULL                        UNIQUE,
    subject_name            VARCHAR         NULL
);

-- -- -- Test pass entity table
CREATE TABLE test_passes
(
    pass_id                 INT             GENERATED ALWAYS AS IDENTITY    PRIMARY KEY,
    --
    record_id               CHAR(36)        NOT NULL                        REFERENCES records(record_id),
    subject_id              INT             NOT NULL                        REFERENCES subjects(subject_id),

    test_status             test_status     NOT NULL,
    super_pass_id           INT             NULL                            REFERENCES test_passes(pass_id),

    test_point_id           INT             NULL                            REFERENCES test_points(point_id),

    test_lang_id            INT             NULL                            REFERENCES edu_langs(lang_id),
    adapt_scale             SMALLINT        NULL,
    dpa_level               dpa_level       NULL,

    score                   SMALLINT        NULL,
    score_12                SMALLINT        NULL,
    score_100               DECIMAL(4, 1)   NULL
);
