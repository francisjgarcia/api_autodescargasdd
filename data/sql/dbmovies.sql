/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

<<<<<<< HEAD
-- Volcando estructura de base de datos para dbmovies
CREATE DATABASE IF NOT EXISTS `dbmovies` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `dbmovies`;

-- Volcando estructura para tabla dbmovies.tbhistory
CREATE TABLE IF NOT EXISTS `tbhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link_id` int(11) NOT NULL,
  `user_id` int(20) DEFAULT NULL,
=======
CREATE DATABASE IF NOT EXISTS `dbmovies` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `dbmovies`;

CREATE TABLE IF NOT EXISTS `tbhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link_id` int(11) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
>>>>>>> dev
  `state_id` int(1) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `link_id` (`link_id`),
  KEY `user_id` (`user_id`),
  KEY `state_id` (`state_id`),
<<<<<<< HEAD
  CONSTRAINT `FK_tbhistory_tblinks` FOREIGN KEY (`link_id`) REFERENCES `tblinks` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
=======
  CONSTRAINT `FK_tbhistory_tblinks` FOREIGN KEY (`link_id`) REFERENCES `tblinks` (`id`),
>>>>>>> dev
  CONSTRAINT `FK_tbhistory_tbstate` FOREIGN KEY (`state_id`) REFERENCES `tbstate` (`id`),
  CONSTRAINT `FK_tbhistory_tbusers` FOREIGN KEY (`user_id`) REFERENCES `tbusers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

<<<<<<< HEAD
-- Volcando datos para la tabla dbmovies.tbhistory: ~24 rows (aproximadamente)
/*!40000 ALTER TABLE `tbhistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbhistory` ENABLE KEYS */;

-- Volcando estructura para tabla dbmovies.tblinks
=======
>>>>>>> dev
CREATE TABLE IF NOT EXISTS `tblinks` (
  `id` int(6) NOT NULL,
  `movie_id` int(11) NOT NULL,
  `quality_id` int(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `quality_id` (`quality_id`),
  CONSTRAINT `FK_tblinks_tbmovies` FOREIGN KEY (`movie_id`) REFERENCES `tbmovies` (`id`),
  CONSTRAINT `FK_tblinks_tbquality` FOREIGN KEY (`quality_id`) REFERENCES `tbquality` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

<<<<<<< HEAD
-- Volcando datos para la tabla dbmovies.tblinks: ~24 rows (aproximadamente)
/*!40000 ALTER TABLE `tblinks` DISABLE KEYS */;
/*!40000 ALTER TABLE `tblinks` ENABLE KEYS */;

-- Volcando estructura para tabla dbmovies.tbmovies
CREATE TABLE IF NOT EXISTS `tbmovies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(150) COLLATE utf8_spanish_ci NOT NULL,
  `year` int(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- Volcando datos para la tabla dbmovies.tbmovies: ~23 rows (aproximadamente)
/*!40000 ALTER TABLE `tbmovies` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbmovies` ENABLE KEYS */;

-- Volcando estructura para tabla dbmovies.tbquality
CREATE TABLE IF NOT EXISTS `tbquality` (
  `id` int(1) NOT NULL AUTO_INCREMENT,
  `quality` varchar(50) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- Volcando datos para la tabla dbmovies.tbquality: ~4 rows (aproximadamente)
=======
CREATE TABLE IF NOT EXISTS `tbmovies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `year` int(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `tbquality` (
  `id` int(1) NOT NULL AUTO_INCREMENT,
  `quality` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

DELETE FROM `tbquality`;
>>>>>>> dev
/*!40000 ALTER TABLE `tbquality` DISABLE KEYS */;
INSERT INTO `tbquality` (`id`, `quality`) VALUES
	(1, 'SD'),
	(2, 'HD'),
	(3, 'FullHD'),
	(4, '4K');
/*!40000 ALTER TABLE `tbquality` ENABLE KEYS */;

<<<<<<< HEAD
-- Volcando estructura para tabla dbmovies.tbsettings
CREATE TABLE IF NOT EXISTS `tbsettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `option` varchar(50) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  `value` varchar(50) COLLATE utf8_spanish_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- Volcando datos para la tabla dbmovies.tbsettings: ~1 rows (aproximadamente)
=======
CREATE TABLE IF NOT EXISTS `tbsettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `option` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `value` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

DELETE FROM `tbsettings`;
>>>>>>> dev
/*!40000 ALTER TABLE `tbsettings` DISABLE KEYS */;
INSERT INTO `tbsettings` (`id`, `option`, `value`) VALUES
	(1, 'api_enable', '0');
/*!40000 ALTER TABLE `tbsettings` ENABLE KEYS */;

<<<<<<< HEAD
-- Volcando estructura para tabla dbmovies.tbstate
=======
>>>>>>> dev
CREATE TABLE IF NOT EXISTS `tbstate` (
  `id` int(1) NOT NULL AUTO_INCREMENT,
  `state` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `description` varchar(100) COLLATE utf8_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

<<<<<<< HEAD
-- Volcando datos para la tabla dbmovies.tbstate: ~4 rows (aproximadamente)
=======
DELETE FROM `tbstate`;
>>>>>>> dev
/*!40000 ALTER TABLE `tbstate` DISABLE KEYS */;
INSERT INTO `tbstate` (`id`, `state`, `description`) VALUES
	(1, 'Error', 'Ha sucedido algún error al descargar esta película.'),
	(2, 'Nueva película', 'Se ha notificado en telegram de una nueva película.'),
	(3, 'Descargando', 'La película ya se está descargando.'),
	(4, 'Descargada', 'Esta película ya está descargada.');
/*!40000 ALTER TABLE `tbstate` ENABLE KEYS */;

<<<<<<< HEAD
-- Volcando estructura para tabla dbmovies.tbusers
CREATE TABLE IF NOT EXISTS `tbusers` (
  `id` int(20) NOT NULL,
  `user` varchar(150) COLLATE utf8_spanish_ci DEFAULT NULL,
  `last_name` varchar(150) C COLLATE utf8_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- Volcando datos para la tabla dbmovies.tbusers: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `tbusers` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbusers` ENABLE KEYS */;
=======
CREATE TABLE IF NOT EXISTS `tbusers` (
  `id` bigint(20) NOT NULL,
  `user` varchar(150) COLLATE utf8_spanish_ci DEFAULT NULL,
  `last_name` varchar(150) COLLATE utf8_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

CREATE TABLE `vwfullhistory` (
	`state` VARCHAR(50) NOT NULL COLLATE 'utf8_spanish_ci',
	`title` VARCHAR(150) NOT NULL COLLATE 'utf8_general_ci',
	`YEAR` INT(4) NULL,
	`link` INT(6) NOT NULL,
	`quality` VARCHAR(50) NULL COLLATE 'utf8_general_ci',
	`date` DATETIME NOT NULL
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `vwfullhistory`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vwfullhistory` AS select `tbstate`.`state` AS `state`,`tbmovies`.`title` AS `title`,`tbmovies`.`year` AS `YEAR`,`tblinks`.`id` AS `link`,`tbquality`.`quality` AS `quality`,`tbhistory`.`date` AS `date` from ((((`tbmovies` join `tblinks` on((`tbmovies`.`id` = `tblinks`.`movie_id`))) join `tbhistory` on((`tbhistory`.`link_id` = `tblinks`.`id`))) join `tbquality` on((`tbquality`.`id` = `tblinks`.`quality_id`))) join `tbstate` on((`tbstate`.`id` = `tbhistory`.`state_id`))) order by `tbhistory`.`date`;
>>>>>>> dev

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
