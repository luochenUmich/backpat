CREATE TABLE IF NOT EXISTS `mydb`.`permission` (
  `username` VARCHAR(20) NOT NULL COMMENT '',
  `adminLevel` INT ZEROFILL NULL COMMENT '',
  PRIMARY KEY (`username`)  COMMENT '',
  CONSTRAINT `username`
    FOREIGN KEY (`username`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB