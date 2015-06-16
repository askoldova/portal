UPDATE pub_items SET pbi_author = NULL WHERE pbi_author = '' AND pbi_id > 0;
UPDATE pub_items SET pbi_author = 'Любов Михайлюк' WHERE pbi_author = 'Любов Михайоюк' AND pbi_id > 0;
UPDATE pub_items SET pbi_author = 'Віталіна Онишкевич' WHERE pbi_author = 'Віталіна Онишкеви' AND pbi_id > 0;
UPDATE pub_items SET pbi_author = 'Віталіна Онишкевич' WHERE pbi_author = 'Выталына Онишкевич' AND pbi_id > 0;

INSERT INTO auth_user (username, password, is_superuser, first_name, last_name, email, is_staff, is_active, date_joined) 
SELECT distinct pbi_author, '' , false, '', pbi_author, '', false, true, current_timestamp()
FROM pub_items 
WHERE pbi_author IS NOT NULL
AND PBI_AUTHOR NOT IN (
	SELECT username FROM auth_user
);
