CREATE TABLE IF NOT EXISTS `mydb`.`permission` (
  `userid` INT NOT NULL COMMENT '',
  `adminLevel` INT ZEROFILL NULL COMMENT '',
  PRIMARY KEY (`userid`)  COMMENT '',
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB