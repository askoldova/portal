/*
-- Query: SELECT * FROM askoldova.portal_lang
LIMIT 0, 1000

-- Date: 2016-04-17 19:11
*/
INSERT INTO `portal_lang` (`id`,`code`,`caption`,`default`) VALUES (1,'UK','Українська',1);
INSERT INTO `portal_lang` (`id`,`code`,`caption`,`default`) VALUES (2,'EN','English',0);

INSERT INTO `portal_langlocale` (`id`,`caption`,`lang_id`,`locale_id`) VALUES (2,'Ukrainian',1,2);
INSERT INTO `portal_langlocale` (`id`,`caption`,`lang_id`,`locale_id`) VALUES (3,'Англійська',2,1);
