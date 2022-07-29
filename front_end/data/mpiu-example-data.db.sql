BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `Usage` (
	`call_id`	INTEGER,
	`repo_id`	INTEGER,
	`num_calls`	INTEGER,
	FOREIGN KEY(`repo_id`) REFERENCES `Repos`(`repo_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY(`call_id`) REFERENCES `MPICalls`(`call_id`) ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(`call_id`,`repo_id`)
);
INSERT INTO `Usage` (call_id,repo_id,num_calls) VALUES (3,4,62),
 (4,4,24),
 (5,4,32),
 (7,4,3),
 (8,4,787),
 (11,4,45),
 (12,4,3);
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
INSERT INTO `Repos` (repo_id,owner,reponame,revision_id,clone_url,retrieval_date,omp_occs,acc_occs,cuda_occs,ocl_occs,c_lines,cpp_lines,c_cpp_h_lines,fortran_lines,total_lines) VALUES (3,'jithinjosepkl','Microsoft-MPI',0,NULL,NULL,0,0,0,0,0,118798,22800,1467,148544),
 (4,'PlatONnetwork','privacy-contract-compiler',0,NULL,NULL,37204,0,781,880,136866,1953796,478016,18,3103634),
 (5,'gbibek','hpx',0,NULL,NULL,13,0,0,0,0,91853,423293,0,541885),
 (6,'ChokJohn','LightGBM-Win10-GPU-',0,NULL,NULL,210,0,0,187,507,13197,11141,0,42527),
 (7,'songmeixu','pytorch',0,NULL,NULL,107,0,1692,2,33057,362333,192006,0,980243),
 (9,'lm-konda','llvm_low_precision',0,NULL,NULL,74902,0,2480,1768,291136,2505205,643441,18,4145177),
 (10,'MichaelAxtmann','RBC',0,NULL,NULL,0,0,0,0,0,7154,559,0,11515);
CREATE TABLE IF NOT EXISTS `Owners` (
	`repo_id`	INTEGER,
	`user_id`	INTEGER
);
INSERT INTO `Owners` (repo_id,user_id) VALUES (3,'jithinjosepkl'),
 (4,'PlatONnetwork'),
 (5,'gbibek'),
 (6,'ChokJohn'),
 (7,'songmeixu'),
 (9,'lm-konda'),
 (10,'MichaelAxtmann');
CREATE TABLE IF NOT EXISTS `MPICalls` (
	`call_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`call_name`	STRING ( 256 )
);
INSERT INTO `MPICalls` (call_id,call_name) VALUES (1,'MPI_ADD'),
 (2,'MPI_ALLGATHER'),
 (3,'MPI_ALLREDUCE'),
 (4,'MPI_ASSIGN'),
 (5,'MPI_BARRIER'),
 (6,'MPI_BCAST'),
 (7,'MPI_COMM_RANK'),
 (8,'MPI_COMM_SIZE'),
 (9,'MPI_DOT'),
 (10,'MPI_FINALIZE'),
 (11,'MPI_GENERATE'),
 (12,'MPI_INIT'),
 (13,'MPI_MULTIPLY'),
 (14,'MPI_OUTPUT'),
 (15,'MPI_SEARCH'),
 (16,'MPI_SENDRECV'),
 (17,'MPI_SETONE'),
 (18,'MPI_SETZERO'),
 (19,'MPI_SUBTRACT');
COMMIT;
