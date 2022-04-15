CREATE TABLE IF NOT EXISTS public.genres
(
    id integer NOT NULL DEFAULT nextval('genre_id_seq'::regclass),
    name character varying(256) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT genre_pkey PRIMARY KEY (id),
    CONSTRAINT genre_unic UNIQUE (name)
)

CREATE TABLE IF NOT EXISTS public.artists
(
    id integer NOT NULL DEFAULT nextval('artists_id_seq'::regclass),
    name character varying(256) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT artists_pkey PRIMARY KEY (id),
    CONSTRAINT artist_unic UNIQUE (name)
)

CREATE TABLE IF NOT EXISTS public.albums
(
    id integer NOT NULL DEFAULT nextval('albums_id_seq'::regclass),
    name character varying(256) COLLATE pg_catalog."default" NOT NULL,
    start_year integer NOT NULL,
    CONSTRAINT albums_pkey PRIMARY KEY (id),
    CONSTRAINT album_unic UNIQUE (name)
)

CREATE TABLE IF NOT EXISTS public.tracks
(
    id integer NOT NULL DEFAULT nextval('tracks_id_seq'::regclass),
    album_id integer NOT NULL,
    name character varying(256) COLLATE pg_catalog."default" NOT NULL,
    duration integer NOT NULL,
    CONSTRAINT tracks_pkey PRIMARY KEY (id),
    CONSTRAINT track_unic UNIQUE (name),
    CONSTRAINT tracks_album_id_fkey FOREIGN KEY (album_id)
        REFERENCES public.albums (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE IF NOT EXISTS public.collections
(
    id integer NOT NULL DEFAULT nextval('collections_id_seq'::regclass),
    name character varying(256) COLLATE pg_catalog."default" NOT NULL,
    start_year integer NOT NULL,
    CONSTRAINT collections_pkey PRIMARY KEY (id),
    CONSTRAINT collection_unic UNIQUE (name)
)

REATE TABLE IF NOT EXISTS public.genres_artists
(
    genre_id integer NOT NULL,
    artist_id integer NOT NULL,
    CONSTRAINT pk_ga PRIMARY KEY (genre_id, artist_id),
    CONSTRAINT genre_artists_id_artist_fkey FOREIGN KEY (artist_id)
        REFERENCES public.artists (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT genre_artists_id_genre_fkey FOREIGN KEY (genre_id)
        REFERENCES public.genres (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE IF NOT EXISTS public.albums_artists
(
    album_id integer NOT NULL,
    artist_id integer NOT NULL,
    CONSTRAINT pk_aa PRIMARY KEY (album_id, artist_id),
    CONSTRAINT album_artists_id_album_fkey FOREIGN KEY (album_id)
        REFERENCES public.albums (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT album_artists_id_artist_fkey FOREIGN KEY (artist_id)
        REFERENCES public.artists (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

CREATE TABLE IF NOT EXISTS public.collections_tracks
(
    collection_id integer NOT NULL,
    track_id integer NOT NULL,
    CONSTRAINT pk_ct PRIMARY KEY (collection_id, track_id),
    CONSTRAINT collections_tracks_id_collection_fkey FOREIGN KEY (collection_id)
        REFERENCES public.collections (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT collections_tracks_id_track_fkey FOREIGN KEY (track_id)
        REFERENCES public.tracks (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

