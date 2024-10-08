Drop table TestData;

CREATE TABLE TestData (
    Col1 STRING(2000) NOT NULL,
    Col2 STRING(2000) NOT NULL,
    Col3 STRING(2000) NOT NULL,
    Col4 STRING(2000) NOT NULL,
    Col5 STRING(1992) NOT NULL,
    Col6 STRING(64) NOT NULL,  
) PRIMARY KEY(Col6);

INSERT INTO TestData (Col1,Col2,Col3,Col4,Col5,Col6)
SELECT
    TO_HEX(SHA256(CAST(num * 1000 AS STRING))) AS Col1,
    TO_HEX(SHA256(CAST(num * 20 AS STRING))) AS Col2,
    TO_HEX(SHA256(CAST(num * 10 AS STRING))) AS Col3,
    TO_HEX(SHA256(CAST(num * 100 AS STRING))) AS Col4,
    TO_HEX(SHA256(CAST(num * 1000 AS STRING)))  AS Col5,
    CAST(num AS STRING) AS Col6 
  FROM
    UNNEST(GENERATE_ARRAY(1, 10000)) AS num;