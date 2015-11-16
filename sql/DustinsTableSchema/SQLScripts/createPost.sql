CREATE TABLE IF NOT EXISTS `mydb`.`post` (
  `postid` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `username` VARCHAR(20) NULL COMMENT '',
  `summary` VARCHAR(100) NULL COMMENT '',
  `description` MEDIUMTEXT NULL COMMENT '',
  `dateCreated` DATE NULL COMMENT '',
  `dateLastModified` DATE NULL COMMENT '',
  `active` TINYINT(1) NULL COMMENT '',
  PRIMARY KEY (`postid`)  COMMENT '',
  INDEX `username_idx` (`username` ASC)  COMMENT '',
  CONSTRAINT `username`
    FOREIGN KEY (`username`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB