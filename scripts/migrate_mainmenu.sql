DELETE FROM portal_menuitemi18n WHERE id > 0;
DELETE FROM portal_menuitem WHERE id > 0;
DELETE FROM portal_mainmenui18n WHERE id > 0;
DELETE FROM portal_mainmenu WHERE id > 0;

INSERT INTO portal_mainmenu(id, caption, locale_id, `order`, hidden, width)
SELECT cat_id, cat_name, (SELECT id FROM portal_lang WHERE code = 'UK'), 
cat_order, cat_hidden, cat_width
FROM categories;

INSERT INTO portal_mainmenui18n(caption, menu_id, locale_id)
SELECT cat_name_eng, cat_id, (SELECT id FROM portal_lang WHERE code = 'EN')
FROM categories;

INSERT INtO portal_menuitem(id, caption, locale_id, `order`, menu_id)
SELECT sct_id, sct_name,(SELECT id FROM portal_lang WHERE code = 'UK'), 
sct_order, sct_cat_id
FROM subcategories;

INSERT INTO `portal_menuitemi18n`
(
`caption`,
`locale_id`,
`menu_id`,
`menu_item_id`)
SELECT  sct_name_eng,(SELECT id FROM portal_lang WHERE code = 'EN'), 
sct_cat_id, sct_id
FROM subcategories;

