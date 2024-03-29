\c dormyboba;

CREATE TABLE "academic_type" (
  "type_id" integer PRIMARY KEY,
  "type_name" varchar(50)
);

CREATE TABLE "institute" (
  "institute_id" integer PRIMARY KEY,
  "institute_name" varchar(50)
);

CREATE TABLE "dormyboba_role" (
  "role_id" serial PRIMARY KEY,
  "role_name" varchar(50) UNIQUE
);

CREATE TABLE "dormyboba_user" (
  "user_id" integer PRIMARY KEY,
  "role_id" integer NOT NULL REFERENCES "dormyboba_role" ("role_id"),
  "academic_type_id" integer REFERENCES "academic_type" ("type_id"),
  "institute_id" integer REFERENCES "institute" ("institute_id"),
  "enroll_year" integer,
  "academic_group" varchar(20),
  "registration_complete" boolean NOT NULL
);

CREATE TABLE "mailing" (
  "mailing_id" serial PRIMARY KEY,
  "theme" varchar(256),
  "mailing_text" text,
  "at" timestamp,
  "academic_type_id" integer REFERENCES "academic_type" ("type_id"),
  "institute_id" integer REFERENCES "institute" ("institute_id"),
  "enroll_year" integer,
  "academic_group" varchar(20),
  "is_event_generated" boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE "queue" (
  "queue_id" serial PRIMARY KEY,
  "title" varchar(256),
  "description" varchar(256),
  "open" timestamp,
  "close" timestamp,
  "active_user_id" integer REFERENCES "dormyboba_user" ("user_id"),
  "is_event_generated" boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE "queue_to_user" (
  "user_id" integer REFERENCES "dormyboba_user" ("user_id"),
  "queue_id" integer REFERENCES "queue" ("queue_id"),
  PRIMARY KEY ("user_id", "queue_id"),
  "joined" timestamp NOT NULL
);


