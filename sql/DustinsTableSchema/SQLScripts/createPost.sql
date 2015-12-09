CREATE TABLE IF NOT EXISTS `mydb`.`post` (
  `postid` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `username` VARCHAR(20) NULL COMMENT '',
  `summary` VARCHAR(100) NULL COMMENT '',
  `description` MEDIUMTEXT NULL COMMENT '',
  `dateCreated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `dateLastModified` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `active` TINYINT(1) DEFAULT 1 COMMENT '',
  'categoryid' INT DEFAULT 0,
  PRIMARY KEY (`postid`)  COMMENT '',
  INDEX `username_idx` (`username` ASC)  COMMENT '',
  CONSTRAINT `username`
    FOREIGN KEY (`username`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB