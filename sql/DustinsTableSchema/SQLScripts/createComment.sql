CREATE TABLE IF NOT EXISTS `mydb`.`comment` (
  `commentid` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `postid` INT NOT NULL COMMENT '',
  `parentCommentid` INT NULL COMMENT '',
  `username` VARCHAR(20) NULL COMMENT '',
  `deletedByDate` TIMESTAMP NULL COMMENT '',
  `active` INT DEFAULT 1 COMMENT '',
  `dateCreated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `comment` MEDIUMTEXT NULL COMMENT '',
  PRIMARY KEY (`commentid`)  COMMENT '',
  INDEX `postid_idx` (`postid` ASC)  COMMENT '',
  INDEX `username_idx` (`username` ASC)  COMMENT '',
  CONSTRAINT `postid`
    FOREIGN KEY (`postid`)
    REFERENCES `mydb`.`post` (`postid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `username`
    FOREIGN KEY (`username`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = '		'