BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `Usage` (
	`call_id`	INTEGER,
	`repo_id`	INTEGER,
	`num_calls`	INTEGER,
	FOREIGN KEY(`repo_id`) REFERENCES `Repos`(`repo_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY(`call_id`) REFERENCES `MPICalls`(`call_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(`call_id`,`repo_id`)
);
CREATE TABLE IF NOT EXISTS `Repos` (
	`repo_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`owner`	STRING ( 64 ),
	`reponame`	STRING ( 64 ),
	`revision_id`	STRING,
	`clone_url`	STRING ( 256 ),
	`retrieval_date`	DATETIME,
	`omp_occs`	INTEGER,
	`acc_occs`	INTEGER,
	`cuda_occs`	INTEGER,
	`ocl_occs`	INTEGER,
	`c_lines`	INTEGER,
	`cpp_lines`	INTEGER,
	`c_cpp_h_lines`	INTEGER,
	`fortran_lines`	INTEGER,
	`total_lines`	INTEGER
);
CREATE TABLE IF NOT EXISTS `Owners` (
	`repo_id`	INTEGER,
	`user_id`	INTEGER
);
CREATE TABLE IF NOT EXISTS `MPICalls` (
	`call_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`call_name`	STRING ( 256 )
);
COMMIT;
