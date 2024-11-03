--@(#) script.ddl

CREATE TABLE category
(
	category_id bigint NOT NULL,
	name varchar (50) NOT NULL,
	description varchar (255),
	created_at timestamp with timezone NOT NULL,
	PRIMARY KEY(category_id)
);

CREATE TABLE user
(
	user_id bigint NOT NULL,
	username varchar (50) NOT NULL,
	email varchar (100) NOT NULL,
	password_hash varchar (255) NOT NULL,
	created_at timestamp with timezone NOT NULL,
	role varchar (15) DEFAULT 'registered_user' NOT NULL,
	PRIMARY KEY(user_id),
	CHECK(role in ('registered_user', 'admin'))
);

CREATE TABLE private_upload
(
	private_upload_id bigint NOT NULL,
	title varchar (100) NOT NULL,
	description varchar (255),
	file_path varchar (255) NOT NULL,
	max_download_count bigint,
	download_count bigint DEFAULT 0,
	expiration_date timestamp with timezone NOT NULL,
	virus_free boolean DEFAULT false NOT NULL,
	uploaded_at timestamp with timezone NOT NULL,
	size_in_bytes bigint NOT NULL,
	file_hash varchar (64) NOT NULL,
	views bigint DEFAULT 0,
	password_protected boolean NOT NULL,
	password_hash varchar (255),
	download_link varchar (2083) NOT NULL,
	fk_user_id bigint NOT NULL,
	PRIMARY KEY(private_upload_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES user (user_id) ON DELETE CASCADE
);

CREATE TABLE public_upload
(
	public_upload_id bigint NOT NULL,
	title varchar (100) NOT NULL,
	description varchar (255),
	file_path varchar (255) NOT NULL,
	max_download_count bigint,
	download_count bigint DEFAULT 0,
	expiration_date timestamp with timezone NOT NULL,
	virus_free boolean DEFAULT false NOT NULL,
	uploaded_at timestamp with timezone NOT NULL,
	size_in_bytes bigint NOT NULL,
	file_hash varchar (64) NOT NULL,
	views bigint DEFAULT 0,
	like_count bigint DEFAULT 0,
	dislike_count bigint DEFAULT 0,
	comment_count bigint DEFAULT 0,
	admin_approved boolean DEFAULT false NOT NULL,
	fk_user_id bigint NOT NULL,
	PRIMARY KEY(public_upload_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES user (user_id) ON DELETE CASCADE
);

CREATE TABLE sub_category
(
	sub_category_id bigint NOT NULL,
	name varchar (50) NOT NULL,
	description varchar (255),
	created_at timestamp with timezone NOT NULL,
	fk_category_id bigint NOT NULL,
	PRIMARY KEY(sub_category_id),
	CONSTRAINT fk_category_id FOREIGN KEY(fk_category_id) REFERENCES category (category_id) ON DELETE RESTRICT
);

CREATE TABLE user_session
(
	session_id bigint NOT NULL,
	created_at timestamp with timezone NOT NULL,
	ip_address varchar (45) NOT NULL,
	fk_user_id bigint NOT NULL,
	PRIMARY KEY(session_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES user (user_id) ON DELETE CASCADE
);

CREATE TABLE comment
(
	comment_id bigint NOT NULL,
	content varchar (255) NOT NULL,
	created_at timestamp with timezone NOT NULL,
	fk_user_id bigint NOT NULL,
	fk_public_upload_id bigint NOT NULL,
	PRIMARY KEY(comment_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES user (user_id) ON DELETE CASCADE,
	CONSTRAINT gets FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE
);

CREATE TABLE file_approval
(
	approval_id bigint NOT NULL,
	reason varchar (255),
	action_date timestamp with timezone NOT NULL,
	status varchar (8) DEFAULT 'pending' NOT NULL,
	fk_public_upload_id bigint NOT NULL,
	fk_user_id bigint NOT NULL,
	PRIMARY KEY(approval_id),
	CHECK(status in ('approved', 'pending', 'rejected')),
	UNIQUE(fk_public_upload_id),
	CONSTRAINT gets FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE,
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES user (user_id) ON DELETE CASCADE
);

CREATE TABLE file_dislike
(
	dislike_id bigint NOT NULL,
	disliked_at timestamp with timezone NOT NULL,
	fk_user_id bigint NOT NULL,
	fk_public_upload_id bigint NOT NULL,
	PRIMARY KEY(dislike_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES user (user_id) ON DELETE CASCADE,
	CONSTRAINT gets FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE
);

CREATE TABLE file_download
(
	download_id bigint NOT NULL,
	download_date timestamp with timezone NOT NULL,
	successful boolean DEFAULT false NOT NULL,
	ip_address varchar (45) NOT NULL,
	fk_private_upload_id bigint,
	fk_public_upload_id bigint,
	PRIMARY KEY(download_id),
	CHECK ((fk_private_upload_id IS NOT NULL AND fk_public_upload_id IS NULL) OR 
           (fk_private_upload_id IS NULL AND fk_public_upload_id IS NOT NULL)),
	CONSTRAINT fk_private_upload_download FOREIGN KEY(fk_private_upload_id) REFERENCES private_upload (private_upload_id) ON DELETE CASCADE,
    CONSTRAINT fk_public_upload_download FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE
);

CREATE TABLE file_like
(
	like_id bigint NOT NULL,
	liked_at timestamp with timezone NOT NULL,
	fk_user_id bigint NOT NULL,
	fk_public_upload_id bigint NOT NULL,
	PRIMARY KEY(like_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES user (user_id) ON DELETE CASCADE,
	CONSTRAINT gets FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE
);

CREATE TABLE has
(
	fk_public_upload_id bigint NOT NULL,
	fk_sub_category_id bigint NOT NULL,
	CONSTRAINT fk_public_upload_has FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE,
	CONSTRAINT fk_sub_category_id FOREIGN KEY(fk_sub_category_id) REFERENCES sub_category (sub_category_id) ON DELETE RESTRICT
);

















FINAL


















--@(#) script.ddl

CREATE TABLE category
(
	category_id bigint NOT NULL,
	name varchar (50) NOT NULL,
	description varchar (255),
	created_at timestamptz NOT NULL,
	PRIMARY KEY(category_id)
);

CREATE TABLE "user"
(
	user_id bigint NOT NULL,
	username varchar (50) NOT NULL,
	email varchar (100) NOT NULL,
	password_hash varchar (255) NOT NULL,
	created_at timestamptz NOT NULL,
	role varchar (15) DEFAULT 'registered_user' NOT NULL,
	PRIMARY KEY(user_id),
	CHECK(role in ('registered_user', 'admin'))
);

CREATE TABLE private_upload
(
	private_upload_id bigint NOT NULL,
	title varchar (100) NOT NULL,
	description varchar (255),
	file_path varchar (255) NOT NULL,
	max_download_count bigint,
	download_count bigint DEFAULT 0,
	expiration_date timestamptz NOT NULL,
	virus_free boolean DEFAULT false NOT NULL,
	uploaded_at timestamptz NOT NULL,
	size_in_bytes bigint NOT NULL,
	file_hash varchar (64) NOT NULL,
	views bigint DEFAULT 0,
	password_protected boolean NOT NULL,
	password_hash varchar (255),
	download_link varchar (2083) NOT NULL,
	fk_user_id bigint NOT NULL,
	PRIMARY KEY(private_upload_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES "user" (user_id) ON DELETE CASCADE
);

CREATE TABLE public_upload
(
	public_upload_id bigint NOT NULL,
	title varchar (100) NOT NULL,
	description varchar (255),
	file_path varchar (255) NOT NULL,
	max_download_count bigint,
	download_count bigint DEFAULT 0,
	expiration_date timestamptz NOT NULL,
	virus_free boolean DEFAULT false NOT NULL,
	uploaded_at timestamptz NOT NULL,
	size_in_bytes bigint NOT NULL,
	file_hash varchar (64) NOT NULL,
	views bigint DEFAULT 0,
	like_count bigint DEFAULT 0,
	dislike_count bigint DEFAULT 0,
	comment_count bigint DEFAULT 0,
	admin_approved boolean DEFAULT false NOT NULL,
	fk_user_id bigint NOT NULL,
	PRIMARY KEY(public_upload_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES "user" (user_id) ON DELETE CASCADE
);

CREATE TABLE sub_category
(
	sub_category_id bigint NOT NULL,
	name varchar (50) NOT NULL,
	description varchar (255),
	created_at timestamptz NOT NULL,
	fk_category_id bigint NOT NULL,
	PRIMARY KEY(sub_category_id),
	CONSTRAINT fk_category_id FOREIGN KEY(fk_category_id) REFERENCES category (category_id) ON DELETE RESTRICT
);

CREATE TABLE user_session
(
	session_id bigint NOT NULL,
	created_at timestamptz NOT NULL,
	ip_address varchar (45) NOT NULL,
	fk_user_id bigint NOT NULL,
	PRIMARY KEY(session_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES "user" (user_id) ON DELETE CASCADE
);

CREATE TABLE comment
(
	comment_id bigint NOT NULL,
	content varchar (255) NOT NULL,
	created_at timestamptz NOT NULL,
	fk_user_id bigint NOT NULL,
	fk_public_upload_id bigint NOT NULL,
	PRIMARY KEY(comment_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES "user" (user_id) ON DELETE CASCADE,
	CONSTRAINT gets FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE
);

CREATE TABLE file_approval
(
	approval_id bigint NOT NULL,
	reason varchar (255),
	action_date timestamptz NOT NULL,
	status varchar (8) DEFAULT 'pending' NOT NULL,
	fk_public_upload_id bigint NOT NULL,
	fk_user_id bigint NOT NULL,
	PRIMARY KEY(approval_id),
	CHECK(status in ('approved', 'pending', 'rejected')),
	UNIQUE(fk_public_upload_id),
	CONSTRAINT gets FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE,
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES "user" (user_id) ON DELETE CASCADE
);

CREATE TABLE file_dislike
(
	dislike_id bigint NOT NULL,
	disliked_at timestamptz NOT NULL,
	fk_user_id bigint NOT NULL,
	fk_public_upload_id bigint NOT NULL,
	PRIMARY KEY(dislike_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES "user" (user_id) ON DELETE CASCADE,
	CONSTRAINT gets FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE
);

CREATE TABLE file_download
(
	download_id bigint NOT NULL,
	download_date timestamptz NOT NULL,
	successful boolean DEFAULT false NOT NULL,
	ip_address varchar (45) NOT NULL,
	fk_private_upload_id bigint,
	fk_public_upload_id bigint,
	PRIMARY KEY(download_id),
	CHECK ((fk_private_upload_id IS NOT NULL AND fk_public_upload_id IS NULL) OR 
           (fk_private_upload_id IS NULL AND fk_public_upload_id IS NOT NULL)),
	CONSTRAINT fk_private_upload_download FOREIGN KEY(fk_private_upload_id) REFERENCES private_upload (private_upload_id) ON DELETE CASCADE,
    CONSTRAINT fk_public_upload_download FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE
);

CREATE TABLE file_like
(
	like_id bigint NOT NULL,
	liked_at timestamptz NOT NULL,
	fk_user_id bigint NOT NULL,
	fk_public_upload_id bigint NOT NULL,
	PRIMARY KEY(like_id),
	CONSTRAINT fk_user_id_user FOREIGN KEY(fk_user_id) REFERENCES "user" (user_id) ON DELETE CASCADE,
	CONSTRAINT gets FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE
);

CREATE TABLE has
(
	fk_public_upload_id bigint NOT NULL,
	fk_sub_category_id bigint NOT NULL,
	CONSTRAINT fk_public_upload_has FOREIGN KEY(fk_public_upload_id) REFERENCES public_upload (public_upload_id) ON DELETE CASCADE,
	CONSTRAINT fk_sub_category_id FOREIGN KEY(fk_sub_category_id) REFERENCES sub_category (sub_category_id) ON DELETE RESTRICT
);
