CREATE TABLE IF NOT EXISTS `mydb`.`comment` (
  `commentid` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `postid` INT NOT NULL COMMENT '',
  `parentCommentid` INT NULL COMMENT '',
  `userid` INT NULL COMMENT '',
  `deletedByDate` DATE NULL COMMENT '',
  `deletedByUserId` INT NULL COMMENT '',
  `active` INT NULL COMMENT '',
  `dateCreated` DATE NULL COMMENT '',
  `comment` MEDIUMTEXT NULL COMMENT '',
  PRIMARY KEY (`commentid`)  COMMENT '',
  INDEX `deletedByUserId_idx` (`deletedByUserId` ASC)  COMMENT '',
  INDEX `postid_idx` (`postid` ASC)  COMMENT '',
  INDEX `userid_idx` (`userid` ASC)  COMMENT '',
  CONSTRAINT `parentCommentid`
    FOREIGN KEY (`commentid`)
    REFERENCES `mydb`.`comment` (`commentid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `postid`
    FOREIGN KEY (`postid`)
    REFERENCES `mydb`.`post` (`postid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `deletedByUserId`
    FOREIGN KEY (`deletedByUserId`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = '		'