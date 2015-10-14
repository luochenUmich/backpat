CREATE TABLE IF NOT EXISTS `mydb`.`userCommentProperty` (
  `userid` INT NOT NULL COMMENT '',
  `commentid` INT NOT NULL COMMENT '',
  `hidden` TINYINT(1) NULL COMMENT '',
  `liked` INT NULL COMMENT '',
  `reported` INT NULL COMMENT '',
  PRIMARY KEY (`userid`, `commentid`)  COMMENT '',
  INDEX `commentid_idx` (`commentid` ASC)  COMMENT '',
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `commentid`
    FOREIGN KEY (`commentid`)
    REFERENCES `mydb`.`comment` (`commentid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB