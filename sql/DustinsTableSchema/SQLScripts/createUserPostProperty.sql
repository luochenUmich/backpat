CREATE TABLE IF NOT EXISTS `mydb`.`userPostProperty` (
  `username` VARCHAR(20) NOT NULL COMMENT '',
  `postid` INT NOT NULL COMMENT '',
  `liked` TINYINT(1) ZEROFILL NULL COMMENT '',
  `reported` TINYINT(1) ZEROFILL NULL COMMENT '',
  `timesSeen` INT ZEROFILL NULL COMMENT '',
  `hidden` TINYINT(1) ZEROFILL NULL COMMENT '',
  PRIMARY KEY (`username`, `postid`)  COMMENT '',
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