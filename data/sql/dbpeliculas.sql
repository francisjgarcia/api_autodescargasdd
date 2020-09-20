-- --------------------------------------------------------
-- Host:                         192.168.1.200
-- Versión del servidor:         5.7.29 - MySQL Community Server (GPL)
-- SO del servidor:              Linux
-- HeidiSQL Versión:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Volcando estructura de base de datos para dbpeliculas
CREATE DATABASE IF NOT EXISTS `dbpeliculas` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_spanish_ci */;
USE `dbpeliculas`;

-- Volcando estructura para tabla dbpeliculas.tbestado_pelicula
CREATE TABLE IF NOT EXISTS `tbestado_pelicula` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_estado` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `descripcion` varchar(100) COLLATE utf8_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla dbpeliculas.tbpeliculas
CREATE TABLE IF NOT EXISTS `tbpeliculas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `enlace` int(6) NOT NULL,
  `nombre` varchar(150) COLLATE utf8_spanish_ci NOT NULL,
  `anyo_pelicula` int(4) DEFAULT NULL,
  `estado_pelicula` int(11) NOT NULL,
  `fecha` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `enlace` (`enlace`),
  KEY `estado_pelicula` (`estado_pelicula`),
  CONSTRAINT `tbpeliculas_ibfk_1` FOREIGN KEY (`estado_pelicula`) REFERENCES `tbestado_pelicula` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=215 DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

/*!40000 ALTER TABLE `tbestado_pelicula` DISABLE KEYS */;
INSERT INTO `tbestado_pelicula` (`id`, `nombre_estado`, `descripcion`) VALUES
	(0, 'Error', 'Ha sucedido algún error con esta película.'),
	(1, 'Nueva película', 'Se ha notificado en telegram de una nueva película.'),
	(2, 'Pendiente de descargar', 'Poniendo película a descargar.'),
	(3, 'Descargando', 'Ya se ha notificado que se quiere descargar esta película.'),
	(4, 'Descargada', 'Esta película ya está descargada.'),
	(5, 'Plex', 'Ya está disponible en Plex.');
/*!40000 ALTER TABLE `tbestado_pelicula` ENABLE KEYS */;

-- La exportación de datos fue deseleccionada.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
