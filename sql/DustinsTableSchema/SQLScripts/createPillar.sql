CREATE TABLE IF NOT EXISTS `mydb`.`pillar` (
  `username` VARCHAR(20) NOT NULL ,
  `supportUsername` VARCHAR(20) NOT NULL,
  `dateCreated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`supportUsername`, `username`),
  INDEX `username_idx` (`username` ASC),
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