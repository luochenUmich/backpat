CREATE TABLE IF NOT EXISTS `mydb`.`pillar` (
  `username` VARCHAR(20) NOT NULL COMMENT '',
  `supportUsername` VARCHAR(20) NOT NULL COMMENT '',
  `dateCreated` DATE NULL COMMENT '',
  PRIMARY KEY (`supportUsername`, `username`)  COMMENT '',
  INDEX `username_idx` (`username` ASC)  COMMENT '',
  CONSTRAINT `username`
    FOREIGN KEY (`username`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `supportUsername`
    FOREIGN KEY (`supportUsername`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB