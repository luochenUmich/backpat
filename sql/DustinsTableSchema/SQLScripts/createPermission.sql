CREATE TABLE IF NOT EXISTS `mydb`.`permission` (
  `username` VARCHAR(20) NOT NULL COMMENT '',
  `adminLevel` INT ZEROFILL NULL COMMENT '',
  PRIMARY KEY (`username`)  COMMENT '')
ENGINE = InnoDB