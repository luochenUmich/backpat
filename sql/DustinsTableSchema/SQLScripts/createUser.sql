CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `email` VARCHAR(255) NOT NULL COMMENT '',
  `password` VARCHAR(45) NOT NULL COMMENT '',
  `username` VARCHAR(45) NOT NULL COMMENT '',
  `active` TINYINT(1) NULL DEFAULT 1 COMMENT '',
  UNIQUE INDEX `username_UNIQUE` (`username` ASC)  COMMENT '',
  UNIQUE INDEX `email_UNIQUE` (`email` ASC)  COMMENT '',
  PRIMARY KEY (`username`)  COMMENT '')
ENGINE = InnoDB