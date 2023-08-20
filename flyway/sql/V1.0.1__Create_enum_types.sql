-- Version: v1.0.1 // #lab-1 #intermediate-1
-- Description: Create enumeration types "test_status", "dpa_level", "sex", "terrtype", "edu_status"


-- Create test info enumerations

-- -- ENUM represents test pass status
CREATE TYPE test_status AS ENUM
(
    'Анульовано',
    'Зараховано',
    'Не з’явився',
    'Не обрано 100-200',
    'Не подолав поріг'
);


-- -- ENUM represents DPA level
CREATE TYPE dpa_level AS ENUM
(
    'профільний',
    'академічний'
);


-- Examinee info enumerations

-- -- ENUM represents examinee sex
CREATE TYPE sex AS ENUM
(
    'жіноча',
    'чоловіча'
);


-- -- ENUM represents examinee residence territory type
CREATE TYPE terrtype AS ENUM
(
    'СМТ',
    'село',
    'місто'
);


-- -- ENUM represents educational status
CREATE TYPE edu_status AS ENUM
(
    'Випускник ЗСЗО',
    'Випускник ЗСЗО іншої держави',
    'Випускник ЗСЗО минуліх років',
    'Учень (слухач) ЗПО (ЗПТО)',
    'Студент ВНЗ'
);
