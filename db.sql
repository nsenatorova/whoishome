CREATE DATABASE iot_project;

USE iot_project;

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` int(11) NOT NULL COMMENT "id устройства в комнате",
  `email` varchar(500) NOT NULL COMMENT "Электронная почта",
  `pword` varchar(500) NOT NULL COMMENT "Пароль пользователя",
  `is_in_home` tinyint(1) NOT NULL COMMENT "Флаг нахождения пользователя у себя в комнате",
  `token` varchar(1000) NOT NULL COMMENT "Токен смартфона для отправки уведомлений",
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8