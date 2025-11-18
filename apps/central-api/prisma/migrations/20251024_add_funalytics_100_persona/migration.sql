-- CreateTable
CREATE TABLE "health_check" (
    "id" SERIAL NOT NULL,
    "updated_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "health_check_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "scores" (
    "id" TEXT NOT NULL,
    "brand" TEXT NOT NULL,
    "system" TEXT NOT NULL,
    "entity_type" TEXT NOT NULL,
    "entity_id" INTEGER NOT NULL,
    "overall_score" REAL NOT NULL,
    "dimensions" JSONB NOT NULL,
    "reasoning" VARCHAR(500),
    "status" TEXT NOT NULL DEFAULT 'completed',
    "computed_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "scores_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "events" (
    "id" SERIAL NOT NULL,
    "status" TEXT DEFAULT 'pending',
    "title" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "start_time" TIME,
    "end_time" TIME,
    "all_day" BOOLEAN DEFAULT false,
    "street" TEXT NOT NULL,
    "city" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "zip_code" TEXT NOT NULL,
    "latitude" DOUBLE PRECISION,
    "longitude" DOUBLE PRECISION,
    "created_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "category" TEXT NOT NULL,
    "target_audience" TEXT NOT NULL,
    "fun_meter" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "venue_id" INTEGER,
    "location" TEXT,
    "fun_rating" INTEGER,
    "funalytics_score" INTEGER,
    "funalytics_grade" TEXT,
    "funalytics_persona_scores" JSONB,
    "funalytics_engine_version" TEXT,
    "funalytics_last_updated" TIMESTAMPTZ(6),
    "age_restriction" VARCHAR(16),
    "alcohol_present" BOOLEAN,
    "audience_zones" JSONB,

    CONSTRAINT "events_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "users" (
    "id" SERIAL NOT NULL,
    "email" TEXT NOT NULL,
    "password_hash" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "account_active" BOOLEAN NOT NULL DEFAULT true,
    "username" TEXT,
    "first_name" TEXT,
    "last_name" TEXT,
    "is_admin" BOOLEAN DEFAULT false,
    "company_name" TEXT,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "venues" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "street" TEXT,
    "city" TEXT,
    "state" TEXT,
    "zip_code" TEXT,
    "phone" TEXT,
    "email" TEXT,
    "website" TEXT,
    "created_at" TIMESTAMP(3) DEFAULT CURRENT_TIMESTAMP,
    "user_id" INTEGER,
    "latitude" DOUBLE PRECISION,
    "longitude" DOUBLE PRECISION,

    CONSTRAINT "venues_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "funalytics_scores" (
    "id" UUID NOT NULL,
    "event_id" INTEGER NOT NULL,
    "community_vibe" INTEGER,
    "family_fun" INTEGER,
    "overall_score" INTEGER,
    "reasoning" TEXT,
    "computed_at" TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "funalytics_scores_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "scores_brand_system_entity_type_entity_id_idx" ON "scores"("brand", "system", "entity_type", "entity_id");

-- CreateIndex
CREATE INDEX "scores_computed_at_idx" ON "scores"("computed_at" DESC);

-- CreateIndex
CREATE UNIQUE INDEX "scores_brand_system_entity_type_entity_id_computed_at_key" ON "scores"("brand", "system", "entity_type", "entity_id", "computed_at");

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users"("email");

-- AddForeignKey
ALTER TABLE "events" ADD CONSTRAINT "events_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "events" ADD CONSTRAINT "events_venue_id_fkey" FOREIGN KEY ("venue_id") REFERENCES "venues"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "venues" ADD CONSTRAINT "venues_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "funalytics_scores" ADD CONSTRAINT "funalytics_scores_event_id_fkey" FOREIGN KEY ("event_id") REFERENCES "events"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

