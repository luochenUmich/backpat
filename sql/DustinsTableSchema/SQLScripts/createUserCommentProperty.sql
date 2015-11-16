CREATE TABLE IF NOT EXISTS `mydb`.`userCommentProperty` (
  `username` VARCHAR(20) NOT NULL COMMENT '',
  `commentid` INT NOT NULL COMMENT '',
  `hidden` TINYINT(1) NULL COMMENT '',
  `liked` INT NULL COMMENT '',
  `reported` INT NULL COMMENT '',
  PRIMARY KEY (`username`, `commentid`)  COMMENT '',
  INDEX `commentid_idx` (`commentid` ASC)  COMMENT '',
  CONSTRAINT `commentid`
    FOREIGN KEY (`commentid`)
    REFERENCES `mydb`.`comment` (`commentid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `username`
    FOREIGN KEY (`username`)
    REFERENCES `mydb`.`user` (`username`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB