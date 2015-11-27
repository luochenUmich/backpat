CREATE TABLE IF NOT EXISTS `mydb`.`report` (
  `reportid` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `postid` INT NULL COMMENT '',
  `commentid` INT NULL COMMENT '',
  `reportText` LONGTEXT NULL COMMENT '',
  `dateReported` DATE NULL COMMENT '',
  `reportedByUsername` VARCHAR(20) NULL COMMENT '',
  `active` BIT NULL COMMENT '',
  PRIMARY KEY (`reportid`)  COMMENT '')
ENGINE = InnoDB