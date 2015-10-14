CREATE TABLE IF NOT EXISTS `mydb`.`pillar` (
  `userid` INT NOT NULL COMMENT '',
  `supportUserId` INT NOT NULL COMMENT '',
  `dateCreated` DATE NULL COMMENT '',
  INDEX `supportUserId_idx` (`supportUserId` ASC, `userid` ASC)  COMMENT '',
  PRIMARY KEY (`supportUserId`, `userid`)  COMMENT '',
  CONSTRAINT `userid`
    FOREIGN KEY ()
    REFERENCES `mydb`.`user` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `supportUserId`
    FOREIGN KEY (`supportUserId` , `userid`)
    REFERENCES `mydb`.`user` (`userid` , `userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB