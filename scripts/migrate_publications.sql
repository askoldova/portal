UPDATE load_askolodva.pub_items SET pbi_author = NULL WHERE pbi_author = '' AND pbi_id > 0;
UPDATE load_askolodva.pub_items SET pbi_author = 'Любов Михайлюк' WHERE pbi_author = 'Любов Михайоюк' AND pbi_id > 0;
UPDATE load_askolodva.pub_items SET pbi_author = 'Віталіна Онишкевич' WHERE pbi_author = 'Віталіна Онишкеви' AND pbi_id > 0;
UPDATE load_askolodva.pub_items SET pbi_author = 'Віталіна Онишкевич' WHERE pbi_author = 'Выталына Онишкевич' AND pbi_id > 0;

INSERT INTO auth_user (username, password, is_superuser, first_name, last_name, email, is_staff, is_active, date_joined) 
SELECT distinct pbi_author, '' , false, '', pbi_author, '', false, true, current_timestamp()
FROM load_askolodva.pub_items 
WHERE pbi_author IS NOT NULL
AND PBI_AUTHOR NOT IN (
	SELECT username FROM auth_user
);

DELETE FROM publications_publicationimage WHERE id > 0;
DELETE FROM publications_publicationitem WHERE id > 0;
DELETE FROM publications_publicationsubcategory WHERE id > 0;
DELETE FROM publications_publication WHERE id > 0;

INSERT INTO `publications_publication`
(`id`,
`type`,
`slug`,
`rss_stream`,
`rss_url`,
`subcategory_id`)
SELECT DISTINCT p.pub_id, p.pub_type, null, pi.pbi_rss_id, pi.pbi_rss_url, 
(SELECT psc_sct_id FROM load_askoldova.pub_subcats WHERE psc_order = 0 AND psc_pub_id = pub_id)
FROM load_askoldova.publications p 
INNER JOIN load_askoldova.pub_items pi ON pbi_pub_id = pub_id
WHERE NOT EXISTS (SELECT id FROM publications_publication WHERE id = pub_id);

INSERT INTO `publications_publicationsubcategory`
(
`publication_id`,
`subcategory_id`)
SELECT psc_pub_id, psc_sct_id 
FROM load_askoldova.pub_subcats 
WHERE psc_order > 0
ORDER BY psc_order;

INSERT INTO `publications_publicationitem`
(`id`,
`publication_date`,
`show_date`,
`state`,
`title`,
`short_text`,
`text`,
`author_id`,
`locale_id`,
`publication_id`)
SELECT DISTINCT pbi_id, pbi_date, pbi_show_date, pbi_state, pbi_title, pbi_text_short, pbi_text,
(SELECT id FROM auth_user WHERE username = pbi_author),
(SELECT id FROM portal_lang WHERE code = UPPER(pbi_lang_id)),
pbi_pub_id
FROM load_askoldova.pub_items pi;

INSERT INTO `publications_publicationimage`
(`id`,
`file`,
`caption`,
`name`,
`publication_id`)
SELECT DISTINCT max(img_id), img_file_name, null, img_name, img_pub_id 
FROM load_askoldova.images
WHERE exists (SELECT id FROM publications_publication WHERE id = img_pub_id)
GROUP BY img_file_name, img_name, img_pub_id;


