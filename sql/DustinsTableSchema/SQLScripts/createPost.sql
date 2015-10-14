CREATE TABLE IF NOT EXISTS `mydb`.`post` (
  `postid` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `userid` INT NULL COMMENT '',
  `summary` VARCHAR(100) NULL COMMENT '',
  `description` MEDIUMTEXT NULL COMMENT '',
  `dateCreated` DATE NULL COMMENT '',
  `dateLastModified` DATE NULL COMMENT '',
  `active` TINYINT(1) NULL COMMENT '',
  PRIMARY KEY (`postid`)  COMMENT '',
  INDEX `userid_idx` (`userid` ASC)  COMMENT '',
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB