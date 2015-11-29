CREATE TABLE IF NOT EXISTS `mydb`.`report` (
  `reportid` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `postid` INT NULL COMMENT '',
  `commentid` INT NULL COMMENT '',
  `reportText` LONGTEXT NULL COMMENT '',
  `dateReported` timestamp default current_timestamp COMMENT '',
  `reportedByUsername` VARCHAR(20) NULL COMMENT '',
  `active` TINYINT(1) DEFAULT 1 COMMENT '',
  PRIMARY KEY (`reportid`)  COMMENT '')
ENGINE = InnoDB