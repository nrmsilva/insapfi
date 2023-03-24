CREATE TABLE media (
  id             NUMBER(10)     NOT NULL,
  content_type   VARCHAR2(100)  NOT NULL,
  file_name      VARCHAR2(100)  NOT NULL,
  content        CLOB           NOT NULL
);

ALTER TABLE media ADD (
  CONSTRAINT media_pk PRIMARY KEY (id)
);

ALTER TABLE media ADD (
  CONSTRAINT media_uk UNIQUE (file_name)
);

CREATE SEQUENCE media_seq;