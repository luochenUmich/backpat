CREATE TABLE IF NOT EXISTS `mydb`.`userPostProperty` (
  `userid` INT NOT NULL COMMENT '',
  `postid` INT NOT NULL COMMENT '',
  `liked` TINYINT(1) ZEROFILL NULL COMMENT '',
  `reported` TINYINT(1) ZEROFILL NULL COMMENT '',
  `timesSeen` INT ZEROFILL NULL COMMENT '',
  `hidden` TINYINT(1) ZEROFILL NULL COMMENT '',
  PRIMARY KEY (`userid`, `postid`)  COMMENT '',
  CONSTRAINT `userid`
    FOREIGN KEY (`userid`)
    REFERENCES `mydb`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `postid`
    FOREIGN KEY (`postid`)
    REFERENCES `mydb`.`post` (`postid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB