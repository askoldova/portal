UPDATE load_askoldova.pub_items SET pbi_author = NULL WHERE pbi_author = '' AND pbi_id > 0;
UPDATE load_askoldova.pub_items SET pbi_author = 'Любов Михайлюк' WHERE pbi_author = 'Любов Михайоюк' AND pbi_id > 0;
UPDATE load_askoldova.pub_items SET pbi_author = 'Віталіна Онишкевич' WHERE pbi_author = 'Віталіна Онишкеви' AND pbi_id > 0;
UPDATE load_askoldova.pub_items SET pbi_author = 'Віталіна Онишкевич' WHERE pbi_author = 'Выталына Онишкевич' AND pbi_id > 0;

INSERT INTO auth_user (username, password, is_superuser, first_name, last_name, email, is_staff, is_active, date_joined) 
SELECT distinct pbi_author, '' , false, '', pbi_author, '', false, true, current_timestamp()
FROM load_askoldova.pub_items 
WHERE pbi_author IS NOT NULL
AND PBI_AUTHOR NOT IN (
	SELECT username FROM auth_user
);

DELETE FROM publications_publicationimage WHERE id > 0;
DELETE FROM publications_publicationsubcategory WHERE id > 0;
DELETE FROM publications_publication WHERE id > 0;
DELETE FROM publications_rssimportstream WHERE id > 0;

INSERT INTO `askoldovadev`.`publications_rssimportstream`
(`id`,
`enabled`,
`rss_url`,
`pool_period_mins`,
`next_pool`,
`link_caption`,
`language_id`,
`menu_item_id`)
SELECT rss_id, rss_active, rss_url, rss_pool_period_minutes, rss_next_pool,
rss_caption, (SELECT id FROM portal_lang WHERE code = UPPER(rss_lang)),
rss_sbc_id
FROM load_askoldova.rss_feeds;

INSERT INTO `publications_publication`
(
	state, publication_date, show_date, slug, `type`, 
    title, short_text, text, rss_stream, rss_url, 
    old_id, author_id, locale_id, subcategory_id
)
SELECT 
	pbi_state, pbi_date, pbi_show_date, null, p.pub_type, 
    pbi_title, pbi_text_short, pbi_text, pi.pbi_rss_id, pi.pbi_rss_url, 
    pbi_id, 
    (SELECT id FROM auth_user WHERE username = pbi_author),
	(SELECT id FROM portal_lang WHERE code = UPPER(pbi_lang_id)),
	(SELECT psc_sct_id FROM load_askoldova.pub_subcats WHERE psc_order = 0 AND psc_pub_id = pub_id)
FROM load_askoldova.publications p 
INNER JOIN load_askoldova.pub_items pi ON pbi_pub_id = pub_id
WHERE NOT EXISTS (SELECT id FROM publications_publication WHERE id = pub_id);

INSERT INTO `publications_publicationsubcategory`
(id,
`publication_id`,
`subcategory_id`)
SELECT psc_id, p.id, psc_sct_id 
FROM load_askoldova.pub_subcats 
INNER JOIN publications_publication p ON psc_pub_id = p.old_id
WHERE psc_order > 0
ORDER BY psc_order;

INSERT INTO `publications_publicationimage`
(`id`,
`file`,
`caption`,
`name`,
`publication_id`)
SELECT DISTINCT max(img_id), img_file_name, null, img_name, p.id 
FROM load_askoldova.images
INNER JOIN publications_publication p ON img_pub_id = p.old_id
GROUP BY img_file_name, img_name, p.id;


