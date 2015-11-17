CREATE TABLE IF NOT EXISTS `mydb`.`comment` (
  `commentid` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `postid` INT NOT NULL COMMENT '',
  `parentCommentid` INT NULL COMMENT '',
  `username` VARCHAR(20) NULL COMMENT '',
  `deletedByDate` TIMESTAMP NULL COMMENT '',
  `deletedByUsername` VARCHAR(20) NULL COMMENT '',
  `active` INT DEFAULT 1 COMMENT '',
  `dateCreated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `comment` MEDIUMTEXT NULL COMMENT '',
  PRIMARY KEY (`commentid`)  COMMENT '',
  INDEX `postid_idx` (`postid` ASC)  COMMENT '',
  INDEX `username_idx` (`username` ASC)  COMMENT '',
  INDEX `deletedByUsername_idx` (`deletedByUsername` ASC)  COMMENT '',
  CONSTRAINT `parentCommentid`
    FOREIGN KEY (`commentid`)
    REFERENCES `mydb`.`comment` (`commentid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `postid`
    FOREIGN KEY (`postid`)
    REFERENCES `mydb`.`post` (`postid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `username`
    FOREIGN KEY (`username`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `deletedByUsername`
    FOREIGN KEY (`deletedByUsername`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = '		'